from fastapi import FastAPI
from pydantic_settings import BaseSettings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.models.mqtt_document import MqttDocument
from app.api.api import api_router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """
    Application settings using Pydantic BaseSettings
    """
    mongodb_url: str = "mongodb://localhost:27017/testing"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Initialize settings
settings = Settings()

# Create FastAPI application
app = FastAPI(
    title="MQTT Data Visualization API",
    description="FastAPI application for retrieving MQTT documents from MongoDB",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.on_event("startup")
async def startup_event():
    """
    Initialize MongoDB connection and Beanie ODM on application startup
    """
    try:
        # Create MongoDB client
        client = AsyncIOMotorClient(settings.mongodb_url)
        
        database = client["testing"]
        
        # Initialize Beanie with the database and document models
        await init_beanie(
            database=database,
            document_models=[MqttDocument]
        )
        
        logger.info(f"Successfully connected to MongoDB: {settings.mongodb_url}")
        logger.info(f"Database: {database}")
        logger.info("Beanie ODM initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise e


@app.on_event("shutdown")
async def shutdown_event():
    """
    Clean up resources on application shutdown
    """
    logger.info("Application shutting down...")


# Include API routes
app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
