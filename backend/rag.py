from backend.ingestion import ingest_file
from backend.vector_store import VectorStore
from backend.retrieval import Retriever


class RAGPipeline:
    def __init__(self):
        self.store = VectorStore()
        self.retriever = Retriever(self.store)

    def ingest(self, file_path: str, chunk_size: int = 500, chunk_overlap: int = 100):
        chunks = ingest_file(
            file_path,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        self.store.add_chunks(chunks)
        self.store.save("data/vector_store")

        return {
            "documents": len(set(chunk.document_id for chunk in chunks)),
            "chunks": len(chunks)
        }

    def query(self, question: str, top_k: int = 5):
        results = self.retriever.retrieve(
            question,
            top_k=top_k
        )

        return results