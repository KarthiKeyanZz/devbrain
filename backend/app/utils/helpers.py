"""
Helper utility functions.
"""
import hashlib
from datetime import datetime
from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)


def hash_string(text: str) -> str:
    """
    Hash a string using SHA256.
    
    Useful for message deduplication and checksums.
    """
    return hashlib.sha256(text.encode()).hexdigest()


def get_iso_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat() + "Z"


def parse_timestamp(timestamp: str) -> datetime:
    """
    Parse ISO format timestamp.
    
    Args:
        timestamp: ISO format timestamp string
        
    Returns:
        datetime object
    """
    if timestamp.endswith('Z'):
        timestamp = timestamp[:-1]
    return datetime.fromisoformat(timestamp)


def extract_service_from_logs(logs: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Extract service names and their log counts from log list.
    
    Returns:
        Dict mapping service name to log count
    """
    services = {}
    for log in logs:
        service = log.get("service", "unknown")
        services[service] = services.get(service, 0) + 1
    return services


def extract_error_logs(logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter logs for error and critical level messages.
    """
    error_levels = {"ERROR", "CRITICAL", "FATAL"}
    return [log for log in logs if log.get("log_level", "").upper() in error_levels]


def calculate_error_rate(logs: List[Dict[str, Any]]) -> float:
    """
    Calculate error rate from logs.
    
    Returns:
        Error rate as percentage (0-100)
    """
    if not logs:
        return 0.0
    
    error_logs = extract_error_logs(logs)
    return (len(error_logs) / len(logs)) * 100


def calculate_average_latency(logs: List[Dict[str, Any]]) -> float:
    """
    Calculate average latency from logs.
    
    Returns:
        Average latency in milliseconds
    """
    latencies = [
        log.get("latency_ms", 0)
        for log in logs
        if log.get("latency_ms") is not None
    ]
    
    if not latencies:
        return 0.0
    
    return sum(latencies) / len(latencies)


def flatten_dict(d: Dict, parent_key: str = "", sep: str = ".") -> Dict:
    """
    Flatten nested dictionary.
    
    Example:
        {"a": {"b": 1}} -> {"a.b": 1}
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def safe_json_parse(json_str: str, default: Any = None) -> Any:
    """
    Safely parse JSON string.
    
    Returns:
        Parsed object or default value if parsing fails
    """
    import json
    try:
        return json.loads(json_str)
    except Exception as e:
        logger.warning(f"Failed to parse JSON: {e}")
        return default
