import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def query_backend(question: str, top_k: int = 2):
    response = requests.post(
        f"{API_URL}/query",
        json={
            "question": question,
            "top_k": top_k
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()

st.set_page_config(
    page_title="RAG Gen AI",
    page_icon="🤖"
)

st.title("🤖 RAG Gen AI")
st.write("Ask questions about your documents.")

question = st.chat_input("Ask a question...")

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        try:
            data = query_backend(question, top_k=2)

            results = data.get("results", [])

            if results:
                st.write(results[0]["text"])

                if len(results) > 1:
                    st.subheader("Sources")

                    for i, result in enumerate(results, start=1):
                        st.write(
                            f"**Source {i}** — "
                            f"Score: {result.get('score', 0):.4f}"
                        )
                        st.write(result.get("text", ""))

            else:
                st.write("No relevant information found.")

        except requests.RequestException as e:
            st.error(f"Could not connect to backend: {e}")