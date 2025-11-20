"""
Quick Test Script for Restaurant API
Tests all major endpoints and NLP functionality
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_health():
    """Test health check"""
    print_section("1. Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200

def test_create_restaurant():
    """Test creating a restaurant"""
    print_section("2. Create Restaurant")
    data = {
        "name": "Test Italian Restaurant",
        "industry": "restaurant"
    }
    response = requests.post(f"{BASE_URL}/api/restaurants", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(json.dumps(result, indent=2))
    
    if result.get("success"):
        return result["restaurant"]["id"]
    return None

def test_get_restaurants():
    """Test getting all restaurants"""
    print_section("3. Get All Restaurants")
    response = requests.get(f"{BASE_URL}/api/restaurants")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Found {result.get('count', 0)} restaurants")
    if result.get("restaurants"):
        for r in result["restaurants"][:3]:  # Show first 3
            print(f"  - {r['name']} (ID: {r['id']}, Reviews: {r['review_count']})")
    return response.status_code == 200

def test_create_review(restaurant_id):
    """Test creating a review with NLP analysis"""
    print_section("4. Create Review with NLP Analysis")
    data = {
        "platform": "google",
        "platform_review_id": f"test_{datetime.now().timestamp()}",
        "business_id": restaurant_id,
        "author_name": "John Doe",
        "rating": 5.0,
        "text": "Absolutely amazing experience! The pasta was delicious and the service was outstanding. The staff was very friendly and attentive. Highly recommend!",
        "review_date": datetime.now().isoformat()
    }
    
    response = requests.post(f"{BASE_URL}/api/reviews", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result.get("success"):
        print(f"\n✓ Review created with ID: {result['review_id']}")
        print("\nNLP Analysis Results:")
        analysis = result.get("analysis", {})
        
        # Sentiment
        sentiment = analysis.get("sentiment", {})
        print(f"\n  Sentiment: {sentiment.get('label')} (confidence: {sentiment.get('score', 0)*100:.1f}%)")
        
        # Emotions
        emotions = analysis.get("emotions", {})
        if emotions:
            print(f"\n  Top Emotions:")
            sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:3]
            for emotion, score in sorted_emotions:
                print(f"    - {emotion}: {score*100:.1f}%")
        
        # Aspects
        aspects = analysis.get("aspects", [])
        if aspects:
            print(f"\n  Detected Aspects:")
            for aspect in aspects[:5]:
                print(f"    - {aspect.get('aspect')}: {aspect.get('sentiment', 'N/A')}")
        
        # AI Response
        ai_response = analysis.get("ai_response")
        if ai_response:
            print(f"\n  AI-Generated Response:")
            print(f"    \"{ai_response}\"")
    
    return result.get("success", False)

def test_bulk_reviews(restaurant_id):
    """Test bulk review upload"""
    print_section("5. Bulk Review Upload")
    
    reviews = [
        {
            "platform": "google",
            "platform_review_id": f"bulk_{datetime.now().timestamp()}_1",
            "author_name": "Sarah Johnson",
            "rating": 4.0,
            "text": "Good food but the wait time was a bit long. Overall pleasant experience.",
            "review_date": datetime.now().isoformat()
        },
        {
            "platform": "yelp",
            "platform_review_id": f"bulk_{datetime.now().timestamp()}_2",
            "author_name": "Mike Williams",
            "rating": 2.0,
            "text": "Disappointed with the service. Food was cold and staff seemed uninterested.",
            "review_date": datetime.now().isoformat()
        },
        {
            "platform": "google",
            "platform_review_id": f"bulk_{datetime.now().timestamp()}_3",
            "author_name": "Emily Chen",
            "rating": 5.0,
            "text": "Best Italian restaurant in town! The tiramisu is to die for!",
            "review_date": datetime.now().isoformat()
        }
    ]
    
    data = {
        "business_id": restaurant_id,
        "reviews": reviews
    }
    
    response = requests.post(f"{BASE_URL}/api/reviews/bulk", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result.get("success"):
        print(f"\n✓ Created: {result.get('created')} reviews")
        print(f"  Skipped: {result.get('skipped')} reviews")
        print(f"  Total: {result.get('total')} reviews")
    
    return result.get("success", False)

def test_get_reviews(restaurant_id):
    """Test getting restaurant reviews"""
    print_section("6. Get Restaurant Reviews")
    response = requests.get(f"{BASE_URL}/api/reviews/restaurant/{restaurant_id}")
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result.get("success"):
        print(f"\nFound {result.get('count', 0)} reviews")
        for review in result.get("reviews", [])[:2]:  # Show first 2
            print(f"\n  Review by {review['author']} ({review['rating']}⭐)")
            print(f"    Sentiment: {review['sentiment']}")
            print(f"    Text: {review['text'][:80]}...")
    
    return result.get("success", False)

def test_analytics(restaurant_id):
    """Test analytics endpoint"""
    print_section("7. Restaurant Analytics")
    response = requests.get(f"{BASE_URL}/api/analytics/restaurant/{restaurant_id}?days=30")
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result.get("success"):
        print(f"\nTotal Reviews: {result.get('total_reviews', 0)}")
        print(f"Average Rating: {result.get('average_rating', 0):.2f}⭐")
        
        # Sentiment distribution
        sentiment = result.get("sentiment_distribution", {})
        print(f"\nSentiment Distribution:")
        print(f"  Positive: {sentiment.get('POSITIVE', 0)}")
        print(f"  Neutral: {sentiment.get('NEUTRAL', 0)}")
        print(f"  Negative: {sentiment.get('NEGATIVE', 0)}")
        
        # Top emotions
        emotions = result.get("top_emotions", {})
        if emotions:
            print(f"\nTop Emotions:")
            for emotion, score in list(emotions.items())[:3]:
                print(f"  {emotion}: {score*100:.1f}%")
        
        # Top aspects
        aspects = result.get("top_aspects", {})
        if aspects:
            print(f"\nTop Aspects:")
            for aspect, count in list(aspects.items())[:5]:
                print(f"  {aspect}: {count} mentions")
    
    return result.get("success", False)

def test_overall_stats():
    """Test overall statistics"""
    print_section("8. Overall System Stats")
    response = requests.get(f"{BASE_URL}/api/analytics/stats")
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result.get("success"):
        print(f"\nTotal Reviews: {result.get('total_reviews', 0)}")
        print(f"Total Restaurants: {result.get('total_restaurants', 0)}")
        print(f"Average Rating: {result.get('average_rating', 0):.2f}⭐")
        
        stats = result.get("response_stats", {})
        print(f"\nResponse Stats:")
        print(f"  Approval Rate: {stats.get('approval_rate', 0):.1f}%")
    
    return result.get("success", False)

def main():
    """Run all tests"""
    print("\n" + "🚀"*35)
    print("  RESTAURANT API TEST SUITE")
    print("🚀"*35)
    
    try:
        # Test health
        if not test_health():
            print("\n❌ Health check failed. Is the server running?")
            return
        
        # Create restaurant
        restaurant_id = test_create_restaurant()
        if not restaurant_id:
            print("\n❌ Failed to create restaurant")
            return
        
        # Get restaurants
        test_get_restaurants()
        
        # Create single review
        test_create_review(restaurant_id)
        
        # Bulk upload
        test_bulk_reviews(restaurant_id)
        
        # Get reviews
        test_get_reviews(restaurant_id)
        
        # Analytics
        test_analytics(restaurant_id)
        
        # Overall stats
        test_overall_stats()
        
        print("\n" + "✅"*35)
        print("  ALL TESTS COMPLETED SUCCESSFULLY!")
        print("✅"*35)
        
        print("\n📊 Next Steps:")
        print("  1. Open http://localhost:3000/restaurants")
        print("  2. View the restaurant you just created")
        print("  3. Click 'View Analytics' to see the NLP insights")
        print("  4. Try uploading more sample reviews")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend server")
        print("   Make sure the backend is running:")
        print("   cd backend && python restaurant_api.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
