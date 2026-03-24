"""
Log ingestion and search API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from app.core.database import get_db
from app.schemas.log_schema import (
    LogCreate, LogResponse, LogSearchRequest, LogSearchResponse, LogBatchCreate
)
from app.models.service import Service
from app.models.log_metadata import LogMetadata
from app.services.log_service import LogService
from app.utils.helpers import get_iso_timestamp

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=LogResponse)
async def create_log(
    log: LogCreate,
    db: Session = Depends(get_db)
):
    """
    Ingest a single log.
    
    This endpoint:
    1. Saves log metadata to PostgreSQL
    2. Indexes log message in Elasticsearch
    3. Sends log to Kafka for async processing
    """
    log_service = LogService(db)
    
    try:
        result = log_service.create_log(log)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create log: {e}")
        raise HTTPException(status_code=500, detail="Failed to create log")


@router.post("/batch", response_model=dict)
async def create_batch_logs(
    batch: LogBatchCreate,
    db: Session = Depends(get_db)
):
    """
    Ingest multiple logs at once.
    
    Efficient for bulk log ingestion from services.
    """
    log_service = LogService(db)
    
    try:
        results = log_service.create_batch_logs(batch.logs)
        return {
            "total": len(batch.logs),
            "successful": len(results),
            "failed": len(batch.logs) - len(results),
            "log_ids": results
        }
    except Exception as e:
        logger.error(f"Failed to create batch logs: {e}")
        raise HTTPException(status_code=500, detail="Failed to create batch logs")


@router.post("/search", response_model=LogSearchResponse)
async def search_logs(
    search_request: LogSearchRequest,
    db: Session = Depends(get_db)
):
    """
    Search logs with text and optional semantic search.
    
    Features:
    - Full-text search on message and metadata
    - Filter by service, log level, timestamp range
    - Semantic search using embeddings
    """
    log_service = LogService(db)
    
    try:
        logs = log_service.search_logs(search_request)
        return {
            "total": len(logs),
            "logs": logs
        }
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail="Search failed")


@router.get("/", response_model=dict)
async def list_logs(
    service: str = Query(None, description="Filter by service"),
    log_level: str = Query(None, description="Filter by level"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    List logs with pagination and filters.
    """
    query = db.query(LogMetadata)
    
    if service:
        query = query.filter(LogMetadata.service_id == (
            db.query(Service.id).filter(Service.name == service).scalar()
        ))
    
    if log_level:
        query = query.filter(LogMetadata.log_level == log_level)
    
    total = query.count()
    logs = query.order_by(LogMetadata.timestamp.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "logs": [
            {
                "id": log.id,
                "service_id": log.service_id,
                "log_level": log.log_level,
                "timestamp": log.timestamp.isoformat(),
                "latency_ms": log.latency_ms,
                "cluster_id": log.cluster_id,
                "created_at": log.created_at.isoformat(),
            }
            for log in logs
        ]
    }


@router.get("/service/{service_name}/stats")
async def get_service_stats(
    service_name: str,
    db: Session = Depends(get_db)
):
    """
    Get statistics for a specific service's logs.
    """
    log_service = LogService(db)
    
    try:
        stats = log_service.get_service_stats(service_name)
        return stats
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get stats")


@router.get("/{log_id}")
async def get_log(
    log_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific log by ID.
    """
    log = db.query(LogMetadata).filter(LogMetadata.id == log_id).first()
    
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    
    return {
        "id": log.id,
        "service_id": log.service_id,
        "log_level": log.log_level,
        "timestamp": log.timestamp.isoformat(),
        "latency_ms": log.latency_ms,
        "cluster_id": log.cluster_id,
        "created_at": log.created_at.isoformat(),
    }
