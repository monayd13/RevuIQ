# Review Approval Feature

## What's New

Added manual review approval system to verify if reviews are genuine or fake before including them in analytics.

## Features Added

### Backend (API)

**New Database Fields:**
- `is_genuine` - Boolean flag (True=genuine, False=fake, None=pending)
- `approval_status` - Status: "pending", "approved", "rejected"
- `approved_by` - Username who approved/rejected
- `approval_notes` - Notes about the decision
- `approved_at` - Timestamp of approval

**New API Endpoints:**
- `GET /api/reviews/pending` - Get all reviews waiting for approval
- `POST /api/reviews/{id}/approve` - Approve or reject a review
- `GET /api/reviews/stats` - Get approval statistics

### Frontend

**New Page: `/reviews/approve`**
- View all pending reviews
- See sentiment analysis and emotion detection
- Approve as genuine or reject as fake
- Real-time stats dashboard
- Beautiful UI with animations

**Dashboard Integration:**
- Added "Approve Reviews" card on main dashboard
- Quick access to approval page
- Shows pending count

## How to Use

1. **Go to Dashboard:** http://localhost:3000/dashboard
2. **Click "Approve Reviews"** card
3. **Review each submission:**
   - See author, rating, text
   - Check sentiment and emotion analysis
   - Click "Approve as Genuine" or "Reject as Fake"
4. **Track stats:**
   - Total reviews
   - Pending approvals
   - Approved count
   - Rejected count

## API Examples

### Get Pending Reviews
```bash
curl http://localhost:8000/api/reviews/pending
```

### Approve a Review
```bash
curl -X POST http://localhost:8000/api/reviews/123/approve \
  -H "Content-Type: application/json" \
  -d '{
    "is_genuine": true,
    "approval_notes": "Verified as genuine",
    "approved_by": "admin"
  }'
```

### Get Stats
```bash
curl http://localhost:8000/api/reviews/stats
```

## Database Migration

The database was automatically updated with new columns when you restarted the backend. All existing reviews default to "pending" status.

## Next Steps

You can now:
- Filter analytics to show only approved reviews
- Add bulk approval actions
- Add approval history tracking
- Add email notifications for new reviews
- Add approval workflow with multiple reviewers
