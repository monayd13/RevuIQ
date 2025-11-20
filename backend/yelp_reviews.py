"""
Yelp Fusion API - Free Restaurant Reviews Fetcher
No credit card required! 5,000 calls/day free
"""

import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class YelpReviewsFetcher:
    """Fetch reviews from Yelp Fusion API (FREE - No credit card needed!)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("YELP_API_KEY")
        self.base_url = "https://api.yelp.com/v3"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else ""
        }
    
    def search_business(self, name: str, location: str = "") -> Optional[str]:
        """
        Search for a business and get its ID
        
        Args:
            name: Business name
            location: Location (e.g., "New York, NY")
        
        Returns:
            business_id if found, None otherwise
        """
        if not self.api_key:
            print("⚠️  No Yelp API key found. Using demo mode.")
            return None
        
        try:
            url = f"{self.base_url}/businesses/search"
            params = {
                "term": name,
                "location": location or "New York",
                "limit": 1
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                businesses = data.get("businesses", [])
                
                if businesses:
                    business = businesses[0]
                    print(f"✅ Found: {business['name']} - {business.get('location', {}).get('address1', 'N/A')}")
                    print(f"   Rating: {business.get('rating', 'N/A')} ⭐ ({business.get('review_count', 0)} reviews)")
                    return business["id"]
                else:
                    print(f"❌ Business not found: {name}")
                    return None
            else:
                print(f"❌ API Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Search error: {e}")
            return None
    
    def get_reviews(self, business_id: str) -> List[Dict]:
        """
        Get reviews for a business
        
        Args:
            business_id: Yelp business ID
        
        Returns:
            List of review dictionaries
        """
        if not self.api_key:
            return self._get_demo_reviews()
        
        try:
            url = f"{self.base_url}/businesses/{business_id}/reviews"
            params = {"limit": 50, "sort_by": "yelp_sort"}
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                reviews = data.get("reviews", [])
                
                # Format reviews
                formatted_reviews = []
                for review in reviews:
                    formatted_reviews.append({
                        "text": review.get("text", ""),
                        "rating": review.get("rating", 0),
                        "author": review.get("user", {}).get("name", "Anonymous"),
                        "time": review.get("time_created", ""),
                        "platform": "Yelp"
                    })
                
                print(f"✅ Fetched {len(formatted_reviews)} reviews from Yelp")
                return formatted_reviews
            else:
                print(f"❌ Failed to get reviews: {response.status_code}")
                return self._get_demo_reviews()
                
        except Exception as e:
            print(f"❌ Error fetching reviews: {e}")
            return self._get_demo_reviews()
    
    def fetch_business_reviews(self, business_name: str, location: str = "") -> List[Dict]:
        """
        One-step function to search and fetch reviews
        
        Args:
            business_name: Name of the business
            location: Location (optional)
        
        Returns:
            List of reviews
        """
        print(f"🔍 Searching Yelp for: {business_name}")
        
        # Search for business
        business_id = self.search_business(business_name, location)
        
        if not business_id:
            print("⚠️  Using demo reviews instead")
            return self._get_demo_reviews()
        
        # Get reviews
        return self.get_reviews(business_id)
    
    def _get_demo_reviews(self) -> List[Dict]:
        """Return demo reviews when API is not available"""
        return [
            {
                "text": "Amazing food and service! The pasta was perfectly cooked and the staff was incredibly attentive. Highly recommend!",
                "rating": 5,
                "author": "John Smith",
                "time": "2024-11-01",
                "platform": "Yelp"
            },
            {
                "text": "Good experience overall. The food was tasty but the wait time was a bit long. Would come back though.",
                "rating": 4,
                "author": "Sarah Johnson",
                "time": "2024-10-15",
                "platform": "Yelp"
            },
            {
                "text": "Disappointing visit. The food was cold and service was slow. Not worth the price.",
                "rating": 2,
                "author": "Mike Davis",
                "time": "2024-10-20",
                "platform": "Yelp"
            },
            {
                "text": "Decent place. Nothing special but nothing bad either. Average food at average prices.",
                "rating": 3,
                "author": "Emily Chen",
                "time": "2024-11-05",
                "platform": "Yelp"
            },
            {
                "text": "Best restaurant in town! The ambiance is perfect and every dish is a masterpiece. Will definitely return!",
                "rating": 5,
                "author": "David Martinez",
                "time": "2024-11-10",
                "platform": "Yelp"
            }
        ]


# Test the fetcher
if __name__ == "__main__":
    fetcher = YelpReviewsFetcher()
    
    print("\n" + "="*70)
    print("🍽️  Yelp Reviews Fetcher Test (FREE - No Credit Card!)")
    print("="*70 + "\n")
    
    # Example: Search for a restaurant
    restaurant = input("Enter restaurant name (or press Enter for 'Olive Garden'): ").strip()
    if not restaurant:
        restaurant = "Olive Garden"
    
    location = input("Enter location (or press Enter for 'New York'): ").strip()
    if not location:
        location = "New York"
    
    print()
    reviews = fetcher.fetch_business_reviews(restaurant, location)
    
    print(f"\n📊 Found {len(reviews)} reviews:\n")
    for i, review in enumerate(reviews[:5], 1):
        print(f"{i}. {'⭐' * review['rating']} ({review['rating']}/5)")
        print(f"   {review['text'][:100]}...")
        print(f"   - {review['author']} ({review['time']})\n")
