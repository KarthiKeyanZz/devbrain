"""
Log generator script for testing and simulation.

Generates realistic log data for different services.
"""
import requests
import random
import time
import json
from datetime import datetime, timedelta
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API endpoint
API_URL = "http://localhost:8000/api/logs"

# Simulated services
SERVICES = [
    "payment-service",
    "auth-service",
    "order-service",
    "inventory-service",
    "notification-service",
]

# Log messages templates
LOG_TEMPLATES = {
    "INFO": [
        "Request processed successfully",
        "User login initiated",
        "Payment processed",
        "Order created",
        "Inventory updated",
        "Email notification sent",
        "Cache hit",
    ],
    "WARNING": [
        "Slow database query detected",
        "High memory usage",
        "Connection pool nearly exhausted",
        "Rate limiter activated",
        "Cache miss ratio increasing",
    ],
    "ERROR": [
        "Database connection failed",
        "Timeout while processing request",
        "Authentication failed",
        "Payment gateway error",
        "Invalid request format",
        "Service unavailable",
        "Out of memory error",
    ],
    "CRITICAL": [
        "System crash detected",
        "Data corruption error",
        "Database is unreachable",
        "All retries exhausted",
    ],
}

# Log level distribution (weighted)
LOG_LEVEL_WEIGHTS = {
    "INFO": 70,
    "WARNING": 15,
    "ERROR": 12,
    "CRITICAL": 3,
}


def generate_log():
    """Generate a random log entry."""
    log_level = random.choices(
        list(LOG_LEVEL_WEIGHTS.keys()),
        weights=list(LOG_LEVEL_WEIGHTS.values())
    )[0]
    
    return {
        "service": random.choice(SERVICES),
        "message": random.choice(LOG_TEMPLATES[log_level]),
        "log_level": log_level,
        "timestamp": (datetime.utcnow() - timedelta(seconds=random.randint(0, 3600))).isoformat() + "Z",
        "latency_ms": round(random.uniform(50, 2000), 2),
        "metadata": {
            "user_id": f"user_{random.randint(1000, 9999)}",
            "request_id": f"req_{random.randint(100000, 999999)}",
            "trace_id": f"trace_{random.randint(10000, 99999)}",
        }
    }


def send_log(log):
    """Send a log to the API."""
    try:
        response = requests.post(API_URL, json=log, timeout=5)
        if response.status_code in [200, 201]:
            logger.debug(f"✅ Log sent: {log['service']} - {log['message'][:50]}")
            return True
        else:
            logger.warning(f"❌ Failed to send log: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Error sending log: {e}")
        return False


def send_batch_logs(count: int = 10):
    """Send multiple logs in batch."""
    logs = [generate_log() for _ in range(count)]
    
    try:
        response = requests.post(
            f"{API_URL}/batch",
            json={"logs": logs},
            timeout=10
        )
        if response.status_code in [200, 201]:
            result = response.json()
            logger.info(f"✅ Batch sent: {result['successful']}/{result['total']} logs created")
            return True
        else:
            logger.warning(f"❌ Batch failed: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Error sending batch: {e}")
        return False


def continuous_generation(interval: float = 1.0, batch_size: int = 1):
    """Continuously generate and send logs."""
    logger.info(f"🚀 Starting log generation (interval={interval}s, batch_size={batch_size})")
    
    try:
        while True:
            if batch_size > 1:
                send_batch_logs(batch_size)
            else:
                log = generate_log()
                send_log(log)
            
            time.sleep(interval)
    except KeyboardInterrupt:
        logger.info("⏹️  Log generation stopped")


def main():
    parser = argparse.ArgumentParser(description="DevBrain Log Generator")
    parser.add_argument(
        "--mode",
        choices=["single", "batch", "continuous"],
        default="continuous",
        help="Generation mode"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of logs to generate (for batch mode)"
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Interval between logs (for continuous mode)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1,
        help="Batch size (for continuous mode)"
    )
    
    args = parser.parse_args()
    
    logger.info(f"DevBrain Log Generator")
    logger.info(f"API URL: {API_URL}")
    logger.info(f"Services: {', '.join(SERVICES)}")
    
    if args.mode == "single":
        log = generate_log()
        logger.info(f"Generated: {json.dumps(log, indent=2)}")
        send_log(log)
    
    elif args.mode == "batch":
        logger.info(f"Generating {args.count} logs in batch...")
        send_batch_logs(args.count)
    
    elif args.mode == "continuous":
        continuous_generation(args.interval, args.batch_size)


if __name__ == "__main__":
    main()
