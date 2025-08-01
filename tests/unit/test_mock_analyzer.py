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


def test_negative_sentiment(analyzer):
    review = ReviewRequest(text="This is a terrible product. I hate it!")
    result = analyzer.analyze(review.text)
    feedback = ReviewFeedback(**result)
    assert feedback.sentiment == "negative"
    assert isinstance(feedback.readability_score, float)


def test_neutral_sentiment(analyzer):
    review = ReviewRequest(text="The product works as expected.")
    result = analyzer.analyze(review.text)
    feedback = ReviewFeedback(**result)
    assert feedback.sentiment == "neutral"


def test_short_review_suggestion(analyzer):
    review = ReviewRequest(text="Short review")
    result = analyzer.analyze(review.text)
    feedback = ReviewFeedback(**result)
    assert "Add more details to your review." in feedback.suggestions


def test_readability_no_punctuation(analyzer):
    review = ReviewRequest(text="one two three four")
    result = analyzer.analyze(review.text)
    feedback = ReviewFeedback(**result)
    assert feedback.readability_score == 4.0
