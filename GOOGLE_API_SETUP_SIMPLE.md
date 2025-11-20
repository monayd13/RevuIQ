# 🔑 Google Places API Setup Guide

## Quick Setup (5 minutes)

### Step 1: Get Your API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable **Places API**:
   - Click "Enable APIs and Services"
   - Search for "Places API"
   - Click "Enable"
4. Create API Key:
   - Go to "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy your API key

### Step 2: Add to Your Project

Create or edit `.env` file in the `backend/` directory:

```bash
cd /Users/tarang/CascadeProjects/windsurf-project/RevuIQ/backend
nano .env
```

Add this line:
```
GOOGLE_PLACES_API_KEY=YOUR_API_KEY_HERE
```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 3: Restart Backend

```bash
# Kill the current backend
lsof -ti:8000 | xargs kill -9

# Start again
python3 simple_api.py
```

### Step 4: Test It!

1. Go to http://localhost:3000/restaurants
2. Add a restaurant (e.g., "Olive Garden" or "McDonald's")
3. Click **"Fetch from Google"** button
4. Wait 5-10 seconds
5. Click "View Analytics" to see real Google reviews!

---

## 🎯 How It Works

When you click "Fetch from Google":

1. **Search**: Finds the restaurant on Google Places
2. **Fetch**: Gets up to 5 real reviews
3. **Analyze**: Runs NLP analysis (sentiment, emotions, aspects)
4. **Store**: Saves to database
5. **Display**: Shows in analytics dashboard

---

## 💡 Tips

### Free Tier Limits
- Google gives you **$200 free credit** per month
- Each request costs ~$0.017
- You can make ~11,000 requests/month for free

### Best Practices
1. **Use specific names**: "Olive Garden Times Square" better than "Olive Garden"
2. **Add location**: Helps find the right restaurant
3. **Check results**: First time, verify it found the right place

### Troubleshooting

**"No reviews found"**
- Check API key is correct in `.env`
- Make sure backend restarted after adding key
- Try a more specific restaurant name
- Check Google Cloud Console for API errors

**"API key not configured"**
- Make sure `.env` file exists in `backend/` folder
- Check spelling: `GOOGLE_PLACES_API_KEY` (exact)
- Restart backend after adding key

**"Restaurant not found"**
- Try adding location: "McDonald's New York"
- Use full name: "The Cheesecake Factory" not "Cheesecake"
- Check if restaurant exists on Google Maps

---

## 🔒 Security

**Important**: Never commit your API key to Git!

The `.env` file is already in `.gitignore`, but double-check:

```bash
# Make sure .env is ignored
cat .gitignore | grep .env
```

If not there, add it:
```bash
echo ".env" >> .gitignore
```

---

## 📊 What You Get

Each Google review includes:
- ⭐ **Rating** (1-5 stars)
- 📝 **Review text**
- 👤 **Author name**
- 📅 **Date posted**
- 🤖 **Auto NLP analysis**:
  - Sentiment (positive/neutral/negative)
  - Emotions (joy, anger, gratitude, etc.)
  - Aspects (food, service, ambiance, price)
  - AI-generated response

---

## 🚀 Example Usage

### Test with a Famous Restaurant

```bash
# In your browser:
1. Add restaurant: "The French Laundry"
2. Location: "Yountville, CA"
3. Click "Fetch from Google"
4. View Analytics → See real reviews!
```

### Command Line Test

```bash
cd backend
python3 google_places_integration.py "Olive Garden" "New York"
```

This will show you what the API returns before storing in database.

---

## 📈 Next Steps

Once you have Google working:

1. **Try different restaurants**
   - Local favorites
   - Chain restaurants
   - Fine dining

2. **Compare analytics**
   - See which have better sentiment
   - Check emotion patterns
   - Identify common aspects

3. **Add more platforms**
   - Yelp Fusion API
   - TripAdvisor
   - Facebook reviews

---

## ❓ FAQ

**Q: Do I need a credit card?**
A: Yes, but you won't be charged unless you exceed $200/month.

**Q: How many reviews can I fetch?**
A: Google returns up to 5 reviews per restaurant (API limitation).

**Q: Can I get more reviews?**
A: Not through the free API. You'd need to use web scraping (against ToS) or paid services.

**Q: Will this work for any restaurant?**
A: Only restaurants that exist on Google Maps with reviews.

**Q: Can I fetch reviews for multiple locations?**
A: Yes! Just add each location as a separate restaurant.

---

**Need help?** Check the main `GOOGLE_API_SETUP.md` for detailed troubleshooting.
