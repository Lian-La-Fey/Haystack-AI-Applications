from haystack import Pipeline
from haystack.components.converters.txt import TextFileToDocument
from haystack.components.preprocessors.document_splitter import DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever

from embedding import get_document_embedder
from embedding import get_text_embedder

def create_indexing_pipeline(document_store):
    converter = TextFileToDocument()
    splitter = DocumentSplitter()
    embedder = get_document_embedder()
    writer = DocumentWriter(document_store=document_store)

    indexing_pipeline = Pipeline()
    indexing_pipeline.add_component("converter", converter)
    indexing_pipeline.add_component("splitter", splitter)
    indexing_pipeline.add_component("embedder", embedder)
    indexing_pipeline.add_component("writer", writer)

    indexing_pipeline.connect("converter", "splitter")
    indexing_pipeline.connect("splitter", "embedder")
    indexing_pipeline.connect("embedder", "writer")
    
    return indexing_pipeline

def create_search_pipeline(document_store):

    query_embedder = get_text_embedder()
    retriever = InMemoryEmbeddingRetriever(document_store=document_store)

    search_pipeline = Pipeline()
    search_pipeline.add_component("query_embedder", query_embedder)
    search_pipeline.add_component("retriever", retriever)

    search_pipeline.connect("query_embedder.embedding", "retriever.query_embedding")
    
    return search_pipeline
