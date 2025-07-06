from fastapi import APIRouter
from app.api.endpoints import endpoint

# Create the main API router
api_router = APIRouter()

# Include the MQTT endpoints
api_router.include_router(
    endpoint.router,
    prefix="/mqtt",
    tags=["MQTT Documents"]
)
