"""
RAG System for RevuIQ - Free & Open Source
Uses Sentence Transformers + ChromaDB for semantic search and retrieval
"""

import os
from typing import List, Dict, Optional
from datetime import datetime

try:
    from sentence_transformers import SentenceTransformer
    import chromadb
    from chromadb.config import Settings
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    print("⚠️  RAG dependencies not installed. Run: pip install sentence-transformers chromadb")


class ReviewRAG:
    """
    Retrieval-Augmented Generation system for reviews
    - Stores reviews with embeddings
    - Semantic search for similar reviews
    - Context-aware response generation
    """
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize RAG system with local vector database"""
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("Please install: pip install sentence-transformers chromadb")
        
        # Initialize embedding model (free, runs locally)
        print("🔄 Loading embedding model...")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')  # Fast & lightweight
        print("✅ Embedding model loaded!")
        
        # Initialize ChromaDB (free, local vector database)
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="reviews",
            metadata={"description": "Restaurant reviews with embeddings"}
        )
        
        print(f"✅ RAG system initialized! ({self.collection.count()} reviews in database)")
    
    def add_review(self, review_text: str, metadata: Dict) -> str:
        """
        Add a review to the vector database
        
        Args:
            review_text: The review text
            metadata: Additional info (rating, sentiment, business, etc.)
        
        Returns:
            Review ID
        """
        # Generate unique ID
        review_id = f"review_{datetime.now().timestamp()}"
        
        # Generate embedding
        embedding = self.embedder.encode(review_text).tolist()
        
        # Store in ChromaDB
        self.collection.add(
            embeddings=[embedding],
            documents=[review_text],
            metadatas=[metadata],
            ids=[review_id]
        )
        
        return review_id
    
    def add_reviews_batch(self, reviews: List[Dict]) -> List[str]:
        """
        Add multiple reviews at once (faster)
        
        Args:
            reviews: List of dicts with 'text' and 'metadata'
        
        Returns:
            List of review IDs
        """
        texts = [r['text'] for r in reviews]
        metadatas = [r['metadata'] for r in reviews]
        
        # Generate embeddings in batch (much faster)
        embeddings = self.embedder.encode(texts).tolist()
        
        # Generate IDs
        ids = [f"review_{datetime.now().timestamp()}_{i}" for i in range(len(reviews))]
        
        # Store in ChromaDB
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        return ids
    
    def find_similar_reviews(self, query: str, n_results: int = 5, 
                            sentiment_filter: Optional[str] = None) -> List[Dict]:
        """
        Find reviews similar to the query using semantic search
        
        Args:
            query: Search query or review text
            n_results: Number of results to return
            sentiment_filter: Filter by sentiment (POSITIVE, NEGATIVE, NEUTRAL)
        
        Returns:
            List of similar reviews with metadata
        """
        # Generate query embedding
        query_embedding = self.embedder.encode(query).tolist()
        
        # Build filter
        where = {}
        if sentiment_filter:
            where["sentiment"] = sentiment_filter
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where if where else None
        )
        
        # Format results
        similar_reviews = []
        for i in range(len(results['documents'][0])):
            similar_reviews.append({
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'similarity': 1 - results['distances'][0][i],  # Convert distance to similarity
                'id': results['ids'][0][i]
            })
        
        return similar_reviews
    
    def generate_response(self, review_text: str, sentiment: str, 
                         business_name: str = "our business") -> str:
        """
        Generate AI response using RAG
        - Finds similar reviews
        - Uses them as context
        - Generates appropriate response
        
        Args:
            review_text: The review to respond to
            sentiment: Review sentiment (POSITIVE, NEGATIVE, NEUTRAL)
            business_name: Name of the business
        
        Returns:
            Generated response
        """
        # Find similar reviews with same sentiment
        similar = self.find_similar_reviews(
            review_text, 
            n_results=3,
            sentiment_filter=sentiment
        )
        
        # Extract common themes from similar reviews
        themes = self._extract_themes(similar)
        
        # Generate contextual response
        response = self._build_response(review_text, sentiment, themes, business_name)
        
        return response
    
    def _extract_themes(self, similar_reviews: List[Dict]) -> List[str]:
        """Extract common themes from similar reviews"""
        themes = []
        
        # Common keywords for different aspects
        aspect_keywords = {
            'food': ['food', 'dish', 'meal', 'taste', 'flavor', 'delicious'],
            'service': ['service', 'staff', 'waiter', 'server', 'friendly', 'helpful'],
            'atmosphere': ['atmosphere', 'ambiance', 'decor', 'vibe', 'environment'],
            'price': ['price', 'expensive', 'cheap', 'value', 'cost', 'worth'],
            'cleanliness': ['clean', 'dirty', 'hygiene', 'sanitary'],
            'speed': ['fast', 'slow', 'quick', 'wait', 'time']
        }
        
        # Count mentions across similar reviews
        for aspect, keywords in aspect_keywords.items():
            count = 0
            for review in similar_reviews:
                text_lower = review['text'].lower()
                if any(keyword in text_lower for keyword in keywords):
                    count += 1
            
            if count >= 2:  # If mentioned in 2+ similar reviews
                themes.append(aspect)
        
        return themes
    
    def _build_response(self, review_text: str, sentiment: str, 
                       themes: List[str], business_name: str) -> str:
        """Build contextual response based on sentiment and themes"""
        
        if sentiment == "POSITIVE":
            responses = {
                'food': f"We're thrilled you enjoyed our food! Our chefs work hard to deliver quality dishes.",
                'service': f"Thank you for recognizing our team's efforts! We'll share your kind words with our staff.",
                'atmosphere': f"We're so glad you appreciated the atmosphere! We strive to create a welcoming environment.",
                'default': f"Thank you so much for your wonderful review! We're delighted you had a great experience at {business_name}."
            }
            
            if themes:
                return responses.get(themes[0], responses['default'])
            return responses['default']
        
        elif sentiment == "NEGATIVE":
            responses = {
                'food': f"We sincerely apologize for the disappointing food quality. This doesn't meet our standards, and we're addressing this with our kitchen team immediately.",
                'service': f"We're truly sorry about the poor service you experienced. This is unacceptable, and we're taking immediate steps to improve our team's performance.",
                'cleanliness': f"We apologize for the cleanliness issues. This is a top priority for us, and we're addressing this immediately with our staff.",
                'speed': f"We're sorry for the long wait time. We're working on improving our efficiency to serve you better.",
                'default': f"We sincerely apologize for your negative experience at {business_name}. Your feedback is invaluable, and we're committed to making improvements. Please contact us directly so we can make this right."
            }
            
            if themes:
                return responses.get(themes[0], responses['default'])
            return responses['default']
        
        else:  # NEUTRAL
            return f"Thank you for your feedback about {business_name}. We appreciate you taking the time to share your experience. We're always working to improve, and your input helps us do that."
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        total = self.collection.count()
        
        # Get sentiment distribution
        try:
            all_reviews = self.collection.get()
            sentiments = [m.get('sentiment', 'UNKNOWN') for m in all_reviews['metadatas']]
            
            return {
                'total_reviews': total,
                'positive': sentiments.count('POSITIVE'),
                'negative': sentiments.count('NEGATIVE'),
                'neutral': sentiments.count('NEUTRAL')
            }
        except:
            return {'total_reviews': total}
    
    def clear_database(self):
        """Clear all reviews from database"""
        self.client.delete_collection("reviews")
        self.collection = self.client.get_or_create_collection(
            name="reviews",
            metadata={"description": "Restaurant reviews with embeddings"}
        )
        print("✅ Database cleared!")


# Demo usage
if __name__ == "__main__":
    print("\n" + "="*70)
    print("🤖 RAG System Demo - Free & Open Source")
    print("="*70 + "\n")
    
    # Initialize RAG
    rag = ReviewRAG()
    
    # Add sample reviews
    print("📝 Adding sample reviews...")
    sample_reviews = [
        {
            'text': "Amazing food! The pasta was perfectly cooked and the service was excellent.",
            'metadata': {'sentiment': 'POSITIVE', 'rating': 5, 'business': 'Demo Restaurant'}
        },
        {
            'text': "Great atmosphere and friendly staff. Will definitely come back!",
            'metadata': {'sentiment': 'POSITIVE', 'rating': 5, 'business': 'Demo Restaurant'}
        },
        {
            'text': "Terrible experience. Food was cold and service was slow.",
            'metadata': {'sentiment': 'NEGATIVE', 'rating': 1, 'business': 'Demo Restaurant'}
        },
        {
            'text': "The food was okay but nothing special. Service was average.",
            'metadata': {'sentiment': 'NEUTRAL', 'rating': 3, 'business': 'Demo Restaurant'}
        }
    ]
    
    rag.add_reviews_batch(sample_reviews)
    print(f"✅ Added {len(sample_reviews)} reviews\n")
    
    # Test semantic search
    print("🔍 Testing semantic search...")
    query = "delicious meal with great service"
    similar = rag.find_similar_reviews(query, n_results=3)
    
    print(f"\nQuery: '{query}'")
    print("\nSimilar reviews:")
    for i, review in enumerate(similar, 1):
        print(f"\n{i}. Similarity: {review['similarity']:.2f}")
        print(f"   Text: {review['text'][:80]}...")
        print(f"   Sentiment: {review['metadata']['sentiment']}")
    
    # Test response generation
    print("\n" + "="*70)
    print("💬 Testing RAG-based response generation...")
    print("="*70 + "\n")
    
    test_review = "The food was amazing and the staff was so friendly!"
    response = rag.generate_response(test_review, "POSITIVE", "Demo Restaurant")
    
    print(f"Review: {test_review}")
    print(f"\nRAG Response: {response}")
    
    # Show stats
    print("\n" + "="*70)
    stats = rag.get_stats()
    print(f"📊 Database Stats: {stats}")
    print("="*70)
