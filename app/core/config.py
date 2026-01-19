import os
import cohere
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        
        if self._initialized:
            return 
        
        self.initialized = True
        
        self.COHERE_API_KEY = os.getenv('COHERE_API_KEY')
        
        self.QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
        self.QDRANT_URL = os.getenv('QDRANT_URL')
        
        self.EMBEDDING_MODEL = "embed-v4.0"
        
        self.COLLECTION_NAME = os.getenv("COLLECTION_NAME")
        
    def get_embedding_client(self):
        return cohere.Client(self.COHERE_API_KEY)
        
        
        
        
        
            
        