import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("CHAT_MODEL", "gpt-4o-mini")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY was not found in .env")


client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: OpenAI connection successful.",
        }
    ],
)

answer = response.choices[0].message.content

print("Model:", model)
print("Response:", answer)