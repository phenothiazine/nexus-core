
import chromadb
from typing import List, Dict, Any
from core.config import Config
import uuid

class MemoryManager:
    """
    Manages long-term memory using ChromaDB for RAG.
    """
    def __init__(self, collection_name: str = "nexus_memory"):
        """
        Initialize the ChromaDB client and collection.
        
        Args:
            collection_name (str): Name of the ChromaDB collection.
        """
        try:
            # Initialize persistent client to save data to disk
            self.client = chromadb.PersistentClient(path=Config.CHROMA_PERSIST_DIRECTORY)
            self.collection = self.client.get_or_create_collection(name=collection_name)
        except Exception as e:
            print(f"Error initializing Memory Manager: {e}")
            raise e

    def add_document(self, text: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Add a document to the memory.
        
        Args:
            text (str): The content of the document/note.
            metadata (Dict[str, Any], optional): Additional metadata.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        if metadata is None:
            metadata = {}
            
        try:
            doc_id = str(uuid.uuid4())
            self.collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[doc_id]
            )
            return True
        except Exception as e:
            print(f"Error adding document: {e}")
            return False

    def process_file(self, file_obj, filename: str) -> bool:
        """
        Process and store an uploaded file (PDF or TXT).
        
        Args:
            file_obj: The uploaded file object.
            filename (str): The name of the file.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            text = ""
            
            # 1. Extract Text based on extension
            if filename.lower().endswith(".pdf"):
                from pypdf import PdfReader
                reader = PdfReader(file_obj)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            elif filename.lower().endswith(".txt"):
                text = file_obj.read().decode("utf-8")
            else:
                return False
                
            if not text.strip():
                return False

            # 2. Chunking Strategy (Simple fixed-size chunking)
            chunk_size = 1000
            overlap = 100
            chunks = []
            
            for i in range(0, len(text), chunk_size - overlap):
                chunks.append(text[i:i + chunk_size])
            
            # 3. Add chunks to ChromaDB
            ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
            metadatas = [{"source": filename, "chunk_id": i} for i in range(len(chunks))]
            
            self.collection.add(
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            return True
            
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            return False

    def query_context(self, query: str, n_results: int = 3) -> List[str]:
        """
        Retrieve relevant context for a given query.
        
        Args:
            query (str): The search query.
            n_results (int): Number of results to return.
            
        Returns:
            List[str]: A list of relevant document contents.
        """
        try:
            # Check if collection is empty to avoid errors
            if self.collection.count() == 0:
                return []
                
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # ChromaDB returns a list of lists for 'documents'
            if results and results.get("documents"):
                return results["documents"][0]
            return []
        except Exception as e:
            print(f"Error querying context: {e}")
            return []
