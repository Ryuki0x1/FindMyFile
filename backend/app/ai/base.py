"""
Abstract base interface for all AI backends.
Every AI component (embedding, captioning) must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Any
import numpy as np


class BaseEmbedder(ABC):
    """Base class for embedding models (image or text)."""

    @abstractmethod
    def load_model(self) -> None:
        """Load the model into memory."""
        ...

    @abstractmethod
    def embed(self, inputs: list[Any]) -> np.ndarray:
        """
        Generate embeddings for a list of inputs.
        Returns a numpy array of shape (N, embedding_dim).
        """
        ...

    @abstractmethod
    def embed_single(self, input_data: Any) -> np.ndarray:
        """Generate embedding for a single input. Returns shape (embedding_dim,)."""
        ...

    @property
    @abstractmethod
    def embedding_dim(self) -> int:
        """Dimensionality of the embedding vectors."""
        ...

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Human-readable model name."""
        ...
