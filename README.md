# 🧠 RevuIQ - AI-Powered Review Management System

**Centralized NLP-Powered Platform for Multi-Platform Review Analysis & Response**

## 🎯 Project Overview

RevuIQ uses Natural Language Processing to automate customer review management across Google, Yelp, TripAdvisor, and Meta platforms.

### Key Features
- 📊 **Sentiment Analysis** - Classify reviews as Positive, Neutral, or Negative
- 😊 **Emotion Detection** - Identify emotional tone (anger, joy, disappointment, etc.)
- 🔍 **Aspect Extraction** - Detect what customers are talking about (service, food, price)
- ✍️ **AI Response Generation** - Create brand-consistent, empathetic replies
- 👤 **Human-in-the-Loop** - Approve/edit AI suggestions before posting
- 📈 **Analytics Dashboard** - Visualize trends and insights

## 🛠️ Tech Stack

**Backend:**
- FastAPI (Python)
- SQLite / PostgreSQL
- Hugging Face Transformers

**Frontend:**
- Next.js
- Tailwind CSS
- Framer Motion
- Recharts

**NLP Models:**
- RoBERTa (Sentiment Analysis)
- GoEmotions (Emotion Detection)
- Flan-T5 (Response Generation)
- BART/T5 (Summarization)

## 📦 Project Structure

```
RevuIQ/
├── nlp_pipeline/           # Core NLP components
│   ├── sentiment_analyzer.py
│   ├── emotion_detector.py
│   ├── aspect_extractor.py
│   ├── response_generator.py
│   └── demo.py
├── backend/                # FastAPI server
│   ├── simple_api.py      # Main API
│   ├── models.py          # Database models
│   ├── database.py        # DB configuration
│   └── google_places_integration.py
├── frontend/               # Next.js app
│   ├── app/               # Pages
│   ├── components/        # Reusable components
│   └── public/            # Static assets
├── tests/                  # Unit tests
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
cd frontend && npm install
```

### 2. Start the Application

```bash
./start_all.sh
```

This will start:
- Backend API on http://localhost:8000
- Frontend on http://localhost:3000

### 3. Access the Dashboard

Open http://localhost:3000 in your browser and start managing reviews!

## 📊 NLP Pipeline Workflow

```
Review Input
    ↓
[Preprocessing] → Tokenization, Cleaning
    ↓
[Sentiment Analysis] → Positive/Neutral/Negative
    ↓
[Emotion Detection] → Joy, Anger, Disappointment, etc.
    ↓
[Aspect Extraction] → Service, Food, Price, Staff
    ↓
[Response Generation] → AI-generated reply
    ↓
[Human Approval] → Manager reviews & approves
    ↓
Post to Platform
```

## 🎯 Features

### ✅ Implemented
- Restaurant management
- Google Places API integration
- Review fetching and storage
- Sentiment & emotion analysis
- AI response generation
- Review approval workflow
- Response approval workflow
- Analytics dashboard
- Multi-page frontend
- Beautiful UI with animations

### 🔄 In Progress
- Advanced NLP models
- Multi-platform support (Yelp, TripAdvisor, Meta)
- Automated posting to platforms

## 📈 Evaluation Metrics

- **Sentiment Accuracy**: F1-score on labeled dataset
- **Response Relevance**: BLEU/ROUGE scores
- **Approval Rate**: % of AI replies accepted without edits
- **Response Time**: Average time saved vs manual handling

## 🤝 Contributing

This is an educational NLP project demonstrating:
- End-to-end ML pipeline design
- Transformer model integration
- Ethical AI with human oversight
- Real-world business application

## 📝 License

MIT License - Educational Project

## 🎓 Learning Outcomes

- NLP pipeline architecture
- Transformer model fine-tuning
- API design and integration
- Human-in-the-loop AI systems
- Data visualization and UX
- Full-stack development

---

**Built with ❤️ for demonstrating practical NLP applications**

## Scripts

- `./start_all.sh` - Start both backend and frontend
- `./stop_all.sh` - Stop all services
- `./check_status.sh` - Check if services are running

## Notes

- Google Places API only returns 5 reviews per restaurant
- Reviews are analyzed using mock NLP (simplified version)
- Database is SQLite stored in `backend/revuiq.db`
