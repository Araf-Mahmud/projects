import redis, json

EXPIRY_SESSION = 90
LIMIT = 6

redis_client = redis.Redis(
    host = 'localhost',
    port = 6379,
    decode_responses = True
)

def get_session_key(user_id : str, session_id : str):
    
    return f'key:{user_id}:{session_id}'

def store_messages(user_id : str, session_id : str, role : str, content : str):
    
    key = get_session_key(user_id, session_id)
    
    now  = datetime.now().isoformat()
    
    message = {
        'role': role,
        'content': content,
        'datestamp': now
    }
    
    redis_client.lpush(key, json.dumps(message))
    
    redis_client.expire(key, EXPIRY_SESSION)
        
def get_user_conversation_history(user_id : str, session_id : str):
    
    user_key_pattern = f'key:{user_id}:*'
    
    keys = redis_client.keys(user_key_pattern)
    
def get_session_history(user_id : str, session_id : str, key : str = None):
    
    if not key:
        key = get_session_key(user_id, session_id)
    
    messages = redis_client.lrange(key, 0, LIMIT - 1)[::-1]
    
    messages = [str(json.loads(message)) for message in messages]
    
    history = ('\n').join(messages)
    
    print(history)
    
    return history