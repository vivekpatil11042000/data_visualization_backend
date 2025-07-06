from beanie import Document
from pydantic import Field, field_validator
from typing import Dict, Any, Optional
from bson import ObjectId


class MqttDocument(Document):
    """
    Beanie model for MQTT documents in MongoDB collection
    Only the essential fields are required, others are optional
    """
    # Required fields that we need
    id: str
    payload: str
    publish_received_at: int

    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    # All other fields are optional to avoid validation errors
    flags: Optional[Dict[str, Any]] = Field(default_factory=dict)
    node: Optional[str] = None
    timestamp: Optional[int] = None
    peername: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    event: Optional[str] = None
    username: Optional[str] = None
    peerhost: Optional[str] = None
    client_attrs: Optional[Dict[str, Any]] = Field(default_factory=dict)
    topic: Optional[str] = None
    clientid: Optional[str] = None
    qos: Optional[int] = None
    pub_props: Optional[Dict[str, Any]] = Field(default_factory=dict)

    class Settings:
        name = "mqtt"  # MongoDB collection name
        use_state_management = True
