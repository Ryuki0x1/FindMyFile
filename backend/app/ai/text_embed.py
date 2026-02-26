"""
Text embedding for document search.
Uses sentence-transformers models (e.g., all-MiniLM-L6-v2) for embedding
text extracted from documents via OCR or direct parsing.
"""

from typing import Any
import numpy as np
from app.ai.base import BaseEmbedder


class TextEmbedder(BaseEmbedder):
    """
    Text embedder using sentence-transformers.
    Used for embedding OCR text, document content, and text-heavy queries.
    """

    def __init__(self, model_id: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self._model_id = model_id
        self._model = None
        self._embedding_dim = 384  # MiniLM default

    def load_model(self) -> None:
        """Load the sentence transformer model."""
        from transformers import AutoTokenizer, AutoModel

        print(f"[TextEmbed] Loading model: {self._model_id}")
        self._tokenizer = AutoTokenizer.from_pretrained(self._model_id)
        self._model = AutoModel.from_pretrained(self._model_id)
        self._model.eval()

        # Try GPU
        try:
            import torch
            if torch.cuda.is_available():
                self._model = self._model.to("cuda")
                self._device = "cuda"
                print("[TextEmbed] Using GPU")
            else:
                self._device = "cpu"
        except ImportError:
            self._device = "cpu"

        print(f"[TextEmbed] Model loaded. Dim: {self._embedding_dim}")

    def _ensure_loaded(self):
        if self._model is None:
            self.load_model()

    def _mean_pooling(self, model_output, attention_mask):
        """Mean pool the token embeddings using the attention mask."""
        import torch
        token_emb = model_output[0]  # (batch, seq_len, hidden)
        mask_expanded = attention_mask.unsqueeze(-1).expand(token_emb.size()).float()
        return torch.sum(token_emb * mask_expanded, 1) / torch.clamp(
            mask_expanded.sum(1), min=1e-9
        )

    def embed_text(self, text: str) -> np.ndarray:
        """Embed a single text string. Returns shape (embedding_dim,)."""
        return self.embed_texts([text])[0]

    def embed_texts(self, texts: list[str]) -> np.ndarray:
        """Embed a batch of text strings. Returns shape (N, embedding_dim)."""
        self._ensure_loaded()
        import torch

        encoded = self._tokenizer(
            texts, padding=True, truncation=True, max_length=512, return_tensors="pt"
        )
        encoded = {k: v.to(self._device) for k, v in encoded.items()}

        with torch.no_grad():
            output = self._model(**encoded)

        embeddings = self._mean_pooling(output, encoded["attention_mask"])
        # Normalize
        embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
        return embeddings.cpu().numpy()

    # --- BaseEmbedder interface ---

    def embed(self, inputs: list[Any]) -> np.ndarray:
        return self.embed_texts(inputs)

    def embed_single(self, input_data: Any) -> np.ndarray:
        return self.embed_text(input_data)

    @property
    def embedding_dim(self) -> int:
        return self._embedding_dim

    @property
    def model_name(self) -> str:
        return self._model_id
