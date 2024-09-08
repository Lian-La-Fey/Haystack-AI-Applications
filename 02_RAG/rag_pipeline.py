import os

from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack_integrations.components.embedders.cohere import CohereTextEmbedder
from haystack_integrations.components.generators.ollama import OllamaGenerator


def create_rag_pipeline(document_store, template, model="mistral", timeout=1200):
    query_embedder = CohereTextEmbedder(model="embed-english-v3.0", api_base_url=os.getenv("CO_API_URL"))
    retriever = InMemoryEmbeddingRetriever(document_store=document_store)
    prompt_builder = PromptBuilder(template=template)
    generator = OllamaGenerator(model=model, timeout=timeout)

    # Build RAG
    rag_pipeline = Pipeline()
    rag_pipeline.add_component("query_embedder", query_embedder)
    rag_pipeline.add_component("retriever", retriever)
    rag_pipeline.add_component("prompt", prompt_builder)
    rag_pipeline.add_component("generator", generator)

    # Connect components
    rag_pipeline.connect("query_embedder.embedding", "retriever.query_embedding")
    rag_pipeline.connect("retriever.documents", "prompt.documents")
    rag_pipeline.connect("prompt", "generator")
    
    rag_pipeline.draw("./rag.png")

    return rag_pipeline

def ask_question(rag_pipeline, question, language="English", top_k=1):
    result = rag_pipeline.run(
        {
            "query_embedder": {"text": question},
            "retriever": {"top_k": top_k},
            "prompt": {"query": question, "language": language},
        }
    )
    return result["generator"]["replies"][0]
