"""
Business logic for log operations.
"""
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
import logging

from app.models.service import Service
from app.models.log_metadata import LogMetadata
from app.schemas.log_schema import LogCreate, LogSearchRequest
from app.core.elasticsearch import index_log, search_logs as es_search_logs
from app.core.kafka import send_log_event  # UNCOMMENT FOR PHASE 3+
from app.utils.helpers import hash_string, get_iso_timestamp
from app.core.config import settings

logger = logging.getLogger(__name__)


class LogService:
    """Service for handling log operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _ensure_service(self, service_name: str) -> Service:
        """Ensure service exists, create if not."""
        service = self.db.query(Service).filter(
            Service.name == service_name
        ).first()
        
        if not service:
            service = Service(name=service_name)
            self.db.add(service)
            self.db.commit()
            logger.info(f"Created new service: {service_name}")
        
        return service
    
    def create_log(self, log: LogCreate) -> dict:
        """
        Create a single log entry.
        
        Process:
        1. Ensure service exists
        2. Save metadata to PostgreSQL
        # 3. Index message in Elasticsearch - UNCOMMENT FOR PHASE 2+
        # 4. Send to Kafka for async processing - UNCOMMENT FOR PHASE 3+
        """
        # Ensure service exists
        service = self._ensure_service(log.service)
        
        # Parse timestamp
        if log.timestamp:
            timestamp = datetime.fromisoformat(log.timestamp.replace('Z', '+00:00'))
        else:
            timestamp = datetime.utcnow()
        
        # Create log metadata record
        log_metadata = LogMetadata(
            service_id=service.id,
            log_level=log.log_level.upper(),
            timestamp=timestamp,
            latency_ms=log.latency_ms,
            message_hash=hash_string(log.message),
            extra_metadata=log.metadata or {},
        )
        
        self.db.add(log_metadata)
        self.db.flush()  # Get the ID
        
        # Index in Elasticsearch - UNCOMMENT FOR PHASE 2+
        es_doc_id = None
        try:
            es_doc_id = index_log(
                message=log.message,
                service=log.service,
                log_level=log.log_level.upper(),
                timestamp=timestamp.isoformat(),
                latency_ms=log.latency_ms,
                extra_metadata=log.metadata,
            )
            log_metadata.es_doc_id = es_doc_id
        except Exception as e:
            logger.error(f"Failed to index log in Elasticsearch: {e}")
            # Don't fail the request, just log the error
        
        self.db.commit()
        
        # Send to Kafka for async processing - UNCOMMENT FOR PHASE 3+
        log_event = {
            "id": log_metadata.id,
            "service_id": service.id,
            "service": log.service,
            "message": log.message,
            "log_level": log.log_level.upper(),
            "timestamp": timestamp.isoformat(),
            "latency_ms": log.latency_ms,
        }
        
        try:
            send_log_event(log_event)
        except Exception as e:
            logger.warning(f"Failed to send log to Kafka: {e}")
            # Don't fail the request if Kafka is unavailable
        
        return {
            "id": log_metadata.id,
            "service": log.service,
            "message": log.message,
            "log_level": log.log_level.upper(),
            "timestamp": timestamp,
            "latency_ms": log.latency_ms,
            "es_doc_id": es_doc_id,
            "cluster_id": None,
            "created_at": datetime.utcnow(),
        }
    
    def create_batch_logs(self, logs: List[LogCreate]) -> List[int]:
        """
        Create multiple logs efficiently.
        """
        created_ids = []
        
        for log in logs:
            try:
                result = self.create_log(log)
                created_ids.append(result["id"])
            except Exception as e:
                logger.error(f"Failed to create log: {e}")
        
        return created_ids
    
    def search_logs(self, search_request: LogSearchRequest) -> List[dict]:
        """
        Search logs with filters.
        """
        results = es_search_logs(
            query=search_request.query,
            service=search_request.service,
            log_level=search_request.log_level,
            from_timestamp=search_request.from_timestamp,
            to_timestamp=search_request.to_timestamp,
            size=search_request.size,
        )
        
        return results
    
    def get_service_stats(self, service_name: str) -> dict:
        """
        Get statistics for a service's logs.
        """
        service = self.db.query(Service).filter(
            Service.name == service_name
        ).first()
        
        if not service:
            raise ValueError(f"Service not found: {service_name}")
        
        # Query log metadata
        logs = self.db.query(LogMetadata).filter(
            LogMetadata.service_id == service.id
        ).all()
        
        if not logs:
            return {
                "service": service_name,
                "total_logs": 0,
                "error_rate": 0.0,
                "average_latency": 0.0,
                "log_levels": {},
            }
        
        # Calculate statistics
        error_logs = [l for l in logs if l.log_level in ["ERROR", "CRITICAL"]]
        error_rate = (len(error_logs) / len(logs)) * 100
        
        latencies = [l.latency_ms for l in logs if l.latency_ms is not None]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        
        # Log level distribution
        level_counts = {}
        for log in logs:
            level = log.log_level
            level_counts[level] = level_counts.get(level, 0) + 1
        
        return {
            "service": service_name,
            "total_logs": len(logs),
            "error_rate": round(error_rate, 2),
            "average_latency_ms": round(avg_latency, 2),
            "log_levels": level_counts,
        }
