# Starting RevuIQ

## Quick start

Run this to start everything:
```bash
./start_all.sh
```

This starts the backend (port 8000) and frontend (port 3000).

Check if things are running:
```bash
./check_status.sh
```

Stop everything:
```bash
./stop_all.sh
```

## Service URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main application |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **ReDoc** | http://localhost:8000/redoc | Alternative API docs |

## Pages

- `/` - Home
- `/dashboard` - Dashboard with stats
- `/restaurants` - Add/manage restaurants
- `/restaurants/[id]` - View restaurant analytics
- `/analytics` - Overall analytics

## If something breaks

If services won't start, just run:
```bash
./stop_all.sh
./start_all.sh
```

Check logs if needed:
```bash
tail -f logs/backend.log
tail -f logs/frontend.log
```
