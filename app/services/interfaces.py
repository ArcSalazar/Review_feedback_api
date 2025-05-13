from abc import ABC, abstractmethod
from typing import Dict


class ReviewAnalyzerInterface(ABC):
    @abstractmethod
    def analyze(self, text: str) -> Dict:
        """Analyzes a product review and returns structured feedback."""
        pass
