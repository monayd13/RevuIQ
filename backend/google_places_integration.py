"""
Google Places API Integration
Fetch real restaurant reviews from Google Places
"""

import requests
import os
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY", "")

class GooglePlacesAPI:
    """Google Places API client for fetching restaurant reviews"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or GOOGLE_API_KEY
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        
    def search_restaurant(self, name: str, location: str = "") -> Optional[str]:
        """
        Search for a restaurant and get its place_id
        
        Args:
            name: Restaurant name
            location: Optional location (city, address)
            
        Returns:
            place_id if found, None otherwise
        """
        if not self.api_key:
            print("⚠️  No Google API key found. Set GOOGLE_PLACES_API_KEY in .env")
            return None
        
        # Build search query
        query = name
        if location:
            query += f" {location}"
        
        # Text search endpoint
        url = f"{self.base_url}/textsearch/json"
        params = {
            "query": query,
            "type": "restaurant",
            "key": self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "OK" and data.get("results"):
                place_id = data["results"][0]["place_id"]
                print(f"✓ Found restaurant: {data['results'][0].get('name')} (ID: {place_id})")
                return place_id
            else:
                print(f"❌ Restaurant not found: {data.get('status')}")
                return None
                
        except Exception as e:
            print(f"❌ Error searching restaurant: {str(e)}")
            return None
    
    def get_place_details(self, place_id: str) -> Optional[Dict]:
        """
        Get detailed information about a place including reviews
        
        Args:
            place_id: Google Place ID
            
        Returns:
            Place details with reviews
        """
        if not self.api_key:
            return None
        
        url = f"{self.base_url}/details/json"
        params = {
            "place_id": place_id,
            "fields": "name,rating,reviews,user_ratings_total,formatted_address,types",
            "key": self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "OK":
                return data.get("result")
            else:
                print(f"❌ Error getting place details: {data.get('status')}")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching place details: {str(e)}")
            return None
    
    def get_reviews(self, restaurant_name: str, location: str = "") -> List[Dict]:
        """
        Get reviews for a restaurant
        
        Args:
            restaurant_name: Name of the restaurant
            location: Optional location
            
        Returns:
            List of reviews in standardized format
        """
        # Search for restaurant
        place_id = self.search_restaurant(restaurant_name, location)
        if not place_id:
            return []
        
        # Get place details with reviews
        place_details = self.get_place_details(place_id)
        if not place_details:
            return []
        
        # Extract and format reviews
        google_reviews = place_details.get("reviews", [])
        formatted_reviews = []
        
        for review in google_reviews:
            formatted_review = {
                "platform": "google",
                "platform_review_id": f"google_{place_id}_{review.get('time', '')}",
                "author_name": review.get("author_name", "Anonymous"),
                "rating": float(review.get("rating", 0)),
                "text": review.get("text", ""),
                "review_date": datetime.fromtimestamp(review.get("time", 0)).isoformat() if review.get("time") else datetime.now().isoformat(),
                "profile_photo_url": review.get("profile_photo_url", ""),
                "relative_time": review.get("relative_time_description", "")
            }
            formatted_reviews.append(formatted_review)
        
        print(f"✓ Fetched {len(formatted_reviews)} reviews from Google")
        return formatted_reviews
    
    def get_restaurant_info(self, restaurant_name: str, location: str = "") -> Optional[Dict]:
        """
        Get basic restaurant information
        
        Args:
            restaurant_name: Name of the restaurant
            location: Optional location
            
        Returns:
            Restaurant info dict
        """
        place_id = self.search_restaurant(restaurant_name, location)
        if not place_id:
            return None
        
        place_details = self.get_place_details(place_id)
        if not place_details:
            return None
        
        return {
            "name": place_details.get("name"),
            "address": place_details.get("formatted_address"),
            "rating": place_details.get("rating"),
            "total_ratings": place_details.get("user_ratings_total"),
            "types": place_details.get("types", []),
            "place_id": place_id
        }


# Convenience functions
def fetch_google_reviews(restaurant_name: str, location: str = "", api_key: str = None) -> List[Dict]:
    """
    Fetch reviews from Google Places API
    
    Args:
        restaurant_name: Restaurant name
        location: Optional location
        api_key: Optional API key (uses env var if not provided)
        
    Returns:
        List of formatted reviews
    """
    client = GooglePlacesAPI(api_key)
    return client.get_reviews(restaurant_name, location)


def get_restaurant_details(restaurant_name: str, location: str = "", api_key: str = None) -> Optional[Dict]:
    """
    Get restaurant details from Google Places
    
    Args:
        restaurant_name: Restaurant name
        location: Optional location
        api_key: Optional API key
        
    Returns:
        Restaurant info dict
    """
    client = GooglePlacesAPI(api_key)
    return client.get_restaurant_info(restaurant_name, location)


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python google_places_integration.py <restaurant_name> [location]")
        print("Example: python google_places_integration.py 'Olive Garden' 'New York'")
        sys.exit(1)
    
    restaurant = sys.argv[1]
    location = sys.argv[2] if len(sys.argv) > 2 else ""
    
    print(f"\n🔍 Searching for: {restaurant}")
    if location:
        print(f"📍 Location: {location}")
    print("-" * 60)
    
    # Get restaurant info
    info = get_restaurant_details(restaurant, location)
    if info:
        print(f"\n📊 Restaurant Info:")
        print(f"   Name: {info['name']}")
        print(f"   Address: {info['address']}")
        print(f"   Rating: {info['rating']} ⭐")
        print(f"   Total Ratings: {info['total_ratings']}")
    
    # Get reviews
    reviews = fetch_google_reviews(restaurant, location)
    if reviews:
        print(f"\n📝 Reviews ({len(reviews)}):")
        for i, review in enumerate(reviews[:3], 1):  # Show first 3
            print(f"\n   Review {i}:")
            print(f"   Author: {review['author_name']}")
            print(f"   Rating: {review['rating']} ⭐")
            print(f"   Date: {review['relative_time']}")
            print(f"   Text: {review['text'][:100]}...")
    else:
        print("\n❌ No reviews found")
