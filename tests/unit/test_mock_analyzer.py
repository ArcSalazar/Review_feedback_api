import pytest
from app.services.mock_analyzer import MockReviewAnalyzer
from app.models.review_models import ReviewRequest, ReviewFeedback

@pytest.fixture
def analyzer():
    return MockReviewAnalyzer()

def test_positive_sentiment(analyzer):
    review = ReviewRequest(text="This product is amazing! I love it!")
    result = analyzer.analyze(review.text)
    feedback = ReviewFeedback(**result)
    assert feedback.sentiment == "positive"
    assert isinstance(feedback.readability_score, float)
    assert isinstance(feedback.suggestions, list)

    review = ReviewRequest(text="THIS IS AMAZING I LOVE IT!!!!!!!!!!")
    result = analyzer.analyze(review.text)
    feedback = ReviewFeedback(**result)
    assert feedback.sentiment == "positive"
    assert isinstance(feedback.readability_score, float)
    assert isinstance(feedback.suggestions, list)
    assert len(feedback.suggestions) > 0
    assert "Avoid excessive exclamation marks." in feedback.suggestions
    assert "Avoid writing in all caps." in feedback.suggestions
