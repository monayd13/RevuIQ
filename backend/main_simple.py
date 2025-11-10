"""
RevuIQ Backend API - Simplified Version
FastAPI server without NLP dependencies (for testing)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="RevuIQ API",
    description="AI-Powered Review Management System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== DATA MODELS ====================

class Review(BaseModel):
    """Review data model"""
    id: Optional[int] = None
    platform: str
    review_id: str
    author: str
    rating: float
    text: str
    date: datetime
    business_id: str

class ResponseRequest(BaseModel):
    """Request for AI response generation"""
    review_text: str
    sentiment: Optional[str] = None
    business_name: Optional[str] = None
    tone: Optional[str] = "professional"

# ==================== ENDPOINTS ====================

@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "online",
        "service": "RevuIQ API",
        "version": "1.0.0",
        "message": "Backend API is running!",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "analyze": "/api/analyze",
            "generate_response": "/api/generate-response"
        }
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "message": "All systems operational"
    }

@app.post("/api/analyze")
async def analyze_review(review: dict):
    """
    Analyze a single review (mock response for now)
    """
    try:
        text = review.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="Review text is required")
        
        # Mock sentiment analysis
        sentiment_result = {
            "label": "POSITIVE" if "good" in text.lower() or "great" in text.lower() else "NEUTRAL",
            "score": 0.85
        }
        
        # Mock emotion detection
        emotion_result = {
            "joy": 0.7,
            "neutral": 0.3
        }
        
        return {
            "success": True,
            "review_id": review.get("id", "unknown"),
            "sentiment": sentiment_result,
            "emotions": emotion_result,
            "timestamp": datetime.now().isoformat(),
            "note": "This is a mock response. Install NLP models for real analysis."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-response")
async def generate_response(request: ResponseRequest):
    """
    Generate AI response (mock for now)
    """
    try:
        # Mock response generation
        mock_response = f"Thank you for your feedback! We appreciate your review about our {request.business_name or 'business'}."
        
        return {
            "success": True,
            "ai_response": mock_response,
            "tone": request.tone,
            "timestamp": datetime.now().isoformat(),
            "note": "This is a mock response. Install NLP models for real AI generation."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    """Get API statistics"""
    return {
        "total_requests": 0,
        "uptime": "N/A",
        "version": "1.0.0",
        "status": "running"
    }

# ==================== RUN SERVER ====================

if __name__ == "__main__":
    print("🚀 Starting RevuIQ API Server (Simplified Version)...")
    print("📊 Visit http://localhost:8000/docs for API documentation")
    print("💡 This version uses mock responses. Install NLP models for real analysis.")
    
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
