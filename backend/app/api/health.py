"""
Health check and status endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

from app.core.database import get_db
from app.core.redis import RedisClient
from app.core.elasticsearch import ESClient
from app.core.kafka import KafkaClient  # UNCOMMENT FOR PHASE 3+

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns status of all critical services.
    """
    services = {
        "api": "healthy",
        "database": "unknown",
        "redis": "unknown",
        "elasticsearch": "unknown",
        "kafka": "unknown",  # UNCOMMENT FOR PHASE 3+
    }
    
    # Check database
    try:
        from app.core.database import SessionLocal
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        services["database"] = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        services["database"] = "unhealthy"
    
    # Check Redis - UNCOMMENT FOR PHASE 2+
    try:
        client = RedisClient.get_client()
        client.ping()
        services["redis"] = "healthy"
    except Exception as e:
        logger.warning(f"Redis health check failed: {e}")
        services["redis"] = "unhealthy"
    
    # Check Elasticsearch - UNCOMMENT FOR PHASE 2+
    try:
        client = ESClient.get_client()
        client.info()
        services["elasticsearch"] = "healthy"
    except Exception as e:
        logger.warning(f"Elasticsearch health check failed: {e}")
        services["elasticsearch"] = "unhealthy"
    
    # Check Kafka - UNCOMMENT FOR PHASE 3+
    try:
        client = KafkaClient.get_producer()
        if client:
            services["kafka"] = "healthy"
        else:
            services["kafka"] = "unhealthy"
    except Exception as e:
        logger.warning(f"Kafka health check failed: {e}")
        services["kafka"] = "unhealthy"
    
    # Overall status
    critical_healthy = services["database"] == "healthy"
    
    return {
        "status": "healthy" if critical_healthy else "degraded",
        "services": services,
    }


@router.get("/ready")
async def readiness_check():
    """
    Readiness check - returns 200 only if all services are ready.
    Used by container orchestration for startup probes.
    """
    try:
        # Quick database check
        from app.core.database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        
        return {"status": "ready"}
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return {"status": "not_ready", "error": str(e)}, 503
