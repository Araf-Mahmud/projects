import asyncio

from app.services.ai_services.rag_service import CustomRAG
from app.services.ai_services.llm_service import LLMResponse


async def run_chat( query : str, previous_conversations : str = None, trace):
    
    rag = CustomRAG()
    
    with trace.span(name = "retrieval"):

        retrieved_context = await asyncio.to_thread(
            rag.retrieve_documents,
            query, 
            trace
        )
    
    llm = LLMResponse(query, retrieved_context, previous_conversations, trace)        
   
    result = llm.generate_response()

    return result


