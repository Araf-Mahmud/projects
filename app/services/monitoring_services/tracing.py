from langfuse import Langfuse

langfuse = Langfuse()

def start_trace(name : str, user_id : str, session_id : str ):
    return langfuse.trace(
        name = name,
        user_id = user_id,
        session_id = session_id
    )