"""
Elasticsearch integration for log storage and search.
"""
from elasticsearch import Elasticsearch
from typing import Dict, List, Any, Optional
import logging
import time
from app.core.config import settings

logger = logging.getLogger(__name__)


class ESClient:
    """Elasticsearch client wrapper."""
    
    _instance: Optional[Elasticsearch] = None
    
    @classmethod
    def get_client(cls, retry_attempts: int = 5, retry_delay: int = 2) -> Elasticsearch:
        """Get or create Elasticsearch client (singleton).
        
        Args:
            retry_attempts: Number of connection retry attempts
            retry_delay: Initial delay in seconds between retries (exponential backoff)
        """
        if cls._instance is None:
            last_error = None
            for attempt in range(retry_attempts):
                try:
                    cls._instance = Elasticsearch([settings.elasticsearch_url])
                    # Test connection
                    cls._instance.info()
                    logger.info(f"Connected to Elasticsearch at {settings.elasticsearch_url}")
                    return cls._instance
                except Exception as e:
                    last_error = e
                    if attempt < retry_attempts - 1:
                        wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                        logger.warning(
                            f"Failed to connect to Elasticsearch (attempt {attempt + 1}/{retry_attempts}). "
                            f"Retrying in {wait_time} seconds: {e}"
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Failed to connect to Elasticsearch after {retry_attempts} attempts: {e}")
                        cls._instance = None
                        raise
        return cls._instance
    
    @classmethod
    def close(cls):
        """Close Elasticsearch connection."""
        if cls._instance:
            cls._instance.close()
            cls._instance = None


def init_es_indices():
    """Initialize Elasticsearch indices."""
    client = ESClient.get_client()
    
    # Create logs index with mapping
    logs_mapping = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        },
        "mappings": {
            "properties": {
                "message": {"type": "text"},
                "service": {"type": "keyword"},
                "log_level": {"type": "keyword"},
                "timestamp": {"type": "date"},
                "latency_ms": {"type": "float"},
                "embedding": {
                    "type": "dense_vector",
                    "dims": settings.EMBEDDING_DIM,
                    "index": True,
                    "similarity": "cosine"
                },
                "cluster_id": {"type": "integer"},
                "extra_metadata": {"type": "object", "enabled": True},
                "created_at": {"type": "date"},
            }
        }
    }
    
    index_name = "logs_index"
    try:
        if not client.indices.exists(index=index_name):
            client.indices.create(index=index_name, body=logs_mapping)
            logger.info(f"Created Elasticsearch index: {index_name}")
        else:
            logger.info(f"Elasticsearch index already exists: {index_name}")
    except Exception as e:
        logger.error(f"Failed to create index: {e}")
        raise


def index_log(
    message: str,
    service: str,
    log_level: str,
    timestamp: str,
    embedding: Optional[List[float]] = None,
    latency_ms: Optional[float] = None,
    cluster_id: Optional[int] = None,
    extra_metadata: Optional[Dict] = None,
) -> str:
    """
    Index a log document in Elasticsearch.
    
    Returns the document ID.
    """
    client = ESClient.get_client()
    
    doc = {
        "message": message,
        "service": service,
        "log_level": log_level,
        "timestamp": timestamp,
        "latency_ms": latency_ms,
        "embedding": embedding,
        "cluster_id": cluster_id,
        "extra_metadata": extra_metadata or {},
        "created_at": timestamp,
    }
    
    response = client.index(index="logs_index", document=doc)
    return response["_id"]


def search_logs(
    query: str,
    embedding: Optional[List[float]] = None,
    service: Optional[str] = None,
    log_level: Optional[str] = None,
    from_timestamp: Optional[str] = None,
    to_timestamp: Optional[str] = None,
    size: int = 10,
) -> List[Dict[str, Any]]:
    """
    Search logs with optional filters and semantic search.
    """
    client = ESClient.get_client()
    
    must_clauses = []
    
    # Text search
    if query:
        must_clauses.append({
            "multi_match": {
                "query": query,
                "fields": ["message", "extra_metadata"]
            }
        })
    
    # Service filter
    if service:
        must_clauses.append({"term": {"service.keyword": service}})
    
    # Log level filter
    if log_level:
        must_clauses.append({"term": {"log_level.keyword": log_level}})
    
    # Timestamp range
    if from_timestamp or to_timestamp:
        range_clause = {}
        if from_timestamp:
            range_clause["gte"] = from_timestamp
        if to_timestamp:
            range_clause["lte"] = to_timestamp
        must_clauses.append({"range": {"timestamp": range_clause}})
    
    # Semantic search with embedding
    query_body = {
        "size": size,
        "query": {
            "bool": {
                "must": must_clauses if must_clauses else [{"match_all": {}}]
            }
        }
    }
    
    # Add knn query if embedding provided
    if embedding:
        query_body["knn"] = {
            "field": "embedding",
            "query_vector": embedding,
            "k": size,
            "num_candidates": size * 10,
        }
    
    try:
        response = client.search(index="logs_index", body=query_body)
        results = []
        for hit in response["hits"]["hits"]:
            hit["_source"]["_id"] = hit["_id"]
            hit["_source"]["_score"] = hit.get("_score", 0.0)
            results.append(hit["_source"])
        return results
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return []


def get_log_by_id(doc_id: str) -> Optional[Dict[str, Any]]:
    """Get a log document by ID."""
    client = ESClient.get_client()
    try:
        response = client.get(index="logs_index", id=doc_id)
        return response["_source"]
    except Exception as e:
        logger.error(f"Failed to get log: {e}")
        return None


def delete_log(doc_id: str) -> bool:
    """Delete a log document."""
    client = ESClient.get_client()
    try:
        client.delete(index="logs_index", id=doc_id)
        return True
    except Exception as e:
        logger.error(f"Failed to delete log: {e}")
        return False


def count_logs(
    service: Optional[str] = None,
    log_level: Optional[str] = None,
    from_timestamp: Optional[str] = None,
    to_timestamp: Optional[str] = None,
) -> int:
    """Count logs matching filters."""
    client = ESClient.get_client()
    
    must_clauses = []
    if service:
        must_clauses.append({"term": {"service.keyword": service}})
    if log_level:
        must_clauses.append({"term": {"log_level.keyword": log_level}})
    
    if from_timestamp or to_timestamp:
        range_clause = {}
        if from_timestamp:
            range_clause["gte"] = from_timestamp
        if to_timestamp:
            range_clause["lte"] = to_timestamp
        must_clauses.append({"range": {"timestamp": range_clause}})
    
    query_body = {
        "query": {
            "bool": {
                "must": must_clauses if must_clauses else [{"match_all": {}}]
            }
        }
    }
    
    try:
        response = client.count(index="logs_index", body=query_body)
        return response["count"]
    except Exception as e:
        logger.error(f"Count failed: {e}")
        return 0
