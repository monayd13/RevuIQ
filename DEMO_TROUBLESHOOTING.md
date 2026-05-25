# RevuIQ Demo - Troubleshooting Guide

## 🚨 **Before You Start**

### Pre-Demo Checklist (10 minutes before)

- [ ] Backend is running on port 8000
  ```bash
  cd backend
  python3 working_nlp_api.py
  ```

- [ ] Frontend is running on port 3000
  ```bash
  cd frontend
  npm run dev
  ```

- [ ] Database has sample data
  ```bash
  sqlite3 backend/revuiq.db "SELECT COUNT(*) FROM reviews;"
  ```

- [ ] Browser is open to `http://localhost:3000`

- [ ] All other tabs closed (clean demo)

- [ ] Internet connection is stable (for Google API)

- [ ] Have backup plan ready (sample reviews button)

---

## ⚠️ **Common Issues & Solutions**

### Issue 1: Backend Not Running

**Symptom:** "Failed to connect to backend" error

**Solution:**
```bash
cd /Users/tarang/CascadeProjects/windsurf-project/RevuIQ/backend
python3 working_nlp_api.py
```

**What to Say:**
"Let me quickly restart the backend service - this demonstrates the importance of monitoring in production systems."

---

### Issue 2: Frontend Not Loading

**Symptom:** Page won't load or shows error

**Solution:**
```bash
cd /Users/tarang/CascadeProjects/windsurf-project/RevuIQ/frontend
npm run dev
```

**What to Say:**
"While this loads, let me explain the architecture - we have a React frontend and FastAPI backend..."

---

### Issue 3: Google API Fetch Fails

**Symptom:** "No reviews found" or API error

**Solution:**
- Click "Add Sample Reviews" instead
- This loads 15 pre-made personalized reviews

**What to Say:**
"For this demo, I'll use our sample data which shows the full functionality. In production, this would fetch live Google reviews."

---

### Issue 4: Reviews Not Showing in Analytics

**Symptom:** Analytics page is empty

**Solution:**
1. Check if reviews were actually created
2. Refresh the page
3. Click "View Analytics" again

**What to Say:**
"Let me refresh to ensure we're seeing the latest data - real-time updates are crucial for restaurant managers."

---

### Issue 5: Slow Loading

**Symptom:** Everything is slow

**Solution:**
- Close other applications
- Use sample reviews instead of API fetch
- Skip to already-loaded data

**What to Say:**
"In production, this would be optimized with caching and CDN delivery. For the demo, let me show you the results..."

---

### Issue 6: Database is Empty

**Symptom:** No restaurants or reviews

**Solution:**
```bash
cd backend
# Re-run the reanalyze endpoint
curl -X POST http://localhost:3005/api/reviews/reanalyze-all
```

Or just add a restaurant and use "Add Sample Reviews"

**What to Say:**
"Let me quickly set up a restaurant - this is what a new user would do on their first login."

---

## 🎯 **Backup Demo Plan**

If everything fails, have these ready:

### Option 1: Screenshots
- Take screenshots of each page beforehand
- Walk through screenshots instead of live demo
- Still explain functionality

### Option 2: Video Recording
- Record a successful demo run
- Play video if live demo fails
- Can pause and explain

### Option 3: Slide Deck
- Create PowerPoint with screenshots
- Add annotations and explanations
- Professional fallback option

---

## 💡 **Quick Fixes During Demo**

### If a button doesn't work:
"Let me try that again - sometimes there's a slight delay..."
*[Click again or refresh]*

### If data looks wrong:
"This is test data for demonstration purposes. In production, this would show real customer reviews."

### If you forget what to say:
"Let me show you something interesting here..."
*[Look at quick reference card]*

### If you go over time:
"I'll skip ahead to the most important part - the analytics dashboard..."

### If you finish early:
"Let me show you some additional features..."
*[Dive deeper into any section]*

---

## 🔧 **Emergency Commands**

### Restart Everything:
```bash
# Kill all processes
pkill -f "python3 working_nlp_api.py"
pkill -f "next"

# Restart backend
cd /Users/tarang/CascadeProjects/windsurf-project/RevuIQ/backend
python3 working_nlp_api.py &

# Restart frontend
cd /Users/tarang/CascadeProjects/windsurf-project/RevuIQ/frontend
npm run dev &
```

### Check if Services are Running:
```bash
# Check backend
curl http://localhost:3005/api/restaurants

# Check frontend
curl http://localhost:3000
```

### Reset Database (LAST RESORT):
```bash
cd backend
rm revuiq.db
python3 working_nlp_api.py
# Then add sample data again
```

---

## 🎤 **Professional Recovery Phrases**

### When something breaks:
- "Let me address this quickly - in production, we have error handling for this..."
- "This is actually a great opportunity to show our fallback system..."
- "Technical difficulties aside, the key point is..."

### When you need time:
- "While this loads, let me explain the technology behind it..."
- "This is a good moment to discuss the business value..."
- "Let me show you something else while that processes..."

### When you make a mistake:
- "Let me correct that - what I meant to show you is..."
- "Actually, there's a better way to demonstrate this..."
- "Let me navigate back and show you the proper workflow..."

---

## ✅ **Post-Demo Checklist**

After the demo:
- [ ] Thank the audience
- [ ] Ask for questions
- [ ] Provide contact information
- [ ] Offer to send demo link/materials
- [ ] Get feedback for improvement

---

## 📞 **Emergency Contacts**

If you need help during setup:
- Check the README.md for setup instructions
- Review the DEMO_SCRIPT.md for talking points
- Use DEMO_QUICK_REFERENCE.md for key phrases

---

## 🎯 **Remember**

1. **Stay calm** - Technical issues happen
2. **Keep talking** - Don't let silence fill the room
3. **Focus on value** - Even if demo fails, explain the benefits
4. **Be honest** - "This is a prototype" is okay to say
5. **Smile** - Confidence is contagious

---

**You're prepared for anything! Go crush that demo! 💪**
