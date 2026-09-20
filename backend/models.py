from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExtractedDocument:
    """
    Represents text extracted from an input document.
    """

    text: str
    source_file: str
    source_type: str
    location: dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentChunk:
    """
    Represents a chunk created from extracted document text.
    """

    text: str
    source_file: str
    source_type: str
    location: dict[str, Any] = field(default_factory=dict)

    chunk_id: str = ""
    document_id: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchResult:
    """
    Represents a retrieved chunk from the vector store.
    """

    text: str
    score: float
    source_file: str
    source_type: str
    location: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)