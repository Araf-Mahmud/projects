import re, hashlib, math
from qdrant_client import models
def group_name_extractor(text:str) -> tuple :
    match = re.search(r"^\d+:\s+(.*?)\s+(Q\d+:.*)", text, re.DOTALL | re.MULTILINE)

    if match:
        heading = match.group(1)
        content = match.group(2)
        
        return (heading.strip(), content.strip())
    
def hash_content(text:str) -> str:
    
    encoded_text = text.encode('utf-8')
    
    hash_obj = hashlib.sha256(encoded_text)
    
    return hash_obj.hexdigest()

def tokenize(text: str) -> list:
    return re.findall(r'[a-z0-9]+', text.lower())

def get_sparse_vector(text: str):
    
    tokens = tokenize(text)
    
    freq : dict[int, int] = {}
    
    for tok in tokens:
        hash_tok = int.from_bytes(hashlib.blake2b(tok.encode('utf-8'), digest_size = 8).digest()[:4], 'big')
        
        freq[hash_tok] = freq.get(hash_tok, 0) + 1
        
    return models.SparseVector(
        indices = list(freq.keys()),
        values = [1 + math.log(v) for v in freq.values()]
    )