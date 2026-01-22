from fastapi import FastAPI
from app.api.v1.endpoints.docs import router as docs_router

def register_routes( app : FastAPI):
    app.include_router(docs_router)
