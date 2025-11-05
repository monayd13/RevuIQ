# 🚀 RevuIQ Quick Start Guide

Get your NLP pipeline running in 5 minutes!

## ⚡ Installation

### Step 1: Navigate to Project
```bash
cd /Users/tarang/CascadeProjects/windsurf-project/RevuIQ
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note:** First installation will download ~2GB of models. This is normal!

### Step 3: Download spaCy Model (Optional)
```bash
python -m spacy download en_core_web_sm
```

## 🎮 Run the Demo

### Full Pipeline Demo
```bash
cd nlp_pipeline
python demo.py
```

This will:
- ✅ Load all NLP models (RoBERTa, GoEmotions, Flan-T5)
- ✅ Analyze 5 sample reviews
- ✅ Generate AI responses
- ✅ Show summary statistics

**Expected output:**
```
🧠 RevuIQ - AI-Powered Review Management System
════════════════════════════════════════════════

Loading models...
✓ Sentiment analyzer ready!
✓ Emotion detector ready!
✓ Response generator ready!

📝 Review: "The coffee was amazing!"
🔍 Analyzing sentiment...
   😊 Sentiment: POSITIVE (confidence: 98.5%)
💭 Detecting emotions...
   Primary: joy
✍️  Generating AI response...
   💬 AI Reply: "Thank you for the wonderful feedback! We're thrilled you enjoyed our coffee."
```

## 🧪 Test Individual Components

### Sentiment Analysis Only
```bash
cd nlp_pipeline
python sentiment_analyzer.py
```

### Emotion Detection Only
```bash
cd nlp_pipeline
python emotion_detector.py
```

### Response Generation Only
```bash
cd nlp_pipeline
python response_generator.py
```

## 💻 Use in Your Code

```python
from nlp_pipeline import SentimentAnalyzer, EmotionDetector, ResponseGenerator

# Initialize
sentiment = SentimentAnalyzer()
emotion = EmotionDetector()
generator = ResponseGenerator()

# Analyze a review
review = "Great service but food was cold"

# Get sentiment
sent_result = sentiment.analyze(review)
print(f"Sentiment: {sent_result['label']}")

# Get emotions
emot_result = emotion.detect(review)
print(f"Emotion: {emot_result['primary_emotion']}")

# Generate response
response = generator.generate(
    review=review,
    sentiment=sent_result['label'],
    emotion=emot_result['primary_emotion'],
    business_name="Your Restaurant"
)
print(f"AI Reply: {response['response']}")
```

## 🎯 Quick Test with Your Own Review

Create a file `test_my_review.py`:

```python
from nlp_pipeline import SentimentAnalyzer, EmotionDetector, ResponseGenerator

# Your review here
my_review = "Put your customer review here!"

# Initialize models
print("Loading models...")
sentiment = SentimentAnalyzer()
emotion = EmotionDetector()
generator = ResponseGenerator()

# Analyze
print(f"\nReview: {my_review}\n")

sent = sentiment.analyze(my_review)
print(f"Sentiment: {sent['label']} ({sent['score']:.0%})")

emot = emotion.detect(my_review)
print(f"Emotion: {emot['primary_emotion']}")

resp = generator.generate(my_review, sent['label'], emot['primary_emotion'])
print(f"\nAI Response: {resp['response']}")
```

Run it:
```bash
python test_my_review.py
```

## ⏱️ Performance Tips

### Speed Up Loading (Use Smaller Models)
Edit the model names in each file:

**sentiment_analyzer.py:**
```python
# Change from:
model_name="cardiffnlp/twitter-roberta-base-sentiment-latest"
# To:
model_name="distilbert-base-uncased-finetuned-sst-2-english"
```

**response_generator.py:**
```python
# Change from:
model_name="google/flan-t5-base"
# To:
model_name="google/flan-t5-small"  # Faster but less accurate
```

### Use GPU (if available)
Models automatically use GPU if CUDA is available. Check with:
```python
import torch
print(f"GPU Available: {torch.cuda.is_available()}")
```

## 🐛 Troubleshooting

### Issue: "No module named 'transformers'"
```bash
pip install transformers torch
```

### Issue: "CUDA out of memory"
Models will automatically fall back to CPU. Or use smaller models (see Performance Tips).

### Issue: Models downloading slowly
First run downloads ~2GB. Be patient! Models are cached for future use.

### Issue: "ImportError: cannot import name 'SentimentAnalyzer'"
Make sure you're in the right directory:
```bash
cd /Users/tarang/CascadeProjects/windsurf-project/RevuIQ
python -c "from nlp_pipeline import SentimentAnalyzer; print('Success!')"
```

## 📊 What's Next?

1. ✅ **You are here** - NLP Pipeline working
2. 🔄 **Phase 2** - Build FastAPI backend
3. 🎨 **Phase 3** - Create Next.js dashboard
4. 🔌 **Phase 4** - Integrate with Google/Yelp APIs

## 🎓 Learning Resources

- **Hugging Face Docs**: https://huggingface.co/docs
- **Transformers Tutorial**: https://huggingface.co/course
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Next.js Docs**: https://nextjs.org/docs

## 💡 Tips

- Start with the demo to see everything working
- Test individual components to understand each part
- Modify prompts in `response_generator.py` to match your brand voice
- Adjust thresholds in `emotion_detector.py` for sensitivity

---

**Need help?** Check the main README.md or create an issue!

**Ready to build?** Let's move to Phase 2 - Backend API! 🚀
