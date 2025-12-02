"""
Advanced NLP Engine for RevuIQ
Uses state-of-the-art deep learning models for review analysis
"""

import torch
import torch.nn as nn
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    AutoModelForTokenClassification,
    T5ForConditionalGeneration,
    pipeline,
    BertModel,
    RobertaForSequenceClassification
)
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Tuple
import asyncio
from functools import lru_cache

class AdvancedNLPEngine:
    """
    Multi-model NLP engine using:
    - RoBERTa for sentiment analysis
    - BERT for emotion detection
    - T5 for response generation
    - Sentence-BERT for semantic similarity
    - Custom aspect extraction model
    """
    
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"🚀 Initializing NLP Engine on {self.device}")
        
        # Load models
        self._load_sentiment_model()
        self._load_emotion_model()
        self._load_response_generator()
        self._load_embedding_model()
        self._load_aspect_extractor()
        
    def _load_sentiment_model(self):
        """Load RoBERTa fine-tuned for sentiment analysis"""
        print("📊 Loading Sentiment Analysis Model (RoBERTa)...")
        model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
        self.sentiment_tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.sentiment_model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.sentiment_model.to(self.device)
        self.sentiment_model.eval()
        
    def _load_emotion_model(self):
        """Load GoEmotions model for multi-label emotion detection"""
        print("😊 Loading Emotion Detection Model (GoEmotions)...")
        model_name = "SamLowe/roberta-base-go_emotions"
        self.emotion_tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.emotion_model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.emotion_model.to(self.device)
        self.emotion_model.eval()
        
        # GoEmotions labels
        self.emotion_labels = [
            'admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring',
            'confusion', 'curiosity', 'desire', 'disappointment', 'disapproval',
            'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude', 'grief',
            'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization',
            'relief', 'remorse', 'sadness', 'surprise', 'neutral'
        ]
        
    def _load_response_generator(self):
        """Load T5 model for response generation"""
        print("✍️ Loading Response Generator (T5)...")
        model_name = "google/flan-t5-base"
        self.response_tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.response_model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.response_model.to(self.device)
        self.response_model.eval()
        
    def _load_embedding_model(self):
        """Load Sentence-BERT for semantic embeddings"""
        print("🔤 Loading Embedding Model (Sentence-BERT)...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def _load_aspect_extractor(self):
        """Load NER model for aspect extraction"""
        print("🎯 Loading Aspect Extraction Model (NER)...")
        self.aspect_pipeline = pipeline(
            "ner",
            model="dslim/bert-base-NER",
            aggregation_strategy="simple",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Custom aspect categories for restaurants
        self.aspect_keywords = {
            'food_quality': ['food', 'dish', 'meal', 'taste', 'flavor', 'delicious', 'fresh', 'quality'],
            'service': ['service', 'staff', 'waiter', 'server', 'waitress', 'manager', 'host'],
            'ambiance': ['atmosphere', 'ambiance', 'decor', 'music', 'lighting', 'vibe', 'environment'],
            'price': ['price', 'cost', 'expensive', 'cheap', 'value', 'worth', 'affordable'],
            'wait_time': ['wait', 'waiting', 'slow', 'fast', 'quick', 'time', 'delay'],
            'cleanliness': ['clean', 'dirty', 'hygiene', 'sanitary', 'spotless', 'messy'],
            'portion_size': ['portion', 'size', 'amount', 'quantity', 'serving', 'big', 'small'],
            'location': ['location', 'parking', 'access', 'convenient', 'area']
        }
    
    @torch.no_grad()
    async def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment using RoBERTa
        Returns: {'positive': 0.8, 'neutral': 0.15, 'negative': 0.05}
        """
        inputs = self.sentiment_tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.device)
        
        outputs = self.sentiment_model(**inputs)
        scores = torch.nn.functional.softmax(outputs.logits, dim=-1)
        scores = scores.cpu().numpy()[0]
        
        return {
            'negative': float(scores[0]),
            'neutral': float(scores[1]),
            'positive': float(scores[2])
        }
    
    @torch.no_grad()
    async def detect_emotions(self, text: str, top_k: int = 5) -> List[Dict[str, float]]:
        """
        Detect emotions using GoEmotions model
        Returns: [{'emotion': 'joy', 'score': 0.95}, ...]
        """
        inputs = self.emotion_tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.device)
        
        outputs = self.emotion_model(**inputs)
        scores = torch.nn.functional.sigmoid(outputs.logits)
        scores = scores.cpu().numpy()[0]
        
        # Get top-k emotions
        top_indices = np.argsort(scores)[-top_k:][::-1]
        
        emotions = []
        for idx in top_indices:
            if scores[idx] > 0.3:  # Threshold
                emotions.append({
                    'emotion': self.emotion_labels[idx],
                    'score': float(scores[idx])
                })
        
        return emotions
    
    async def extract_aspects(self, text: str) -> List[Dict[str, any]]:
        """
        Extract aspects mentioned in review
        Returns: [{'aspect': 'food_quality', 'mentions': ['pasta', 'pizza'], 'sentiment': 'positive'}, ...]
        """
        text_lower = text.lower()
        aspects_found = []
        
        for aspect, keywords in self.aspect_keywords.items():
            mentions = []
            for keyword in keywords:
                if keyword in text_lower:
                    mentions.append(keyword)
            
            if mentions:
                # Analyze sentiment for this aspect
                aspect_sentiment = await self._analyze_aspect_sentiment(text, mentions)
                aspects_found.append({
                    'aspect': aspect,
                    'mentions': mentions,
                    'sentiment': aspect_sentiment
                })
        
        return aspects_found
    
    async def _analyze_aspect_sentiment(self, text: str, keywords: List[str]) -> str:
        """Analyze sentiment for specific aspect"""
        # Simple context-based sentiment
        text_lower = text.lower()
        positive_words = ['good', 'great', 'excellent', 'amazing', 'perfect', 'love', 'best']
        negative_words = ['bad', 'terrible', 'awful', 'worst', 'hate', 'poor', 'disappointing']
        
        score = 0
        for keyword in keywords:
            idx = text_lower.find(keyword)
            if idx != -1:
                # Check surrounding words
                context = text_lower[max(0, idx-50):min(len(text_lower), idx+50)]
                for word in positive_words:
                    if word in context:
                        score += 1
                for word in negative_words:
                    if word in context:
                        score -= 1
        
        if score > 0:
            return 'positive'
        elif score < 0:
            return 'negative'
        else:
            return 'neutral'
    
    @torch.no_grad()
    async def generate_response(
        self,
        review_text: str,
        sentiment: str,
        emotions: List[str],
        aspects: List[str],
        business_name: str = "our restaurant"
    ) -> str:
        """
        Generate contextual response using T5
        """
        # Create prompt for T5
        emotion_str = ", ".join(emotions[:3]) if emotions else "neutral"
        aspect_str = ", ".join(aspects[:3]) if aspects else "overall experience"
        
        prompt = f"""Generate a professional restaurant response to this review.
Review: {review_text}
Sentiment: {sentiment}
Emotions detected: {emotion_str}
Topics mentioned: {aspect_str}
Business: {business_name}

Response:"""
        
        inputs = self.response_tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.device)
        
        outputs = self.response_model.generate(
            **inputs,
            max_length=150,
            num_beams=5,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
        
        response = self.response_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Post-process response
        response = self._enhance_response(response, sentiment, emotions)
        
        return response
    
    def _enhance_response(self, response: str, sentiment: str, emotions: List[str]) -> str:
        """Add personalization and emojis based on sentiment"""
        if sentiment == 'positive':
            if 'joy' in emotions or 'excitement' in emotions:
                response += " 🌟"
            elif 'gratitude' in emotions:
                response += " 🙏"
            else:
                response += " ⭐"
        elif sentiment == 'negative':
            if not response.startswith("We"):
                response = "We sincerely apologize. " + response
        
        return response
    
    async def get_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts
        Useful for finding similar reviews or responses
        """
        embeddings = self.embedding_model.encode([text1, text2])
        similarity = np.dot(embeddings[0], embeddings[1]) / (
            np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
        )
        return float(similarity)
    
    async def analyze_review_complete(self, review_text: str, business_name: str = "our restaurant") -> Dict:
        """
        Complete analysis pipeline
        Returns all insights in one call
        """
        # Run all analyses in parallel
        sentiment_task = self.analyze_sentiment(review_text)
        emotion_task = self.detect_emotions(review_text)
        aspect_task = self.extract_aspects(review_text)
        
        sentiment, emotions, aspects = await asyncio.gather(
            sentiment_task,
            emotion_task,
            aspect_task
        )
        
        # Determine overall sentiment
        overall_sentiment = max(sentiment, key=sentiment.get)
        
        # Generate response
        emotion_names = [e['emotion'] for e in emotions]
        aspect_names = [a['aspect'] for a in aspects]
        
        response = await self.generate_response(
            review_text,
            overall_sentiment,
            emotion_names,
            aspect_names,
            business_name
        )
        
        return {
            'sentiment': sentiment,
            'overall_sentiment': overall_sentiment,
            'emotions': emotions,
            'aspects': aspects,
            'suggested_response': response,
            'confidence': float(sentiment[overall_sentiment])
        }


class DeepLearningInsights:
    """
    Advanced deep learning features for insights
    """
    
    def __init__(self, nlp_engine: AdvancedNLPEngine):
        self.nlp = nlp_engine
        
    async def predict_review_trend(self, historical_reviews: List[Dict]) -> Dict:
        """
        Predict future review trends using time series analysis
        """
        # Extract sentiment scores over time
        sentiments = []
        for review in historical_reviews:
            sentiment = await self.nlp.analyze_sentiment(review['text'])
            sentiments.append({
                'date': review['date'],
                'positive': sentiment['positive'],
                'negative': sentiment['negative']
            })
        
        # Simple trend analysis (can be enhanced with Prophet or LSTM)
        recent = sentiments[-30:]  # Last 30 reviews
        avg_positive = np.mean([s['positive'] for s in recent])
        avg_negative = np.mean([s['negative'] for s in recent])
        
        # Predict next week
        trend = "improving" if avg_positive > 0.6 else "declining" if avg_negative > 0.4 else "stable"
        
        return {
            'trend': trend,
            'predicted_positive_rate': avg_positive,
            'predicted_negative_rate': avg_negative,
            'confidence': 0.85,
            'recommendation': self._get_recommendation(trend, avg_negative)
        }
    
    def _get_recommendation(self, trend: str, negative_rate: float) -> str:
        """Generate actionable recommendation"""
        if trend == "declining" and negative_rate > 0.4:
            return "⚠️ Alert: Negative reviews increasing. Immediate action needed on service quality."
        elif trend == "improving":
            return "✅ Great! Keep up the good work. Consider requesting more reviews."
        else:
            return "📊 Stable performance. Monitor for changes."
    
    async def cluster_reviews(self, reviews: List[str]) -> Dict:
        """
        Cluster similar reviews using embeddings
        Useful for finding common themes
        """
        # Get embeddings for all reviews
        embeddings = self.nlp.embedding_model.encode(reviews)
        
        # Simple clustering (can use KMeans for better results)
        from sklearn.cluster import KMeans
        
        n_clusters = min(5, len(reviews) // 10 + 1)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(embeddings)
        
        # Group reviews by cluster
        clustered = {}
        for idx, cluster_id in enumerate(clusters):
            if cluster_id not in clustered:
                clustered[cluster_id] = []
            clustered[cluster_id].append(reviews[idx])
        
        return {
            'clusters': clustered,
            'n_clusters': n_clusters,
            'themes': await self._extract_cluster_themes(clustered)
        }
    
    async def _extract_cluster_themes(self, clusters: Dict) -> Dict:
        """Extract main theme from each cluster"""
        themes = {}
        for cluster_id, reviews in clusters.items():
            # Analyze most common aspects
            all_aspects = []
            for review in reviews[:5]:  # Sample
                aspects = await self.nlp.extract_aspects(review)
                all_aspects.extend([a['aspect'] for a in aspects])
            
            if all_aspects:
                from collections import Counter
                most_common = Counter(all_aspects).most_common(1)[0][0]
                themes[cluster_id] = most_common
            else:
                themes[cluster_id] = "general"
        
        return themes


# Example usage
if __name__ == "__main__":
    async def main():
        # Initialize engine
        engine = AdvancedNLPEngine()
        
        # Test review
        review = "The pasta was absolutely delicious! Service was a bit slow but the staff was very friendly. Great atmosphere and reasonable prices."
        
        # Complete analysis
        result = await engine.analyze_review_complete(review, "Bella Italia")
        
        print("\n📊 Analysis Results:")
        print(f"Sentiment: {result['overall_sentiment']} ({result['confidence']:.2%})")
        print(f"Emotions: {[e['emotion'] for e in result['emotions']]}")
        print(f"Aspects: {[a['aspect'] for a in result['aspects']]}")
        print(f"\n✍️ Suggested Response:\n{result['suggested_response']}")
    
    asyncio.run(main())
