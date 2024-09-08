import os
import sys
import argparse

from document_indexing import create_document_indexing_pipeline, run_document_indexing
from rag_pipeline import create_rag_pipeline, ask_question

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env_config import load_env_variables


def main():
    load_env_variables()
    
    parser = argparse.ArgumentParser(description="Run Customized RAG pipeline.")
    parser.add_argument(
        '--model',
        type=str,
        default="mistral",
        help="The model to be used in the generator. Default is 'mistral'. Options: 'mistral', 'llama3', etc."
    )
    
    args = parser.parse_args()
    
    indexing_pipeline, document_store = create_document_indexing_pipeline()
    run_document_indexing(indexing_pipeline)
    
    prompt_template = """
    You will be provided some context, followed by the URL that this context comes from.
    Answer the question based on the context, and reference the URL from which your answer is generated.
    Your answer should be in {{ language }}.
    Context:
    {% for doc in documents %}
       {{ doc.content }} 
       URL: {{ doc.meta['url']}}
    {% endfor %}
    Question: {{ query }}
    Answer:
    """
    
    rag_pipeline = create_rag_pipeline(document_store, template=prompt_template, model=args.model)
    question = "How can I use Cohere with Haystack?"
    answer = ask_question(rag_pipeline, question, language="German")
    print(answer)

if __name__ == "__main__":
    main()