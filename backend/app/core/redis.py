"""
Redis integration for caching.
"""
import redis
import json
import logging
from typing import Optional, Any
from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis client for caching."""
    
    _instance: Optional[redis.Redis] = None
    
    @classmethod
    def get_client(cls) -> redis.Redis:
        """Get or create Redis client (singleton)."""
        if cls._instance is None:
            try:
                cls._instance = redis.from_url(
                    settings.redis_url,
                    decode_responses=True,
                    socket_connect_timeout=5,
                )
                # Test connection
                cls._instance.ping()
                logger.info(f"Connected to Redis at {settings.redis_url}")
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                raise
        return cls._instance
    
    @classmethod
    def close(cls):
        """Close Redis connection."""
        if cls._instance:
            cls._instance.close()
            cls._instance = None


def get_cached(key: str, default: Any = None) -> Any:
    """
    Get a value from Redis cache.
    
    Args:
        key: Cache key
        default: Default value if not found
        
    Returns:
        Cached value or default
    """
    try:
        client = RedisClient.get_client()
        value = client.get(key)
        if value is None:
            return default
        
        # Try to deserialize JSON
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    except Exception as e:
        logger.error(f"Failed to get cache: {e}")
        return default


def set_cached(key: str, value: Any, ttl: Optional[int] = None) -> bool:
    """
    Set a value in Redis cache.
    
    Args:
        key: Cache key
        value: Value to cache (will be JSON encoded if dict/list)
        ttl: Time to live in seconds (default from config)
        
    Returns:
        True if successful
    """
    try:
        client = RedisClient.get_client()
        ttl = ttl or settings.CACHE_TTL
        
        # Serialize value
        if isinstance(value, (dict, list)):
            serialized = json.dumps(value)
        else:
            serialized = str(value)
        
        client.setex(key, ttl, serialized)
        return True
    except Exception as e:
        logger.error(f"Failed to set cache: {e}")
        return False


def delete_cached(key: str) -> bool:
    """
    Delete a value from Redis cache.
    
    Args:
        key: Cache key
        
    Returns:
        True if successful
    """
    try:
        client = RedisClient.get_client()
        client.delete(key)
        return True
    except Exception as e:
        logger.error(f"Failed to delete cache: {e}")
        return False


def clear_cache(pattern: str = "*") -> int:
    """
    Clear cache by pattern.
    
    Args:
        pattern: Key pattern (e.g., "logs:*")
        
    Returns:
        Number of keys deleted
    """
    try:
        client = RedisClient.get_client()
        keys = client.keys(pattern)
        if keys:
            return client.delete(*keys)
        return 0
    except Exception as e:
        logger.error(f"Failed to clear cache: {e}")
        return 0
