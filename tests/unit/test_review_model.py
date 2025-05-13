import pytest
from app.models.review_models import ReviewRequest
from pydantic import ValidationError

def test_valid_review():
    review = ReviewRequest(text="Excellent product, very useful!")
    assert review.text == "Excellent product, very useful!"

def test_invalid_review_empty():
    with pytest.raises(ValidationError):
        ReviewRequest(text="")

def test_invalid_review_too_short():
    with pytest.raises(ValidationError):
        ReviewRequest(text=" ")  # whitespace only
