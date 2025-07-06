from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class MqttDocumentResponse(BaseModel):
    """
    Simplified response schema for MQTT document with only essential fields
    """
    id: str = Field(..., description="Document ID")
    payload: Dict[str, Any] = Field(..., description="Message payload as JSON object")
    publish_received_at: int = Field(..., description="Timestamp when message was received")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "0006394492CE2D11F4450000265C0000",
                "payload": {
                    "heartBeatRate": 72,
                    "timestamp": 1751816536
                },
                "publish_received_at": 1751816543808
            }
        }


class ErrorResponse(BaseModel):
    """
    Error response schema
    """
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "No documents found",
                "error_code": "NOT_FOUND"
            }
        }
