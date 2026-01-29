from app.core.config import Config

config = Config()
class GetAIRespnse():
    
    def __init__(self, query : str, context : str, previous_conversations : str = None):
        
        self.query = query
        self.system_message = self._build_system_prompt()
        self.user_message = self._build_user_prompt(query, context, previous_conversations)
        self.messages = [  
            ("system", self.system_message),  
            ("human", self.user_message),
        ]
        self.response = config.gpt_oss_response(self.messages)

    def _build_system_prompt(self) -> str:
        return f"""You are GenX Assistant, a helpful and friendly assistant for the GenX Application.
                GUIDELINES:
                - Use the provided rag retrieved context to answer questions accurately
                - If the user ask something related to previous conversations, consider previous_conversations information appropriately
                - Present information in a natural, conversational way. 
                - Maintain a warm, professional tone
                - If context is available, base your answer on it while expressing it naturally
                - Address all parts of the user's message
                - Keep responses concise and clear
                - If no relevant context exists, respond helpfully using general reasoning
    """ 

    def _build_user_prompt(self, query: str, context: str, previous_conversations: str = None) -> str:
        if context:
            return f"""
                    User question: {query}

                    Rag Retrieved Context: {context}

                    previous conversations: {previous_conversations}

                    Please provide a helpful response based on the context above."""
        else:
            return f"""User question: {query}

                    No specific context available. Please provide a general helpful response."""
                    
    
    
    
