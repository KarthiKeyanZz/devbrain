"""
Pydantic schemas for anomaly-related API requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AnomalyCreate(BaseModel):
    """Schema for creating a new anomaly."""
    service_id: int = Field(..., description="Service ID")
    detection_method: str = Field(..., description="Detection method used")
    anomaly_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Anomaly score [0, 1]"
    )
    feature_type: str = Field(
        ...,
        description="Type of feature: error_rate, latency, pattern"
    )
    description: Optional[str] = Field(
        default=None,
        description="Human-readable description"
    )
    related_logs: Optional[str] = Field(
        default=None,
        description="Related log IDs"
    )


class AnomalyResponse(BaseModel):
    """Schema for anomaly response."""
    id: int
    service_id: int
    detection_method: str
    anomaly_score: float
    feature_type: str
    detected_at: datetime
    description: Optional[str]
    root_cause: Optional[str]
    suggested_action: Optional[str]
    status: str
    created_at: datetime
    acknowledged_at: Optional[datetime]
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True


class AnomalyAnalyzeRequest(BaseModel):
    """Schema for analyzing anomalies with AI."""
    anomaly_id: int = Field(..., description="Anomaly ID to analyze")
    lookback_minutes: int = Field(
        default=60,
        ge=5,
        le=1440,
        description="Minutes of historical data to analyze"
    )


class AnomalyAnalyzeResponse(BaseModel):
    """Schema for anomaly analysis response."""
    anomaly_id: int
    root_cause: str = Field(..., description="Identified root cause")
    suggested_action: str = Field(..., description="Suggested remediation")
    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in the analysis"
    )
    related_events: list[dict] = Field(..., description="Related system events")


class AnomalyListResponse(BaseModel):
    """Schema for listing anomalies."""
    total: int = Field(..., description="Total anomalies")
    anomalies: list[AnomalyResponse] = Field(..., description="Anomaly list")
    unread_count: int = Field(..., description="Unacknowledged anomalies")


class AnomalyAcknowledgeRequest(BaseModel):
    """Schema for acknowledging an anomaly."""
    anomaly_id: int = Field(..., description="Anomaly ID")
    notes: Optional[str] = Field(
        default=None,
        description="Acknowledgement notes"
    )
