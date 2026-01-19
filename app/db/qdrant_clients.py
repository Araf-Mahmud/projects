from qdrant_client import QdrantClient
from app.core.config import Config

class GetQdrantClient:
    _instance = None
    _client = None
    
    @classmethod
    def get_qdrant_client(cls):
        if not cls._client:
            config = Config()
            cls._client = QdrantClient(
                url = config.QDRANT_URL,
                api_key = config.QDRANT_API_KEY,
                timeout = 120
            )
        return cls._client
            
            
        
    