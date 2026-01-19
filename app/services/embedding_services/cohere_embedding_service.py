from dotenv import load_dotenv
from app.core.config import Config

load_dotenv()

config = Config()

co = config.get_embedding_client()

def get_embeddings(doc : str) :
    response = co.embed(
    texts = [doc],
    model = config.EMBEDDING_MODEL, 
    input_type="search_document",
    embedding_types=["float"]
    )

    embeddings = response.embeddings.float[0]

    return embeddings


