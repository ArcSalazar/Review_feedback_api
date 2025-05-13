import logging

from fastapi import APIRouter, Depends

from app.dependencies import get_review_analyzer
from app.models.review_models import ReviewFeedback, ReviewRequest
from app.services.interfaces import ReviewAnalyzerInterface
from fastapi import HTTPException

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/",
             response_model=ReviewFeedback,
             summary="Analyze product review",
             description="Analyzes a product review and returns sentiment, readability score, and suggestions.",
             responses={
                 200: {"description": "Success"},
                 422: {"description": "Validation Error"}
             }
             )
def get_review_feedback(
        request: ReviewRequest,
        analyzer: ReviewAnalyzerInterface = Depends(get_review_analyzer),
) -> ReviewFeedback:
    """
    Analyze a product review and provide feedback.

    Args:
        request: The review request containing the text to analyze
        analyzer: The review analyzer service dependency

    Returns:
        ReviewFeedback object containing sentiment, readability score and suggestions

    Raises:
        HTTPException: If analysis fails with 422 status code
    """
    logger.info(f"Processing review: {request.text[:50]}...")
    try:
        result = analyzer.analyze(request.text)
        logger.info("Analysis completed successfully")
        return ReviewFeedback(**result)
    except AnalysisError as e:
        raise HTTPException(status_code=422, detail=str(e))


class AnalysisError(Exception):
    """Custom exception for review analysis errors."""
    pass
