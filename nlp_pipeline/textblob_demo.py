"""
RevuIQ Demo - TextBlob Version (No PyTorch)
Works on ALL systems without threading issues
"""

print("🧠 RevuIQ - Alternative NLP Demo (TextBlob)\n")
print("Installing TextBlob if needed...")

try:
    from textblob import TextBlob
    import nltk
    print("✅ TextBlob ready!\n")
except ImportError:
    print("Installing TextBlob...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'textblob'])
    from textblob import TextBlob
    import nltk

# Download required data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading NLTK data...")
    nltk.download('punkt', quiet=True)
    nltk.download('brown', quiet=True)

def analyze_sentiment_simple(text):
    """Simple sentiment analysis using TextBlob"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        sentiment = "POSITIVE"
        emoji = "😊"
    elif polarity < -0.1:
        sentiment = "NEGATIVE"
        emoji = "😞"
    else:
        sentiment = "NEUTRAL"
        emoji = "😐"
    
    return {
        'sentiment': sentiment,
        'emoji': emoji,
        'score': abs(polarity),
        'polarity': polarity
    }

def detect_emotion_simple(text, sentiment):
    """Simple emotion detection based on keywords"""
    text_lower = text.lower()
    
    # Emotion keywords
    emotions = {
        'joy': ['amazing', 'great', 'excellent', 'wonderful', 'love', 'best', 'fantastic'],
        'anger': ['terrible', 'worst', 'awful', 'horrible', 'hate', 'angry', 'furious'],
        'disappointment': ['disappointed', 'let down', 'expected better', 'not good'],
        'gratitude': ['thank', 'appreciate', 'grateful'],
        'confusion': ['confused', 'unclear', 'don\'t understand'],
        'sadness': ['sad', 'unhappy', 'depressed']
    }
    
    detected = []
    for emotion, keywords in emotions.items():
        if any(keyword in text_lower for keyword in keywords):
            detected.append(emotion)
    
    if not detected:
        return 'neutral'
    return detected[0]

def generate_response_simple(review, sentiment, emotion):
    """Generate response based on sentiment and emotion"""
    
    responses = {
        'POSITIVE': [
            "Thank you so much for your wonderful feedback! We're thrilled you had a great experience.",
            "We're so happy to hear you enjoyed your visit! Your kind words mean a lot to us.",
            "Thank you for the amazing review! We look forward to serving you again soon."
        ],
        'NEGATIVE': [
            "We sincerely apologize for your experience. This is not the standard we aim for, and we'd like to make it right.",
            "We're sorry to hear about your disappointing visit. Please contact us so we can address this issue.",
            "Thank you for bringing this to our attention. We take your feedback seriously and will work to improve."
        ],
        'NEUTRAL': [
            "Thank you for your feedback! We appreciate you taking the time to share your thoughts.",
            "We value your input and are always looking for ways to improve. Thank you for visiting!",
            "Thanks for your review! We hope to exceed your expectations next time."
        ]
    }
    
    import random
    return random.choice(responses[sentiment])

def main():
    """Main demo"""
    print("="*80)
    print("  🧠 RevuIQ - Simple NLP Demo")
    print("="*80)
    print("\nThis version uses TextBlob (no PyTorch) - works on all systems!\n")
    
    # Test reviews
    test_reviews = [
        "The coffee was absolutely amazing! Best I've ever had.",
        "Terrible service. Waited forever and food was cold.",
        "It was okay, nothing special.",
        "Great atmosphere but a bit pricey.",
        "I'm confused about the menu options."
    ]
    
    print("Analyzing reviews...\n")
    
    for i, review in enumerate(test_reviews, 1):
        print(f"{'='*80}")
        print(f"Review #{i}")
        print(f"{'='*80}")
        print(f"📝 Text: \"{review}\"")
        print()
        
        # Analyze
        sentiment_result = analyze_sentiment_simple(review)
        emotion = detect_emotion_simple(review, sentiment_result['sentiment'])
        response = generate_response_simple(review, sentiment_result['sentiment'], emotion)
        
        print(f"🔍 Sentiment: {sentiment_result['emoji']} {sentiment_result['sentiment']}")
        print(f"   Confidence: {sentiment_result['score']:.1%}")
        print(f"\n💭 Emotion: {emotion}")
        print(f"\n✍️  AI Response:")
        print(f"   \"{response}\"")
        print()
    
    print("="*80)
    print("✅ Demo Complete!")
    print("="*80)
    print("\nThis simple version works! Next steps:")
    print("1. Fix PyTorch installation for advanced models")
    print("2. Or continue with TextBlob for now")
    print("3. Build the backend API")
    print("\nTo fix PyTorch issue, try:")
    print("  conda install pytorch -c pytorch")
    print("  (or)")
    print("  pip install torch==2.0.0")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
