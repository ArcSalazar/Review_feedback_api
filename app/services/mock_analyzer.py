from typing import Dict, List
from app.services.interfaces import ReviewAnalyzerInterface
import logging

logger = logging.getLogger(__name__)


class AnalysisConfig:
    def __init__(self, model_config: dict = None):
        if model_config is None:
            model_config = {}
        self.threshold = model_config.get('threshold', 0.5)
        self.sentiment_model = model_config.get('sentiment_model', 'mock_sentiment_model')
        self.readability_model = model_config.get('readability_model', 'mock_readability_model')
        self.suggestion_model = model_config.get('suggestion_model', 'mock_suggestion_model')
        self.min_review_length = model_config.get('min_review_length', 20)
        self.max_exclamations = model_config.get('max_exclamations', 3)


class MockReviewAnalyzer(ReviewAnalyzerInterface):
    """Mock implementation of review analysis functionality for testing purposes."""

    def __init__(self, config: Dict = None):
        """Initialize mock models for sentiment, readability and suggestions."""
        self.config = AnalysisConfig(config)

    def analyze(self, text: str) -> Dict:
        """
        Analyze the given text and return sentiment, readability and suggestions.
        
        Args:
            text: The review text to analyze
            
        Returns:
            Dict containing sentiment, readability score, suggestions and models used
            
        Raises:
            Exception: If analysis fails
        """
        try:
            sentiment = self._determine_sentiment(text)
            readability = self._calculate_readability(text)
            suggestions = self._generate_suggestions(text)

            logger.info(
                f"Analysis completed using models: {self.config.sentiment_model}, {self.config.readability_model}, {self.config.suggestion_model}")

            return {
                "sentiment": sentiment,
                "readability_score": readability,
                "suggestions": suggestions,
                "models_used": {
                    "sentiment": self.config.sentiment_model,
                    "readability": self.config.readability_model,
                    "suggestions": self.config.suggestion_model
                }
            }
        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}")
            raise

    def _determine_sentiment(self, text: str) -> str:
        """
        Determine sentiment of text using basic keyword matching.
        
        Args:
            text: Text to analyze
            
        Returns:
            str: 'positive', 'negative' or 'neutral'
            
        Raises:
            Exception: If sentiment analysis fails
        """
        try:
            positives = ["good", "great", "excellent", "love", "amazing"]
            negatives = ["bad", "terrible", "poor", "hate", "awful"]

            text_lower = text.lower()
            pos_hits = sum(word in text_lower for word in positives)
            neg_hits = sum(word in text_lower for word in negatives)

            logger.debug(f"Sentiment analysis: pos_hits={pos_hits}, neg_hits={neg_hits}")

            threshold = self.config.threshold
            if pos_hits > neg_hits and pos_hits >= threshold:
                return "positive"
            elif neg_hits > pos_hits and neg_hits >= threshold:
                return "negative"
            else:
                return "neutral"
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            raise

    def _calculate_readability(self, text: str) -> float:
        """
        Calculate readability score based on words per sentence.
        
        Args:
            text: Text to analyze
            
        Returns:
            float: Readability score
            
        Raises:
            Exception: If readability calculation fails
        """
        try:
            words = text.split()
            sentences = text.count(".") + text.count("!") + text.count("?")
            if sentences == 0:
                sentences = 1
            score = len(words) / sentences

            logger.debug(f"Readability calculation: words={len(words)}, sentences={sentences}")

            return round(score, 2)
        except Exception as e:
            logger.error(f"Error in readability calculation: {str(e)}")
            raise

    def _generate_suggestions(self, text: str) -> List[str]:
        """
        Generate writing suggestions based on text analysis.
        
        Args:
            text: Text to analyze
            
        Returns:
            List[str]: List of writing suggestions
            
        Raises:
            Exception: If suggestion generation fails
        """
        try:
            suggestions = []
            text_length = len(text)
            exclamation_count = text.count("!")

            logger.debug(f"Suggestion analysis: length={text_length}, exclamations={exclamation_count}")

            if text_length < self.config.min_review_length:
                suggestions.append("Add more details to your review.")
            if exclamation_count > self.config.max_exclamations:
                suggestions.append("Avoid excessive exclamation marks.")
            if text.isupper():
                suggestions.append("Avoid writing in all caps.")

            return suggestions
        except Exception as e:
            logger.error(f"Error generating suggestions: {str(e)}")
            raise
