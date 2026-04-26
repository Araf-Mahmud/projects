from datetime import datetime

from fastapi import APIRouter, BackgroundTasks

from app.schema.chat_schema import ChatRequest, ChatResponse
from app.components.session_manger import SessionManager
from app.services.monitoring_services.langfuse_service import (
    get_langfuse_client,
    get_propagate_attribute
)

from app.components.components import run_chat


router = APIRouter()
session_manager = SessionManager()

def store_message(user_id, session_id, query, response ):

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
    
    langfuse = get_langfuse_client()
    propagate_attributes = get_propagate_attribute() 
    
    if langfuse is None:
        print("Langfuse client not initialized. Proceeding without logging.")

        previous_conversations = session_manager.get_session_history(request.user_id, request.session_id)

        chat_response = await run_chat(request.query, previous_conversations)

        background_tasks.add_task(store_message, request.user_id, request.session_id, request.query, chat_response)

        return ChatResponse(
            user_id = request.user_id,
            session_id = request.session_id,
            query = request.query,
            response = chat_response,
            background_tasks = background_tasks
        )

    else:
        
        trace = f'chatbot-{request.session_id}-{request.user_id}'

        with propagate_attributes(
            trace_name = trace,
            tags=['chatbot', 'rag-based bot'],
            session_id = request.session_id,
            user_id = request.user_id
        ):

            with langfuse.start_as_current_observation(name = trace, 
                input = {
                    'user_id' : request.user_id,
                    'session_id' : request.session_id,
                    'query' : request.query,
                    'query_length' : len(request.query),
                    'query_timestamp' : datetime.now().isoformat()
                },
                metadata = {
                    'trace' : trace,
                    'parameter_count' : len(request.model_dump())
                }
                ) as trace:
                
                previous_conversations = session_manager.get_session_history(request.user_id, request.session_id)

                chat_response = await run_chat(request.query, previous_conversations)
                
                trace.update(
                    output = {
                        'status' : 200,
                        'response_length' : len(chat_response),
                        'response' : chat_response,
                        'response_tokens' : len(chat_response.split())
                        },
                    metadata = {
                        'response_timestamp' : datetime.now().isoformat()
                    }
                )

                background_tasks.add_task(store_message, request.user_id, request.session_id, request.query, chat_response)

                return ChatResponse(
                    user_id = request.user_id,
                    session_id = request.session_id,
                    query = request.query,
                    response = chat_response,
                    background_tasks = background_tasks
                )