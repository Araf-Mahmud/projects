import asyncio
from datetime import datetime

from app.services.ai_services.rag_service import CustomRAG
from app.services.ai_services.llm_service import LLMResponse

from app.services.monitoring_services.langfuse_service import (
    get_langfuse_client,
    get_propagate_attribute
)

async def run_chat(query: str, previous_conversations: str = None):

    propagate_attributes = get_propagate_attribute()

    langfuse = get_langfuse_client()

    if langfuse is None:
        print("Langfuse client not initialized. Proceeding without logging.")

        rag = CustomRAG()

        retrieved_context = await asyncio.to_thread(
            rag.retrieve_documents,
            query
        )

        llm = LLMResponse(query, retrieved_context, previous_conversations)

        return llm.generate_response()

    with propagate_attributes(tags=['chatbot-crew']):
        with langfuse.start_as_current_observation(name = 'chat_interaction',
                input = {
                    'query' : query,
                    'previous_conversations' : previous_conversations
                    },
                    metadata = {
                        'type': 'chat_interaction'
                    }
                ) as crew_span:


                rag = CustomRAG()

                retrieved_context = await asyncio.to_thread(
                    rag.retrieve_documents,
                    query
                )

                llm = LLMResponse(query, retrieved_context, previous_conversations)

                result = llm.generate_response()

                crew_span.update(
                    output = {
                        'retrieved_context' : retrieved_context,
                        'llm_response' : result,
                        'response_length' : len(result),
                        'response_tokens' : len(result.split())
                    },
                    metadata = {
                        'response_timestamp' : datetime.now().isoformat()
                    }
                )

    return result