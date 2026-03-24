"""
Log clustering using DBSCAN.
"""
import logging
from typing import List
import numpy as np

logger = logging.getLogger(__name__)


class LogClusterer:
    """Cluster similar logs together."""

    def __init__(self, eps: float = 0.5, min_samples: int = 5):
        self.eps = eps
        self.min_samples = min_samples
        self.model = None
        try:
            from sklearn.cluster import DBSCAN
            self.model_cls = DBSCAN
            logger.info("LogClusterer: Using sklearn DBSCAN")
        except Exception as e:
            self.model_cls = None
            logger.warning("DBSCAN unavailable: %s", e)

    def fit_predict(self, embeddings: np.ndarray) -> List[int]:
        """Fit DBSCAN and return cluster labels."""
        if self.model_cls is None or embeddings.shape[0] == 0:
            return [-1] * embeddings.shape[0]
        self.model = self.model_cls(eps=self.eps, min_samples=self.min_samples)
        labels = self.model.fit_predict(embeddings)
        return labels.tolist()

    def update_clusters(self, new_embeddings: np.ndarray) -> List[int]:
        """Update clusters with new embeddings (re-fit)."""
        return self.fit_predict(new_embeddings)

