from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.file.pymu_pdf import PyMuPDFReader
import config

def run_indexing():
    print("Loading documents...")
    
    # 1. Initialize the PyMuPDFReader
    pdf_reader = PyMuPDFReader()

    # 2. Map the .pdf extension to the PyMuPDFReader
    # This tells SimpleDirectoryReader: "If you see a PDF, use this specific tool."
    file_extractor = {".pdf": pdf_reader}

    # 3. Pass the extractor to the reader
    documents = SimpleDirectoryReader(
        config.DATA_PATH, 
        file_extractor=file_extractor
    ).load_data()

    print(f"Successfully loaded {len(documents)} document pages.")

    print("Chunking documents...")
    # Use SentenceSplitter (modern replacement for SimpleNodeParser)
    # It respects sentence boundaries so chunks make more sense.
    #sentensesplitter
    parser = SentenceSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    nodes = parser.get_nodes_from_documents(documents)

    print(f"Created {len(nodes)} nodes.")

    print("Creating index...")
    index = VectorStoreIndex(nodes)

    print("Saving index...")
    index.storage_context.persist(persist_dir=config.STORAGE_PATH)

    print("✅ Indexing completed!")

if __name__ == "__main__":
    run_indexing()