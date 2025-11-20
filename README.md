# RevuIQ

Analyze restaurant reviews and track customer sentiment.

## What it does

Pulls reviews from Google Places and analyzes them to understand what customers think. Shows sentiment (positive/negative), common topics mentioned, and overall ratings.

## Features

- Fetch real reviews from Google Places API
- Sentiment analysis (positive, neutral, negative)
- Emotion detection
- Analytics dashboard with charts
- Filter reviews by time period

## Tech

- Backend: FastAPI + SQLite
- Frontend: Next.js + TailwindCSS
- Charts: Recharts
- Icons: Lucide React

## Setup

1. Get a Google Places API key from Google Cloud Console
2. Add it to `backend/.env`:
   ```
   GOOGLE_PLACES_API_KEY=your_key_here
   ```
3. Run the startup script:
   ```bash
   ./start_all.sh
   ```

## Usage

After starting the services:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

Add restaurants, fetch their Google reviews, and view analytics.

## Scripts

- `./start_all.sh` - Start both backend and frontend
- `./stop_all.sh` - Stop all services
- `./check_status.sh` - Check if services are running

## Notes

- Google Places API only returns 5 reviews per restaurant
- Reviews are analyzed using mock NLP (simplified version)
- Database is SQLite stored in `backend/revuiq.db`
