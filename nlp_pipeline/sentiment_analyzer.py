"""
Sentiment Analysis Module
Uses RoBERTa model fine-tuned for sentiment classification
"""

from transformers import pipeline
import torch

class SentimentAnalyzer:
    """
    Analyzes sentiment of customer reviews using transformer models.
    
    Returns:
        - label: 'POSITIVE', 'NEUTRAL', or 'NEGATIVE'
        - score: confidence score (0-1)
    """
    
    def __init__(self, model_name="cardiffnlp/twitter-roberta-base-sentiment-latest"):
        """
        Initialize sentiment analyzer with pre-trained model.
        
        Args:
            model_name: Hugging Face model identifier
        """
        print(f"Loading sentiment model: {model_name}")
        self.device = 0 if torch.cuda.is_available() else -1
        
        # Load pre-trained sentiment analysis pipeline
        self.classifier = pipeline(
            "sentiment-analysis",
            model=model_name,
            device=self.device
        )
        print("✓ Sentiment analyzer ready!")
    
    def analyze(self, text):
        """
        Analyze sentiment of a single review.
        
        Args:
            text (str): Review text to analyze
            
        Returns:
            dict: {
                'label': 'POSITIVE'|'NEUTRAL'|'NEGATIVE',
                'score': float,
                'raw_output': original model output
            }
        """
        if not text or not text.strip():
            return {
                'label': 'NEUTRAL',
                'score': 0.0,
                'raw_output': None,
                'error': 'Empty text'
            }
        
        try:
            # Get prediction
            result = self.classifier(text[:512])[0]  # Truncate to model max length
            
            # Map labels to standard format
            label_map = {
                'positive': 'POSITIVE',
                'negative': 'NEGATIVE',
                'neutral': 'NEUTRAL',
                'LABEL_0': 'NEGATIVE',
                'LABEL_1': 'NEUTRAL',
                'LABEL_2': 'POSITIVE'
            }
            
            label = label_map.get(result['label'].lower(), result['label'].upper())
            
            return {
                'label': label,
                'score': round(result['score'], 4),
                'raw_output': result
            }
            
        except Exception as e:
            return {
                'label': 'NEUTRAL',
                'score': 0.0,
                'raw_output': None,
                'error': str(e)
            }
    
    def analyze_batch(self, texts):
        """
        Analyze sentiment for multiple reviews at once.
        
        Args:
            texts (list): List of review texts
            
        Returns:
            list: List of sentiment results
        """
        return [self.analyze(text) for text in texts]


def analyze_sentiment(text):
    """
    Convenience function for quick sentiment analysis.
    
    Args:
        text (str): Review text
        
    Returns:
        dict: Sentiment analysis result
    """
    analyzer = SentimentAnalyzer()
    return analyzer.analyze(text)


# Example usage
if __name__ == "__main__":
    # Test the sentiment analyzer
    analyzer = SentimentAnalyzer()
    
    test_reviews = [
        "The coffee was absolutely amazing! Best I've ever had.",
        "Service was terrible and the food was cold.",
        "It was okay, nothing special but not bad either.",
        "Great atmosphere but a bit pricey."
    ]
    
    print("\n" + "="*70)
    print("SENTIMENT ANALYSIS DEMO")
    print("="*70 + "\n")
    
    for review in test_reviews:
        result = analyzer.analyze(review)
        print(f"Review: {review}")
        print(f"Sentiment: {result['label']} (confidence: {result['score']:.2%})")
        print("-" * 70)
