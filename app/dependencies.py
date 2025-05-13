from app.services.mock_analyzer import MockReviewAnalyzer
from app.services.interfaces import ReviewAnalyzerInterface

from functools import lru_cache

@lru_cache(maxsize=100)
def get_review_analyzer() -> ReviewAnalyzerInterface:
    return MockReviewAnalyzer()
