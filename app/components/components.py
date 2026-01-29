import asyncio
from app.services.ai_services.rag_service import CustomRAG
from app.components.generate_response import GetAIRespnse

async def run_chat( query : str, previous_conversations : str = None):
    
    rag = CustomRAG()

    retrieved_context = await asyncio.to_thread(
        rag.retrieve_documents,
        query
    )
    
    result = GetAIRespnse(query, retrieved_context, previous_conversations).response

    return result


