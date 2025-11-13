# 🔑 Google Places API Setup Guide

Complete guide to get real restaurant reviews from Google Places API

---

## 🎯 What You'll Get

With Google Places API, you can:
- ✅ Search for any restaurant by name
- ✅ Get real customer reviews
- ✅ See ratings, author names, and timestamps
- ✅ Analyze sentiment automatically
- ✅ Build beautiful dashboards

---

## 📋 Step 1: Get Google API Key

### **1.1 Go to Google Cloud Console**
Visit: https://console.cloud.google.com

### **1.2 Create a New Project**
1. Click "Select a project" at the top
2. Click "NEW PROJECT"
3. Name it: "RevuIQ" or "Restaurant Reviews"
4. Click "CREATE"

### **1.3 Enable Places API**
1. Go to "APIs & Services" → "Library"
2. Search for "Places API"
3. Click on "Places API"
4. Click "ENABLE"

### **1.4 Create API Key**
1. Go to "APIs & Services" → "Credentials"
2. Click "CREATE CREDENTIALS" → "API key"
3. Copy the API key (looks like: `AIzaSyD...`)
4. Click "RESTRICT KEY" (recommended)
5. Under "API restrictions", select "Restrict key"
6. Choose "Places API"
7. Click "SAVE"

---

## 📝 Step 2: Add API Key to Project

### **2.1 Create .env File**

In the `RevuIQ` folder, create a file named `.env`:

```bash
cd /Users/tarang/CascadeProjects/windsurf-project/RevuIQ
touch .env
```

### **2.2 Add Your API Key**

Open `.env` and add:

```env
GOOGLE_PLACES_API_KEY=your_actual_api_key_here
```

Replace `your_actual_api_key_here` with the key you copied.

**Example:**
```env
GOOGLE_PLACES_API_KEY=AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### **2.3 Install Required Package**

```bash
pip install python-dotenv requests
```

---

## 🚀 Step 3: Run the Application

### **3.1 Start Backend**

```bash
cd backend
python main_production.py
```

You should see:
```
🚀 Starting RevuIQ API Server (Production)
📊 NLP Engine: TextBlob (Fast & Reliable)
🌐 Server: http://localhost:8000
```

### **3.2 Start Frontend**

In a new terminal:

```bash
cd frontend
npm run dev
```

You should see:
```
▲ Next.js 16.0.1
- Local: http://localhost:3000
```

---

## 🎨 Step 4: Use the Dashboard

### **4.1 Open Reviews Dashboard**

Go to: http://localhost:3000/reviews

### **4.2 Search for a Restaurant**

Try these examples:
- **Restaurant Name:** "Olive Garden"
- **Location:** "New York, NY"

Or:
- **Restaurant Name:** "McDonald's"
- **Location:** "Los Angeles, CA"

Or:
- **Restaurant Name:** "The French Laundry"
- **Location:** "Yountville, CA"

### **4.3 Click "Fetch Reviews"**

The dashboard will:
1. ✅ Search Google for the restaurant
2. ✅ Fetch real customer reviews
3. ✅ Display ratings and sentiment
4. ✅ Show statistics and charts

---

## 📊 What You'll See

### **Stats Cards:**
- Total Reviews
- Average Rating (⭐)
- Positive Reviews (4-5 stars)
- Negative Reviews (1-2 stars)

### **Sentiment Distribution:**
- Visual bar charts
- Percentage breakdown
- Color-coded (green/yellow/red)

### **Reviews List:**
- Full review text
- Star ratings
- Author names
- Timestamps
- Sentiment labels

---

## 🧪 Testing Without API Key

If you don't have an API key yet, the system will automatically use **demo mode** with sample reviews.

You'll see a note:
```
ℹ️ Demo mode - Add GOOGLE_PLACES_API_KEY to .env for real reviews
```

---

## 💰 Pricing (Google Places API)

### **Free Tier:**
- **$200 free credit** per month
- Enough for **~40,000 requests**
- Perfect for development and testing

### **After Free Tier:**
- Place Search: $0.032 per request
- Place Details: $0.017 per request
- Very affordable for most use cases

**Tip:** Set up billing alerts in Google Cloud Console to monitor usage.

---

## 🔒 Security Best Practices

### **1. Never Commit .env File**

The `.gitignore` already excludes it, but double-check:

```bash
# Make sure .env is in .gitignore
echo ".env" >> .gitignore
```

### **2. Restrict API Key**

In Google Cloud Console:
- ✅ Restrict to "Places API" only
- ✅ Add IP restrictions (optional)
- ✅ Add HTTP referrer restrictions (for production)

### **3. Use Environment Variables**

Never hardcode API keys in your code!

---

## 🐛 Troubleshooting

### **Problem: "No API key found"**

**Solution:**
1. Check `.env` file exists in RevuIQ folder
2. Check spelling: `GOOGLE_PLACES_API_KEY`
3. Restart backend after adding key

### **Problem: "API key not valid"**

**Solution:**
1. Check you enabled "Places API" in Google Cloud
2. Wait 5 minutes after creating key
3. Check for extra spaces in `.env` file

### **Problem: "Restaurant not found"**

**Solution:**
1. Try adding location (e.g., "New York, NY")
2. Use full restaurant name
3. Try a well-known chain (e.g., "Starbucks")

### **Problem: "Quota exceeded"**

**Solution:**
1. Check usage in Google Cloud Console
2. You may have hit the free tier limit
3. Enable billing or wait for next month

---

## 📁 File Structure

```
RevuIQ/
├── .env                              # ← Add your API key here
├── backend/
│   ├── main_production.py           # ← Backend server
│   └── simple_google_reviews.py     # ← Google API integration
└── frontend/
    └── app/
        └── reviews/
            └── page.tsx              # ← Dashboard page
```

---

## 🎯 Quick Start Commands

```bash
# 1. Add API key to .env
echo "GOOGLE_PLACES_API_KEY=your_key_here" > .env

# 2. Install dependencies
pip install python-dotenv requests

# 3. Start backend
cd backend && python main_production.py

# 4. Start frontend (new terminal)
cd frontend && npm run dev

# 5. Open dashboard
open http://localhost:3000/reviews
```

---

## 🎉 Success Checklist

- [ ] Created Google Cloud project
- [ ] Enabled Places API
- [ ] Created and restricted API key
- [ ] Added key to `.env` file
- [ ] Installed python-dotenv and requests
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Dashboard accessible at /reviews
- [ ] Successfully fetched real reviews

---

## 🚀 Next Steps

Once you have real reviews:

1. **Analyze Sentiment** - Use the /analyze page
2. **View Analytics** - Check /analytics page
3. **Generate Responses** - AI-powered replies
4. **Export Data** - Download reviews as CSV
5. **Deploy** - Put it in production!

---

## 📞 Need Help?

Check these resources:
- Google Places API Docs: https://developers.google.com/maps/documentation/places/web-service
- RevuIQ README: `README.md`
- Quick Start: `START_HERE.md`

---

**Status:** ✅ Ready to fetch real restaurant reviews!

**Estimated Setup Time:** 10-15 minutes
