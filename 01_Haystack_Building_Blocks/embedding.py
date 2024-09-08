import os

from haystack_integrations.components.embedders.ollama import OllamaDocumentEmbedder
from haystack_integrations.components.embedders.ollama import OllamaTextEmbedder

def get_document_embedder(model_name="nomic-embed-text"):
    return OllamaDocumentEmbedder(model=model_name)

def get_text_embedder(model_name="nomic-embed-text"):
    return OllamaTextEmbedder(model=model_name)