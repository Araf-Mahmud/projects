from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    user_id: str = Field(..., description="The ID of the user")
    session_id: str = Field(..., description="The ID of the session")
    query: str = Field(..., description="The user query")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user-01",
                "session_id": "session-01",
                "query": "Is there a mentorship program?"
            }
        }

class ChatResponse(BaseModel):
    user_id: str = Field(..., description="The ID of the user")
    session_id: str = Field(..., description="The ID of the session")
    response: str = Field(..., description="The AI-generated response")    
    query: str = Field(..., description="The user query")

    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user-01",
                "session_id": "session-01",
                "query": "Is there a mentorship program?",
                "response": "The user response here."
            }
        }