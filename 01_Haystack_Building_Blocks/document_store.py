from haystack.document_stores.in_memory import InMemoryDocumentStore

def get_document_store(file_path=None):
    if file_path:
        print(f"Loading document store from {file_path}")
        return InMemoryDocumentStore.load_from_disk(file_path)
    
    print("Creating new document store")
    return InMemoryDocumentStore()