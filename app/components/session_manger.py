import json
from datetime import datetime
from app.core.config import Config

class SessionManager:
    def __init__(self, EXPIRY_SESSION : int = 90, LIMIT : int = 6):
        self.EXPIRY_SESSION = EXPIRY_SESSION
        self.LIMIT = LIMIT
        self.redis_client = Config().get_redis_client()

    def get_session_key(self, user_id : str, session_id : str):
        return f'key:{user_id}:{session_id}'

    def store_messages(self, user_id : str, session_id : str, role : str, content : str):

        key = self.get_session_key(user_id, session_id)

        now  = datetime.now().isoformat()
        
        message = {
            'role': role,
            'content': content,
            'datestamp': now
        }

        self.redis_client.lpush(key, json.dumps(message))

        self.redis_client.expire(key, self.EXPIRY_SESSION)

    def get_user_conversation_history(self, user_id : str, session_id : str):

        user_key_pattern = f'key:{user_id}:*'

        keys = self.redis_client.keys(user_key_pattern)
        
        last_conversations_of_sessions = [
            self.redis_client.lrange(key, 0, self.LIMIT - 1)[-2]['content'] for key in keys
        ]

        return last_conversations_of_sessions

    def get_session_history(self, user_id : str, session_id : str, key : str = None):

        if not key:
            key = self.get_session_key(user_id, session_id)

        messages = self.redis_client.lrange(key, 0, self.LIMIT - 1)[::-1]

        messages = [json.loads(message) for message in messages]
        
        history  = ('\n').join(['[{datestamp}] {role} : {content}'.format(**msg) for msg in messages])
        
        print(history)
        
        return history