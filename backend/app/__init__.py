"""
FastAPI application factory and initialization.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.database import init_db
from app.core.elasticsearch import init_es_indices
from app.utils.logger import setup_logging
from app.api.health import router as health_router
from app.api.logs import router as logs_router
from app.api.anomalies import router as anomalies_router
from app.api.ai import router as ai_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle application startup and shutdown events.
    """
    # Startup
    logger.info("🚀 Starting DevBrain API...")
    
    try:
        # Setup logging
        setup_logging()
        logger.info("✅ Logging configured")
        
        # Initialize database
        init_db()
        logger.info("✅ Database initialized")
        
        logger.info("✅ All services initialized successfully!")
    except Exception as e:
        logger.error(f"❌ Initialization failed: {e}")
        raise
    
    # Initialize Elasticsearch indices (non-blocking)
    try:
        init_es_indices()
        logger.info("✅ Elasticsearch indices initialized")
    except Exception as e:
        logger.warning(
            f"⚠️  Elasticsearch initialization failed (will retry on first search): {e}. "
            "API will continue to function with basic operations."
        )
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down DevBrain API...")
    # Add cleanup code here if needed


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    """
    app = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        description="AI-powered observability and debugging platform",
        lifespan=lifespan,
    )
    
    # Middleware
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict this
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Trusted hosts
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "*.herokuapp.com", "*.railway.app"],
    )
    
    # API Routes
    app.include_router(health_router, prefix="/api", tags=["health"])
    app.include_router(logs_router, prefix="/api/logs", tags=["logs"])
    app.include_router(anomalies_router, prefix="/api/anomalies", tags=["anomalies"])
    app.include_router(ai_router, prefix="/api/ai", tags=["ai"])
    
    # Root endpoint
    @app.get("/", tags=["root"])
    def root():
        return {
            "name": settings.API_TITLE,
            "version": settings.API_VERSION,
            "status": "running",
            "docs": "/docs",
            "health": "/api/health",
        }
    
    return app


app = create_app()
