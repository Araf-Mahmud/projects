import os
import uuid
import logging
import pymupdf 
import datetime
from qdrant_client import models
from qdrant_client.models import Distance
from app.db.qdrant_clients import GetQdrantClient
from app.core.config import Config
from app.utils.utils import group_name_extractor, hash_content
from app.services.embedding_services.cohere_embedding_service import get_embeddings

script_dir = os.path.dirname(os.path.abspath(__file__))

file_name = "Sample Knowledge Base.pdf"

abs_path = script_dir + "/" + file_name

class Index:
    def __init__(self, path):
        self.pdf_doc = pymupdf.open(path)
        self.client = GetQdrantClient.get_qdrant_client()
        self.collection_name = Config().COLLECTION_NAME
        
    def _indexing(self):
        existing_collection_names = [collection.name for collection in self.client.get_collections().collections]
        
        if self.collection_name not in existing_collection_names: 
            
            docs = []

            for page in self.pdf_doc:
                single_page_docs = page.get_text().split('Group ')
                docs += [doc.strip() for doc in single_page_docs if doc.strip()] 

            points = []

            for doc in docs: 
                
                group_name, content = group_name_extractor(doc)
                
                points.append(
                    models.PointStruct(
                        id = str(uuid.uuid4()),
                        payload = {
                            'group_name' : group_name,
                            'Text' : content,
                            'hash' : hash_content(content),
                            'source' : file_name,
                            'timestamp' : datetime.datetime.now(datetime.timezone.utc).isoformat()
                        },
                        vector = get_embeddings(doc)
                    )
                )
            
            existing_collection_names = [collection.name for collection in self.client.get_collections().collections]
            
            if self.collection_name not in existing_collection_names: 
                self.client.create_collection(
                collection_name = self.collection_name,  
                vectors_config = models.VectorParams(
                        size = 1536,                
                        distance = Distance.COSINE
                    )
                )
                
                print("Data Insertion Started...")
                
                self.client.upsert(
                    collection_name = self.collection_name,
                    points = points
                )
        
        else:
            logging.info(f"{self.collection_name} is already exist.")
            
if __name__ == '__main__':
    qdrant_obj = Index(abs_path)
    qdrant_obj._indexing()
    print("Indexing Completed.")
    
        

    

    
