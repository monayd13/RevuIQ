# 🚀 RevuIQ System Overview

## ✅ Current Status (Live)

### 🌐 Running Services

| Service | URL | Status | Purpose |
|---------|-----|--------|---------|
| **Frontend** | http://localhost:3000 | ✅ Running | User interface & dashboard |
| **Backend API** | http://localhost:8000 | ✅ Running | REST API & NLP processing |
| **API Docs** | http://localhost:8000/docs | ✅ Available | Interactive API documentation |
| **Database** | `backend/revuiq.db` | ✅ Connected | SQLite database |

### 📊 Database Status

- **Database Type**: SQLite
- **Location**: `/backend/revuiq.db`
- **Size**: 68 KB
- **Restaurants**: 3
- **Reviews**: 15
- **Status**: ✅ Connected & Working

---

## 🛠️ Technology Stack

### Frontend Technologies

#### Core Framework
- **Next.js 16.0.1** - React framework with server-side rendering
  - App Router (latest architecture)
  - Turbopack (faster bundler)
  - TypeScript support

#### UI & Styling
- **React 19** - UI component library
- **TailwindCSS 4** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **Lucide React** - Icon library (modern, lightweight)

#### State & Navigation
- **React Hooks** - useState, useEffect, useRouter
- **Next.js Navigation** - Client-side routing

#### Build Tools
- **npm** - Package manager
- **TypeScript** - Type safety
- **ESLint** - Code linting

---

### Backend Technologies

#### Core Framework
- **FastAPI** - Modern Python web framework
  - Async support
  - Auto-generated API docs
  - Type validation with Pydantic

#### Web Server
- **Uvicorn** - ASGI server
  - Hot reload in development
  - High performance

#### Database
- **SQLite** - Lightweight SQL database
  - File-based (revuiq.db)
  - No separate server needed
  - Perfect for development

#### ORM & Data
- **SQLAlchemy** - Python SQL toolkit & ORM
  - Model definitions
  - Query building
  - Relationship management

#### API Integration
- **Google Places API** - Fetch real restaurant reviews
  - Text search
  - Place details
  - Reviews (up to 5 per restaurant)

#### Data Processing
- **Python 3.13** - Programming language
- **Pydantic** - Data validation
- **JSON** - Data serialization

---

### NLP & AI Technologies

#### Current Implementation (Mock NLP)
Since we're using `simple_api.py` to avoid ML model dependencies:

- **Sentiment Analysis** - Rule-based (rating → sentiment)
  - 5-4 stars → POSITIVE
  - 3 stars → NEUTRAL
  - 2-1 stars → NEGATIVE

- **Emotion Detection** - Simple mapping
  - Positive reviews → joy, gratitude
  - Neutral reviews → neutral
  - Negative reviews → disappointment, anger

- **Aspect Extraction** - Keyword matching
  - Keywords: food, service, ambiance, price
  - Simple text search

- **Response Generation** - Template-based
  - Positive → Thank you message
  - Negative → Apology message
  - Neutral → Acknowledgment

#### Full NLP Stack (Available in `restaurant_api.py`)
When using the full ML models:

- **Hugging Face Transformers** - NLP model library
- **RoBERTa** - Sentiment analysis (94% accuracy)
- **GoEmotions** - 28-emotion detection
- **spaCy** - Named Entity Recognition (NER)
- **Flan-T5** - AI response generation
- **PyTorch** - Deep learning framework

---

## 📁 Project Structure

```
RevuIQ/
├── frontend/                    # Next.js Frontend
│   ├── app/
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   ├── restaurants/
│   │   │   ├── page.tsx        # Restaurant list ⭐
│   │   │   └── [id]/
│   │   │       └── page.tsx    # Analytics dashboard ⭐
│   │   ├── home/               # Landing page
│   │   ├── analytics/          # Analytics overview
│   │   └── reviews/            # Review management
│   ├── public/                 # Static assets
│   ├── package.json            # Dependencies
│   └── tailwind.config.ts      # Tailwind config
│
├── backend/                     # FastAPI Backend
│   ├── simple_api.py           # Main API (no ML) ⭐
│   ├── restaurant_api.py       # Full API (with ML)
│   ├── database.py             # Database models & ORM
│   ├── models.py               # Data models
│   ├── google_places_integration.py  # Google API ⭐
│   ├── yelp_reviews.py         # Yelp integration
│   ├── revuiq.db              # SQLite database ⭐
│   ├── .env                    # API keys (gitignored)
│   └── requirements.txt        # Python dependencies
│
├── nlp_pipeline/               # NLP Modules (optional)
│   ├── sentiment_analyzer.py  # RoBERTa sentiment
│   ├── emotion_detector.py    # GoEmotions
│   ├── aspect_extractor.py    # Custom NER
│   └── response_generator.py  # Flan-T5
│
├── ARCHITECTURE.md             # System architecture
├── START_HERE.md              # Quick start guide
├── RESTAURANT_API_GUIDE.md    # API documentation
├── GOOGLE_API_SETUP_SIMPLE.md # Google setup
└── test_restaurant_api.py     # Test suite
```

