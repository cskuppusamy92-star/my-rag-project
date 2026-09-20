import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv(
    "EMBEDDING_MODEL",
    "text-embedding-3-small",
)

if not api_key:
    raise RuntimeError("OPENAI_API_KEY was not found in .env")


client = OpenAI(api_key=api_key)

texts = [
    "The ABC Scheme is administered by the Industries Department.",
    "Applicants must submit an identity proof and project report.",
]

response = client.embeddings.create(
    model=model,
    input=texts,
)

embeddings = [
    item.embedding
    for item in response.data
]

print("Embedding model:", model)
print("Number of embeddings:", len(embeddings))
print("Vector dimensions:", len(embeddings[0]))
print("First vector created:", len(embeddings[0]) > 0)
print("Second vector created:", len(embeddings[1]) > 0)