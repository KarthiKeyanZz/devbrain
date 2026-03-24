"""
Application configuration and settings.
"""
import os
from typing import Optional
from functools import lru_cache


class Settings:
    """Application settings with environment variable support."""

    # API Config
    API_TITLE: str = "DevBrain API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # Database Config
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://devbrain:devbrain@localhost:5432/devbrain"
    )
    
    # Elasticsearch Config - UNCOMMENT FOR PHASE 2+
    ELASTICSEARCH_HOST: str = os.getenv("ELASTICSEARCH_HOST", "localhost")
    ELASTICSEARCH_PORT: int = int(os.getenv("ELASTICSEARCH_PORT", "9200"))
    ELASTICSEARCH_PROTOCOL: str = os.getenv("ELASTICSEARCH_PROTOCOL", "http")
    
    @property
    def elasticsearch_url(self) -> str:
        return f"{self.ELASTICSEARCH_PROTOCOL}://{self.ELASTICSEARCH_HOST}:{self.ELASTICSEARCH_PORT}"

    # Redis Config - UNCOMMENT FOR PHASE 2+
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    
    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # Kafka Config - UNCOMMENT FOR PHASE 3+
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS",
        "localhost:9092"
    )
    KAFKA_LOG_TOPIC: str = os.getenv("KAFKA_LOG_TOPIC", "logs")
    KAFKA_ANOMALY_TOPIC: str = os.getenv("KAFKA_ANOMALY_TOPIC", "anomalies")
    
    @property
    def kafka_servers(self) -> list:
        return self.KAFKA_BOOTSTRAP_SERVERS.split(",")

    # ML Config - UNCOMMENT FOR PHASE 2+
    EMBEDDINGS_MODEL: str = os.getenv(
        "EMBEDDINGS_MODEL",
        "all-MiniLM-L6-v2"
    )
    EMBEDDING_DIM: int = int(os.getenv("EMBEDDING_DIM", "384"))
    # ANOMALY_THRESHOLD: float = float(os.getenv("ANOMALY_THRESHOLD", "0.7"))
    
    # Clustering Config - UNCOMMENT FOR PHASE 2+
    # DBSCAN_EPS: float = float(os.getenv("DBSCAN_EPS", "0.5"))
    # DBSCAN_MIN_SAMPLES: int = int(os.getenv("DBSCAN_MIN_SAMPLES", "5"))
    
    # Isolation Forest Config - UNCOMMENT FOR PHASE 2+
    # ISOLATION_FOREST_CONTAMINATION: float = float(
    #     os.getenv("ISOLATION_FOREST_CONTAMINATION", "0.1")
    # )
    

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Cache TTL (seconds)
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Export singleton
settings = get_settings()
