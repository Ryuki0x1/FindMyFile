"""
CLIP image & text embedding using HuggingFace Transformers.
Generates embeddings for images (visual search) and text queries.
Runs locally via CPU or CUDA GPU — no internet required after model download.
"""

import os
from typing import Any, Union

import numpy as np
from PIL import Image

from app.ai.base import BaseEmbedder


class CLIPEmbedder(BaseEmbedder):
    """
    CLIP-based embedder for images and text.
    Uses HuggingFace transformers CLIPModel + CLIPProcessor.
    """

    def __init__(self, model_id: str = None):
        # Try to load model ID from user config (hardware-optimized)
        if model_id is None:
            try:
                from app.core.first_run import get_or_create_config
                config = get_or_create_config()
                model_id = config.get("optimizations", {}).get("clip_model", "openai/clip-vit-base-patch32")
                print(f"[CLIP] Using hardware-optimized model: {model_id}")
            except:
                # Fallback to base model (smaller, works on all hardware)
                model_id = "openai/clip-vit-base-patch32"
                print(f"[CLIP] Using default model: {model_id}")
        
        self._model_id = model_id
        self._model = None
        self._processor = None
        self._tokenizer = None
        self._device = "cpu"
        
        # Detect embedding dimension from model name
        if "large" in model_id.lower():
            self._embedding_dim = 768  # ViT-L/14
        else:
            self._embedding_dim = 512  # ViT-B/32 or ViT-B/16

    def load_model(self) -> None:
        """Load CLIP model and processor."""
        from transformers import CLIPModel, CLIPProcessor

        print(f"[CLIP] Loading model: {self._model_id}")

        # Detect device
        try:
            import torch
            if torch.cuda.is_available():
                self._device = "cuda"
                print(f"[CLIP] Using GPU: {torch.cuda.get_device_name(0)}")
            else:
                print("[CLIP] No GPU detected, using CPU")
        except ImportError:
            print("[CLIP] PyTorch not available, using CPU")

        self._model = CLIPModel.from_pretrained(self._model_id)
        self._processor = CLIPProcessor.from_pretrained(self._model_id)

        # Move model to device
        self._model = self._model.to(self._device)
        self._model.eval()

        # Detect embedding dim from model config
        self._embedding_dim = self._model.config.projection_dim
        print(f"[CLIP] Model loaded. Embedding dim: {self._embedding_dim}")

    def _ensure_loaded(self):
        if self._model is None:
            self.load_model()

    def embed_image(self, image: Image.Image) -> np.ndarray:
        """Embed a single PIL Image. Returns shape (embedding_dim,)."""
        self._ensure_loaded()
        import torch

        inputs = self._processor(images=image, return_tensors="pt").to(self._device)
        with torch.no_grad():
            features = self._model.get_image_features(**inputs)
        # Normalize
        features = features / features.norm(p=2, dim=-1, keepdim=True)
        return features.cpu().numpy().flatten()

    def embed_images(self, images: list[Image.Image]) -> np.ndarray:
        """Embed a batch of PIL Images. Returns shape (N, embedding_dim)."""
        self._ensure_loaded()
        import torch

        inputs = self._processor(images=images, return_tensors="pt", padding=True).to(self._device)
        with torch.no_grad():
            features = self._model.get_image_features(**inputs)
        features = features / features.norm(p=2, dim=-1, keepdim=True)
        return features.cpu().numpy()

    def embed_text(self, text: str) -> np.ndarray:
        """Embed a text query. Returns shape (embedding_dim,)."""
        self._ensure_loaded()
        import torch

        inputs = self._processor(text=[text], return_tensors="pt", padding=True).to(self._device)
        with torch.no_grad():
            features = self._model.get_text_features(**inputs)
        features = features / features.norm(p=2, dim=-1, keepdim=True)
        return features.cpu().numpy().flatten()

    def embed_texts(self, texts: list[str]) -> np.ndarray:
        """Embed a batch of text queries. Returns shape (N, embedding_dim)."""
        self._ensure_loaded()
        import torch

        inputs = self._processor(text=texts, return_tensors="pt", padding=True).to(self._device)
        with torch.no_grad():
            features = self._model.get_text_features(**inputs)
        features = features / features.norm(p=2, dim=-1, keepdim=True)
        return features.cpu().numpy()

    # --- BaseEmbedder interface ---

    def embed(self, inputs: list[Any]) -> np.ndarray:
        """Embed a list of PIL Images."""
        return self.embed_images(inputs)

    def embed_single(self, input_data: Any) -> np.ndarray:
        """Embed a single PIL Image."""
        return self.embed_image(input_data)

    @property
    def embedding_dim(self) -> int:
        return self._embedding_dim

    @property
    def model_name(self) -> str:
        return self._model_id
