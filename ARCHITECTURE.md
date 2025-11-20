# RevuIQ Restaurant Review NLP Analytics - Architecture

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                      (Next.js Frontend)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  /restaurants              /restaurants/[id]      /analytics   │
│  ┌──────────────┐         ┌──────────────┐       ┌──────────┐ │
│  │ Restaurant   │         │ Analytics    │       │ Global   │ │
│  │ List         │────────▶│ Dashboard    │       │ Stats    │ │
│  │              │         │              │       │          │ │
│  │ • Add        │         │ • Sentiment  │       │ • Trends │ │
│  │ • Upload     │         │ • Emotions   │       │ • Metrics│ │
│  │ • View       │         │ • Aspects    │       │          │ │
│  └──────────────┘         └──────────────┘       └──────────┘ │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST API
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                      BACKEND API LAYER                          │
│                      (FastAPI Server)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Restaurant Endpoints          Review Endpoints                │
│  ┌──────────────────┐         ┌──────────────────┐            │
│  │ POST /restaurants│         │ POST /reviews     │            │
│  │ GET  /restaurants│         │ POST /reviews/bulk│            │
│  │ GET  /restaurants│         │ GET  /reviews/    │            │
│  │      /{id}       │         │      restaurant/  │            │
│  └──────────────────┘         │      {id}         │            │
│                                └──────────────────┘            │
│                                                                 │
│  Analytics Endpoints                                           │
│  ┌────────────────────────────────────────────┐               │
│  │ GET /analytics/restaurant/{id}             │               │
│  │ GET /analytics/sentiment-distribution      │               │
│  │ GET /analytics/emotion-distribution        │               │
│  │ GET /analytics/stats                       │               │
│  └────────────────────────────────────────────┘               │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                      NLP PIPELINE LAYER                         │
│                   (Hugging Face Transformers)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐ │
│  │ Sentiment       │  │ Emotion         │  │ Aspect         │ │
│  │ Analyzer        │  │ Detector        │  │ Extractor      │ │
│  │                 │  │                 │  │                │ │
│  │ Model:          │  │ Model:          │  │ Method:        │ │
│  │ RoBERTa         │  │ GoEmotions      │  │ Custom NER     │
│  │                 │  │ DistilRoBERTa   │  │ + Keywords     │ │
│  │ Output:         │  │                 │  │                │ │
│  │ • POSITIVE      │  │ Output:         │  │ Output:        │ │
│  │ • NEUTRAL       │  │ • joy           │  │ • food         │ │
│  │ • NEGATIVE      │  │ • anger         │  │ • service      │ │
│  │ • confidence    │  │ • gratitude     │  │ • ambiance     │ │
│  │                 │  │ • disappointment│  │ • price        │ │
│  └─────────────────┘  └─────────────────┘  └────────────────┘ │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ Response Generator                                      │  │
│  │                                                         │  │
│  │ Model: Flan-T5                                         │  │
│  │                                                         │  │
│  │ Input: Review + Sentiment + Context                    │  │
│  │ Output: Professional, empathetic response              │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                      DATABASE LAYER                             │
│                   (PostgreSQL / SQLite)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ businesses   │  │ reviews      │  │ analytics    │         │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤         │
│  │ id           │  │ id           │  │ id           │         │
│  │ name         │  │ business_id  │  │ business_id  │         │
│  │ industry     │  │ platform     │  │ date         │         │
│  │ created_at   │  │ author_name  │  │ total_reviews│         │
│  └──────────────┘  │ rating       │  │ avg_rating   │         │
│                    │ text         │  │ positive_cnt │         │
│                    │ sentiment    │  │ negative_cnt │         │
│                    │ emotions     │  └──────────────┘         │
│                    │ aspects      │                            │
│                    │ ai_response  │                            │
│                    └──────────────┘                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow

### 1. Review Upload Flow

```
User Action
    │
    ▼
Frontend: POST /api/reviews
    │
    ▼
Backend API: Receive review data
    │
    ├──▶ Sentiment Analyzer (RoBERTa)
    │        │
    │        ▼
    │    Returns: POSITIVE/NEUTRAL/NEGATIVE + score
    │
    ├──▶ Emotion Detector (GoEmotions)
    │        │
    │        ▼
    │    Returns: {joy: 0.8, gratitude: 0.6, ...}
    │
    ├──▶ Aspect Extractor (Custom NER)
    │        │
    │        ▼
    │    Returns: [{aspect: "food", sentiment: "positive"}, ...]
    │
    └──▶ Response Generator (Flan-T5)
             │
             ▼
         Returns: "Thank you for your feedback..."
    │
    ▼
Database: Store review + NLP results
    │
    ▼
Frontend: Display success + analytics
```

### 2. Analytics Query Flow

```
User Action: View Analytics
    │
    ▼
Frontend: GET /api/analytics/restaurant/{id}?days=30
    │
    ▼
Backend API: Query database
    │
    ├──▶ Aggregate sentiment counts
    ├──▶ Calculate average rating
    ├──▶ Extract top emotions
    ├──▶ Count aspect mentions
    └──▶ Build rating distribution
    │
    ▼
Return JSON analytics
    │
    ▼
Frontend: Render charts & visualizations
```

---

## 🔧 Technology Stack

### Frontend
- **Framework:** Next.js 16 (React 19)
- **Styling:** TailwindCSS 4
- **UI Components:** Radix UI
- **Icons:** Lucide React
- **Animations:** Framer Motion
- **Charts:** Recharts

