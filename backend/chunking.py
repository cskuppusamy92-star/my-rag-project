from typing import List

from backend.models import ExtractedDocument, DocumentChunk


def chunk_documents(
    documents: List[ExtractedDocument],
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> List[DocumentChunk]:
    """
    Split extracted documents into smaller chunks.

    Args:
        documents: Extracted documents.
        chunk_size: Maximum number of characters per chunk.
        chunk_overlap: Number of characters shared between chunks.

    Returns:
        List of DocumentChunk objects.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks: List[DocumentChunk] = []

    for document_index, document in enumerate(documents):
        text = document.text.strip()

        if not text:
            continue

        start = 0
        chunk_index = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunk_id = (
                    f"{document.source_file}:"
                    f"{document_index}:"
                    f"{chunk_index}"
                )

                chunks.append(
                    DocumentChunk(
                        text=chunk_text,
                        source_file=document.source_file,
                        source_type=document.source_type,
                        location=document.location.copy(),
                        chunk_id=chunk_id,
                        document_id=document.source_file,
                        metadata={
                            "chunk_index": chunk_index,
                            "start": start,
                            "end": end,
                        },
                    )
                )

            if end >= len(text):
                break

            start = end - chunk_overlap
            chunk_index += 1

    return chunks
