# Restaurant Review NLP Analytics API - Complete Guide

## 🎯 Overview

This is a complete restaurant review management system with advanced NLP analytics. Upload reviews, get AI-powered sentiment analysis, emotion detection, aspect extraction, and automated response generation.

## 🚀 Quick Start

### 1. Start the Backend API

```bash
cd RevuIQ/backend
python restaurant_api.py
```

The API will start on `http://localhost:8000`

**API Documentation:** http://localhost:8000/docs (Swagger UI)

### 2. Start the Frontend

```bash
cd RevuIQ/frontend
npm install  # First time only
npm run dev
```

The frontend will start on `http://localhost:3000`

### 3. Use the System

1. Navigate to http://localhost:3000/restaurants
2. Click "Add Restaurant" and create a new restaurant
3. Click "Add Sample Reviews" to upload demo reviews with NLP analysis
4. Click "View Analytics" to see comprehensive insights

---

## 📊 Features

### NLP Analytics (Automatic on Every Review)

- **Sentiment Analysis** - RoBERTa-based classification (Positive/Neutral/Negative)
- **Emotion Detection** - GoEmotions multi-label detection (joy, anger, gratitude, etc.)
- **Aspect Extraction** - Identifies topics (food, service, ambiance, price)
- **AI Response Generation** - T5/Flan-T5 powered professional responses

### Analytics Dashboard

- Sentiment distribution with visual charts
- Top emotions detected across reviews
- Most mentioned aspects/topics
- Rating distribution (1-5 stars)
- Time-based filtering (7, 30, 90 days)

---

## 🔌 API Endpoints

### Restaurant Management

#### Create Restaurant
```bash
POST /api/restaurants
Content-Type: application/json

{
  "name": "Olive Garden",
  "industry": "restaurant"
}
```

#### Get All Restaurants
```bash
GET /api/restaurants
```

#### Get Restaurant Details
```bash
GET /api/restaurants/{restaurant_id}
```

### Review Management

#### Add Single Review (with NLP Analysis)
```bash
POST /api/reviews
Content-Type: application/json

{
  "platform": "google",
  "platform_review_id": "unique_id_123",
  "business_id": 1,
  "author_name": "John Doe",
  "rating": 5.0,
  "text": "Amazing food and service!",
  "review_date": "2024-01-15T10:30:00Z"
}
```

**Response includes:**
- Sentiment analysis (label + confidence score)
- Emotion detection (multiple emotions with scores)
- Aspect extraction (food, service, etc.)
- AI-generated response

#### Bulk Upload Reviews
```bash
POST /api/reviews/bulk
Content-Type: application/json

{
  "business_id": 1,
  "reviews": [
    {
      "platform": "google",
      "platform_review_id": "review_1",
      "author_name": "Jane Smith",
      "rating": 4.0,
      "text": "Great experience!",
      "review_date": "2024-01-15T10:30:00Z"
    },
    ...
  ]
}
```

#### Get Restaurant Reviews
```bash
GET /api/reviews/restaurant/{restaurant_id}?skip=0&limit=50
```

### Analytics Endpoints

#### Restaurant Analytics
```bash
GET /api/analytics/restaurant/{restaurant_id}?days=30
```

**Returns:**
- Total reviews count
- Average rating
- Sentiment distribution (positive/neutral/negative counts)
- Top emotions (with average scores)
- Top aspects (most mentioned topics)
- Rating distribution (1-5 star breakdown)

#### Sentiment Distribution
```bash
GET /api/analytics/sentiment-distribution?days=30&business_id=1
```

#### Emotion Distribution
```bash
GET /api/analytics/emotion-distribution?days=30&business_id=1
```

#### Overall Stats
```bash
GET /api/analytics/stats
```

---

## 💾 Database Schema

### Business Table
```sql
- id (Primary Key)
- name (String)
- industry (String) - e.g., "restaurant"
- created_at (DateTime)
```

### Review Table
```sql
- id (Primary Key)
- business_id (Foreign Key)
- platform (String) - google, yelp, manual
- platform_review_id (String, Unique)
- author_name (String)
- rating (Float)
- text (Text)
- review_date (DateTime)
- sentiment (String) - POSITIVE/NEUTRAL/NEGATIVE
- sentiment_score (Float)
- emotions (JSON String)
- aspects (JSON String)
- ai_response (Text)
- created_at (DateTime)
```

---

## 🧠 NLP Pipeline Details

### 1. Sentiment Analysis
- **Model:** `cardiffnlp/twitter-roberta-base-sentiment-latest`
- **Output:** Label (POSITIVE/NEUTRAL/NEGATIVE) + Confidence Score
- **Accuracy:** ~94% on benchmark datasets

