import sys
import os
from dotenv import load_dotenv
from pathlib import Path
from fastapi import FastAPI
from app.api.v1.routes.route import register_routes 

load_dotenv()

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def create_app() -> FastAPI:
    app = FastAPI(title="Chatbot API", version="1.0.0")
    register_routes(app)
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
