from haystack import Document
from haystack.document_stores.in_memory import InMemoryDocumentStore

def load_documents():
    documents = [
        Document(content="Retrievers: Retrieves relevant documents to a user query using keyword search or semantic search."),
        Document(content="Embedders: Creates embeddings for text or documents."),
        Document(content="Generators: Use a number of model providers to generate answers or content based on a prompt"),
        Document(content="File Converters: Converts different file types like TXT, Markdown, PDF, etc. into a Haystack Document type")
    ]
    return documents

def get_document_store():
    document_store = InMemoryDocumentStore()
    document_store.write_documents(documents=load_documents())
    return document_store
