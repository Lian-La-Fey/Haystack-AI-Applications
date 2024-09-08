import os
import argparse

from pipeline import create_indexing_pipeline, create_search_pipeline
from document_store import get_document_store

STORE_PATH=r"store\DaVinci_document_store.json"

def create_store_path():
    directory = os.path.dirname(STORE_PATH)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

def run_indexing_pipeline():
    document_store = get_document_store()

    indexing_pipeline = create_indexing_pipeline(document_store)
    indexing_pipeline.draw("./indexing_pipeline.png")
    indexing_pipeline.run({"converter": {"sources": ['data/davinci.txt']}})
    
    print(document_store.filter_documents()[-1].content)
    
    create_store_path()
    document_store.save_to_disk(STORE_PATH)

def run_search_pipeline(question):
    document_store = get_document_store(file_path=STORE_PATH)
    
    search_pipeline = create_search_pipeline(document_store)
    search_pipeline.draw("./search_pipeline.png")
    
    results = search_pipeline.run({"query_embedder": {"text": question}, "retriever": {"top_k": 5}})
    
    for i, document in enumerate(results["retriever"]["documents"]):
        print("\n--------------\n")
        print(f"DOCUMENT {i}")
        print(document.content)

def main():
    parser = argparse.ArgumentParser(description="Run indexing or search pipeline")
    parser.add_argument(
        '--pipeline', 
        choices=['indexing', 'search'], 
        required=True, 
        help="Choose which pipeline to run: 'indexing' or 'search'"
    )
    parser.add_argument(
        '--question',
        type=str,
        help="The question to ask the search pipeline (required if --pipeline search)",
        required=False
    )
    
    args = parser.parse_args()
    
    if args.pipeline == 'indexing':
        run_indexing_pipeline()
    elif args.pipeline == 'search':
        if not args.question:
            parser.error("--question is required when --pipeline is 'search'")
        run_search_pipeline(args.question)

if __name__ == "__main__":
    main()