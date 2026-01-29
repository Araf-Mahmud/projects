import os
import cohere
import redis
from dotenv import load_dotenv
from pathlib import Path
from langchain_groq import ChatGroq

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
        
        self.GROQ_API_KEY = os.getenv('GROQ_API_KEY')

        
    def get_embedding_client(self):
        return cohere.Client(self.COHERE_API_KEY)
    
    def gpt_oss_response(self, messages : list[tuple]) -> str:
        model = ChatGroq(api_key = self.GROQ_API_KEY, model = 'openai/gpt-oss-120b', temperature = 0.4)
        response = model.invoke(messages).content
        return response
    
    def get_redis_client(self):
        return redis.Redis(
            host = 'localhost',
            port = 6379,
            decode_responses = True
        )
        
        
        
        
            
        