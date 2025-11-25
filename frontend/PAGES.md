# 📄 RevuIQ - Complete Page Structure

## 🗺️ Site Map

```
RevuIQ
├── / (Root) → Redirects to /home
├── /home (Landing Page)
├── /pricing (Pricing Plans)
├── /about (About Us)
├── /careers (Job Openings)
│   └── /apply (Application Form)
├── /login (Authentication)
└── /dashboard (Protected)
    ├── / (Main Dashboard)
    └── /analytics (Analytics & Insights)
```

---

## 📍 Page Details

### 1. **Home Page** (`/home`)
**Purpose**: Marketing landing page for new visitors

**Sections**:
- Hero with CTA buttons
- Features showcase (6 features)
- Call-to-action
- Footer

**Navigation**:
- Features (scroll to #features)
- Pricing → `/pricing`
- About → `/about`
- Sign in → `/login`
- Get Started → `/login`

---

### 2. **Pricing Page** (`/pricing`)
**Purpose**: Display pricing plans and features

**Content**:
- 3 Pricing tiers:
  - **Starter**: $29/month
  - **Professional**: $99/month (Most Popular)
  - **Enterprise**: $299/month
- FAQ section
- CTA to start free trial

**Features**:
- Detailed feature comparison
- 14-day free trial
- No credit card required

---

### 3. **About Page** (`/about`)
**Purpose**: Company information and mission

**Sections**:
- Mission statement
- Company stats (10K+ reviews, 500+ businesses)
- Core values (Customer First, Trust, Innovation)
- Technology stack (NLP models)
- Team information

---

### 4. **Careers Page** (`/careers`)
**Purpose**: Job openings and internship opportunities

**Content**:
- Company mission and stats
- Internship perks:
  - Certificate of Completion
  - Full-Time Conversion Opportunity
  - Expert Mentorship
  - Hands-on Experience

**Open Positions**:
1. **Backend Engineer Intern**
   - FastAPI, Python, PostgreSQL
   - NLP model integration
   - Unpaid internship

2. **Software Engineering Intern**
   - Next.js, React, Full-stack
   - UI/UX development
   - Unpaid internship

3. **Data Scientist Intern**
   - NLP models, ML, Python
   - Sentiment analysis
   - Unpaid internship

**Features**:
- Detailed job descriptions
- Expandable job details
- Apply Now button → `/careers/apply`
- Perks and benefits section

**Application Form** (`/careers/apply`):
- Personal information fields
- Education details
- Professional links (LinkedIn, GitHub, Portfolio)
- Resume upload
- Cover letter
- Form validation
- Success confirmation page

---

### 5. **Login Page** (`/login`)
**Purpose**: User authentication

**Features**:
- Email/password login
- Social login (Google, GitHub)
- Remember me checkbox
- Forgot password link
- Sign up link

**Demo Login**:
- Enter any email and password
- Redirects to `/dashboard`

---

### 6. **Dashboard** (`/dashboard`)
**Purpose**: Main application interface

**Features**:
- **Stats Cards**:
  - Total Reviews: 1,284
  - Avg Sentiment: 4.2/5
  - Response Rate: 87%
  - Pending: 23

- **Recent Reviews**:
  - Review cards with sentiment
  - Emotion tags
  - AI-generated responses
  - Approve/Edit/Reject buttons

- **Header Actions**:
  - 🌓 Dark/Light mode toggle
  - Analytics link
  - Settings button
  - User profile

---

### 7. **Analytics Page** (`/dashboard/analytics`)
**Purpose**: Detailed insights and trends

**Features**:
- Time period selector (7/30/90 days)
- Overview stats with trends
- Sentiment trend chart
- Platform distribution
- Top keywords
- Response time performance

**Navigation**:
- Back arrow → `/dashboard`

---

## 🎨 Design System

### Color Palette
- **Primary**: Blue-500 to Purple-600 gradient
- **Success**: Emerald-500 to Green-500
- **Warning**: Orange-500 to Amber-500
- **Error**: Red-500
- **Background**: White with subtle blue-purple gradient

### Typography
- **Headings**: Bold, tracking-tight
- **Body**: Regular, leading-relaxed
- **Small**: Uppercase, tracking-wide

### Components
- **Cards**: White, rounded-2xl, shadow-lg
- **Buttons**: Gradient, rounded-xl, shadow
- **Badges**: Rounded-full, colored backgrounds
- **Icons**: Lucide React, gradient backgrounds

---

## 🔐 Authentication Flow

```
User visits / 
  ↓
Redirected to /home
  ↓
Clicks "Get Started" or "Sign in"
  ↓
Goes to /login
  ↓
Enters credentials
  ↓
Redirected to /dashboard
  ↓
Can access /dashboard/analytics
```

---

## 🌓 Dark Mode

**Location**: Dashboard header (top-right)

**How it works**:
1. Click Moon icon (light mode) or Sun icon (dark mode)
2. Theme switches instantly
3. Preference saved to localStorage
4. Smooth transitions

**Note**: Currently only implemented in dashboard. Can be extended to all pages.

---

## 📱 Responsive Design

All pages are fully responsive:
- **Mobile**: < 640px (Hamburger menu, stacked layout)
- **Tablet**: 640px - 1024px (2-column grid)
- **Desktop**: > 1024px (Full layout)

---

## 🚀 Navigation Tips

### From Home Page:
- Click "Features" → Scroll to features section
- Click "Pricing" → Go to `/pricing`
- Click "About" → Go to `/about`
- Click "Sign in" or "Get Started" → Go to `/login`

### From Dashboard:
- Click "Analytics" → Go to `/dashboard/analytics`
- Click Moon/Sun icon → Toggle dark mode
- Click "Settings" → (To be implemented)
- Click user avatar → (To be implemented)

### From Analytics:
- Click back arrow → Return to `/dashboard`

---

## 🎯 Key Features

### ✅ Implemented
- Landing page with hero and features
- Pricing page with 3 tiers
- About page with mission and values
- Login page with social auth
- Dashboard with stats and reviews
- Analytics page with charts
- Dark/Light mode toggle
- Responsive design
- Smooth animations

### 🔄 To Be Implemented
- Real authentication (JWT/OAuth)
- Backend API integration
- Settings page
- User profile management
- Reviews page (full list)
- Notifications system
- Search functionality
- Filters and sorting

---

## 📝 Notes

- All pages use **Apple-style design** with clean whites, gradients, and shadows
- **Framer Motion** for smooth animations
- **Lucide React** for icons
- **Tailwind CSS** for styling
- **Next.js 14** with App Router

---

## 🔗 Quick Links

- **Home**: http://localhost:3000/home
- **Pricing**: http://localhost:3000/pricing
- **About**: http://localhost:3000/about
- **Login**: http://localhost:3000/login
- **Dashboard**: http://localhost:3000/dashboard
- **Analytics**: http://localhost:3000/dashboard/analytics

---

**Remember**: The project follows the original NLP-powered review management concept with multi-platform aggregation, sentiment analysis, and AI response generation! 🧠✨
