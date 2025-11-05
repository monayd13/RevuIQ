# 🎨 RevuIQ Dashboard Design

## Overview
Modern, responsive dashboard for managing customer reviews across multiple platforms.

## Tech Stack
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui
- **Charts**: Recharts
- **Icons**: Lucide React
- **State**: React Context + Hooks

## Pages & Routes

### 1. Dashboard Home (`/`)
**Purpose**: Overview of all review activity

**Components**:
- Summary cards (Total Reviews, Avg Sentiment, Response Rate)
- Sentiment trend chart (last 30 days)
- Recent reviews list
- Platform breakdown pie chart

### 2. Reviews (`/reviews`)
**Purpose**: Manage all reviews

**Features**:
- Filter by platform, sentiment, status
- Search reviews
- Bulk actions
- Pagination

**Review Card Shows**:
- Platform icon
- Star rating
- Review text (truncated)
- Sentiment badge
- Emotion tags
- AI-generated response
- Action buttons (Approve, Edit, Reject)

### 3. Review Detail (`/reviews/[id]`)
**Purpose**: Full review analysis and response management

**Sections**:
- Review metadata (date, platform, customer)
- Full review text
- NLP Analysis:
  - Sentiment score with confidence
  - Emotion breakdown
  - Aspect extraction (service, food, price, etc.)
- AI Response:
  - Generated reply
  - Edit interface
  - Tone selector
  - Regenerate button
- Action buttons:
  - Approve & Post
  - Save Draft
  - Reject

### 4. Analytics (`/analytics`)
**Purpose**: Data insights and trends

**Visualizations**:
- Sentiment over time (line chart)
- Platform comparison (bar chart)
- Emotion distribution (radar chart)
- Top keywords (word cloud)
- Response time metrics
- Approval rate stats

**Filters**:
- Date range picker
- Platform selector
- Location filter (if multi-location)

### 5. Settings (`/settings`)
**Purpose**: Configuration and preferences

**Sections**:
- API Keys (Google, Yelp, Meta)
- Business Information
- Response Templates
- Notification Preferences
- Team Members
- Brand Voice Settings

## Color Scheme

```css
/* Primary Colors */
--primary: #3B82F6 (Blue)
--secondary: #8B5CF6 (Purple)
--accent: #10B981 (Green)

/* Sentiment Colors */
--positive: #10B981 (Green)
--neutral: #F59E0B (Amber)
--negative: #EF4444 (Red)

/* Background */
--bg-primary: #FFFFFF
--bg-secondary: #F9FAFB
--bg-dark: #111827

/* Text */
--text-primary: #111827
--text-secondary: #6B7280
--text-muted: #9CA3AF
```

## Component Library

### Core Components

1. **ReviewCard**
   - Compact view for lists
   - Shows key info
   - Quick actions

2. **SentimentBadge**
   - Color-coded
   - Shows emoji + label
   - Confidence indicator

3. **EmotionTags**
   - Pill-style tags
   - Color-coded by emotion
   - Percentage display

4. **ResponseEditor**
   - Rich text editor
   - Tone selector
   - Character counter
   - Preview mode

5. **StatCard**
   - Number display
   - Trend indicator
   - Icon
   - Sparkline (optional)

6. **PlatformIcon**
   - Google, Yelp, TripAdvisor, Meta logos
   - Consistent sizing
   - Hover effects

### Chart Components

1. **SentimentTrendChart** (Line)
2. **PlatformBreakdownChart** (Pie/Donut)
3. **EmotionRadarChart** (Radar)
4. **ResponseTimeChart** (Bar)

## Layout Structure

```
┌─────────────────────────────────────────────┐
│  Header (Logo, Search, Notifications, User) │
├──────┬──────────────────────────────────────┤
│      │                                      │
│      │                                      │
│ Side │         Main Content Area            │
│ Nav  │                                      │
│      │                                      │
│      │                                      │
├──────┴──────────────────────────────────────┤
│              Footer (optional)              │
└─────────────────────────────────────────────┘
```

## Responsive Breakpoints

- **Mobile**: < 640px (Hamburger menu)
- **Tablet**: 640px - 1024px (Collapsible sidebar)
- **Desktop**: > 1024px (Full sidebar)

## Key Features

### Human-in-the-Loop Workflow

```
Review Received
    ↓
AI Analysis (Sentiment, Emotion, Aspects)
    ↓
AI Response Generated
    ↓
[Dashboard Shows Review Card]
    ↓
Manager Reviews:
  - Read original review
  - See AI analysis
  - Review AI response
    ↓
Manager Actions:
  ✅ Approve → Post to platform
  ✏️  Edit → Modify response → Approve
  🔄 Regenerate → Get new AI response
  ❌ Reject → Don't respond
```

### Real-time Updates

- WebSocket connection for new reviews
- Toast notifications
- Badge counts update automatically

### Keyboard Shortcuts

- `Cmd/Ctrl + K`: Quick search
- `A`: Approve selected review
- `E`: Edit response
- `R`: Reject
- `N`: Next review
- `P`: Previous review

## Mock Data Structure

```typescript
interface Review {
  id: string;
  platform: 'google' | 'yelp' | 'tripadvisor' | 'meta';
  businessName: string;
  customerName: string;
  rating: number; // 1-5
  text: string;
  timestamp: Date;
  
  // NLP Analysis
  sentiment: {
    label: 'POSITIVE' | 'NEUTRAL' | 'NEGATIVE';
    score: number; // 0-1
  };
  
  emotions: Array<{
    label: string;
    score: number;
  }>;
  
  aspects: Array<{
    category: string; // 'service', 'food', 'price', etc.
    sentiment: 'positive' | 'neutral' | 'negative';
  }>;
  
  // AI Response
  aiResponse: {
    text: string;
    tone: string;
    generatedAt: Date;
  };
  
  // Status
  status: 'pending' | 'approved' | 'rejected' | 'posted';
  approvedBy?: string;
  approvedAt?: Date;
  postedAt?: Date;
}
```

## Next Steps

1. ✅ Set up Next.js project
2. Install dependencies (shadcn/ui, Recharts, Lucide)
3. Create layout components
4. Build dashboard home page
5. Implement review list and detail pages
6. Add analytics visualizations
7. Connect to backend API (Phase 2)

## Design Inspiration

- **Vercel Dashboard**: Clean, modern
- **Linear**: Smooth animations
- **Notion**: Intuitive UX
- **Stripe Dashboard**: Data visualization

---

**Goal**: Create a beautiful, intuitive dashboard that makes review management effortless! 🎨✨
