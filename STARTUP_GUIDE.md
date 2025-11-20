# 🚀 RevuIQ Startup Guide

## Quick Start (Recommended)

### Start All Services
```bash
./start_all.sh
```

This will:
- ✅ Kill any existing processes on ports 3000 and 8000
- ✅ Start Backend API on port 8000
- ✅ Start Frontend on port 3000
- ✅ Create log files in `logs/` directory
- ✅ Display service URLs and PIDs

### Check Status
```bash
./check_status.sh
```

Shows:
- Backend status (running/stopped)
- Frontend status (running/stopped)
- Database connection and stats
- Service URLs

### Stop All Services
```bash
./stop_all.sh
```

---

## Manual Start (Alternative)

### Start Backend Only
```bash
cd backend
python3 simple_api.py
```

### Start Frontend Only
```bash
cd frontend
npm run dev
```

---

## Service URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main application |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **ReDoc** | http://localhost:8000/redoc | Alternative API docs |

---

## Key Pages

### Frontend Routes
- `/` - Home page
- `/dashboard` - Real-time analytics dashboard
- `/restaurants` - Restaurant management (add, fetch Google reviews)
- `/restaurants/[id]` - Detailed analytics for a restaurant
- `/analytics` - System-wide analytics
- `/reviews` - All reviews

---

## Troubleshooting

### Backend Won't Start
```bash
# Check if port 8000 is in use
lsof -ti:8000

# Kill the process
lsof -ti:8000 | xargs kill -9

# Restart
cd backend && python3 simple_api.py
```

### Frontend Won't Start
```bash
# Check if port 3000 is in use
lsof -ti:3000

# Kill the process
lsof -ti:3000 | xargs kill -9

# Restart
cd frontend && npm run dev
```

### Connection Issues
1. **Check both services are running**:
   ```bash
   ./check_status.sh
   ```

2. **Check logs**:
   ```bash
   tail -f logs/backend.log
   tail -f logs/frontend.log
   ```

3. **Restart all services**:
   ```bash
   ./stop_all.sh
   ./start_all.sh
   ```

### Database Issues
```bash
# Check database exists
ls -lh backend/revuiq.db

# View data
sqlite3 backend/revuiq.db "SELECT * FROM businesses;"
sqlite3 backend/revuiq.db "SELECT COUNT(*) FROM reviews;"

# Reset database (CAUTION: deletes all data!)
rm backend/revuiq.db
cd backend && python3 simple_api.py  # Will recreate
```

---

## Why Backend Keeps Disconnecting?

### Common Causes:
1. **Process killed manually** - Use `./start_all.sh` to restart
2. **Port conflict** - Another app using port 8000
3. **Python error** - Check `logs/backend.log`
4. **Out of memory** - Restart your computer

### Solution:
The `start_all.sh` script ensures:
- ✅ Old processes are killed before starting
- ✅ Services run in background
- ✅ Logs are captured for debugging
- ✅ Process IDs are tracked

---

## Environment Variables

Backend uses `.env` file:
```bash
# Database
DATABASE_URL=sqlite:///./revuiq.db

# Google Places API
GOOGLE_PLACES_API_KEY=AIzaSyC...

# Optional: Yelp API
YELP_API_KEY=your_key_here
```

**Note**: `.env` is gitignored for security

---

## Database Info

- **Type**: SQLite
- **Location**: `backend/revuiq.db`
- **Current Size**: 72 KB
- **Restaurants**: 4
- **Reviews**: 20

---

## Logs

Logs are stored in `logs/` directory:
- `backend.log` - Backend API logs
- `frontend.log` - Frontend build/runtime logs

View logs in real-time:
```bash
tail -f logs/backend.log
tail -f logs/frontend.log
```

---

## Process Management

### View Running Processes
```bash
# Check what's running on ports 3000 and 8000
lsof -i :3000 -i :8000 | grep LISTEN
```

### Kill Specific Process
```bash
# By port
lsof -ti:8000 | xargs kill -9

# By PID (from start_all.sh output)
kill -9 54816
```

---

## Best Practices

1. **Always use `start_all.sh`** for starting services
2. **Check status** with `check_status.sh` before debugging
3. **Stop cleanly** with `stop_all.sh` before shutting down
4. **Monitor logs** if you encounter issues
5. **Keep `.env` file secure** - never commit to git

---

## Quick Commands Reference

```bash
# Start everything
./start_all.sh

# Check if running
./check_status.sh

# Stop everything
./stop_all.sh

# View backend logs
tail -f logs/backend.log

# View frontend logs
tail -f logs/frontend.log

# Test backend API
curl http://localhost:8000/health

# Test frontend
curl http://localhost:3000
```

---

## Support

If services keep disconnecting:
1. Run `./check_status.sh` to see what's running
2. Check logs in `logs/` directory
3. Restart with `./stop_all.sh && ./start_all.sh`
4. Verify ports 3000 and 8000 are not used by other apps

---

**Status**: ✅ All services connected and running  
**Last Updated**: November 19, 2025
