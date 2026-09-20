from pathlib import Path
import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from .models import DocumentChunk


class VectorStore:
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self.model = SentenceTransformer(model_name)

        self.index = None
        self.chunks: list[DocumentChunk] = []

    def add_chunks(self, chunks: list[DocumentChunk]) -> None:
        """Create embeddings and add chunks to the vector index."""

        if not chunks:
            return

        texts = [chunk.text for chunk in chunks]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        embeddings = embeddings.astype("float32")

        if self.index is None:
            dimension = embeddings.shape[1]

            self.index = faiss.IndexFlatIP(dimension)

        self.index.add(embeddings)

        self.chunks.extend(chunks)

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[tuple[DocumentChunk, float]]:
        """Search for chunks most similar to the query."""

        if self.index is None or not self.chunks:
            return []

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        query_embedding = query_embedding.astype("float32")

        scores, indices = self.index.search(
            query_embedding,
            min(top_k, len(self.chunks)),
        )

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index < 0:
                continue

            results.append(
                (
                    self.chunks[index],
                    float(score),
                )
            )

        return results

    def save(self, directory: str | Path) -> None:
        """Save the FAISS index and chunks to disk."""

        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)

        if self.index is None:
            raise ValueError("Vector store is empty.")

        faiss.write_index(
            self.index,
            str(directory / "index.faiss"),
        )

        with open(directory / "chunks.pkl", "wb") as file:
            pickle.dump(self.chunks, file)

    def load(self, directory: str | Path) -> None:
        """Load the FAISS index and chunks from disk."""

        directory = Path(directory)

        index_path = directory / "index.faiss"
        chunks_path = directory / "chunks.pkl"

        if not index_path.exists():
            raise FileNotFoundError(
                f"Vector index not found: {index_path}"
            )

        if not chunks_path.exists():
            raise FileNotFoundError(
                f"Chunks file not found: {chunks_path}"
            )

        self.index = faiss.read_index(
            str(index_path)
        )

        with open(chunks_path, "rb") as file:
            self.chunks = pickle.load(file)
