"""
Sentiment Analysis Module
Uses VADER (lightweight, no GPU/torch needed) for sentiment classification
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as VaderAnalyzer


class SentimentAnalyzer:
    """
    Analyzes sentiment of customer reviews using VADER.

    Returns:
        - label: 'POSITIVE', 'NEUTRAL', or 'NEGATIVE'
        - score: confidence score (0-1)
    """

    def __init__(self, model_name=None):
        self._vader = VaderAnalyzer()
        print("✓ Sentiment analyzer ready!")

    def analyze(self, text):
        if not text or not text.strip():
            return {'label': 'NEUTRAL', 'score': 0.0, 'raw_output': None, 'error': 'Empty text'}

        try:
            scores = self._vader.polarity_scores(text)
            compound = scores['compound']

            if compound >= 0.05:
                label = 'POSITIVE'
                score = (compound + 1) / 2
            elif compound <= -0.05:
                label = 'NEGATIVE'
                score = (1 - compound) / 2
            else:
                label = 'NEUTRAL'
                score = 1 - abs(compound)

            return {
                'label': label,
                'score': round(score, 4),
                'raw_output': scores
            }
        except Exception as e:
            return {'label': 'NEUTRAL', 'score': 0.0, 'raw_output': None, 'error': str(e)}

    def analyze_batch(self, texts):
        return [self.analyze(text) for text in texts]


def analyze_sentiment(text):
    analyzer = SentimentAnalyzer()
    return analyzer.analyze(text)
