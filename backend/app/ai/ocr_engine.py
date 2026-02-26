"""
OCR Engine — Extracts text from images using EasyOCR.
GPU-accelerated via PyTorch.
"""

from typing import Optional
from PIL import Image
import numpy as np


class OCREngine:
    """Extracts readable text from images using EasyOCR."""

    def __init__(self, languages: list[str] = None):
        self._reader = None
        self._languages = languages or ["en"]

    def load_model(self) -> None:
        """Load EasyOCR reader."""
        import easyocr

        self._reader = easyocr.Reader(
            self._languages,
            gpu=True,  # Will fallback to CPU if no CUDA
        )
        print(f"[OCR] Loaded EasyOCR with languages: {self._languages}")

    def _ensure_loaded(self):
        if self._reader is None:
            self.load_model()

    def extract_text(self, image: Image.Image) -> str:
        """
        Extract all readable text from an image.

        Returns:
            Concatenated text string from the image, or empty string.
        """
        self._ensure_loaded()

        try:
            # Convert PIL Image to numpy array for EasyOCR
            img_array = np.array(image)

            # Run OCR
            results = self._reader.readtext(
                img_array,
                detail=0,  # Just return text strings, no bounding boxes
                paragraph=True,  # Merge nearby text into paragraphs
            )

            # Join all detected text
            text = " ".join(results).strip()
            return text

        except Exception as e:
            print(f"[OCR] Error: {e}")
            return ""

    def extract_text_from_path(self, filepath: str) -> str:
        """
        Extract text from an image file path.
        """
        self._ensure_loaded()

        try:
            results = self._reader.readtext(
                filepath,
                detail=0,
                paragraph=True,
            )
            return " ".join(results).strip()
        except Exception as e:
            print(f"[OCR] Error on {filepath}: {e}")
            return ""
