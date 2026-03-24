"""
Log processing worker - consumes from Kafka and processes logs.
"""
import logging
import json
import numpy as np
from kafka import KafkaConsumer
from app.core.config import settings
from app.core.kafka import send_anomaly_event
from app.ml.embedding import EmbeddingModel
from app.ml.anomaly_detection import AnomalyDetector
from app.ml.clustering import LogClusterer

logger = logging.getLogger(__name__)


def start_log_worker():
    """Start log processing worker."""
    logger.info("Starting log worker...")

    consumer = KafkaConsumer(
        settings.KAFKA_LOG_TOPIC,
        bootstrap_servers=settings.kafka_servers,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        group_id='devbrain-log-processor',
    )

    embedding_model = EmbeddingModel(dim=128)
    anomaly_detector = AnomalyDetector(contamination=0.1)
    clusterer = LogClusterer(eps=0.5, min_samples=2)

    history = []
    embeddings = []

    logger.info(f"Log worker listening on topic: {settings.KAFKA_LOG_TOPIC}")

    for message in consumer:
        try:
            log_data = message.value
            process_log(log_data, embedding_model, anomaly_detector, clusterer, history, embeddings)
        except Exception as e:
            logger.error(f"Error processing log: {e}")


def process_log(log_data: dict, embedding_model: EmbeddingModel, anomaly_detector: AnomalyDetector,
                clusterer: LogClusterer, history: list, embeddings: list):
    """Process a single log and run anomaly/clustering analysis."""
    logger.info(f"Processing log: {log_data}")

    # Embed the log message as a lightweight vector
    embed = embedding_model.generate_embedding(str(log_data.get("message", "")))
    embeddings.append(embed)

    # Keep last 200 logs in memory
    history.append(log_data)
    if len(history) > 200:
        history.pop(0)
        embeddings.pop(0)

    # Anomaly detection using latency/text features
    features = anomaly_detector.extract_features(history)
    if features.shape[0] >= 5:
        anomaly_detector.fit(features)
        labels, scores = anomaly_detector.predict(features)
        if labels and labels[-1] == -1:
            anomaly = {
                "service_id": log_data.get("service_id", 0),
                "message": log_data.get("message"),
                "log_level": log_data.get("log_level"),
                "anomaly_score": float(scores[-1] if scores else 1.0),
                "detection_method": "isolation_forest" if anomaly_detector.model is not None else "threshold",
                "description": "Detected anomaly in log pipeline",
            }
            try:
                send_anomaly_event(anomaly)
                logger.info("Anomaly event sent to Kafka: %s", anomaly)
            except Exception as e:
                logger.error("Failed to send anomaly event: %s", e)

    # Clustering updates
    if len(embeddings) >= 5:
        cluster_labels = clusterer.fit_predict(np.array(embeddings))
        if len(cluster_labels) > 0:
            log_data['cluster_id'] = int(cluster_labels[-1])
            logger.debug("Assigned cluster_id=%s for log", log_data['cluster_id'])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_log_worker()
