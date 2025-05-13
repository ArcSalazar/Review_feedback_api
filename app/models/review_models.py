from pydantic import BaseModel, Field
from typing import List


class ReviewRequest(BaseModel):
    text: str = Field(..., min_length=4, max_length=1000,
 description="The text of the product review")


class ReviewFeedback(BaseModel):
    sentiment: str = Field(..., description="Sentiment of the review (positive, negative, neutral)")
    readability_score: float = Field(..., description="Readability score of the review")
    suggestions: List[str] = Field(..., description="List of improvement suggestions")
