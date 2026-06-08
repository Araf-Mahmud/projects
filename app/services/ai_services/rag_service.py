from app.core.config import Config
from qdrant_client import models
from app.db.qdrant_clients import GetQdrantClient
from app.services.embedding_services.cohere_embedding_service import get_embeddings
from app.utils.utils import get_sparse_vector
import logging

class CustomRAG:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.config = Config()
        self.qdrant_client = GetQdrantClient.get_qdrant_client()
        self.collection_name = self.config.COLLECTION_NAME
        self._initialized = True

    def retrieve_documents(self, query: str):

        dense_query = get_embeddings(query)
        sparse_query = get_sparse_vector(query)

        dense_results = self.qdrant_client.query_points(
            collection_name = self.collection_name,
            query = dense_query,
            using = 'dense',
            limit = 8,
            with_payload=True,
            with_vectors=False
        )

        sparse_results = self.qdrant_client.query_points(
            collection_name = self.collection_name,
            query = sparse_query,
            using = 'lexical',
            limit = 8,
            with_payload=True,
            with_vectors=False
        )
        
        common_ids = set(result.id for result in dense_results.points) & set(result.id for result in sparse_results.points)

        filtered_dense_results = {res.id : res for res in dense_results.points if res.id in common_ids}
        filtered_sparse_results = {res.id : res for res in sparse_results.points if res.id in common_ids}

        
        results = []

        for id in common_ids:
            dense_result = filtered_dense_results[id]
            sparse_result = filtered_sparse_results[id]
            combined_score = dense_result.score * 0.8 + sparse_result.score * 0.2
            
            combined_result = {
                'id' : id,
                'payload' : dense_result.payload,
                'score' : combined_score
            }
            
            results.append(combined_result)
        
        

        if not results:
            logging.warning(f'[RAG] : No Common Data Retrieved from Collection: {self.collection_name}')
            return ""


        scored_results = [(result, result['score']) for result in results]

        scored_results.sort(key = lambda x : x[1], reverse = True)

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

        retrieved_docs = [doc['payload']['Text'] for doc in filtered_matches]

        retrieved_context = ('\n').join(retrieved_docs)
        
        print(retrieved_context)

        return retrieved_context