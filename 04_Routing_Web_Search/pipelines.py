from haystack import Pipeline
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.routers import ConditionalRouter
from haystack.components.websearch.serper_dev import SerperDevWebSearch
from haystack_integrations.components.generators.ollama import OllamaGenerator

from templates import rag_prompt_template, websearch_prompt_template

def create_rag_pipeline(document_store, model):
    rag = Pipeline()
    rag.add_component("retriever", InMemoryBM25Retriever(document_store=document_store))
    rag.add_component("prompt_builder", PromptBuilder(template=rag_prompt_template))
    rag.add_component("llm", OllamaGenerator(model=model, timeout=1200))

    rag.connect("retriever.documents", "prompt_builder.documents")
    rag.connect("prompt_builder", "llm")
    
    return rag

def create_conditional_pipeline(document_store, model):
    routes = [
        {
            "condition": "{{'no_answer' in replies[0]|lower}}",
            "output": "{{query}}",
            "output_name": "go_to_websearch",
            "output_type": str,
        },
        {
            "condition": "{{'no_answer' not in replies[0]|lower}}",
            "output": "{{replies[0]}}",
            "output_name": "answer",
            "output_type": str,
        },
    ]

    rag_or_websearch = Pipeline()
    rag_or_websearch.add_component("retriever", InMemoryBM25Retriever(document_store=document_store))
    rag_or_websearch.add_component("prompt_builder", PromptBuilder(template=rag_prompt_template))
    rag_or_websearch.add_component("llm", OllamaGenerator(model=model, timeout=1200))
    rag_or_websearch.add_component("router", ConditionalRouter(routes))
    rag_or_websearch.add_component("websearch", SerperDevWebSearch())
    rag_or_websearch.add_component("prompt_builder_for_websearch", PromptBuilder(template=websearch_prompt_template))
    rag_or_websearch.add_component("llm_for_websearch", OllamaGenerator(model=model, timeout=1200))

    rag_or_websearch.connect("retriever", "prompt_builder.documents")
    rag_or_websearch.connect("prompt_builder", "llm")
    rag_or_websearch.connect("llm.replies", "router.replies")
    rag_or_websearch.connect("router.go_to_websearch", "websearch.query")
    rag_or_websearch.connect("router.go_to_websearch", "prompt_builder_for_websearch.query")
    rag_or_websearch.connect("websearch.documents", "prompt_builder_for_websearch.documents")
    rag_or_websearch.connect("prompt_builder_for_websearch", "llm_for_websearch")

    return rag_or_websearch
