# RevuIQ Frontend Routes

## 📍 Available Pages

### 1. **Home Page** (`/` or `/home`)
- **Purpose**: Landing page for new visitors
- **Features**:
  - Hero section with CTA
  - Feature showcase
  - Pricing information
  - Footer with links
- **Access**: Public

### 2. **Login Page** (`/login`)
- **Purpose**: User authentication
- **Features**:
  - Email/password login
  - Social login (Google, GitHub)
  - Remember me checkbox
  - Forgot password link
- **Access**: Public

### 3. **Dashboard** (`/dashboard`)
- **Purpose**: Main application interface
- **Features**:
  - Stats cards (Total Reviews, Avg Sentiment, Response Rate, Pending)
  - Recent reviews with AI responses
  - Human-in-the-loop approval workflow
  - **Dark/Light mode toggle** 🌓
- **Access**: Protected (requires login)

## 🎨 Theme System

### Dark Mode Toggle
- Located in dashboard header (top-right)
- Click the Moon/Sun icon to switch themes
- State persists in localStorage
- Smooth transitions between modes

## 🔐 Authentication Flow

```
/ (root)
  ↓
/home (landing page)
  ↓
/login (authentication)
  ↓
/dashboard (protected - requires auth)
```

## 🚀 Getting Started

1. **Start the dev server:**
   ```bash
   npm run dev
   ```

2. **Navigate to:**
   - Home: http://localhost:3000
   - Login: http://localhost:3000/login
   - Dashboard: http://localhost:3000/dashboard

3. **Demo Login:**
   - Enter any email and password
   - Click "Sign in"
   - You'll be redirected to the dashboard

## 📱 Responsive Design

All pages are fully responsive:
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

## 🎯 Next Steps

- [ ] Add real authentication (JWT, OAuth)
- [ ] Connect to backend API
- [ ] Add more dashboard pages (Analytics, Settings)
- [ ] Implement protected routes middleware
- [ ] Add user profile management