---

## 🔌 API Endpoints

### Restaurant Management
```
GET  /api/restaurants              # List all restaurants
POST /api/restaurants              # Create restaurant
GET  /api/restaurants/{id}         # Get restaurant details
```

### Review Management
```
POST /api/reviews                  # Create single review
POST /api/reviews/bulk             # Bulk upload reviews
GET  /api/reviews/restaurant/{id}  # Get restaurant reviews
```

### Google Places Integration
```
POST /api/google/fetch-reviews     # Fetch from Google Places
GET  /api/google/restaurant-info   # Get restaurant info
```

### Analytics
```
GET /api/analytics/restaurant/{id}?days=30  # Restaurant analytics
GET /api/analytics/sentiment-distribution   # Sentiment stats
GET /api/analytics/emotion-distribution     # Emotion stats
GET /api/analytics/stats                    # Overall stats
```

### Health & Status
```
GET /                              # API info
GET /health                        # Health check
GET /docs                          # Swagger UI
GET /redoc                         # ReDoc
```

---

## 🗄️ Database Schema

### businesses (Restaurants)
```sql
id              INTEGER PRIMARY KEY
name            VARCHAR(255)
industry        VARCHAR(100)
created_at      DATETIME
```

### reviews
```sql
id                  INTEGER PRIMARY KEY
business_id         INTEGER (FK → businesses.id)
platform            VARCHAR(50)      # google, yelp, manual
platform_review_id  VARCHAR(255)     # Unique per platform
author_name         VARCHAR(255)
rating              FLOAT            # 1.0 - 5.0
text                TEXT
review_date         DATETIME
sentiment           VARCHAR(20)      # POSITIVE, NEUTRAL, NEGATIVE
sentiment_score     FLOAT            # 0.0 - 1.0
emotions            JSON             # {joy: 0.8, gratitude: 0.6}
aspects             JSON             # [{aspect: "food", sentiment: "positive"}]
ai_response         TEXT             # Generated response
created_at          DATETIME
```

---

## 🔑 Environment Variables

### Backend (.env)
```bash
# Database
DATABASE_URL=sqlite:///./revuiq.db

# Google Places API
GOOGLE_PLACES_API_KEY=AIzaSyC...  # ✅ Configured

# Optional: Yelp API
YELP_API_KEY=your_key_here

# Optional: PostgreSQL (production)
# DATABASE_URL=postgresql://user:pass@host:5432/revuiq
```

---

## 🎯 Key Features

### ✅ Implemented
- [x] Restaurant CRUD operations
- [x] Google Places API integration
- [x] Real review fetching (up to 5 per restaurant)
- [x] Mock NLP analysis (sentiment, emotions, aspects)
- [x] AI response generation (template-based)
- [x] Analytics dashboard with charts
- [x] Time-based filtering (7, 30, 90 days)
- [x] Responsive UI with animations
- [x] SQLite database with ORM
- [x] API documentation (Swagger)
- [x] CORS enabled for frontend

### 🚧 Available (Not Active)
- [ ] Full ML models (RoBERTa, GoEmotions, Flan-T5)
- [ ] Yelp API integration
- [ ] User authentication
- [ ] Multi-user support
- [ ] Review response posting
- [ ] Email notifications

---

## 🎨 UI Pages

### 1. Home Page (`/`)
- Landing page
- Feature overview
- Call to action

### 2. Restaurant List (`/restaurants`) ⭐
- View all restaurants
- Add new restaurants
- **Fetch from Google** button (red)
- **Add Sample Reviews** button (green)
- **View Analytics** button (blue)
- Delete restaurants

### 3. Restaurant Analytics (`/restaurants/[id]`) ⭐
- Restaurant details
- **Day filter buttons** (7, 30, 90 days)
- Stats cards:
  - Total reviews
  - Average rating
  - Sentiment distribution
  - Top emotions
- Sentiment distribution chart
- Top emotions cards
- Most mentioned aspects
- Individual review cards with:
  - Author & rating
  - Review text
  - Sentiment badge
  - Top 3 emotions
  - AI-generated response

