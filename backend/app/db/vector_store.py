"""
ChromaDB vector store wrapper.
Stores file embeddings and metadata for fast similarity search.
All data persisted to local disk — no cloud, no network.
"""

import os
from typing import Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
import numpy as np


class VectorStore:
    """Wrapper around ChromaDB for storing and querying file embeddings."""

    COLLECTION_NAME = "findmypic_files"

    def __init__(self, persist_dir: str, embedding_dim: int = None):
        self.persist_dir = persist_dir
        self._embedding_dim = embedding_dim
        os.makedirs(persist_dir, exist_ok=True)

        print(f"[VectorStore] Initializing ChromaDB at: {persist_dir}")
        self._client = chromadb.PersistentClient(
            path=persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},  # cosine similarity
        )
        count = self._collection.count()
        print(f"[VectorStore] Collection '{self.COLLECTION_NAME}' ready. "
              f"Current count: {count}")

        # Detect & handle embedding dimension mismatch (happens after model upgrades)
        if count > 0 and embedding_dim is not None:
            self._check_and_fix_dimension_mismatch(embedding_dim)

    def _check_and_fix_dimension_mismatch(self, expected_dim: int) -> None:
        """
        Check if stored embeddings match the current model's dimension.
        If not, clear the collection so re-indexing works cleanly.
        ChromaDB locks embedding dimensions per collection — mismatches cause silent failures.
        """
        try:
            # Get one embedding to check its dimension
            sample = self._collection.get(limit=1, include=["embeddings"])
            if sample and sample.get("embeddings") and len(sample["embeddings"]) > 0:
                stored_dim = len(sample["embeddings"][0])
                if stored_dim != expected_dim:
                    print(f"[VectorStore] ⚠️  Embedding dimension mismatch!")
                    print(f"[VectorStore]    Stored: {stored_dim}-dim, Current model: {expected_dim}-dim")
                    print(f"[VectorStore]    Clearing collection for fresh re-index...")
                    self._client.delete_collection(self.COLLECTION_NAME)
                    self._collection = self._client.get_or_create_collection(
                        name=self.COLLECTION_NAME,
                        metadata={"hnsw:space": "cosine"},
                    )
                    print(f"[VectorStore] ✅ Collection reset. Please run Full Re-Index.")
                else:
                    print(f"[VectorStore] ✅ Embedding dimensions match ({expected_dim}-dim)")
        except Exception as e:
            print(f"[VectorStore] Could not check embedding dimensions: {e}")

    def add_file(
        self,
        file_id: str,
        embedding: np.ndarray,
        metadata: dict,
    ) -> None:
        """Add a single file's embedding and metadata."""
        self._collection.upsert(
            ids=[file_id],
            embeddings=[embedding.tolist()],
            metadatas=[metadata],
        )

    def add_files_batch(
        self,
        file_ids: list[str],
        embeddings: np.ndarray,
        metadatas: list[dict],
    ) -> None:
        """Add a batch of file embeddings and metadata."""
        self._collection.upsert(
            ids=file_ids,
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: np.ndarray,
        n_results: int = 20,
        where: Optional[dict] = None,
    ) -> dict:
        """
        Search for similar files by query embedding.
        Returns dict with 'ids', 'distances', 'metadatas'.
        """
        count = self._collection.count()
        if count == 0:
            return {"ids": [], "distances": [], "metadatas": []}
        # Cap at actual collection size — ChromaDB errors if n_results > count
        actual_n = min(n_results, count)
        kwargs = {
            "query_embeddings": [query_embedding.tolist()],
            "n_results": actual_n,
        }
        if where:
            kwargs["where"] = where

        results = self._collection.query(**kwargs)

        return {
            "ids": results["ids"][0] if results["ids"] else [],
            "distances": results["distances"][0] if results["distances"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else [],
        }

    def delete_file(self, file_id: str) -> None:
        """Remove a file from the index."""
        self._collection.delete(ids=[file_id])

    def has_file(self, file_id: str) -> bool:
        """Check if a file is already indexed."""
        result = self._collection.get(ids=[file_id])
        return len(result["ids"]) > 0

    def get_file(self, file_id: str) -> Optional[dict]:
        """Get metadata for a specific file."""
        result = self._collection.get(ids=[file_id])
        if result["ids"]:
            return result["metadatas"][0]
        return None

    def count(self) -> int:
        """Total number of indexed files."""
        return self._collection.count()

    def clear(self) -> None:
        """Delete all indexed data."""
        self._client.delete_collection(self.COLLECTION_NAME)
        self._collection = self._client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        print("[VectorStore] Index cleared.")

    def get_stats(self) -> dict:
        """Get index statistics."""
        return {
            "total_files": self._collection.count(),
            "persist_dir": self.persist_dir,
        }
    
    def get_all_indexed_files(self) -> dict:
        """
        Get all indexed files with their metadata.
        Returns a dict mapping file_path -> metadata.
        """
        try:
            # Get all documents
            results = self._collection.get()
            
            indexed_files = {}
            if results and results.get("metadatas"):
                for metadata in results["metadatas"]:
                    if metadata and "filepath" in metadata:
                        filepath = metadata["filepath"]
                        indexed_files[filepath] = {
                            "file_hash": metadata.get("file_hash", ""),
                            "last_modified": metadata.get("last_modified", 0),
                            "last_indexed": metadata.get("last_indexed", 0),
                            "size_bytes": metadata.get("size_bytes", 0),
                        }
            
            return indexed_files
        except Exception as e:
            print(f"[VectorStore] Error getting indexed files: {e}")
            return {}
    
    def remove_files_by_path(self, file_paths: list[str]) -> int:
        """
        Remove files from the index by their file paths.
        Returns the number of files removed.
        """
        if not file_paths:
            return 0
        
        try:
            # Get all documents
            results = self._collection.get()
            
            # Find IDs matching the file paths
            ids_to_delete = []
            if results and results.get("ids") and results.get("metadatas"):
                for i, metadata in enumerate(results["metadatas"]):
                    if metadata and metadata.get("filepath") in file_paths:
                        ids_to_delete.append(results["ids"][i])
            
            # Delete the documents
            if ids_to_delete:
                self._collection.delete(ids=ids_to_delete)
                print(f"[VectorStore] Removed {len(ids_to_delete)} files from index")
                return len(ids_to_delete)
            
            return 0
        except Exception as e:
            print(f"[VectorStore] Error removing files: {e}")
            return 0
    
    def get_file_metadata(self, file_path: str) -> dict | None:
        """
        Get metadata for a specific file.
        Returns None if file not found.
        """
        try:
            results = self._collection.get(where={"filepath": file_path})
            
            if results and results.get("metadatas") and len(results["metadatas"]) > 0:
                return results["metadatas"][0]
            
            return None
        except Exception as e:
            print(f"[VectorStore] Error getting file metadata: {e}")
            return None

    def text_search(self, query_text: str, n_results: int = 20) -> dict:
        """
        Search file metadata for OCR text matches.
        Returns files whose 'ocr_text' metadata contains the query string.
        """
        try:
            results = self._collection.get(
                where={"ocr_text": {"$ne": ""}},
                include=["metadatas"],
            )
        except Exception:
            return {"ids": [], "metadatas": []}

        if not results["ids"]:
            return {"ids": [], "metadatas": []}

        # Filter by text match (case-insensitive)
        query_lower = query_text.lower()
        matched_ids = []
        matched_metas = []
        for i, meta in enumerate(results["metadatas"]):
            ocr_text = meta.get("ocr_text", "").lower()
            if query_lower in ocr_text:
                matched_ids.append(results["ids"][i])
                matched_metas.append(meta)

        return {
            "ids": matched_ids[:n_results],
            "metadatas": matched_metas[:n_results],
        }


class FaceStore:
    """Separate ChromaDB collection for face embeddings (512-dim, one per detected face)."""

    COLLECTION_NAME = "findmypic_faces"

    def __init__(self, persist_dir: str):
        self.persist_dir = persist_dir
        os.makedirs(persist_dir, exist_ok=True)

        self._client = chromadb.PersistentClient(
            path=persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        print(f"[FaceStore] Collection ready. Current count: {self._collection.count()}")

    def add_face(
        self,
        face_id: str,
        embedding: np.ndarray,
        metadata: dict,
    ) -> None:
        """Add a single face embedding with metadata linking to source file."""
        self._collection.upsert(
            ids=[face_id],
            embeddings=[embedding.tolist()],
            metadatas=[metadata],
        )

    def add_faces_batch(
        self,
        face_ids: list[str],
        embeddings: np.ndarray,
        metadatas: list[dict],
    ) -> None:
        """Add a batch of face embeddings."""
        if len(face_ids) == 0:
            return
        self._collection.upsert(
            ids=face_ids,
            embeddings=embeddings.tolist() if isinstance(embeddings, np.ndarray) else embeddings,
            metadatas=metadatas,
        )

    def search_face(
        self,
        query_embedding: np.ndarray,
        n_results: int = 50,
    ) -> dict:
        """
        Find faces similar to the query embedding.
        Returns dict with 'ids', 'distances', 'metadatas'.
        """
        count = self._collection.count()
        if count == 0:
            return {"ids": [], "distances": [], "metadatas": []}

        results = self._collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=min(n_results, count),
        )

        return {
            "ids": results["ids"][0] if results["ids"] else [],
            "distances": results["distances"][0] if results["distances"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else [],
        }

    def count(self) -> int:
        return self._collection.count()

    def clear(self) -> None:
        """Delete all face data."""
        self._client.delete_collection(self.COLLECTION_NAME)
        self._collection = self._client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        print("[FaceStore] Cleared.")

    def get_stats(self) -> dict:
        return {
            "total_faces": self._collection.count(),
        }

