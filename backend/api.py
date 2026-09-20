import os

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from backend.rag import RAGPipeline


app = FastAPI(
    title="RAG Gen AI API",
    description="Document Retrieval and Question Answering API",
    version="1.0.0",
)


rag = RAGPipeline()


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    upload_dir = "data/test_documents"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    result = rag.ingest(file_path)

    return {
        "filename": file.filename,
        **result
    }

@app.get("/")
def root():
    return {
        "message": "RAG Gen AI API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.post("/query")
def query(request: QueryRequest):
    result = rag.query(
        request.question,
        top_k=request.top_k
    )

    return {
        "question": request.question,
        "answer": result["answer"],
        "results": [
            {
                "score": item.score,
                "text": item.text,
                "source_file": item.source_file,
                "source_type": item.source_type,
                "location": item.location,
                "metadata": item.metadata,
            }
            for item in result["results"]
        ],
    }