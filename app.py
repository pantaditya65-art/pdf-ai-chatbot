
import streamlit as st
from openai import OpenAI
from pypdf import PdfReader
from io import BytesIO

st.set_page_config(
    page_title="PDF AI Assistant",
    page_icon="📄",
    layout="centered"
)

st.title("📄 PDF AI Assistant")
st.caption("Upload a document and ask questions about its contents.")

# Read the API key from .streamlit/secrets.toml
api_key = st.secrets.get("OPENAI_API_KEY", "")

if not api_key:
    st.error("API key missing. Check .streamlit/secrets.toml.")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)

if uploaded_file:
    try:
        reader = PdfReader(BytesIO(uploaded_file.getvalue()))
        pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append(
                    f"[Page {page_number}]\n{text}"
                )

        document_text = "\n\n".join(pages)

        if not document_text.strip():
            st.warning(
                "No readable text found. "
                "This PDF may contain scanned images."
            )
            st.stop()

        st.success(
            f"PDF loaded: {len(reader.pages)} pages"
        )

        # Keep document content available to the chat model
        if st.session_state.get("pdf_name") != uploaded_file.name:
            st.session_state.pdf_name = uploaded_file.name
            st.session_state.pdf_text = document_text
            st.session_state.messages = []

    except Exception as error:
        st.error(f"Could not read PDF: {error}")
        st.stop()

else:
    st.info("Upload a PDF to start asking questions.")
    st.stop()

# Display conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask something about your PDF...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Reading your document and thinking..."):
            try:
                # Send the document with the question
                response = client.chat.completions.create(
                    model="openrouter/free",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Answer questions using the provided PDF. "
                                "If the answer is not in the document, "
                                "say so. Cite the page numbers shown in "
                                "the document text when possible."
                            )
                        },
                        {
                            "role": "user",
                            "content": (
                                "PDF CONTENT:\n\n"
                                + st.session_state.pdf_text
                                + "\n\nQUESTION:\n"
                                + question
                            )
                        }
                    ]
                )

                answer = response.choices[0].message.content
                if not answer:
                    answer = "The model returned an empty response."

                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as error:
                st.error(f"API request failed: {error}")