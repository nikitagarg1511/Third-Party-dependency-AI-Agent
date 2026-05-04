# PDF RAG Chat

A Retrieval-Augmented Generation (RAG) chatbot for querying PDF documents using Streamlit, LlamaIndex, and OpenAI.

## Features

- **PDF Document Indexing**: Automatically index PDF documents from a specified directory
- **Intelligent Querying**: Ask questions about your documents and get accurate answers
- **Source Attribution**: View the exact source text, file name, and page number for each answer
- **Streamlit Interface**: User-friendly web interface for easy interaction
- **Structured Responses**: Responses include answer, explanation, and metadata in JSON format

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/pdf-rag-chat.git
   cd pdf-rag-chat
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### 1. Index Your Documents

Place your PDF files in the `data/` directory, then run the indexing script:

```bash
python indexing.py
```

This will process all PDFs, create text chunks, and build a vector index stored in the `storage/` directory.

### 2. Run the Chat Application

Start the Streamlit app:

```bash
streamlit run app.py
```

Open your browser to the provided URL (usually `http://localhost:8501`) and start asking questions about your documents.

### 3. Query from Command Line (Optional)

You can also use the query system directly:

```bash
python query.py
```

Type your questions and get JSON responses. Type "exit" to quit.

## Configuration

- **DATA_PATH**: Directory containing PDF files (default: `data/`)
- **STORAGE_PATH**: Directory for storing the vector index (default: `storage/`)
- **LLM Model**: Currently configured to use GPT-4o-mini (can be changed in `query.py`)
- **Chunk Settings**: Chunk size and overlap can be adjusted in `indexing.py`

## How It Works

1. **Document Loading**: PDFs are loaded and parsed using PyMuPDF
2. **Text Chunking**: Documents are split into manageable chunks using sentence-aware splitting
3. **Embedding Creation**: Text chunks are converted to vector embeddings using OpenAI's embedding model
4. **Index Building**: A vector store index is created for efficient similarity search
5. **Query Processing**: User questions are embedded and matched against the index
6. **Response Generation**: Relevant context is passed to the LLM to generate accurate answers

## Project Structure

```
├── app.py              # Streamlit web application
├── config.py           # Configuration settings
├── embedding.py        # Embedding utilities (incomplete)
├── indexing.py         # Document indexing script
├── models.py           # Pydantic response models
├── query.py            # Query engine and CLI interface
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── LICENSE             # MIT License
├── data/               # Directory for PDF documents
└── storage/            # Directory for vector index storage
```

## Dependencies

- **llama-index**: Core RAG framework
- **llama-index-llms-openai**: OpenAI LLM integration
- **llama-index-embeddings-openai**: OpenAI embeddings
- **pypdf**: PDF processing (via PyMuPDF)
- **streamlit**: Web interface
- **python-dotenv**: Environment variable management

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

If you encounter any issues or have questions, please open an issue on GitHub.