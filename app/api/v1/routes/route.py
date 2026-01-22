from fastapi import FastAPI

from app.api.v1.endpoints.docs import router as docs_router
from app.api.v1.endpoints.chat import router as chat_router

def register_routes( app : FastAPI):
    app.include_router(docs_router)
    app.include_router(chat_router, prefix='/api/v1')
