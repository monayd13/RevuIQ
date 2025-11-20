# 🆓 Yelp API Setup - FREE Real Reviews (No Credit Card!)

## ✅ Why Yelp?
- **100% FREE** - No credit card required
- **5,000 API calls per day** - More than enough
- **Real restaurant reviews** - Actual customer feedback
- **Easy setup** - Takes 2 minutes

---

## 📝 Step-by-Step Setup

### 1. Create a Yelp Developer Account (FREE)
1. Go to: https://www.yelp.com/developers
2. Click **"Get Started"** or **"Create App"**
3. Sign up with your email (or use existing Yelp account)
4. **No credit card required!**

### 2. Create an App
1. After logging in, click **"Create New App"**
2. Fill in the form:
   - **App Name**: RevuIQ (or any name)
   - **Industry**: Technology
   - **Company**: Your name or "Personal Project"
   - **Website**: http://localhost:3000 (or leave blank)
   - **Description**: "Review management system for learning"
3. Agree to terms and click **"Create App"**

### 3. Get Your API Key
1. You'll see your app dashboard
2. Copy the **"API Key"** (long string starting with your app name)
3. Keep this safe!

### 4. Add to Your .env File
1. Open `/RevuIQ/.env` file
2. Add this line:
   ```
   YELP_API_KEY=your_api_key_here
   ```
3. Replace `your_api_key_here` with your actual API key
4. Save the file

### 5. Restart Backend
```bash
cd RevuIQ/backend
python main_production.py
```

You should see:
```
✅ Yelp API loaded! (FREE - No credit card needed)
```

---

## 🎯 How to Use

### In the Restaurant Page:
1. Add a restaurant (e.g., "Olive Garden", "New York")
2. Click **"Fetch Reviews"**
3. Real reviews will be fetched from Yelp!

### What You Get:
- Up to 50 reviews per restaurant
- Real customer ratings (1-5 stars)
- Actual review text
- Author names and dates
- **All FREE!**

---

## 🔧 Troubleshooting

### "No API key found"
- Make sure you added `YELP_API_KEY=...` to `.env`
- Restart the backend server
- Check there are no spaces around the `=`

### "API Error: 401"
- Your API key might be wrong
- Copy it again from Yelp dashboard
- Make sure you copied the entire key

### "Business not found"
- Try adding a location (e.g., "New York, NY")
- Use the exact business name
- Try a more famous restaurant first

---

## 📊 API Limits (FREE Tier)

- **5,000 calls per day** - That's a lot!
- **50 reviews per request** - Plenty of data
- **No expiration** - Use it forever
- **No credit card** - Ever!

---

## 🆚 Yelp vs Google Places

| Feature | Yelp (FREE) | Google Places |
|---------|-------------|---------------|
| Credit Card | ❌ Not Required | ✅ Required |
| Cost | 🆓 FREE | 💳 Requires billing |
| Reviews per call | 50 | 5 |
| Daily limit | 5,000 | Varies |
| Setup time | 2 minutes | 10 minutes |

**Winner: Yelp!** 🏆

---

## 🎉 You're All Set!

Your RevuIQ system now fetches **real restaurant reviews** from Yelp - completely FREE, no credit card needed!

Try it now:
1. Go to http://localhost:3000/restaurants
2. Add "Olive Garden" in "New York"
3. Click "Fetch Reviews"
4. Watch real reviews appear! ✨

---

## 💡 Pro Tips

1. **Search works best with:**
   - Famous restaurant chains (Olive Garden, Chipotle, etc.)
   - Specific locations (New York, Los Angeles, etc.)
   - Exact business names

2. **Save your API key:**
   - Don't share it publicly
   - Don't commit it to Git
   - It's already in `.gitignore`

3. **Need more reviews?**
   - Yelp returns up to 50 reviews per business
   - That's usually enough for analysis
   - Completely free!

---

## 🚀 Next Steps

- Try different restaurants
- Analyze sentiment of real reviews
- Build your review database
- All with real data, for FREE!

Enjoy! 🎊
