from dotenv import load_dotenv
from typing import List
from app.core.config import Config
load_dotenv()

config = Config()

co = config.get_embedding_client()

def get_embeddings(doc : str) :
    response = co.embed(
    texts = [doc],
    model = config.EMBEDDING_MODEL, 
    )

    embeddings = response.embeddings[0][0] 

    print(f"Number of embeddings: {len(embeddings)}")
    print(f"Dimension of each embedding: {len(embeddings[:10])}")


