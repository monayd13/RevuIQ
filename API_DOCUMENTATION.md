# RevuIQ API Documentation

Base URL: `http://localhost:8000`

## Health Check

### GET /health
Check API health status

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-25T05:14:42.011133",
  "mode": "simple",
  "models_loaded": false
}
```

---

## Restaurant Management

### GET /api/restaurants
Get all restaurants

**Response:**
```json
{
  "success": true,
  "count": 2,
  "restaurants": [
    {
      "id": 1,
      "name": "Pizza Palace",
      "industry": "restaurant",
      "created_at": "2025-11-25T05:00:00",
      "review_count": 15
    }
  ]
}
```

### POST /api/restaurants
Create a new restaurant

**Request Body:**
```json
{
  "name": "Pizza Palace",
  "industry": "restaurant"
}
```

**Response:**
```json
{
  "success": true,
  "restaurant_id": 1,
  "message": "Restaurant created successfully"
}
```

### GET /api/restaurants/{id}
Get restaurant details

**Response:**
```json
{
  "success": true,
  "restaurant": {
    "id": 1,
    "name": "Pizza Palace",
    "industry": "restaurant",
    "created_at": "2025-11-25T05:00:00",
    "stats": {
      "total_reviews": 15,
      "average_rating": 4.2,
      "sentiment_distribution": {
        "POSITIVE": 10,
        "NEUTRAL": 3,
        "NEGATIVE": 2
      }
    }
  }
}
```

### DELETE /api/restaurants/{id}
Delete a restaurant and all its reviews

**Response:**
```json
{
  "success": true,
  "message": "Restaurant 'Pizza Palace' and all its reviews deleted successfully"
}
```

---

## Review Management

### POST /api/reviews
Create a single review with NLP analysis

**Request Body:**
```json
{
  "platform": "google",
  "platform_review_id": "review_123",
  "business_id": 1,
  "author_name": "John Doe",
  "rating": 5.0,
  "text": "Amazing food and service!",
  "review_date": "2025-11-25T05:00:00"
}
```

**Response:**
```json
{
  "success": true,
  "review_id": 1,
  "analysis": {
    "sentiment": {
      "label": "POSITIVE",
      "score": 0.95
    },
    "emotions": {
      "joy": 0.8,
      "gratitude": 0.6
    },
    "aspects": ["food", "service"],
    "ai_response": "Thank you for your wonderful feedback! We're thrilled you enjoyed our food and service."
  }
}
```

### POST /api/reviews/bulk
Create multiple reviews at once

**Request Body:**
```json
{
  "business_id": 1,
  "reviews": [
    {
      "platform": "google",
      "platform_review_id": "review_1",
      "author_name": "John Doe",
      "rating": 5.0,
      "text": "Great food!",
      "review_date": "2025-11-25T05:00:00"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "created": 15,
  "skipped": 0,
  "message": "Created 15 reviews successfully"
}
```

### GET /api/reviews/restaurant/{id}
Get all reviews for a restaurant

**Query Parameters:**
- `skip` (optional): Number of reviews to skip (default: 0)
- `limit` (optional): Max reviews to return (default: 100)

**Response:**
```json
{
  "success": true,
  "count": 15,
  "reviews": [
    {
      "id": 1,
      "platform": "google",
      "author": "John Doe",
      "rating": 5.0,
      "text": "Amazing food!",
      "date": "2025-11-25T05:00:00",
      "sentiment": "POSITIVE",
      "sentiment_score": 0.95,
      "emotions": "{\"joy\": 0.8}",
      "ai_response": "Thank you for your feedback!"
    }
  ]
}
```

---

## Review Approval

### GET /api/reviews/pending
Get all reviews pending approval

**Response:**
```json
{
  "success": true,
  "count": 5,
  "reviews": [
    {
      "id": 1,
      "business_id": 1,
      "author": "John Doe",
      "rating": 5.0,
      "text": "Great food!",
      "review_date": "2025-11-25T05:00:00",
      "sentiment": "POSITIVE",
      "sentiment_score": 0.95,
      "primary_emotion": "joy",
      "created_at": "2025-11-25T05:00:00",
      "approval_status": "pending"
    }
  ]
}
```

### POST /api/reviews/{id}/approve
Approve or reject a review

**Request Body:**
```json
{
  "is_genuine": true,
  "approval_notes": "Verified as genuine review",
  "approved_by": "admin"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Review approved successfully",
  "review_id": 1,
  "status": "approved"
}
```

### GET /api/reviews/stats
Get review approval statistics

**Response:**
```json
{
  "success": true,
  "stats": {
    "total": 20,
    "pending": 5,
    "approved": 12,
    "rejected": 3
  }
}
```

---

## Response Approval

### GET /api/responses/pending
Get AI responses pending human approval

**Response:**
```json
{
  "success": true,
  "count": 3,
  "reviews": [
    {
      "id": 1,
      "business_id": 1,
      "author": "John Doe",
      "rating": 5.0,
      "text": "Great food!",
      "review_date": "2025-11-25T05:00:00",
      "sentiment": "POSITIVE",
      "ai_response": "Thank you for your feedback!",
      "response_tone": "professional",
      "human_approved": false,
      "final_response": null,
      "response_posted": false
    }
  ]
}
```

### POST /api/responses/{id}/approve
Approve or reject an AI-generated response

**Request Body:**
```json
{
  "approved": true,
  "final_response": "Thank you so much for your wonderful feedback!",
  "approved_by": "admin"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Response approved and ready to post",
  "review_id": 1,
  "approved": true
}
```

### GET /api/responses/stats
Get response approval statistics

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_with_ai_response": 15,
    "pending_approval": 3,
    "approved": 10,
    "posted": 2
  }
}
```

---

## Google Places Integration

### POST /api/google/fetch-reviews
Fetch reviews from Google Places API

**Request Body:**
```json
{
  "restaurant_name": "Pizza Palace",
  "location": "New York, NY",
  "business_id": 1
}
```

**Response:**
```json
{
  "success": true,
  "created": 5,
  "skipped": 0,
  "total_fetched": 5,
  "message": "Fetched 5 reviews from Google Places"
}
```

**Note:** Google Places API returns maximum 5 reviews per restaurant.

### GET /api/google/restaurant-info
Get restaurant information from Google Places

**Query Parameters:**
- `restaurant_name` (required): Name of the restaurant
- `location` (optional): Location to narrow search

**Response:**
```json
{
  "success": true,
  "info": {
    "name": "Pizza Palace",
    "address": "123 Main St, New York, NY",
    "rating": 4.5,
    "total_ratings": 250,
    "types": ["restaurant", "food"],
    "place_id": "ChIJ..."
  }
}
```

---

## Analytics

### GET /api/analytics/restaurant/{id}
Get analytics for a specific restaurant

**Query Parameters:**
- `days` (optional): Number of days to analyze (default: 30)

**Response:**
```json
{
  "success": true,
  "restaurant_id": 1,
  "period_days": 30,
  "total_reviews": 15,
  "average_rating": 4.2,
  "sentiment_distribution": {
    "POSITIVE": 10,
    "NEUTRAL": 3,
    "NEGATIVE": 2
  },
  "emotion_distribution": {
    "joy": 8,
    "gratitude": 5,
    "disappointment": 2
  },
  "top_emotions": {
    "joy": 8,
    "gratitude": 5
  },
  "top_aspects": {
    "food": 12,
    "service": 10,
    "price": 5
  }
}
```

### GET /api/analytics/sentiment-distribution
Get global sentiment distribution

**Query Parameters:**
- `days` (optional): Number of days (default: 30)
- `business_id` (optional): Filter by restaurant

**Response:**
```json
{
  "success": true,
  "distribution": {
    "POSITIVE": 45,
    "NEUTRAL": 15,
    "NEGATIVE": 10
  },
  "total": 70
}
```

### GET /api/analytics/emotion-distribution
Get global emotion distribution

**Query Parameters:**
- `days` (optional): Number of days (default: 30)
- `business_id` (optional): Filter by restaurant

**Response:**
```json
{
  "success": true,
  "distribution": {
    "joy": 25,
    "gratitude": 20,
    "disappointment": 8,
    "anger": 5
  }
}
```

### GET /api/analytics/stats
Get overall statistics

**Response:**
```json
{
  "success": true,
  "total_reviews": 70,
  "total_restaurants": 5,
  "response_stats": {
    "total_reviews": 70,
    "approved_responses": 50,
    "posted_responses": 10,
    "approval_rate": 71.4,
    "post_rate": 14.3
  },
  "average_rating": 4.1
}
```

---

## Error Responses

All endpoints return errors in this format:

```json
{
  "detail": "Error message here"
}
```

Common HTTP status codes:
- `200` - Success
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

---

## Rate Limiting

Currently no rate limiting implemented. Recommended for production:
- 100 requests per minute per IP
- 1000 requests per hour per API key

---

## Authentication

Currently no authentication required. Recommended for production:
- JWT tokens
- API keys
- OAuth 2.0

---

**API Version:** 2.0.0  
**Last Updated:** November 25, 2025
