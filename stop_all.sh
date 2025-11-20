#!/bin/bash

# RevuIQ - Stop All Services

echo "🛑 Stopping RevuIQ Services..."
echo ""

# Stop Frontend (port 3000)
if lsof -ti:3000 > /dev/null; then
    echo "🎨 Stopping Frontend..."
    lsof -ti:3000 | xargs kill -9
    echo "   ✅ Frontend stopped"
else
    echo "   ⚠️  Frontend not running"
fi

# Stop Backend (port 8000)
if lsof -ti:8000 > /dev/null; then
    echo "🔧 Stopping Backend..."
    lsof -ti:8000 | xargs kill -9
    echo "   ✅ Backend stopped"
else
    echo "   ⚠️  Backend not running"
fi

echo ""
echo "✅ All services stopped"
echo ""
