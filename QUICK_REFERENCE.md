# 🚀 Quick Reference Card

## Start Commands

```bash
# Terminal 1 - Backend
cd /Users/tarang/CascadeProjects/windsurf-project/RevuIQ/backend
python restaurant_api.py

# Terminal 2 - Frontend  
cd /Users/tarang/CascadeProjects/windsurf-project/RevuIQ/frontend
npm run dev

# Terminal 3 - Test (Optional)
cd /Users/tarang/CascadeProjects/windsurf-project/RevuIQ
python test_restaurant_api.py
```

## URLs

- **Frontend:** http://localhost:3000/restaurants
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## Key API Endpoints

```bash
# Create Restaurant
POST http://localhost:8000/api/restaurants
{"name": "My Restaurant", "industry": "restaurant"}

# Upload Review (Auto NLP)
POST http://localhost:8000/api/reviews
{
  "platform": "google",
  "platform_review_id": "unique_id",
  "business_id": 1,
  "author_name": "John Doe",
  "rating": 5.0,
  "text": "Amazing food!",
  "review_date": "2024-01-15T10:00:00Z"
}

# Get Analytics
GET http://localhost:8000/api/analytics/restaurant/1?days=30

# Bulk Upload
POST http://localhost:8000/api/reviews/bulk
{"business_id": 1, "reviews": [...]}
```

## NLP Models Used

| Feature | Model | Output |
|---------|-------|--------|
| Sentiment | RoBERTa | POSITIVE/NEUTRAL/NEGATIVE + score |
| Emotions | GoEmotions | joy, anger, gratitude, etc. |
| Aspects | Custom NER | food, service, ambiance, price |
| Responses | Flan-T5 | Professional reply text |

## File Structure

```
RevuIQ/
├── backend/
│   ├── restaurant_api.py      ⭐ Main API server
│   ├── database.py             Database models
│   ├── models.py               Data models
│   └── requirements.txt        Dependencies
├── frontend/
│   └── app/
│       └── restaurants/
│           ├── page.tsx        ⭐ Restaurant list
│           └── [id]/
│               └── page.tsx    ⭐ Analytics dashboard
├── nlp_pipeline/
│   ├── sentiment_analyzer.py   RoBERTa sentiment
│   ├── emotion_detector.py     GoEmotions
│   ├── aspect_extractor.py     Custom NER
│   └── response_generator.py   Flan-T5
├── START_HERE.md              ⭐ Read this first!
├── RESTAURANT_API_GUIDE.md     Complete API docs
├── ARCHITECTURE.md             System design
└── test_restaurant_api.py      Test suite
```

## Quick Demo Flow

1. **Add Restaurant**
   - Open http://localhost:3000/restaurants
   - Click "Add Restaurant"
   - Name: "Olive Garden"
   - Click "Add Restaurant"

2. **Upload Reviews**
   - Click "Add Sample Reviews"
   - Wait 5-10 seconds
   - See success message

3. **View Analytics**
   - Click "View Analytics"
   - See sentiment charts
   - See emotion detection
   - See AI responses

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend won't start | `pip install -r backend/requirements.txt` |
| Frontend won't start | `cd frontend && npm install` |
| Can't connect to backend | Check backend is on port 8000 |
| Models downloading slow | First run only, ~500MB, needs internet |
| Database error | Check DATABASE_URL in .env |

## Performance

- **Review Analysis:** 1-2 sec/review
- **Bulk Upload:** 5-10 reviews/sec
- **Analytics Query:** <100ms
- **Model Loading:** 10-30 sec (first time only)

## What Gets Analyzed (Auto)

Every review automatically gets:
- ✅ Sentiment (positive/neutral/negative)
- ✅ Confidence score (0-100%)
- ✅ Emotions (joy, anger, gratitude, etc.)
- ✅ Aspects (food, service, ambiance, price)
- ✅ AI-generated response

## Sample cURL Commands

```bash
# Health Check
curl http://localhost:8000/health

# Create Restaurant
curl -X POST http://localhost:8000/api/restaurants \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Restaurant", "industry": "restaurant"}'

# Upload Review
curl -X POST http://localhost:8000/api/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "google",
    "platform_review_id": "test_123",
    "business_id": 1,
    "author_name": "John Doe",
    "rating": 5.0,
    "text": "Amazing food!",
    "review_date": "2024-01-15T10:00:00Z"
  }'

# Get Analytics
curl http://localhost:8000/api/analytics/restaurant/1?days=30
```

## Dependencies

```bash
# Backend
pip install fastapi uvicorn sqlalchemy transformers torch pydantic

# Frontend
npm install next react react-dom framer-motion lucide-react
```

## Environment Variables

Create `.env` in `backend/`:
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/revuiq
GOOGLE_PLACES_API_KEY=your_key  # Optional
YELP_API_KEY=your_key           # Optional
```

## Database Schema (Quick)

```sql
businesses: id, name, industry, created_at
reviews: id, business_id, platform, author_name, rating, text,
         sentiment, emotions, aspects, ai_response, review_date
```

## Next Steps

1. ✅ Start backend & frontend
2. ✅ Add a restaurant
3. ✅ Upload sample reviews
4. ✅ View analytics
5. 🚀 Integrate real APIs (Google/Yelp)
6. 🚀 Add authentication
7. 🚀 Deploy to production

---

**Need Help?** Read `START_HERE.md` or `RESTAURANT_API_GUIDE.md`
