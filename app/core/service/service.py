from typing import Optional
from app.core.models.mqtt_document import MqttDocument
from pymongo import DESCENDING
import logging

logger = logging.getLogger(__name__)


class MqttService:
    """
    Service layer for MQTT document operations
    """

    @staticmethod
    async def get_latest_mqtt_document() -> Optional[MqttDocument]:
        """
        Fetch the latest MQTT document based on publish_received_at timestamp

        Returns:
            Optional[MqttDocument]: The latest document or None if no documents found
        """
        try:
            # Query MongoDB to get the document with the most recent publish_received_at
            latest_document = await MqttDocument.find_one(
                sort=[("publish_received_at", DESCENDING)]
            )

            if latest_document:
                logger.info(f"Found latest document with ID: {latest_document.id}")
                return latest_document
            else:
                logger.warning("No MQTT documents found in the collection")
                return None

        except Exception as e:
            logger.error(f"Error fetching latest MQTT document: {str(e)}")
            raise e
