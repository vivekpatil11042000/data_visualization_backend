from fastapi import APIRouter, HTTPException, status
from app.core.service.service import MqttService
from app.core.schema.inputoutput import MqttDocumentResponse, ErrorResponse
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/latest-mqtt-document",
    response_model=MqttDocumentResponse,
    responses={
        404: {"model": ErrorResponse, "description": "No documents found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get Latest MQTT Document",
    description="Retrieve the latest MQTT document based on publish_received_at timestamp"
)
async def get_latest_mqtt_document():
    """
    Get the latest MQTT document from the MongoDB collection.

    Returns the document with the most recent publish_received_at timestamp.

    Returns:
        MqttDocumentResponse: The latest MQTT document with only id, payload, and publish_received_at

    Raises:
        HTTPException: 404 if no documents found, 500 for server errors
    """
    try:
        # Call the service to fetch the latest document
        latest_document = await MqttService.get_latest_mqtt_document()

        if not latest_document:
            logger.warning("No MQTT documents found in the collection")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No MQTT documents found in the collection"
            )

        # Parse payload as JSON
        try:
            payload_json = json.loads(latest_document.payload)
        except (json.JSONDecodeError, TypeError):
            # If payload is not valid JSON, return it as a string in a dict
            payload_json = {"raw_payload": latest_document.payload}

        # Convert the Beanie document to response schema with only required fields
        response_data = MqttDocumentResponse(
            id=latest_document.id,
            payload=payload_json,
            publish_received_at=latest_document.publish_received_at
        )

        logger.info(f"Successfully retrieved latest document with ID: {latest_document.id}")
        return response_data

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving latest MQTT document: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while fetching the latest document"
        )
