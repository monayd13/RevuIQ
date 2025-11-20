#!/bin/bash

# RevuIQ - Check Service Status

echo "🔍 Checking RevuIQ Services..."
echo ""

# Check Backend
if lsof -ti:8000 > /dev/null; then
    BACKEND_PID=$(lsof -ti:8000 | head -1)
    echo "✅ Backend:  RUNNING (PID: $BACKEND_PID)"
    echo "   URL: http://localhost:8000"
    echo "   Health: $(curl -s http://localhost:8000/health | python3 -c 'import json,sys; print(json.load(sys.stdin)["status"])' 2>/dev/null || echo 'ERROR')"
else
    echo "❌ Backend:  NOT RUNNING"
fi

echo ""

# Check Frontend
if lsof -ti:3000 > /dev/null; then
    FRONTEND_PID=$(lsof -ti:3000 | head -1)
    echo "✅ Frontend: RUNNING (PID: $FRONTEND_PID)"
    echo "   URL: http://localhost:3000"
else
    echo "❌ Frontend: NOT RUNNING"
fi

echo ""

# Check Database
if [ -f "backend/revuiq.db" ]; then
    DB_SIZE=$(ls -lh backend/revuiq.db | awk '{print $5}')
    RESTAURANTS=$(sqlite3 backend/revuiq.db "SELECT COUNT(*) FROM businesses;" 2>/dev/null || echo "0")
    REVIEWS=$(sqlite3 backend/revuiq.db "SELECT COUNT(*) FROM reviews;" 2>/dev/null || echo "0")
    echo "✅ Database: CONNECTED"
    echo "   Size: $DB_SIZE"
    echo "   Restaurants: $RESTAURANTS"
    echo "   Reviews: $REVIEWS"
else
    echo "❌ Database: NOT FOUND"
fi

echo ""
