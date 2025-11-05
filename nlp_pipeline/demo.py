"""
RevuIQ NLP Pipeline Demo
Complete end-to-end demonstration of review analysis and response generation
"""

from sentiment_analyzer import SentimentAnalyzer
from emotion_detector import EmotionDetector
from response_generator import ResponseGenerator
import time

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def print_section(title):
    """Print a section divider"""
    print(f"\n{'─'*80}")
    print(f"  {title}")
    print(f"{'─'*80}\n")

def analyze_review(review, sentiment_analyzer, emotion_detector, response_generator, business_name="Starbucks"):
    """
    Complete analysis pipeline for a single review.
    
    Args:
        review (str): Customer review text
        sentiment_analyzer: SentimentAnalyzer instance
        emotion_detector: EmotionDetector instance
        response_generator: ResponseGenerator instance
        business_name (str): Name of the business
        
    Returns:
        dict: Complete analysis results
    """
    print(f"📝 Review: \"{review}\"")
    print()
    
    # Step 1: Sentiment Analysis
    print("🔍 Analyzing sentiment...")
    sentiment_result = sentiment_analyzer.analyze(review)
    sentiment = sentiment_result['label']
    sentiment_score = sentiment_result['score']
    
    # Map sentiment to emoji
    sentiment_emoji = {
        'POSITIVE': '😊',
        'NEUTRAL': '😐',
        'NEGATIVE': '😞'
    }
    
    print(f"   {sentiment_emoji.get(sentiment, '❓')} Sentiment: {sentiment} (confidence: {sentiment_score:.1%})")
    
    # Step 2: Emotion Detection
    print("\n💭 Detecting emotions...")
    emotion_result = emotion_detector.detect(review, top_n=3)
    primary_emotion = emotion_result['primary_emotion']
    top_emotions = emotion_result['emotions']
    
    print(f"   Primary: {primary_emotion}")
    if top_emotions:
        print("   Top emotions:")
        for emotion in top_emotions:
            print(f"      • {emotion['label']}: {emotion['score']:.1%}")
    
    # Step 3: Response Generation
    print("\n✍️  Generating AI response...")
    response_result = response_generator.generate(
        review=review,
        sentiment=sentiment,
        emotion=primary_emotion,
        business_name=business_name
    )
    ai_response = response_result['response']
    
    print(f"   💬 AI Reply: \"{ai_response}\"")
    
    return {
        'review': review,
        'sentiment': sentiment,
        'sentiment_score': sentiment_score,
        'primary_emotion': primary_emotion,
        'emotions': top_emotions,
        'ai_response': ai_response
    }

def main():
    """Main demo function"""
    
    print_header("🧠 RevuIQ - AI-Powered Review Management System")
    print("Demonstrating complete NLP pipeline:")
    print("  1️⃣  Sentiment Analysis (RoBERTa)")
    print("  2️⃣  Emotion Detection (GoEmotions)")
    print("  3️⃣  Response Generation (Flan-T5)")
    
    # Initialize models
    print_section("🚀 Initializing NLP Models")
    
    print("Loading models (this may take a minute on first run)...\n")
    start_time = time.time()
    
    sentiment_analyzer = SentimentAnalyzer()
    emotion_detector = EmotionDetector()
    response_generator = ResponseGenerator()
    
    load_time = time.time() - start_time
    print(f"\n✅ All models loaded in {load_time:.1f} seconds!")
    
    # Test reviews
    test_reviews = [
        {
            'text': "The coffee was absolutely amazing! Best latte I've ever had. The barista was so friendly and made my day!",
            'business': "Starbucks"
        },
        {
            'text': "Terrible service. Waited 30 minutes for a cold sandwich. Staff was rude and unhelpful. Never coming back.",
            'business': "Subway"
        },
        {
            'text': "It was okay. Nothing special but not bad either. Average food, average service.",
            'business': "Chipotle"
        },
        {
            'text': "Great atmosphere and delicious food, but a bit overpriced. Would recommend for special occasions.",
            'business': "Olive Garden"
        },
        {
            'text': "I'm confused about the menu. Too many options and the descriptions aren't clear. Staff couldn't help much.",
            'business': "Cheesecake Factory"
        }
    ]
    
    # Analyze each review
    print_section("📊 Analyzing Sample Reviews")
    
    results = []
    for i, review_data in enumerate(test_reviews, 1):
        print(f"\n{'═'*80}")
        print(f"  Review #{i} - {review_data['business']}")
        print(f"{'═'*80}")
        
        result = analyze_review(
            review=review_data['text'],
            sentiment_analyzer=sentiment_analyzer,
            emotion_detector=emotion_detector,
            response_generator=response_generator,
            business_name=review_data['business']
        )
        results.append(result)
        
        time.sleep(0.5)  # Small delay for readability
    
    # Summary statistics
    print_section("📈 Summary Statistics")
    
    total_reviews = len(results)
    positive = sum(1 for r in results if r['sentiment'] == 'POSITIVE')
    negative = sum(1 for r in results if r['sentiment'] == 'NEGATIVE')
    neutral = sum(1 for r in results if r['sentiment'] == 'NEUTRAL')
    
    print(f"Total Reviews Analyzed: {total_reviews}")
    print(f"  😊 Positive: {positive} ({positive/total_reviews:.0%})")
    print(f"  😐 Neutral:  {neutral} ({neutral/total_reviews:.0%})")
    print(f"  😞 Negative: {negative} ({negative/total_reviews:.0%})")
    
    avg_confidence = sum(r['sentiment_score'] for r in results) / total_reviews
    print(f"\nAverage Confidence: {avg_confidence:.1%}")
    
    # Most common emotions
    all_emotions = {}
    for result in results:
        for emotion in result['emotions']:
            label = emotion['label']
            all_emotions[label] = all_emotions.get(label, 0) + 1
    
    if all_emotions:
        print("\nMost Common Emotions:")
        sorted_emotions = sorted(all_emotions.items(), key=lambda x: x[1], reverse=True)[:5]
        for emotion, count in sorted_emotions:
            print(f"  • {emotion}: {count}")
    
    # Completion message
    print_header("✅ Demo Complete!")
    print("RevuIQ successfully analyzed all reviews and generated AI responses.")
    print("\nNext Steps:")
    print("  1. Test with your own reviews")
    print("  2. Integrate with FastAPI backend")
    print("  3. Build the dashboard UI")
    print("  4. Connect to real review platforms (Google, Yelp, etc.)")
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
