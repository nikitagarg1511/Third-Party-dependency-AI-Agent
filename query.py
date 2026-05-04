import json
from llama_index.core import StorageContext, load_index_from_storage
from models import FinalResponse
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

import config
Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0.9)

def load_index():
    storage_context = StorageContext.from_defaults(
        persist_dir=config.STORAGE_PATH
    )
    return load_index_from_storage(storage_context)


def query_engine_simple(index):
    query_engine = index.as_query_engine(
    similarity_top_k=3,    
    output_cls=FinalResponse,
    response_mode="compact",
    node_postprocessors=[]
    )
    return query_engine

def main():
    index = load_index()
    query_engine = query_engine_simple(index)

    prompt = (
    "Context information is below. \n"
    "---------------------\n"
    "Answer the user's question using ONLY the provided context. "
    "If the answer is not present in the context, respond with 'I do not know' "
    "for the answer and explanation fields. Do not use your own knowledge.\n"
    "Respond in json format: "
    "{\"answer\": \"...\", \"explanation\": \"...\", \"file_name\": \"...\", \"page_number\": \"...\"}"
)
    # prompt = "Answer what the user asks. Respond in json format. In the json format, give the output in this structure {\"answer\": \"The answer for the query user asked\", \"explanation\": \"Explanation for the answer. This will be the exact text from the context provided,\"file_name\": \"Name of the file for the context used \", \"page_number\": \"Page number of the context node\" }"

    print("\n💬 Simple RAG Query System Ready\n")

    while True:
        query = input("Ask your question: ")

        if query.lower() == "exit":
            break

        result = query_engine.query(prompt + query)
        print(result)

        print("\n--- DETAILED RETRIEVED NODES ---")
        
        # Define your threshold (0.80 is usually a 'good' match, 0.75 is 'fair')
        SIMILARITY_THRESHOLD = 0.80
        nodes_displayed = 0

        for i, node_with_score in enumerate(result.source_nodes, 1):
            # Check if the score is high enough to be considered relevant
            if node_with_score.score < SIMILARITY_THRESHOLD:
                continue  # Skip this node and move to the next one
            
            nodes_displayed += 1
            node = node_with_score.node
            
            # Extract metadata safely
            page_num = node.metadata.get('page_label') or node.metadata.get('page_number') or "Unknown"
            file_name = node.metadata.get('file_name', 'Unknown')
            
            print(f"DEBUG: Node {i} [Score: {node_with_score.score:.4f}]")
            print(f"SOURCE: {file_name} (Page: {page_num})")
            print("-" * 20)
            
            # .get_content() retrieves the full text of the chunk
            full_text = node.get_content().strip()
            
            print("FULL TEXT CONTENT:")
            print(full_text) 
            print("=" * 50)

        # If the loop finishes and no nodes were printed
        if nodes_displayed == 0:
            print(f"⚠️ No nodes met the similarity threshold of {SIMILARITY_THRESHOLD}.")
            print("The AI likely used its internal knowledge or refused to answer.")


if __name__ == "__main__":
    main()