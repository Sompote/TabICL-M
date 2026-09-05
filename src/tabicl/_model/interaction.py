from __future__ import annotations

from typing import Optional, Tuple, Union
from functools import partial
from collections import OrderedDict

import torch
import torch.nn.functional as F
from torch import nn, Tensor
from torch.utils.checkpoint import checkpoint

from .encoders import Encoder
from .inference import InferenceManager
from .inference_config import MgrConfig, InferenceConfig


class RowInteraction(nn.Module):
    """Context-aware row-wise interaction.

    This module captures interactions between features within each row using a transformer
    encoder with rotary positional encoding. It prepends learnable class tokens to the
    learned feature embeddings and uses these tokens to aggregate information.

    Parameters
    ----------
    embed_dim : int
        Embedding dimension.

    num_blocks : int
        Number of blocks used in the encoder.

    nhead : int
        Number of attention heads of the encoder.

    dim_feedforward : int
        Dimension of the feedforward network of the encoder.

    num_cls : int, default=4
        Number of learnable CLS tokens to prepend to the feature embeddings. The outputs
        of these CLS tokens are concatenated for the final representation per row.

    rope_base : float, default=100000
        Base scaling factor for rotary position encoding.

    rope_interleaved : bool, default=True
        If True, uses interleaved rotation where dimension pairs are (0,1), (2,3), etc.
        If False, uses non-interleaved rotation where the embedding is split into
        first half [0:d//2] and second half [d//2:d].

    dropout : float, default=0.0
        Dropout probability used in the encoder.

    activation : str or unary callable, default="gelu"
        The activation function used in the feedforward network, can be
        either string ("relu" or "gelu") or unary callable.

    norm_first : bool, default=True
        If True, uses pre-norm architecture (LayerNorm before attention and feedforward).

    bias_free_ln : bool, default=False
        If True, removes bias from all LayerNorm layers.

    recompute : bool, default=False
        If True, uses gradient checkpointing to save memory at the cost of additional computation.

    missing_aware : bool, default=False
        Observed-only row attention. Feature tokens whose cells are all missing are
        excluded from the attention keys, so a row's representation is a function of
        its observed features only. Rows without any observed feature keep all keys.
        Complete rows are unchanged.

    pattern_token : bool, default=False
        Pattern read-out. A learned query attends once, with fixed sinusoidal position
        codes, to all feature tokens of a row (observed and absent) after the
        penultimate block and its output is projected by the zero-initialised
        ``pattern_out`` and added to the row representation. It gives the model a
        representation of *which* features a row lacks, i.e. of its source. Complete
        data yields the same representations as without the flag.
    """

    def __init__(
        self,
        embed_dim: int,
        num_blocks: int,
        nhead: int,
        dim_feedforward: int,
        num_cls: int = 4,
        rope_base: float = 100000,
        rope_interleaved: bool = True,
        dropout: float = 0.0,
        activation: str | callable = "gelu",
        norm_first: bool = True,
        bias_free_ln: bool = False,
        zero_init: bool = True,
        recompute: bool = False,
        missing_aware: bool = False,
        pattern_token: bool = False,
    ) -> None:
        super().__init__()
        self.embed_dim = embed_dim
        self.num_blocks = num_blocks
        self.num_cls = num_cls
        self.norm_first = norm_first
        self.recompute = recompute
        self.missing_aware = missing_aware
        self.pattern_token = pattern_token

        self.tf_row = Encoder(
            num_blocks=num_blocks,
            d_model=embed_dim,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            activation=activation,
            norm_first=norm_first,
            bias_free_ln=bias_free_ln,
            use_rope=True,
            rope_base=rope_base,
            rope_interleaved=rope_interleaved,
            zero_init=zero_init,
            recompute=recompute,
        )

        self.cls_tokens = nn.Parameter(torch.empty(num_cls, embed_dim))
        nn.init.trunc_normal_(self.cls_tokens, std=0.02)

        self.out_ln = nn.LayerNorm(embed_dim, bias=not bias_free_ln) if norm_first else nn.Identity()

        if pattern_token:
            self.pattern_query = nn.Parameter(torch.empty(embed_dim))
            nn.init.trunc_normal_(self.pattern_query, std=0.02)
            self.pattern_attn = nn.MultiheadAttention(embed_dim, nhead, dropout=dropout, batch_first=True)
            self.pattern_out = nn.Linear(embed_dim, embed_dim * num_cls)
            nn.init.zeros_(self.pattern_out.weight)
            nn.init.zeros_(self.pattern_out.bias)

        self.inference_mgr = InferenceManager(enc_name="tf_row", out_dim=embed_dim * self.num_cls, out_no_seq=True)

    @staticmethod
    def _sinusoid(length: int, dim: int, device, dtype) -> Tensor:
        """Fixed sinusoidal position codes of shape (length, dim)."""
        pos = torch.arange(length, device=device, dtype=torch.float32).unsqueeze(1)
        i = torch.arange(0, dim, 2, device=device, dtype=torch.float32)
        angle = pos / torch.pow(10000.0, i / dim)
        pe = torch.zeros(length, dim, device=device, dtype=torch.float32)
        pe[:, 0::2] = torch.sin(angle)
        pe[:, 1::2] = torch.cos(angle[:, : dim // 2])
        return pe.to(dtype)

    def _pattern_readout(self, tokens: Tensor, pad_mask: Optional[Tensor]) -> Tensor:
        """One attention read-out of a row's token set by the learned pattern query.

        tokens : (B, T, L, E); pad_mask : (B, T, L) bool, True at empty feature slots.
        Returns (B, T, E).
        """
        B, T, L, E = tokens.shape
        kv = tokens.reshape(B * T, L, E) + self._sinusoid(L, E, tokens.device, tokens.dtype)
        q = self.pattern_query.to(kv.dtype).view(1, 1, E).expand(B * T, 1, E)
        kpm = pad_mask.reshape(B * T, L) if pad_mask is not None else None
        out, _ = self.pattern_attn(q, kv, kv, key_padding_mask=kpm, need_weights=False)
        return out.reshape(B, T, E)

    def _key_mask(self, key_mask: Optional[Tensor], absent: Optional[Tensor]) -> Optional[Tensor]:
        """Combine the empty-slot mask with the observed-only mask of absent feature tokens."""
        if not self.missing_aware or absent is None:
            return key_mask
        # Rows with no observed feature at all keep every key.
        absent = absent & ~absent.all(dim=-1, keepdim=True)
        absent = F.pad(absent, (self.num_cls, 0), value=False)  # (B, T, C+H)
        return absent if key_mask is None else (key_mask | absent)

    def _aggregate_embeddings(
        self,
        embeddings: Tensor,
        key_mask: Optional[Tensor] = None,
        return_tokens: bool = False,
        absent: Optional[Tensor] = None,
    ) -> Union[Tensor, Tuple[Tensor, Tensor]]:
        """Process a batch of rows through a transformer encoder.

        This method:

        1. Processes embeddings through the transformer
        2. Extracts only the class token representations and applies normalization if pre-norm
        3. Concatenates the class tokens into a single vector per row

        Parameters
        ----------
        embeddings : Tensor
            Feature embeddings of shape (B, T, H+C, E) where:
             - B is the number of tables
             - T is the number of samples (rows)
             - H is the number of features
             - C is the number of class tokens
             - E is the embedding dimension

        key_mask : Optional[Tensor], default=None
            Boolean mask of shape (B, T, H+C) where True indicates positions
            to ignore during attention (empty feature slots).

        absent : Optional[Tensor], default=None
            Boolean mask of shape (B, T, H), True where every cell of a feature token is
            missing. Used only when ``missing_aware`` is True.

        Returns
        -------
        Tensor
            Flattened class token outputs of shape (B*T, C*E).
        """
        rope = self.tf_row.rope
        pad_mask = key_mask
        key_mask = self._key_mask(key_mask, absent)

        # Process all blocks except the last
        if self.recompute:
            for block in self.tf_row.blocks[:-1]:
                embeddings = checkpoint(
                    partial(block, key_padding_mask=key_mask, rope=rope), embeddings, use_reentrant=False
                )
        else:
            for block in self.tf_row.blocks[:-1]:
                embeddings = block(embeddings, key_padding_mask=key_mask, rope=rope)

        last_block = self.tf_row.blocks[-1]

        if return_tokens:
            # Full self-attention in the last block so that every feature token gets an output.
            # The CLS outputs are identical to the CLS-only query below, because the output of a
            # query does not depend on which other queries are present.
            if self.recompute:
                outputs = checkpoint(
                    partial(last_block, key_padding_mask=key_mask, rope=rope), embeddings, use_reentrant=False
                )
            else:
                outputs = last_block(embeddings, key_padding_mask=key_mask, rope=rope)
            pattern = self._pattern_readout(embeddings, pad_mask) if self.pattern_token else None
            outputs = self.out_ln(outputs)
            cls_outputs = outputs[..., : self.num_cls, :]
            tokens = outputs[..., self.num_cls :, :]  # (B, T, H, E)
            representations = cls_outputs.flatten(-2)
            if pattern is not None:
                representations = representations + self.pattern_out(pattern)
            return representations, tokens

        # Last block: q = CLS tokens, k/v = full sequence
        if self.recompute:
            cls_outputs = checkpoint(
                lambda emb: last_block(
                    q=emb[..., : self.num_cls, :], k=emb, v=emb, key_padding_mask=key_mask, rope=rope
                ),
                embeddings,
                use_reentrant=False,
            )
        else:
            cls_outputs = last_block(
                q=embeddings[..., : self.num_cls, :], k=embeddings, v=embeddings, key_padding_mask=key_mask, rope=rope
            )
        pattern = self._pattern_readout(embeddings, pad_mask) if self.pattern_token else None
        del embeddings
        cls_outputs = self.out_ln(cls_outputs)

        representations = cls_outputs.flatten(-2)  # (B, T, C*E)
        if pattern is not None:
            representations = representations + self.pattern_out(pattern)
        return representations

    def _train_forward(
        self,
        embeddings: Tensor,
        d: Optional[Tensor] = None,
        return_tokens: bool = False,
        absent: Optional[Tensor] = None,
    ) -> Union[Tensor, Tuple[Tensor, Tensor]]:
        """Transform feature embeddings into row representations for training.

        Parameters
        ----------
        embeddings : Tensor
            Feature embeddings of shape (B, T, H+C, E) where:
             - B is the number of tables
             - T is the number of samples (rows)
             - H is the number of features
             - C is the number of class tokens
             - E is the embedding dimension

        d : Optional[Tensor], default=None
            The number of features per dataset. Used only in training mode.

        Returns
        -------
        Tensor
            Row representations of shape (B, T, C*E) where C is the number of class tokens.
        """

        B, T, HC, E = embeddings.shape
        device = embeddings.device

        cls_tokens = self.cls_tokens.expand(B, T, self.num_cls, self.embed_dim)
        # When col embedding is frozen (partial freezing, see #128), embeddings is a
        # no-grad view whose in-place mutation would conflict with autograd. Detach
        # gives a fresh autograd leaf sharing the same storage — zero-copy.
        if torch.is_grad_enabled() and not embeddings.requires_grad:
            embeddings = embeddings.detach()
        embeddings[:, :, : self.num_cls] = cls_tokens.to(device)

        # Create mask to prevent from attending to empty features
        if d is None:
            key_mask = None
        else:
            d = d + self.num_cls
            indices = torch.arange(HC, device=device).view(1, 1, HC).expand(B, T, HC)
            key_mask = indices >= d.view(B, 1, 1)  # (B, T, HC)

        # (B, T, C*E), plus (B, T, H, E) feature-token outputs if requested
        return self._aggregate_embeddings(embeddings, key_mask, return_tokens, absent)

    def _inference_forward(
        self, embeddings: Tensor, mgr_config: MgrConfig = None, absent: Optional[Tensor] = None
    ) -> Tensor:
        """Transform feature embeddings into row representations for inference.

        Parameters
        ----------
        embeddings : Tensor
            Feature embeddings of shape (B, T, H+C, E) where:
             - B is the number of tables
             - T is the number of samples (rows)
             - H is the number of features
             - C is the number of class tokens
             - E is the embedding dimension

        mgr_config : MgrConfig, default=None
            Configuration for InferenceManager.

        Returns
        -------
        Tensor
            Row representations of shape (B, T, C*E) where C is the number of class tokens.
        """
        # Configure inference parameters
        if mgr_config is None:
            mgr_config = InferenceConfig().ROW_CONFIG
        self.inference_mgr.configure(**mgr_config)

        B, T = embeddings.shape[:2]
        cls_tokens = self.cls_tokens.expand(B, T, self.num_cls, self.embed_dim)
        # When col embedding is frozen (partial freezing, see #128), embeddings is a
        # no-grad view whose in-place mutation would conflict with autograd. Detach
        # gives a fresh autograd leaf sharing the same storage — zero-copy.
        if torch.is_grad_enabled() and not embeddings.requires_grad:
            embeddings = embeddings.detach()
        embeddings[:, :, : self.num_cls] = cls_tokens.to(embeddings.device)
        representations = self.inference_mgr(
            self._aggregate_embeddings, inputs=OrderedDict([("embeddings", embeddings), ("absent", absent)])
        )

        return representations  # (B, T, C*E)

    def forward(
        self,
        embeddings: Tensor,
        d: Optional[Tensor] = None,
        mgr_config: MgrConfig = None,
        return_tokens: bool = False,
        absent: Optional[Tensor] = None,
    ) -> Union[Tensor, Tuple[Tensor, Tensor]]:
        """Transform feature embeddings into row representations.

        Parameters
        ----------
        embeddings : Tensor
            Feature embeddings of shape (B, T, H+C, E) where:
             - B is the number of tables
             - T is the number of samples (rows)
             - H is the number of features
             - C is the number of class tokens
             - E is the embedding dimension

        d : Optional[Tensor], default=None
            The number of features per dataset. Used only in training mode.

        mgr_config : MgrConfig, default=None
            Configuration for InferenceManager. Used only in inference mode.

        return_tokens : bool, default=False
            If True (training mode only), also return the per-feature token outputs of
            shape (B, T, H, E) after the last row-wise block, for cell reconstruction.

        Returns
        -------
        Tensor
            Row representations of shape (B, T, C*E) where C is the number of class tokens.
            If ``return_tokens`` is True, a tuple (representations, tokens).
        """

        if self.training:
            representations = self._train_forward(embeddings, d, return_tokens, absent)
        else:
            representations = self._inference_forward(embeddings, mgr_config, absent)

        return representations  # (B, T, C*E)
