from app.schema.chat_schema import ChatRequest, ChatResponse
from app.components.components import run_chat
from app.components.session_manger import SessionManager
from fastapi import APIRouter

router = APIRouter()
session_manager = SessionManager()

@router.post('/chat', response_model = ChatResponse)
async def chat_endpoint( request : ChatRequest):
    
    previous_conversations = session_manager.get_session_history(request.user_id, request.session_id)

    
    chat_response = await run_chat(request.query, previous_conversations)

    session_manager.store_messages(
        user_id = request.user_id,
        session_id = request.session_id,    
        role = 'user',
        content = request.query
    )
    
    session_manager.store_messages(
        user_id = request.user_id,
        session_id = request.session_id,    
        role = 'assistant',         
        content = chat_response
    )
    
    return ChatResponse(
        user_id = request.user_id,
        session_id = request.session_id,
        query = request.query,
        response = chat_response

    )