### Backend
- **Framework:** FastAPI
- **Server:** Uvicorn (ASGI)
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL / SQLite
- **Validation:** Pydantic

### NLP/AI
- **Library:** Hugging Face Transformers
- **Framework:** PyTorch
- **Models:**
  - Sentiment: `cardiffnlp/twitter-roberta-base-sentiment-latest`
  - Emotion: `j-hartmann/emotion-english-distilroberta-base`
  - Response: `google/flan-t5-base`
  - Aspect: Custom NER + spaCy

---

## 🔐 Security Considerations

### API Security
- CORS configured for specific origins
- Input validation via Pydantic models
- SQL injection prevention via SQLAlchemy ORM
- Rate limiting (TODO)
- API key authentication (TODO)

### Data Privacy
- No PII stored beyond review author names
- Database credentials in environment variables
- HTTPS in production (recommended)

---

## 📈 Scalability

### Current Capacity
- **Reviews:** 10,000+ per restaurant
- **Concurrent Users:** 100+
- **NLP Processing:** 5-10 reviews/second
- **Analytics Queries:** <100ms for 1000 reviews

### Scaling Strategies

#### Horizontal Scaling
```
Load Balancer
    │
    ├──▶ API Server 1 ──┐
    ├──▶ API Server 2 ──┼──▶ Database (Primary)
    └──▶ API Server 3 ──┘
```

#### Async Processing
```
API Server ──▶ Message Queue (Redis/RabbitMQ)
                    │
                    ▼
              Worker Pool (NLP Processing)
                    │
                    ▼
              Database (Results)
```

#### Caching Layer
```
Request ──▶ Redis Cache ──▶ Hit? Return
                │
                ▼ Miss
           Database Query
                │
                ▼
           Cache Result
```

---

## 🚀 Deployment Architecture

### Development
```
localhost:3000 (Frontend)
    │
    ▼
localhost:8000 (Backend API)
    │
    ▼
localhost:5432 (PostgreSQL)
```

### Production (Recommended)

```
┌─────────────────────────────────────────┐
│         CDN (Vercel/Netlify)            │
│         Frontend (Next.js)              │
└──────────────────┬──────────────────────┘
                   │ HTTPS
                   ▼
┌─────────────────────────────────────────┐
│      API Gateway / Load Balancer        │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌──────────────┐      ┌──────────────┐
│ API Server 1 │      │ API Server 2 │
│ (AWS/GCP)    │      │ (AWS/GCP)    │
└──────┬───────┘      └──────┬───────┘
       │                     │
       └──────────┬──────────┘
                  ▼
        ┌─────────────────┐
        │   Database      │
        │   (RDS/Cloud    │
        │    SQL)         │
        └─────────────────┘
```

---

## 🔄 API Request/Response Examples

### Create Review with NLP

**Request:**
```json
POST /api/reviews
{
  "platform": "google",
  "platform_review_id": "abc123",
  "business_id": 1,
  "author_name": "John Doe",
  "rating": 5.0,
  "text": "Amazing food and service!",
  "review_date": "2024-01-15T10:00:00Z"
}
```

**Response:**
```json
{
  "success": true,
  "review_id": 42,
  "analysis": {
    "sentiment": {
      "label": "POSITIVE",
      "score": 0.9876
    },
    "emotions": {
      "joy": 0.85,
      "admiration": 0.72,
      "gratitude": 0.45
    },
    "aspects": [
      {"aspect": "food", "sentiment": "positive"},
      {"aspect": "service", "sentiment": "positive"}
    ],
    "ai_response": "Thank you so much for your wonderful feedback! We're thrilled to hear you enjoyed both our food and service..."
  }
}
```

### Get Analytics

**Request:**
```
GET /api/analytics/restaurant/1?days=30
```

**Response:**
```json
{
  "success": true,
  "restaurant_id": 1,
  "period_days": 30,
  "total_reviews": 156,
  "average_rating": 4.3,
  "sentiment_distribution": {
    "POSITIVE": 98,
    "NEUTRAL": 42,
    "NEGATIVE": 16
  },
  "top_emotions": {
    "joy": 0.78,
    "gratitude": 0.65,
    "admiration": 0.52
  },
  "top_aspects": {
    "food": 89,
    "service": 67,
    "ambiance": 45,
    "price": 23
  }
}
```

---

## 📊 Database Schema Details

### businesses
```sql
CREATE TABLE businesses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### reviews
```sql
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    business_id INTEGER REFERENCES businesses(id),
    platform VARCHAR(50) NOT NULL,
    platform_review_id VARCHAR(255) UNIQUE NOT NULL,
    author_name VARCHAR(255),
    rating FLOAT,
    text TEXT NOT NULL,
    review_date TIMESTAMP,
    
    -- NLP Results
    sentiment VARCHAR(20),
    sentiment_score FLOAT,
    emotions TEXT,  -- JSON
    aspects TEXT,   -- JSON
    ai_response TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🎯 Performance Optimization

### Backend
- Lazy loading of NLP models
- Database connection pooling
- Query optimization with indexes
- Async processing for bulk operations

### Frontend
- Server-side rendering (SSR)
- Static generation where possible
- Image optimization
- Code splitting
- Lazy loading components

### NLP
- Model caching in memory
- Batch processing for multiple reviews
- GPU acceleration (optional)
- Quantization for faster inference

---

**Last Updated:** November 2024  
**Version:** 2.0.0
