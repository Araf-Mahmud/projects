from app.schema.chat_schema import ChatRequest, ChatResponse
from app.components.components import run_chat
from fastapi import APIRouter

router = APIRouter()

@router.post('/chat', response_model = ChatResponse)
async def chat_endpoint( request : ChatRequest):
    
    chat_response = await run_chat(request.query)
    
    return ChatResponse(
        user_id = request.user_id,
        session_id = request.session_id,
        query = request.query,
        response = chat_response

    )

