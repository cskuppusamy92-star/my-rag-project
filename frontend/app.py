import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


def query_backend(question: str, top_k: int = 5):

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


# -----------------------------
# Streamlit configuration
# -----------------------------

st.set_page_config(
    page_title="RAG Gen AI",
    page_icon="🤖",
    layout="centered"
)


# -----------------------------
# UI
# -----------------------------

st.title("🤖 RAG Gen AI")

st.write(
    "Ask questions about your documents."
)


question = st.chat_input(
    "Ask a question about your document..."
)


# -----------------------------
# Question processing
# -----------------------------

if question:

    # User message
    with st.chat_message("user"):
        st.write(question)

    # Assistant response
    with st.chat_message("assistant"):

        try:

            # Call FastAPI backend
            data = query_backend(
                question,
                top_k=5
            )

            # Get generated answer
            answer = data.get(
                "answer",
                "No answer returned."
            )

            # Get retrieved sources
            results = data.get(
                "results",
                []
            )

            # -----------------------------
            # Display Answer
            # -----------------------------

            st.subheader("💡 Answer")

            st.write(answer)


            # -----------------------------
            # Display Sources
            # -----------------------------

            if results:

                st.subheader("📚 Sources")

                for i, result in enumerate(
                    results,
                    start=1
                ):

                    score = result.get(
                        "score",
                        0
                    )

                    source_file = result.get(
                        "source_file",
                        "Unknown"
                    )

                    source_type = result.get(
                        "source_type",
                        "Unknown"
                    )

                    location = result.get(
                        "location",
                        {}
                    )

                    text = result.get(
                        "text",
                        ""
                    )

                    with st.expander(
                        f"Source {i} — "
                        f"{source_file} "
                        f"(score: {score:.4f})"
                    ):

                        st.write(
                            f"**File:** {source_file}"
                        )

                        st.write(
                            f"**Type:** {source_type}"
                        )

                        st.write(
                            f"**Score:** {score:.4f}"
                        )

                        if location:
                            st.write(
                                f"**Location:** {location}"
                            )

                        st.write("---")

                        st.write(text)

            else:

                st.warning(
                    "No relevant sources found."
                )


        except requests.RequestException as e:

            st.error(
                f"Could not connect to backend: {e}"
            )

        except Exception as e:

            st.error(
                f"Unexpected error: {e}"
            )