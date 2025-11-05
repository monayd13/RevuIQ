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
- PostgreSQL (Supabase)
- Hugging Face Transformers

**Frontend:**
- Next.js
- Tailwind CSS
- Chart.js

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
├── frontend/               # Next.js app
├── tests/                  # Unit tests
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run NLP Demo

```bash
cd nlp_pipeline
python demo.py
```

### 3. Test with Sample Review

```python
from nlp_pipeline.sentiment_analyzer import analyze_sentiment
from nlp_pipeline.response_generator import generate_response

review = "The coffee was great but service was slow."
sentiment = analyze_sentiment(review)
reply = generate_response(review, sentiment)

print(f"Sentiment: {sentiment}")
print(f"AI Reply: {reply}")
```

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

## 🧪 Development Phases

### ✅ Phase 1: NLP Proof of Concept (Current)
- [x] Sentiment analysis
- [x] Emotion detection
- [x] Response generation
- [x] Demo script

### 🔄 Phase 2: Backend API (Next)
- [ ] FastAPI endpoints
- [ ] Database schema
- [ ] Review storage

### 📅 Phase 3: Frontend Dashboard
- [ ] Next.js UI
- [ ] Review management interface
- [ ] Analytics visualizations

### 🔌 Phase 4: API Integrations
- [ ] Google Places API
- [ ] Yelp Fusion API
- [ ] Meta Graph API

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

---

**Built with ❤️ for demonstrating practical NLP applications**
