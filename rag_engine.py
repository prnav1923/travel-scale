
import os
import glob
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class RagEngine:
    def __init__(self, api_key):
        self.api_key = api_key
        # Use local embeddings to avoid API rate limits
        print("Initializing local embeddings...")
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = None
        self.documents = []

    def ingest(self, directory_path):
        """Load and split documents from a directory."""
        print(f"Loading documents from {directory_path}...")
        loader = DirectoryLoader(directory_path, glob="*.md", loader_cls=TextLoader)
        raw_docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
        )
        self.documents = text_splitter.split_documents(raw_docs)
        print(f"Split into {len(self.documents)} chunks.")
        return len(self.documents)

    def build_index(self):
        """Create FAISS index from loaded documents."""
        if not self.documents:
            print("No documents to index.")
            return
        
        print("Building vector index...")
        self.vector_store = FAISS.from_documents(self.documents, self.embeddings)
        print("Index built successfully.")

    def save_index(self, folder_path="vector_store"):
        """Save the vector index to disk."""
        if self.vector_store:
            self.vector_store.save_local(folder_path)
            print(f"Index saved to {folder_path}")

    def load_index(self, folder_path="vector_store"):
        """Load the vector index from disk."""
        if os.path.exists(folder_path):
            self.vector_store = FAISS.load_local(
                folder_path, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
            print("Index loaded from disk.")
            return True
        return False

    def query(self, text, k=4):
        """Retrieve relevant documents."""
        if not self.vector_store:
            return []
        
        return self.vector_store.similarity_search(text, k=k)

if __name__ == "__main__":
    # Test script
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    rag = RagEngine(api_key)
    
    # Test 1: Ingest and Save
    if not os.path.exists("vector_store"):
        print("Creating new index...")
        rag.ingest("data")
        rag.build_index()
        rag.save_index()
    else:
        print("Loading existing index...")
        rag.load_index()
        
    # Test 2: Query
    results = rag.query("cost of food in Bangkok")
    for doc in results:
        print(f"\n[Source: {doc.metadata['source']}]\n{doc.page_content[:200]}...")
