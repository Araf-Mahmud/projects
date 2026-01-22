from fastapi import APIRouter
from scalar_fastapi import get_scalar_api_reference
from scalar_fastapi.scalar_fastapi import Layout, SearchHotKey
from dotenv import load_dotenv
import os
load_dotenv()

router = APIRouter()

@router.get("/api/docs", include_in_schema=False)
async def get_scalar_docs():
    """
    Serve Scalar API documentation
    """
    return get_scalar_api_reference(
        openapi_url="/openapi.json",
        title="AI Service API Documentation",
        layout=Layout.MODERN,
        dark_mode=True,
        search_hot_key=SearchHotKey.K,
        servers=[
            {
                "url": os.getenv("API_URL_LOCAL"),
                "description": "Local Server"
            },
            {
                "url": os.getenv("API_URL_DEV"),
                "description": "Development Server"
            }
        ]
    )