"""
Platform API Integrations
Google Places, Yelp Fusion, Meta Graph API connectors
"""

import requests
from typing import List, Dict, Optional
from datetime import datetime
import os

class GooglePlacesAPI:
    """Google Places API integration for fetching reviews"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GOOGLE_PLACES_API_KEY")
        self.base_url = "https://maps.googleapis.com/maps/api/place"
    
    def search_place(self, query: str) -> Optional[str]:
        """Search for a place and get place_id"""
        if not self.api_key:
            return None
        
        url = f"{self.base_url}/findplacefromtext/json"
        params = {
            "input": query,
            "inputtype": "textquery",
            "fields": "place_id,name",
            "key": self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if data.get("candidates"):
                return data["candidates"][0]["place_id"]
        except Exception as e:
            print(f"Google Places search error: {e}")
        
        return None
    
    def get_reviews(self, place_id: str) -> List[Dict]:
        """Fetch reviews for a place"""
        if not self.api_key:
            return []
        
        url = f"{self.base_url}/details/json"
        params = {
            "place_id": place_id,
            "fields": "name,reviews,rating",
            "key": self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if data.get("result") and data["result"].get("reviews"):
                reviews = []
                for review in data["result"]["reviews"]:
                    reviews.append({
                        "platform": "google",
                        "platform_review_id": f"google_{review.get('time')}_{review.get('author_name', '').replace(' ', '_')}",
                        "author": review.get("author_name"),
                        "rating": review.get("rating"),
                        "text": review.get("text"),
                        "review_date": datetime.fromtimestamp(review.get("time", 0))
                    })
                return reviews
        except Exception as e:
            print(f"Google Places reviews error: {e}")
        
        return []


class YelpFusionAPI:
    """Yelp Fusion API integration"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("YELP_API_KEY")
        self.base_url = "https://api.yelp.com/v3"
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
    
    def search_business(self, name: str, location: str) -> Optional[str]:
        """Search for a business and get business_id"""
        if not self.api_key:
            return None
        
        url = f"{self.base_url}/businesses/search"
        params = {
            "term": name,
            "location": location,
            "limit": 1
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            data = response.json()
            
            if data.get("businesses"):
                return data["businesses"][0]["id"]
        except Exception as e:
            print(f"Yelp search error: {e}")
        
        return None
    
    def get_reviews(self, business_id: str) -> List[Dict]:
        """Fetch reviews for a business"""
        if not self.api_key:
            return []
        
        url = f"{self.base_url}/businesses/{business_id}/reviews"
        
        try:
            response = requests.get(url, headers=self.headers)
            data = response.json()
            
            if data.get("reviews"):
                reviews = []
                for review in data["reviews"]:
                    reviews.append({
                        "platform": "yelp",
                        "platform_review_id": f"yelp_{review.get('id')}",
                        "author": review.get("user", {}).get("name"),
                        "rating": review.get("rating"),
                        "text": review.get("text"),
                        "review_date": datetime.fromisoformat(review.get("time_created", "").replace("Z", "+00:00"))
                    })
                return reviews
        except Exception as e:
            print(f"Yelp reviews error: {e}")
        
        return []


class MetaGraphAPI:
    """Meta (Facebook) Graph API integration"""
    
    def __init__(self, access_token: str = None):
        self.access_token = access_token or os.getenv("META_ACCESS_TOKEN")
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def get_page_reviews(self, page_id: str) -> List[Dict]:
        """Fetch reviews/ratings for a Facebook page"""
        if not self.access_token:
            return []
        
        url = f"{self.base_url}/{page_id}/ratings"
        params = {
            "access_token": self.access_token,
            "fields": "reviewer,rating,review_text,created_time"
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if data.get("data"):
                reviews = []
                for review in data["data"]:
                    reviews.append({
                        "platform": "meta",
                        "platform_review_id": f"meta_{review.get('id')}",
                        "author": review.get("reviewer", {}).get("name"),
                        "rating": review.get("rating"),
                        "text": review.get("review_text", ""),
                        "review_date": datetime.fromisoformat(review.get("created_time", "").replace("Z", "+00:00"))
                    })
                return reviews
        except Exception as e:
            print(f"Meta reviews error: {e}")
        
        return []


class TripAdvisorAPI:
    """TripAdvisor API integration (requires partnership)"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("TRIPADVISOR_API_KEY")
        self.base_url = "https://api.tripadvisor.com/api/partner/2.0"
    
    def get_reviews(self, location_id: str) -> List[Dict]:
        """Fetch reviews for a location"""
        if not self.api_key:
            return []
        
        url = f"{self.base_url}/location/{location_id}/reviews"
        headers = {"Accept": "application/json"}
        params = {"key": self.api_key}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            if data.get("data"):
                reviews = []
                for review in data["data"]:
                    reviews.append({
                        "platform": "tripadvisor",
                        "platform_review_id": f"tripadvisor_{review.get('id')}",
                        "author": review.get("user", {}).get("username"),
                        "rating": review.get("rating"),
                        "text": review.get("text"),
                        "review_date": datetime.fromisoformat(review.get("published_date", ""))
                    })
                return reviews
        except Exception as e:
            print(f"TripAdvisor reviews error: {e}")
        
        return []


class PlatformAggregator:
    """Aggregates reviews from all platforms"""
    
    def __init__(self):
        self.google = GooglePlacesAPI()
        self.yelp = YelpFusionAPI()
        self.meta = MetaGraphAPI()
        self.tripadvisor = TripAdvisorAPI()
    
    def fetch_all_reviews(self, business_name: str, location: str = None,
                         google_place_id: str = None,
                         yelp_business_id: str = None,
                         meta_page_id: str = None,
                         tripadvisor_location_id: str = None) -> Dict[str, List[Dict]]:
        """Fetch reviews from all configured platforms"""
        
        all_reviews = {
            "google": [],
            "yelp": [],
            "meta": [],
            "tripadvisor": []
        }
        
        # Google Places
        if google_place_id or business_name:
            place_id = google_place_id or self.google.search_place(business_name)
            if place_id:
                all_reviews["google"] = self.google.get_reviews(place_id)
        
        # Yelp
        if yelp_business_id or (business_name and location):
            business_id = yelp_business_id or self.yelp.search_business(business_name, location)
            if business_id:
                all_reviews["yelp"] = self.yelp.get_reviews(business_id)
        
        # Meta
        if meta_page_id:
            all_reviews["meta"] = self.meta.get_page_reviews(meta_page_id)
        
        # TripAdvisor
        if tripadvisor_location_id:
            all_reviews["tripadvisor"] = self.tripadvisor.get_reviews(tripadvisor_location_id)
        
        return all_reviews
    
    def get_total_count(self, reviews_dict: Dict[str, List[Dict]]) -> int:
        """Get total review count across all platforms"""
        return sum(len(reviews) for reviews in reviews_dict.values())


# Demo function for testing without API keys
def get_demo_reviews() -> List[Dict]:
    """Get demo reviews for testing without API keys"""
    return [
        {
            "platform": "google",
            "platform_review_id": "demo_google_1",
            "author": "John Doe",
            "rating": 5.0,
            "text": "Amazing coffee and excellent service! The barista was very friendly.",
            "review_date": datetime.now()
        },
        {
            "platform": "yelp",
            "platform_review_id": "demo_yelp_1",
            "author": "Jane Smith",
            "rating": 2.0,
            "text": "Service was slow and the food arrived cold. Very disappointed.",
            "review_date": datetime.now()
        },
        {
            "platform": "google",
            "platform_review_id": "demo_google_2",
            "author": "Mike Johnson",
            "rating": 4.0,
            "text": "Good atmosphere and decent prices. Will come back again.",
            "review_date": datetime.now()
        },
        {
            "platform": "tripadvisor",
            "platform_review_id": "demo_trip_1",
            "author": "Sarah Williams",
            "rating": 1.0,
            "text": "Terrible experience. Waited 45 minutes for our order and it was wrong.",
            "review_date": datetime.now()
        },
        {
            "platform": "meta",
            "platform_review_id": "demo_meta_1",
            "author": "David Brown",
            "rating": 5.0,
            "text": "Best restaurant in town! The pasta was incredible and staff was attentive.",
            "review_date": datetime.now()
        }
    ]
