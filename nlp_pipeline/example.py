"""
Quick Example - NLP Pipeline Usage
Run this to see the NLP pipeline in action without loading heavy models
"""

def mock_sentiment_analysis(text):
    """Mock sentiment analysis for quick testing"""
    positive_words = ['great', 'amazing', 'excellent', 'love', 'best', 'wonderful', 'fantastic']
    negative_words = ['bad', 'terrible', 'awful', 'worst', 'hate', 'poor', 'disappointing']
    
    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        return {'label': 'POSITIVE', 'score': 0.85}
    elif neg_count > pos_count:
        return {'label': 'NEGATIVE', 'score': 0.80}
    else:
        return {'label': 'NEUTRAL', 'score': 0.70}

def mock_emotion_detection(text):
    """Mock emotion detection for quick testing"""
    text_lower = text.lower()
    emotions = {}
    
    if any(word in text_lower for word in ['happy', 'love', 'great', 'amazing']):
        emotions['joy'] = 0.85
    if any(word in text_lower for word in ['thank', 'appreciate', 'grateful']):
        emotions['gratitude'] = 0.75
    if any(word in text_lower for word in ['angry', 'mad', 'furious']):
        emotions['anger'] = 0.80
    if any(word in text_lower for word in ['sad', 'disappointed', 'upset']):
        emotions['disappointment'] = 0.70
    
    return emotions if emotions else {'neutral': 0.60}

def mock_response_generation(text, sentiment):
    """Mock response generation for quick testing"""
    responses = {
        'POSITIVE': "Thank you so much for your wonderful feedback! We're thrilled you had a great experience. We look forward to serving you again soon!",
        'NEGATIVE': "We sincerely apologize for your disappointing experience. Your feedback is important to us, and we'd like to make this right. Please contact us directly so we can address your concerns.",
        'NEUTRAL': "Thank you for taking the time to share your feedback. We appreciate your input and are always working to improve our service."
    }
    return responses.get(sentiment, responses['NEUTRAL'])

def main():
    """Run example analysis"""
    print("\n" + "="*80)
    print("  RevuIQ NLP Pipeline - Quick Example")
    print("="*80 + "\n")
    
    # Sample reviews
    reviews = [
        "The food was absolutely amazing! Best restaurant I've been to in years. Will definitely come back!",
        "Terrible service and the food was cold. Very disappointed with this place.",
        "It was okay. Nothing special but not bad either. Average experience."
    ]
    
    for i, review in enumerate(reviews, 1):
        print(f"\n{'─'*80}")
        print(f"Review {i}")
        print(f"{'─'*80}\n")
        
        print(f"📝 Text: \"{review}\"")
        print()
        
        # Sentiment Analysis
        sentiment = mock_sentiment_analysis(review)
        emoji = {'POSITIVE': '😊', 'NEGATIVE': '😞', 'NEUTRAL': '😐'}
        print(f"💭 Sentiment: {sentiment['label']} {emoji[sentiment['label']]} (confidence: {sentiment['score']:.2f})")
        
        # Emotion Detection
        emotions = mock_emotion_detection(review)
        print(f"😊 Emotions: {', '.join(f'{k}: {v:.2f}' for k, v in emotions.items())}")
        
        # Response Generation
        response = mock_response_generation(review, sentiment['label'])
        print(f"\n✍️  AI Response:")
        print(f"   \"{response}\"")
    
    print("\n" + "="*80)
    print("  💡 To use real NLP models, run: python nlp_pipeline/demo.py")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
