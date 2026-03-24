"""
Application entry point.
"""
import uvicorn
import logging
from app import create_app
from app.utils.logger import setup_logging

# Setup logging before anything else
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app
app = create_app()


if __name__ == "__main__":
    logger.info("🚀 Starting DevBrain API Server")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
