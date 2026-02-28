"""
Face detection and embedding engine.
Uses facenet-pytorch (MTCNN for detection, InceptionResnetV1 for embeddings).
All face embeddings are 512-dimensional vectors.
"""

import numpy as np
import torch
from PIL import Image
from typing import Optional


class FaceEmbedder:
    """Detects faces in images and generates 512-dim face embeddings."""

    def __init__(self):
        self._detector = None
        self._recognizer = None
        self._device = "cpu"
        self._embedding_dim = 512

    @property
    def embedding_dim(self) -> int:
        return self._embedding_dim

    def load_model(self) -> None:
        """Load MTCNN face detector and InceptionResnetV1 face recognizer."""
        from facenet_pytorch import MTCNN, InceptionResnetV1

        self._device = "cuda" if torch.cuda.is_available() else "cpu"

        # MTCNN for face detection — higher min_face_size catches more faces
        # thresholds: [P-Net, R-Net, O-Net] — lower = more detections, higher = stricter
        self._detector = MTCNN(
            image_size=160,
            margin=30,          # larger margin = better face context for recognition
            min_face_size=30,   # detect smaller faces (default is 20)
            thresholds=[0.6, 0.7, 0.7],  # slightly relaxed for better recall
            factor=0.709,
            keep_all=True,      # detect ALL faces in an image
            device=self._device,
            post_process=True,  # normalize pixel values
        )

        # InceptionResnetV1 pretrained on VGGFace2 for face embeddings
        self._recognizer = InceptionResnetV1(
            pretrained="vggface2",
        ).eval().to(self._device)

        print(f"[FaceEmbedder] Loaded on {self._device}")

    def _ensure_loaded(self):
        if self._detector is None:
            self.load_model()

    def detect_and_embed(self, image: Image.Image) -> list[dict]:
        """
        Detect all faces in an image and return their embeddings.

        Returns:
            List of dicts, each with:
              - 'embedding': np.ndarray (512-dim)
              - 'box': [x1, y1, x2, y2] bounding box
              - 'confidence': float detection confidence
        """
        self._ensure_loaded()

        # Detect faces → get face crops and bounding boxes
        try:
            face_tensors, probs = self._detector.detect(image)
        except Exception:
            return []

        if face_tensors is None:
            return []

        # Get cropped and aligned face tensors for embedding
        try:
            aligned_faces = self._detector(image)
        except Exception:
            return []

        if aligned_faces is None:
            return []

        # If single face, unsqueeze to batch
        if aligned_faces.dim() == 3:
            aligned_faces = aligned_faces.unsqueeze(0)

        results = []
        # Generate embeddings
        with torch.no_grad():
            embeddings = self._recognizer(aligned_faces.to(self._device))
            embeddings = embeddings.cpu().numpy()

        for i in range(len(embeddings)):
            # Normalize embedding
            emb = embeddings[i]
            norm = np.linalg.norm(emb)
            if norm == 0:
                continue
            emb = emb / norm

            box = face_tensors[i].tolist() if face_tensors is not None else [0, 0, 0, 0]
            conf = float(probs[i]) if probs is not None else 0.0

            if conf < 0.85:  # Slightly relaxed threshold (was 0.90) — catches more valid faces
                continue

            # Skip tiny faces (likely false positives)
            x1, y1, x2, y2 = box
            face_w = abs(x2 - x1)
            face_h = abs(y2 - y1)
            if face_w < 20 or face_h < 20:
                continue

            results.append({
                "embedding": emb,
                "box": box,
                "confidence": conf,
            })

        return results

    def embed_single_face(self, image: Image.Image) -> Optional[np.ndarray]:
        """
        Embed a single reference face (e.g., user-uploaded sample).
        Picks the largest/most confident face if multiple detected.
        Returns 512-dim normalized embedding or None if no face found.
        """
        faces = self.detect_and_embed(image)
        if not faces:
            return None

        # Pick highest-confidence face
        best = max(faces, key=lambda f: f["confidence"])
        return best["embedding"]
