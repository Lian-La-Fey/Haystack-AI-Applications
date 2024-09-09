import os
import sys
import argparse

from document_loader import get_document_store
from pipelines import create_rag_pipeline, create_conditional_pipeline

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env_config import load_env_variables

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default="mistral", help='Name of the model')
    parser.add_argument('--query1', type=str, default="What is a retriever for?")
    parser.add_argument('--query2', type=str, default="What Mistral components does Haystack have?")
    args = parser.parse_args()
    
    load_env_variables()
    
    document_store = get_document_store()
    rag_pipeline = create_rag_pipeline(document_store, model=args.model)
    rag_pipeline.draw("rag_pipeline.jpg")
    
    query = args.query1
    print(rag_pipeline.run({"prompt_builder": {"query": query},
                            "retriever": {"query": query}})["llm"]["replies"][0])
    
    conditional_pipeline = create_conditional_pipeline(document_store, model=args.model)
    conditional_pipeline.draw("conditional_pipeline.jpg")
    
    query = args.query2
    conditional_rag = conditional_pipeline.run({"prompt_builder": {"query": query},
                                    "retriever": {"query": query},
                                    "router": {"query": query}})
    print("Websearch Links:", conditional_rag["websearch"]["links"], sep="\n", end="\n\n")
    print("Reply:", conditional_rag["llm_for_websearch"]["replies"][0], sep="\n")

if __name__ == "__main__":
    main() 