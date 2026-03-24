"""
Pydantic schemas for log-related API requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class LogCreate(BaseModel):
    """Schema for creating a new log."""
    service: str = Field(..., description="Service name that generated the log")
    message: str = Field(..., description="Log message content")
    log_level: str = Field(
        default="INFO",
        description="Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL"
    )
    timestamp: Optional[str] = Field(
        default=None,
        description="ISO format timestamp (defaults to current time)"
    )
    latency_ms: Optional[float] = Field(
        default=None,
        description="Request latency in milliseconds"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata"
    )

    class Config:
        schema_extra = {
            "example": {
                "service": "payment-service",
                "message": "Payment processed successfully",
                "log_level": "INFO",
                "timestamp": "2024-03-23T10:30:00Z",
                "latency_ms": 150.5,
                "metadata": {"user_id": "user123", "amount": 99.99}
            }
        }


class LogResponse(BaseModel):
    """Schema for log response."""
    id: int
    service: str
    message: str
    log_level: str
    timestamp: datetime
    latency_ms: Optional[float]
    es_doc_id: Optional[str]
    cluster_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class LogSearchRequest(BaseModel):
    """Schema for log search requests."""
    query: str = Field(
        ...,
        description="Search query (text or semantic)"
    )
    service: Optional[str] = Field(
        default=None,
        description="Filter by service"
    )
    log_level: Optional[str] = Field(
        default=None,
        description="Filter by log level"
    )
    from_timestamp: Optional[str] = Field(
        default=None,
        description="From timestamp (ISO format)"
    )
    to_timestamp: Optional[str] = Field(
        default=None,
        description="To timestamp (ISO format)"
    )
    size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of results"
    )


class LogSearchResponse(BaseModel):
    """Schema for log search response."""
    total: int = Field(..., description="Total logs matching query")
    logs: list = Field(..., description="Log results")


class LogBatchCreate(BaseModel):
    """Schema for batch log creation."""
    logs: list[LogCreate] = Field(
        ...,
        min_items=1,
        max_items=1000,
        description="List of logs to create"
    )
