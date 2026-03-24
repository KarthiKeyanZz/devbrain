"""
Kafka integration for log streaming.
"""
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import json
import logging
import time
from typing import Optional, Callable, Any
from app.core.config import settings

logger = logging.getLogger(__name__)


class KafkaClient:
    """Kafka client for producing and consuming messages."""

    _producer: Optional[KafkaProducer] = None
    _consumer: Optional[KafkaConsumer] = None

    @classmethod
    def get_producer(cls, retry_attempts: int = 5, retry_delay: int = 2) -> Optional[KafkaProducer]:
        """Get or create Kafka producer (singleton).
        
        Args:
            retry_attempts: Number of connection retry attempts
            retry_delay: Initial delay in seconds between retries (exponential backoff)
            
        Returns:
            KafkaProducer instance or None if failed after retries
        """
        if cls._producer is None:
            for attempt in range(retry_attempts):
                try:
                    cls._producer = KafkaProducer(
                        bootstrap_servers=settings.kafka_servers,
                        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                        acks='all',
                        retries=3,
                        compression_type='gzip',
                        request_timeout_ms=10000,
                    )
                    logger.info(f"Kafka producer initialized: {settings.KAFKA_BOOTSTRAP_SERVERS}")
                    return cls._producer
                except Exception as e:
                    if attempt < retry_attempts - 1:
                        wait_time = retry_delay * (2 ** attempt)
                        logger.warning(
                            f"Failed to create Kafka producer (attempt {attempt + 1}/{retry_attempts}). "
                            f"Retrying in {wait_time} seconds: {e}"
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Failed to create Kafka producer after {retry_attempts} attempts: {e}")
                        return None
        return cls._producer

    @classmethod
    def send_message(
        cls,
        topic: str,
        message: dict,
        key: Optional[str] = None,
    ) -> bool:
        """
        Send a message to Kafka topic.

        Args:
            topic: Kafka topic name
            message: Message dict (will be JSON encoded)
            key: Optional message key for partitioning

        Returns:
            True if successful, False otherwise
        """
        producer = cls.get_producer()
        if producer is None:
            logger.error("Kafka producer not available")
            return False
            
        try:
            future = producer.send(
                topic,
                value=message,
                key=key.encode('utf-8') if key else None
            )
            # Wait for send to complete
            record_metadata = future.get(timeout=10)
            logger.debug(f"Message sent to {topic}: partition={record_metadata.partition}, offset={record_metadata.offset}")
            return True
        except KafkaError as e:
            logger.error(f"Failed to send message to Kafka: {e}")
            return False

    @classmethod
    def close_producer(cls):
        """Close Kafka producer."""
        if cls._producer:
            cls._producer.flush()
            cls._producer.close()
            cls._producer = None
            logger.info("Kafka producer closed")


def send_log_event(log_data: dict) -> bool:
    """
    Send a log event to Kafka.

    Args:
        log_data: Dictionary with log info (message, service, level, etc.)

    Returns:
        True if successful
    """
    service = log_data.get("service", "unknown")
    return KafkaClient.send_message(
        topic=settings.KAFKA_LOG_TOPIC,
        message=log_data,
        key=service  # Partition by service
    )


def send_anomaly_event(anomaly_data: dict) -> bool:
    """
    Send an anomaly detection event to Kafka.

    Args:
        anomaly_data: Dictionary with anomaly info

    Returns:
        True if successful
    """
    service_id = anomaly_data.get("service_id", "unknown")
    return KafkaClient.send_message(
        topic=settings.KAFKA_ANOMALY_TOPIC,
        message=anomaly_data,
        key=str(service_id)  # Partition by service_id
    )
