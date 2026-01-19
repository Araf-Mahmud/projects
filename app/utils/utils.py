import re, hashlib

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