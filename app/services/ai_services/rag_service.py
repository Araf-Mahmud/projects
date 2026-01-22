from app.core.config import Config
from app.db.qdrant_clients import GetQdrantClient
from app.services.embedding_services.cohere_embedding_service import get_embeddings
import logging

class CustomRAG:
    
    _initialized = False
    
    def __init__(self):
        if self._initialized:
            return
        
        self.config = Config()
        self.qdrant_client = GetQdrantClient.get_qdrant_client()
        self.collection_name = self.config.COLLECTION_NAME
        
    def retrieve_documents(self, query:str):
        
        embedded_query = get_embeddings(query) 
        
        query_response = self.qdrant_client.query_points(
            collection_name = self.collection_name,
            query = embedded_query,
            limit = 8,
            with_payload=True,
            with_vectors=False
        )
        
        results = query_response.points if query_response.points else ""
        
        if not results:
            logging.warning(f'[RAG] : No Data Retrieved from Collection: {self.collection_name}')
            return ""
        
        scored_results = [(result, result.score) for result in results ]
        
        scored_results.sort(key = lambda x : x[1],reverse = True)
        
        top_score = scored_results[0][1]
        
        if scored_results:
            min_threshold = min(0.4, top_score * 0.7)
        else:
            min_threshold = 0.4
            
        filtered_matches = [doc for doc, score in scored_results if score >= min_threshold]
        
        top_k = 3
        
        if not filtered_matches:
            if scored_results and scored_results[0][1] >= 0.3:
                filtered_matches = [scored_results[0][0]]
                
            else:
                return ""
        
        else:
            filtered_matches = filtered_matches[:top_k]  
            
        retrieved_docs = [doc.payload['Text'] for doc in filtered_matches]  
        
        retrieved_context = ('\n').join(retrieved_docs)

        print(retrieved_context)

        return retrieved_context
    
        
        
        
        
        
        
        
        
        
        
        
        
