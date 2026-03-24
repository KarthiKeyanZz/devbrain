"""
Anomaly detection using Isolation Forest or simple thresholding.
"""
import logging
from typing import List, Tuple

import numpy as np

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """Detect anomalies using Isolation Forest."""

    def __init__(self, contamination: float = 0.1):
        self.contamination = contamination
        self.model = None
        try:
            from sklearn.ensemble import IsolationForest
            self.model = IsolationForest(contamination=self.contamination, random_state=42)
            logger.info("AnomalyDetector: Using sklearn IsolationForest")
        except Exception as e:
            logger.warning("IsolationForest unavailable, using fallback thresholding: %s", e)
            self.model = None

    def fit(self, features: np.ndarray):
        """Fit the model on training data."""
        if self.model is None:
            return
        if features.shape[0] < 2:
            return
        self.model.fit(features)

    def predict(self, features: np.ndarray) -> Tuple[List[int], List[float]]:
        """Predict anomalies.

        Returns:
            (anomaly_labels, anomaly_scores)
        """
        if features.shape[0] == 0:
            return [], []

        if self.model is not None:
            labels = self.model.predict(features)
            scores = -self.model.decision_function(features)
            # Normalize [0,1]
            min_s, max_s = float(min(scores)), float(max(scores))
            if max_s - min_s > 0:
                scores = [(s - min_s) / (max_s - min_s) for s in scores]
            else:
                scores = [0.0 for _ in scores]
            return labels.tolist(), scores

        # fallback based on latency & message size
        labels = []
        scores = []
        latencies = features[:, 0] if features.shape[1] > 0 else np.zeros(features.shape[0])
        if len(latencies) == 0:
            return [], []
        mean = float(np.mean(latencies))
        std = float(np.std(latencies)) or 1.0
        for v in latencies:
            score = min(1.0, max(0.0, (v - mean) / (4.0 * std)))
            scores.append(score)
            labels.append(-1 if score > 0.7 else 1)
        return labels, scores

    def extract_features(self, logs: List[dict]) -> np.ndarray:
        """Extract features from logs for anomaly detection."""
        features = []
        for log in logs:
            latency = float(log.get("latency_ms", 0) or 0)
            msg = str(log.get("message", ""))
            length = float(len(msg))
            level = log.get("log_level", "INFO").upper()
            lvl = {"DEBUG":0, "INFO":1, "WARNING":2, "ERROR":3, "CRITICAL":4}.get(level, 1)
            features.append([latency, length, lvl])
        return np.array(features, dtype=float)

