import os

from haystack import Pipeline
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.converters import HTMLToDocument
from haystack.components.writers import DocumentWriter
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack_integrations.components.embedders.cohere import CohereDocumentEmbedder


def create_document_indexing_pipeline():
    document_store = InMemoryDocumentStore()
    fetcher = LinkContentFetcher()
    converter = HTMLToDocument()
    embedder = CohereDocumentEmbedder(model="embed-english-v3.0", api_base_url=os.getenv("CO_API_URL"))
    writer = DocumentWriter(document_store=document_store)

    # Build pipeline
    indexing_pipeline = Pipeline()
    indexing_pipeline.add_component("fetcher", fetcher)
    indexing_pipeline.add_component("converter", converter)
    indexing_pipeline.add_component("embedder", embedder)
    indexing_pipeline.add_component("writer", writer)

    # Connect components
    indexing_pipeline.connect("fetcher.streams", "converter.sources")
    indexing_pipeline.connect("converter", "embedder")
    indexing_pipeline.connect("embedder", "writer")
    
    indexing_pipeline.draw("./indexing.png")
    
    return indexing_pipeline, document_store

def run_document_indexing(indexing_pipeline):
    indexing_pipeline.run(
        {
            "fetcher": {
                "urls": [
                    "https://haystack.deepset.ai/integrations/cohere",
                    "https://haystack.deepset.ai/integrations/anthropic",
                    "https://haystack.deepset.ai/integrations/jina",
                    "https://haystack.deepset.ai/integrations/nvidia",
                ]
            }
        }
    )
