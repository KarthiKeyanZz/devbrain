"""
Pydantic schemas for AI/Chat-related API requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class ChatMessage(BaseModel):
    """Single chat message."""
    role: str = Field(..., description="Role: user, assistant, system")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Schema for chat request."""
    message: str = Field(..., description="User message")
    service_id: Optional[int] = Field(
        default=None,
        description="Optional service context"
    )
    conversation_history: Optional[List[ChatMessage]] = Field(
        default=None,
        description="Previous messages for context"
    )


class ChatResponse(BaseModel):
    """Schema for chat response."""
    message: str = Field(..., description="Assistant response")
    explanation: Optional[str] = Field(
        default=None,
        description="Detailed explanation"
    )
    related_logs: Optional[List[dict]] = Field(
        default=None,
        description="Related logs from search"
    )
    related_anomalies: Optional[List[dict]] = Field(
        default=None,
        description="Related detected anomalies"
    )
    confidence_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Confidence score"
    )


class ExplainRequest(BaseModel):
    """Schema for explain request (deprecated, use chat)."""
    service_id: int = Field(..., description="Service ID to explain")
    from_timestamp: Optional[str] = Field(
        default=None,
        description="From timestamp (ISO)"
    )
    to_timestamp: Optional[str] = Field(
        default=None,
        description="To timestamp (ISO)"
    )
    focus: Optional[str] = Field(
        default=None,
        description="Focus area: errors, latency, anomalies"
    )


class ExplainResponse(BaseModel):
    """Schema for explain response."""
    service_id: int
    summary: str = Field(..., description="Summary of system state")
    anomalies: List[dict] = Field(..., description="Detected anomalies")
    root_causes: List[str] = Field(..., description="Root cause analysis")
    recommendations: List[str] = Field(..., description="Recommended actions")
