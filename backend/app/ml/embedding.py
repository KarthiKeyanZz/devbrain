"""
Log embedding generation using a lightweight ML embedding pipeline.
"""
import logging
from typing import List

logger = logging.getLogger(__name__)


class EmbeddingModel:
    """Generate embeddings for logs."""

    def __init__(self, dim: int = 128):
        self.dim = dim
        self._vocab = {}

    def _text_to_vector(self, text: str) -> List[float]:
        # Simple deterministic hash-based embedding to avoid external heavy models.
        vec = [0.0] * self.dim
        for i, token in enumerate(text.split(), start=1):
            idx = hash(token) % self.dim
            vec[idx] += 1.0
            if i >= 2 * self.dim:
                break
        # Normalize
        norm = sum(abs(v) for v in vec) or 1.0
        return [v / norm for v in vec]

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a log message."""
        if not text:
            return [0.0] * self.dim
        return self._text_to_vector(text)

    def generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        return [self.generate_embedding(t) for t in texts]

