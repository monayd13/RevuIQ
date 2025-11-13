"""
Aspect Extraction Module
Identifies what customers are talking about (service, food, price, etc.)
"""

import re
from typing import List, Dict, Set
from collections import Counter

class AspectExtractor:
    """Extract aspects/topics from review text"""
    
    def __init__(self):
        # Define aspect keywords for different categories
        self.aspect_keywords = {
            "food": [
                "food", "meal", "dish", "cuisine", "taste", "flavor", "delicious",
                "tasty", "bland", "spicy", "fresh", "stale", "quality", "portion",
                "menu", "breakfast", "lunch", "dinner", "appetizer", "dessert",
                "pizza", "pasta", "burger", "salad", "soup", "sandwich", "steak"
            ],
            "service": [
                "service", "staff", "waiter", "waitress", "server", "bartender",
                "manager", "employee", "friendly", "rude", "attentive", "slow",
                "fast", "helpful", "professional", "courteous", "polite"
            ],
            "price": [
                "price", "cost", "expensive", "cheap", "affordable", "value",
                "money", "worth", "overpriced", "reasonable", "budget", "deal",
                "pricing", "charge", "bill", "payment"
            ],
            "ambiance": [
                "atmosphere", "ambiance", "ambience", "decor", "decoration",
                "interior", "design", "music", "lighting", "seating", "comfortable",
                "cozy", "clean", "dirty", "noisy", "quiet", "crowded", "spacious"
            ],
            "location": [
                "location", "parking", "access", "convenient", "downtown",
                "neighborhood", "area", "nearby", "close", "far", "distance"
            ],
            "wait_time": [
                "wait", "waiting", "waited", "queue", "line", "reservation",
                "booking", "time", "minutes", "hours", "delay", "quick", "prompt"
            ],
            "cleanliness": [
                "clean", "dirty", "hygiene", "sanitary", "spotless", "filthy",
                "tidy", "messy", "bathroom", "restroom", "table", "floor"
            ],
            "drinks": [
                "drink", "beverage", "coffee", "tea", "wine", "beer", "cocktail",
                "juice", "soda", "water", "latte", "cappuccino", "espresso"
            ],
            "staff_behavior": [
                "attitude", "behavior", "manner", "greeting", "smile", "welcome",
                "respect", "disrespect", "ignore", "attention"
            ],
            "quality": [
                "quality", "standard", "excellence", "mediocre", "poor",
                "outstanding", "exceptional", "average", "subpar"
            ]
        }
        
        # Compile patterns for efficiency
        self.aspect_patterns = {}
        for aspect, keywords in self.aspect_keywords.items():
            pattern = r'\b(' + '|'.join(keywords) + r')\b'
            self.aspect_patterns[aspect] = re.compile(pattern, re.IGNORECASE)
    
    def extract(self, text: str) -> Dict:
        """
        Extract aspects from review text
        
        Returns:
            Dict with aspects, confidence, and details
        """
        text_lower = text.lower()
        
        # Find all aspects mentioned
        detected_aspects = {}
        aspect_mentions = []
        
        for aspect, pattern in self.aspect_patterns.items():
            matches = pattern.findall(text_lower)
            if matches:
                detected_aspects[aspect] = len(matches)
                aspect_mentions.extend([(aspect, match) for match in matches])
        
        # Sort by frequency
        sorted_aspects = sorted(
            detected_aspects.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Get primary aspect (most mentioned)
        primary_aspect = sorted_aspects[0][0] if sorted_aspects else "general"
        
        # Calculate confidence based on keyword density
        total_words = len(text.split())
        total_aspect_words = sum(detected_aspects.values())
        confidence = min(total_aspect_words / max(total_words, 1), 1.0)
        
        return {
            "primary_aspect": primary_aspect,
            "all_aspects": [aspect for aspect, _ in sorted_aspects],
            "aspect_counts": dict(sorted_aspects),
            "confidence": confidence,
            "total_mentions": total_aspect_words,
            "aspect_details": aspect_mentions[:10]  # Top 10 mentions
        }
    
    def extract_simple(self, text: str) -> List[str]:
        """Simple extraction returning just aspect names"""
        result = self.extract(text)
        return result["all_aspects"]
    
    def get_aspect_sentiment(self, text: str, aspect: str) -> str:
        """
        Get sentiment for a specific aspect
        (Simple version - looks for positive/negative words near aspect)
        """
        text_lower = text.lower()
        
        # Positive and negative indicators
        positive_words = [
            "good", "great", "excellent", "amazing", "wonderful", "fantastic",
            "love", "best", "perfect", "delicious", "friendly", "clean"
        ]
        negative_words = [
            "bad", "terrible", "awful", "horrible", "worst", "hate", "poor",
            "disappointing", "slow", "rude", "dirty", "cold"
        ]
        
        # Find aspect keywords
        aspect_keywords = self.aspect_keywords.get(aspect, [])
        
        # Look for sentiment words near aspect keywords
        positive_score = 0
        negative_score = 0
        
        for keyword in aspect_keywords:
            if keyword in text_lower:
                # Get context around keyword (50 chars before and after)
                idx = text_lower.find(keyword)
                context = text_lower[max(0, idx-50):min(len(text_lower), idx+50)]
                
                # Count sentiment words in context
                for pos_word in positive_words:
                    if pos_word in context:
                        positive_score += 1
                
                for neg_word in negative_words:
                    if neg_word in context:
                        negative_score += 1
        
        # Determine sentiment
        if positive_score > negative_score:
            return "POSITIVE"
        elif negative_score > positive_score:
            return "NEGATIVE"
        else:
            return "NEUTRAL"
    
    def get_detailed_analysis(self, text: str) -> Dict:
        """
        Get detailed aspect analysis with sentiment for each aspect
        """
        aspects = self.extract(text)
        
        detailed = {
            "primary_aspect": aspects["primary_aspect"],
            "aspects_with_sentiment": {}
        }
        
        for aspect in aspects["all_aspects"]:
            sentiment = self.get_aspect_sentiment(text, aspect)
            detailed["aspects_with_sentiment"][aspect] = {
                "sentiment": sentiment,
                "mentions": aspects["aspect_counts"][aspect]
            }
        
        return detailed


# Example usage and testing
if __name__ == "__main__":
    extractor = AspectExtractor()
    
    # Test reviews
    test_reviews = [
        "The food was amazing but the service was terrible and slow.",
        "Great atmosphere and reasonable prices. The staff was very friendly.",
        "Coffee was cold and the place was dirty. Not coming back.",
        "Excellent pasta and wine selection. A bit pricey but worth it."
    ]
    
    print("🔍 Aspect Extraction Test\n")
    
    for i, review in enumerate(test_reviews, 1):
        print(f"Review {i}: {review}")
        
        # Simple extraction
        aspects = extractor.extract_simple(review)
        print(f"  Aspects: {', '.join(aspects)}")
        
        # Detailed analysis
        detailed = extractor.get_detailed_analysis(review)
        print(f"  Primary: {detailed['primary_aspect']}")
        print(f"  Details: {detailed['aspects_with_sentiment']}")
        print()