### 2. Emotion Detection
- **Model:** `j-hartmann/emotion-english-distilroberta-base` (GoEmotions)
- **Output:** Multi-label emotions with scores
- **Emotions:** joy, anger, sadness, fear, surprise, love, gratitude, etc.

### 3. Aspect Extraction
- **Method:** Custom NER + keyword extraction
- **Aspects:** food, service, ambiance, price, cleanliness, location, etc.
- **Output:** List of aspects with sentiment per aspect

### 4. Response Generation
- **Model:** `google/flan-t5-base`
- **Input:** Review text + sentiment + business context
- **Output:** Professional, empathetic response
- **Tone Options:** professional, friendly, apologetic

---

## 📱 Frontend Pages

### `/restaurants`
- List all restaurants
- Add new restaurants
- Upload sample reviews
- Navigate to analytics

### `/restaurants/[id]`
- Restaurant details
- Comprehensive analytics dashboard
- Sentiment distribution charts
- Top emotions visualization
- Review list with NLP insights
- AI-generated responses

### `/analytics`
- Global analytics across all restaurants
- Sentiment trends
- Emotion distribution
- Response performance metrics

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database (Optional - defaults to SQLite)
DATABASE_URL=postgresql://user:password@localhost:5432/revuiq

# API Keys (Optional - for external review fetching)
GOOGLE_PLACES_API_KEY=your_key_here
YELP_API_KEY=your_key_here
```

### Database Setup

The database is automatically initialized when you start the backend.

**Manual initialization:**
```bash
cd backend
python -c "from database import init_db; init_db()"
```

**Reset database:**
```bash
python -c "from database import drop_db, init_db; drop_db(); init_db()"
```

---

## 📊 Example Use Cases

### 1. Restaurant Owner Dashboard
- Upload all reviews from Google/Yelp
- See sentiment trends over time
- Identify common complaints (aspects)
- Generate professional responses

### 2. Multi-Location Chain
- Compare sentiment across locations
- Identify best/worst performing locations
- Track improvement over time

### 3. Market Research
- Analyze competitor reviews
- Identify market trends
- Understand customer preferences

---

## 🧪 Testing

### Test with Sample Data

```bash
# Start backend
cd backend
python restaurant_api.py

# In another terminal, test endpoints
curl http://localhost:8000/health

# Create a restaurant
curl -X POST http://localhost:8000/api/restaurants \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Restaurant", "industry": "restaurant"}'

# Upload a review
curl -X POST http://localhost:8000/api/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "manual",
    "platform_review_id": "test_1",
    "business_id": 1,
    "author_name": "Test User",
    "rating": 5.0,
    "text": "Amazing food and service!",
    "review_date": "2024-01-15T10:30:00Z"
  }'

# Get analytics
curl http://localhost:8000/api/analytics/restaurant/1?days=30
```

### Frontend Testing

1. Open http://localhost:3000/restaurants
2. Add a restaurant
3. Click "Add Sample Reviews"
4. Click "View Analytics"
5. Verify all NLP features are working

---

## 🚨 Troubleshooting

### Backend won't start
- Check Python version (3.8+)
- Install dependencies: `pip install -r backend/requirements.txt`
- Check port 8000 is not in use

### Frontend won't connect to backend
- Verify backend is running on port 8000
- Check CORS settings in `restaurant_api.py`
- Open browser console for errors

### NLP models not loading
- First run downloads models (~500MB)
- Ensure internet connection
- Check disk space
- Models cache in `~/.cache/huggingface/`

### Database errors
- Check DATABASE_URL in .env
- Ensure PostgreSQL is running (if using)
- Try resetting database (see Database Setup)

---

## 📈 Performance

- **Review Analysis:** ~1-2 seconds per review
- **Bulk Upload:** ~5-10 reviews per second
- **Analytics Query:** <100ms for 1000 reviews
- **Model Loading:** ~10-30 seconds (first time only)

---

## 🎓 Next Steps

1. **Integrate Real APIs**
   - Add Google Places API integration
   - Add Yelp Fusion API integration
   - Automate review fetching

2. **Enhanced Analytics**
   - Time-series sentiment trends
   - Comparative analysis
   - Predictive insights

3. **Response Management**
   - Human-in-the-loop approval workflow
   - Response templates
   - Auto-posting to platforms

4. **Advanced NLP**
   - Custom aspect extraction for specific industries
   - Multi-language support
   - Sarcasm detection

---

## 📚 Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Hugging Face Transformers:** https://huggingface.co/docs/transformers
- **Next.js Docs:** https://nextjs.org/docs
- **RoBERTa Sentiment Model:** https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest
- **GoEmotions Model:** https://huggingface.co/j-hartmann/emotion-english-distilroberta-base

---

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at http://localhost:8000/docs
3. Check browser console for frontend errors
4. Check backend logs for API errors

---

**Built with:** FastAPI, Next.js, Hugging Face Transformers, PostgreSQL, TailwindCSS