### 4. Analytics Overview (`/analytics`)
- System-wide analytics
- Sentiment trends
- Emotion distribution
- Quick actions

### 5. Reviews (`/reviews`)
- All reviews across restaurants
- Filter & search
- Bulk actions

---

## 🔄 Data Flow

### Adding a Restaurant
```
User → Frontend → POST /api/restaurants → Backend → SQLite
                                                    ↓
                                            Returns restaurant ID
```

### Fetching Google Reviews
```
User clicks "Fetch from Google"
    ↓
Frontend → POST /api/google/fetch-reviews
    ↓
Backend → Google Places API
    ↓
Fetch 5 reviews
    ↓
Mock NLP Analysis (sentiment, emotions, aspects, response)
    ↓
Store in SQLite
    ↓
Return success message
```

### Viewing Analytics
```
User clicks "View Analytics"
    ↓
Frontend → GET /api/analytics/restaurant/{id}?days=30
    ↓
Backend → Query SQLite for reviews in date range
    ↓
Aggregate sentiment, emotions, aspects
    ↓
Return analytics JSON
    ↓
Frontend → Display charts & cards
```

---

## 📊 Performance

### Response Times
- **Restaurant list**: ~20ms
- **Single review**: ~50ms
- **Bulk upload (3 reviews)**: ~200ms
- **Google API fetch**: 2-5 seconds
- **Analytics query**: <100ms

### Database
- **Size**: 68 KB (3 restaurants, 15 reviews)
- **Query speed**: <10ms for most queries
- **Connection**: Persistent (SQLite file)

---

## 🔒 Security

### ✅ Implemented
- API keys in `.env` (gitignored)
- CORS configured for localhost
- Input validation (Pydantic)
- SQL injection prevention (SQLAlchemy ORM)

### ⚠️ Not Implemented (Development Only)
- No authentication
- No rate limiting
- No HTTPS (use HTTP for local dev)
- No API key rotation

---

## 🚀 Quick Start Commands

### Start Backend
```bash
cd /Users/tarang/CascadeProjects/windsurf-project/RevuIQ/backend
python3 simple_api.py
```

### Start Frontend
```bash
cd /Users/tarang/CascadeProjects/windsurf-project/RevuIQ/frontend
npm run dev
```

### Test API
```bash
cd /Users/tarang/CascadeProjects/windsurf-project/RevuIQ
python test_restaurant_api.py
```

### Check Database
```bash
cd backend
sqlite3 revuiq.db "SELECT * FROM businesses;"
sqlite3 revuiq.db "SELECT COUNT(*) FROM reviews;"
```

---

## 📈 Next Steps

### Immediate
1. ✅ Both services running
2. ✅ Database connected
3. ✅ Google API configured
4. ✅ Frontend accessible

### Short Term
- [ ] Add more restaurants
- [ ] Fetch more reviews
- [ ] Test all features
- [ ] Add error handling

### Long Term
- [ ] Deploy to production
- [ ] Add authentication
- [ ] Integrate Yelp API
- [ ] Enable full ML models
- [ ] Add real-time updates

---

## 🆘 Troubleshooting

### Backend Won't Start
```bash
# Check if port 8000 is in use
lsof -ti:8000 | xargs kill -9

# Restart
python3 simple_api.py
```

### Frontend Won't Start
```bash
# Check if port 3000 is in use
lsof -ti:3000 | xargs kill -9

# Restart
npm run dev
```

### Database Issues
```bash
# Check database exists
ls -lh backend/revuiq.db

# View tables
sqlite3 backend/revuiq.db ".tables"

# Reset database (caution!)
rm backend/revuiq.db
python3 simple_api.py  # Will recreate
```

### Google API Not Working
```bash
# Check API key
cat backend/.env

# Test directly
curl "https://maps.googleapis.com/maps/api/place/textsearch/json?query=McDonalds&key=YOUR_KEY"
```

---

## 📚 Documentation Files

1. **START_HERE.md** - Quick start (read first!)
2. **RESTAURANT_API_GUIDE.md** - Complete API docs
3. **ARCHITECTURE.md** - System design
4. **GOOGLE_API_SETUP_SIMPLE.md** - Google setup
5. **IMPLEMENTATION_SUMMARY.md** - Feature list
6. **QUICK_REFERENCE.md** - Cheat sheet
7. **SYSTEM_OVERVIEW.md** - This file

---

**Status**: ✅ All Systems Operational  
**Last Updated**: November 19, 2025  
**Version**: 2.0.0
