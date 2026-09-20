from pathlib import Path

from .extraction import extract_file
from .chunking import chunk_documents
from .models import DocumentChunk


def ingest_file(
    path: str | Path,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[DocumentChunk]:
    """
    Extract a document and split it into chunks.
    """

    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Step 1: Extract document content
    documents = extract_file(file_path)

    # Step 2: Create chunks
    chunks = chunk_documents(
        documents,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    return chunks