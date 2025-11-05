"""
Emotion Detection Module
Uses GoEmotions model for multi-label emotion classification
"""

from transformers import pipeline
import torch

class EmotionDetector:
    """
    Detects emotions in customer reviews using GoEmotions dataset.
    
    Emotions detected:
    - admiration, amusement, anger, annoyance, approval, caring, confusion,
    - curiosity, desire, disappointment, disapproval, disgust, embarrassment,
    - excitement, fear, gratitude, grief, joy, love, nervousness, optimism,
    - pride, realization, relief, remorse, sadness, surprise, neutral
    """
    
    def __init__(self, model_name="SamLowe/roberta-base-go_emotions"):
        """
        Initialize emotion detector with pre-trained model.
        
        Args:
            model_name: Hugging Face model identifier
        """
        print(f"Loading emotion model: {model_name}")
        self.device = 0 if torch.cuda.is_available() else -1
        
        # Load emotion classification pipeline
        self.classifier = pipeline(
            "text-classification",
            model=model_name,
            device=self.device,
            top_k=None  # Return all emotion scores
        )
        print("✓ Emotion detector ready!")
    
    def detect(self, text, top_n=3, threshold=0.1):
        """
        Detect emotions in a review.
        
        Args:
            text (str): Review text to analyze
            top_n (int): Number of top emotions to return
            threshold (float): Minimum confidence threshold
            
        Returns:
            dict: {
                'primary_emotion': str,
                'emotions': list of {label, score},
                'all_scores': dict of all emotion scores
            }
        """
        if not text or not text.strip():
            return {
                'primary_emotion': 'neutral',
                'emotions': [],
                'all_scores': {},
                'error': 'Empty text'
            }
        
        try:
            # Get predictions
            results = self.classifier(text[:512])[0]  # Truncate to model max length
            
            # Sort by score
            sorted_emotions = sorted(results, key=lambda x: x['score'], reverse=True)
            
            # Filter by threshold
            significant_emotions = [
                {'label': e['label'], 'score': round(e['score'], 4)}
                for e in sorted_emotions
                if e['score'] >= threshold
            ][:top_n]
            
            # Create emotion score dictionary
            all_scores = {e['label']: round(e['score'], 4) for e in results}
            
            return {
                'primary_emotion': sorted_emotions[0]['label'] if sorted_emotions else 'neutral',
                'emotions': significant_emotions,
                'all_scores': all_scores
            }
            
        except Exception as e:
            return {
                'primary_emotion': 'neutral',
                'emotions': [],
                'all_scores': {},
                'error': str(e)
            }
    
    def detect_batch(self, texts, top_n=3, threshold=0.1):
        """
        Detect emotions for multiple reviews.
        
        Args:
            texts (list): List of review texts
            top_n (int): Number of top emotions per review
            threshold (float): Minimum confidence threshold
            
        Returns:
            list: List of emotion detection results
        """
        return [self.detect(text, top_n, threshold) for text in texts]
    
    def get_emotion_summary(self, text):
        """
        Get a human-readable emotion summary.
        
        Args:
            text (str): Review text
            
        Returns:
            str: Formatted emotion summary
        """
        result = self.detect(text)
        
        if result.get('error'):
            return "Unable to detect emotions"
        
        emotions = result['emotions']
        if not emotions:
            return "Neutral tone"
        
        emotion_str = ", ".join([
            f"{e['label']} ({e['score']:.0%})"
            for e in emotions
        ])
        
        return emotion_str


def detect_emotion(text):
    """
    Convenience function for quick emotion detection.
    
    Args:
        text (str): Review text
        
    Returns:
        dict: Emotion detection result
    """
    detector = EmotionDetector()
    return detector.detect(text)


# Example usage
if __name__ == "__main__":
    # Test the emotion detector
    detector = EmotionDetector()
    
    test_reviews = [
        "I absolutely loved this place! The staff was so friendly and caring.",
        "This was the worst experience ever. I'm so angry and disappointed.",
        "I'm confused about the menu. Not sure what to order.",
        "Thank you so much for the wonderful service! You made my day."
    ]
    
    print("\n" + "="*70)
    print("EMOTION DETECTION DEMO")
    print("="*70 + "\n")
    
    for review in test_reviews:
        result = detector.detect(review)
        print(f"Review: {review}")
        print(f"Primary Emotion: {result['primary_emotion']}")
        print(f"Top Emotions: {detector.get_emotion_summary(review)}")
        print("-" * 70)
