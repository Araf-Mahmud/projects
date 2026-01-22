import asyncio
from app.services.ai_services.rag_service import CustomRAG
from app.components.generate_response import GetAIRespnse

async def run_chat( query : str):
    
    rag = CustomRAG()

    retrieved_context = await asyncio.to_thread(
        rag.retrieve_documents,
        query
    )
    
    result = GetAIRespnse(query, retrieved_context).response

    return result


