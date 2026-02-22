from fastapi import APIRouter, BackgroundTasks

from app.schema.chat_schema import ChatRequest, ChatResponse
from app.components.session_manger import SessionManager

from app.services.monitoring_services.tracing import start_trace
from app.components.components import run_chat


router = APIRouter()
session_manager = SessionManager()

def store_message(user_id, session_id, query, response, trace ):
    
    session_manager.store_messages(
        user_id = user_id,
        session_id = session_id,    
        role = 'user',
        content = query
    )


    session_manager.store_messages(
        user_id = user_id,
        session_id = session_id,    
        role = 'assistant',         
        content = response
    )
    
@router.post('/chat', response_model = ChatResponse)
async def chat_endpoint( request : ChatRequest, background_tasks: BackgroundTasks):
    
    with start_trace(
        name = "Chatbot",
        user_id = request.user_id,
        session_id = request.session_id
        ) as trace:
        
        previous_conversations = session_manager.get_session_history(request.user_id, request.session_id)
    
        chat_response = await run_chat(request.query, previous_conversations, trace)
        
        background_tasks.add_task(store_message, request.user_id, request.session_id, request.query, chat_response)
        
        return ChatResponse(
            user_id = request.user_id,
            session_id = request.session_id,
            query = request.query,
            response = chat_response,
            background_tasks = background_tasks
        )

