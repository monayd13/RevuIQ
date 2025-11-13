"""
Simple Google Places Reviews Fetcher
Fetches real reviews from Google Places API
"""

import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class GoogleReviewsFetcher:
    """Fetch reviews from Google Places API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_PLACES_API_KEY")
        self.base_url = "https://maps.googleapis.com/maps/api/place"
    
    def search_restaurant(self, restaurant_name: str, location: str = "") -> Optional[str]:
        """
        Search for a restaurant and get its place_id
        
        Args:
            restaurant_name: Name of the restaurant
            location: Optional location (e.g., "New York, NY")
        
        Returns:
            place_id if found, None otherwise
        """
        if not self.api_key:
            print("⚠️  No Google API key found. Using demo mode.")
            return None
        
        try:
            # Build search query
            query = restaurant_name
            if location:
                query += f" {location}"
            
            # Search for the place
            search_url = f"{self.base_url}/findplacefromtext/json"
            params = {
                "input": query,
                "inputtype": "textquery",
                "fields": "place_id,name,formatted_address,rating",
                "key": self.api_key
            }
            
            response = requests.get(search_url, params=params)
            data = response.json()
            
            if data.get("status") == "OK" and data.get("candidates"):
                place = data["candidates"][0]
                print(f"✅ Found: {place.get('name')} - {place.get('formatted_address')}")
                return place.get("place_id")
            else:
                print(f"❌ Restaurant not found: {restaurant_name}")
                return None
                
        except Exception as e:
            print(f"❌ Search error: {e}")
            return None
    
    def get_reviews(self, place_id: str) -> List[Dict]:
        """
        Get reviews for a place
        
        Args:
            place_id: Google Place ID
        
        Returns:
            List of review dictionaries
        """
        if not self.api_key:
            return self._get_demo_reviews()
        
        try:
            # Get place details including reviews
            details_url = f"{self.base_url}/details/json"
            params = {
                "place_id": place_id,
                "fields": "name,rating,reviews,user_ratings_total",
                "key": self.api_key
            }
            
            response = requests.get(details_url, params=params)
            data = response.json()
            
            if data.get("status") == "OK":
                result = data.get("result", {})
                reviews = result.get("reviews", [])
                
                # Format reviews
                formatted_reviews = []
                for review in reviews:
                    formatted_reviews.append({
                        "text": review.get("text", ""),
                        "rating": review.get("rating", 0),
                        "author": review.get("author_name", "Anonymous"),
                        "time": review.get("relative_time_description", ""),
                        "platform": "Google"
                    })
                
                print(f"✅ Fetched {len(formatted_reviews)} reviews")
                return formatted_reviews
            else:
                print(f"❌ Failed to get reviews: {data.get('status')}")
                return self._get_demo_reviews()
                
        except Exception as e:
            print(f"❌ Error fetching reviews: {e}")
            return self._get_demo_reviews()
    
    def fetch_restaurant_reviews(self, restaurant_name: str, location: str = "") -> List[Dict]:
        """
        One-step function to search and fetch reviews
        
        Args:
            restaurant_name: Name of the restaurant
            location: Optional location
        
        Returns:
            List of reviews
        """
        print(f"🔍 Searching for: {restaurant_name}")
        
        # Search for restaurant
        place_id = self.search_restaurant(restaurant_name, location)
        
        if not place_id:
            print("⚠️  Using demo reviews instead")
            return self._get_demo_reviews()
        
        # Get reviews
        return self.get_reviews(place_id)
    
    def _get_demo_reviews(self) -> List[Dict]:
        """Return demo reviews when API is not available"""
        return [
            {
                "text": "Amazing food and service! The pasta was perfectly cooked and the staff was incredibly attentive. Highly recommend!",
                "rating": 5,
                "author": "John Smith",
                "time": "2 weeks ago",
                "platform": "Google"
            },
            {
                "text": "Good experience overall. The food was tasty but the wait time was a bit long. Would come back though.",
                "rating": 4,
                "author": "Sarah Johnson",
                "time": "1 month ago",
                "platform": "Google"
            },
            {
                "text": "Disappointing visit. The food was cold and service was slow. Not worth the price.",
                "rating": 2,
                "author": "Mike Davis",
                "time": "3 weeks ago",
                "platform": "Google"
            },
            {
                "text": "Decent place. Nothing special but nothing bad either. Average food at average prices.",
                "rating": 3,
                "author": "Emily Chen",
                "time": "1 week ago",
                "platform": "Google"
            },
            {
                "text": "Best restaurant in town! The ambiance is perfect and every dish is a masterpiece. Will definitely return!",
                "rating": 5,
                "author": "David Martinez",
                "time": "4 days ago",
                "platform": "Google"
            },
            {
                "text": "Great atmosphere and friendly staff. The portions were generous and everything tasted fresh.",
                "rating": 5,
                "author": "Lisa Anderson",
                "time": "1 month ago",
                "platform": "Google"
            },
            {
                "text": "Not impressed. The menu was limited and the food was mediocre at best. Overpriced for what you get.",
                "rating": 2,
                "author": "Robert Wilson",
                "time": "2 months ago",
                "platform": "Google"
            },
            {
                "text": "Solid choice for a casual dinner. Good food, reasonable prices, and nice location.",
                "rating": 4,
                "author": "Jennifer Lee",
                "time": "3 weeks ago",
                "platform": "Google"
            }
        ]


# Test the fetcher
if __name__ == "__main__":
    fetcher = GoogleReviewsFetcher()
    
    # Test with a famous restaurant
    print("\n" + "="*70)
    print("🍽️  Google Reviews Fetcher Test")
    print("="*70 + "\n")
    
    # Example: Search for a restaurant
    restaurant = input("Enter restaurant name (or press Enter for 'Olive Garden'): ").strip()
    if not restaurant:
        restaurant = "Olive Garden"
    
    location = input("Enter location (or press Enter for 'New York'): ").strip()
    if not location:
        location = "New York"
    
    print()
    reviews = fetcher.fetch_restaurant_reviews(restaurant, location)
    
    print(f"\n📊 Found {len(reviews)} reviews:\n")
    for i, review in enumerate(reviews[:5], 1):
        print(f"{i}. {'⭐' * review['rating']} ({review['rating']}/5)")
        print(f"   {review['text'][:100]}...")
        print(f"   - {review['author']} ({review['time']})\n")
