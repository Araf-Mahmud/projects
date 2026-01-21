import asyncio
from app.services.ai_services.rag_service import CustomRAG
from app.components.generate_response import GetAIRespnse

async def run_chat(user_id : str, session_id : str, query : str):
    
    rag = CustomRAG()
    
    result = asyncio.to_thread(
        rag.retrieve_documents,
        query
    )
    
    

