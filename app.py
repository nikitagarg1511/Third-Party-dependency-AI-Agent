import streamlit as st
from query import load_index, query_engine_simple

# Load index once
@st.cache_resource
def get_index():
    return load_index()


st.set_page_config(page_title="PDF RAG Chat", layout="wide")

st.title("📄 Chat with your PDFs")
st.write("Ask questions based on your indexed documents")

index = get_index()
query_engine = query_engine_simple(index)

# User input
query = st.text_input("🔍 Enter your question:")
prompt = "Answer what the user asks. Respond in json format. In the json format, give the output in this structure {\"answer\": \"The answer for the query user asked\", \"explanation\": \"Explanation for the answer. This will be the exact text from the context provided,\"file_name\": \"Name of the file for the context used \", \"page_number\": \"Page number of the context node\" }"

if st.button("Ask"):
    if not query:
        st.warning("Please enter a question")
    else:
        with st.spinner("Thinking..."):
            result = query_engine.query(prompt+query)

        # Display Answer
        st.subheader("✅ Answer")
        st.write(result.answer)

        # Display Explanation (collapsible)
        with st.expander("📌 View Source Text"):
            st.write(result.explanation)

        # Metadata
        st.subheader("📂 Source Info")
        st.write(f"File: {result.file_name}")
        st.write(f"Page: {result.page_number}")