from .vector_store import VectorStore
from .models import DocumentChunk, SearchResult


class Retriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[SearchResult]:

        results = self.vector_store.search(
            query,
            top_k=top_k,
        )

        search_results = []

        for chunk, score in results:
            search_results.append(
                SearchResult(
                    text=chunk.text,
                    score=score,
                    source_file=chunk.source_file,
                    source_type=chunk.source_type,
                    location=chunk.location,
                    metadata=chunk.metadata,
                )
            )

        return search_results