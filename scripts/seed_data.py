"""
Seed database with initial data.

Sets up services, sample logs, and events for testing.
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.core.database import SessionLocal, init_db
from app.models.service import Service
from app.models.log_metadata import LogMetadata
from app.models.event import Event
from app.utils.helpers import hash_string

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_services(db):
    """Create sample services."""
    services_data = [
        {"name": "payment-service", "description": "Handles payment processing"},
        {"name": "auth-service", "description": "Authentication and authorization"},
        {"name": "order-service", "description": "Order management"},
        {"name": "inventory-service", "description": "Inventory management"},
        {"name": "notification-service", "description": "Email and SMS notifications"},
    ]
    
    for service_data in services_data:
        existing = db.query(Service).filter(Service.name == service_data["name"]).first()
        if not existing:
            service = Service(**service_data)
            db.add(service)
            logger.info(f"✅ Created service: {service_data['name']}")
        else:
            logger.info(f"⏭️  Service already exists: {service_data['name']}")
    
    db.commit()


def seed_logs(db):
    """Create sample logs."""
    services = db.query(Service).all()
    
    if not services:
        logger.warning("No services found. Run seed_services first.")
        return
    
    # Create logs for the last 24 hours
    now = datetime.utcnow()
    
    log_messages = [
        "Request processed successfully",
        "Database query took 150ms",
        "Cache hit",
        "Authentication successful",
        "Payment processed",
        "Order created",
        "Timeout while processing request",
        "Database connection failed",
        "High memory usage detected",
        "Service unavailable",
    ]
    
    for i in range(100):
        service = services[i % len(services)]
        timestamp = now - timedelta(minutes=random.randint(0, 1440))  # Last 24 hours
        message = random.choice(log_messages)
        
        log = LogMetadata(
            service_id=service.id,
            log_level=random.choice(["INFO", "WARNING", "ERROR"]),
            timestamp=timestamp,
            latency_ms=random.uniform(50, 2000),
            message_hash=hash_string(message),
        )
        db.add(log)
        
        if (i + 1) % 10 == 0:
            logger.info(f"✅ Created {i + 1} logs")
    
    db.commit()
    logger.info(f"✅ Total logs created: {100}")


def seed_events(db):
    """Create sample events."""
    services = db.query(Service).all()
    
    if not services:
        logger.warning("No services found.")
        return
    
    now = datetime.utcnow()
    
    events_data = [
        {"event_type": "deployment", "details": "Deployed version 1.2.3"},
        {"event_type": "deployment", "details": "Deployed version 1.2.4"},
        {"event_type": "error_spike", "details": "Error rate increased 40%"},
        {"event_type": "service_restart", "details": "Service restarted"},
    ]
    
    for event_data in events_data:
        service = random.choice(services)
        event = Event(
            service_id=service.id,
            event_type=event_data["event_type"],
            timestamp=now - timedelta(hours=random.randint(0, 24)),
            details=event_data["details"],
        )
        db.add(event)
        logger.info(f"✅ Created event: {event_data['event_type']}")
    
    db.commit()


def main():
    logger.info("🌱 Seeding database...")
    
    # Initialize database
    init_db()
    logger.info("✅ Database initialized")
    
    # Create session
    db = SessionLocal()
    
    try:
        # Seed data
        seed_services(db)
        seed_logs(db)
        seed_events(db)
        
        logger.info("🎉 Database seeded successfully!")
    
    except Exception as e:
        logger.error(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    import random
    main()
