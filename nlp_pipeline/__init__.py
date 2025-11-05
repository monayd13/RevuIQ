"""
RevuIQ NLP Pipeline
AI-powered review analysis and response generation
"""

from .sentiment_analyzer import SentimentAnalyzer, analyze_sentiment
from .emotion_detector import EmotionDetector, detect_emotion
from .response_generator import ResponseGenerator, generate_response

__all__ = [
    'SentimentAnalyzer',
    'EmotionDetector',
    'ResponseGenerator',
    'analyze_sentiment',
    'detect_emotion',
    'generate_response'
]

__version__ = '0.1.0'
