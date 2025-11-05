"""
Simple Test - One review at a time
Safest way to test on macOS
"""

import os
# Threading fix for macOS
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

print("🧠 RevuIQ - Simple Test\n")
print("Loading models (first run downloads ~2GB, please wait)...\n")

# Test 1: Sentiment Analysis
print("="*70)
print("TEST 1: Sentiment Analysis")
print("="*70)

try:
    from sentiment_analyzer import SentimentAnalyzer
    
    analyzer = SentimentAnalyzer()
    
    review = "The coffee was amazing! Best I've ever had."
    result = analyzer.analyze(review)
    
    print(f"\n✅ SUCCESS!")
    print(f"Review: {review}")
    print(f"Sentiment: {result['label']} (confidence: {result['score']:.1%})")
    
except Exception as e:
    print(f"\n❌ FAILED: {e}")
    print("\nTry: pip install --upgrade transformers torch")

# Test 2: Emotion Detection
print("\n" + "="*70)
print("TEST 2: Emotion Detection")
print("="*70)

try:
    from emotion_detector import EmotionDetector
    
    detector = EmotionDetector()
    
    review = "I'm so disappointed with the service."
    result = detector.detect(review)
    
    print(f"\n✅ SUCCESS!")
    print(f"Review: {review}")
    print(f"Primary Emotion: {result['primary_emotion']}")
    if result['emotions']:
        print("Top Emotions:")
        for e in result['emotions'][:3]:
            print(f"  • {e['label']}: {e['score']:.1%}")
    
except Exception as e:
    print(f"\n❌ FAILED: {e}")

# Test 3: Response Generation
print("\n" + "="*70)
print("TEST 3: Response Generation")
print("="*70)

try:
    from response_generator import ResponseGenerator
    
    generator = ResponseGenerator()
    
    review = "Great food but service was slow."
    result = generator.generate(review, sentiment="NEUTRAL", emotion="disappointment")
    
    print(f"\n✅ SUCCESS!")
    print(f"Review: {review}")
    print(f"AI Response: {result['response']}")
    
except Exception as e:
    print(f"\n❌ FAILED: {e}")

print("\n" + "="*70)
print("✅ All Tests Complete!")
print("="*70)
print("\nIf all tests passed, you can run the full demo:")
print("  python demo_fixed.py")
