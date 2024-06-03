def main():
    st.title("PDF Question Answering System")

    # Sidebar for file upload
    with st.sidebar:
        uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        text = get_pdf_docs(uploaded_files)
        text_chunks = get_text_chunks(text)
        get_vector_store(text_chunks)

    # Main area for user interaction
    user_question = st.text_input("Enter your question:")
    if st.button("Ask the Question"):
        if uploaded_files and user_question:
            user_input(user_question)
        else:
            st.write("Please upload PDF files and enter a question.")

if __name__ == "__main__":
    main()
#est the function with a sample question
sample_question = "What is the content of the PDF?"
user_input(sample_question)
