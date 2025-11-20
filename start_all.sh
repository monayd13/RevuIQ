#!/bin/bash

# RevuIQ - Start All Services
# This script starts both backend and frontend

echo "🚀 Starting RevuIQ Services..."
echo ""

# Kill any existing processes on ports 3000 and 8000
echo "🧹 Cleaning up existing processes..."
lsof -ti:3000 | xargs kill -9 2>/dev/null || true
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
sleep 2

# Start Backend
echo "🔧 Starting Backend API on port 8000..."
cd backend
python3 simple_api.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
cd ..

# Wait for backend to start
sleep 3

# Check if backend is running
if lsof -ti:8000 > /dev/null; then
    echo "   ✅ Backend started successfully"
else
    echo "   ❌ Backend failed to start"
    exit 1
fi

# Start Frontend
echo "🎨 Starting Frontend on port 3000..."
cd frontend
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"
cd ..

# Wait for frontend to start
sleep 5

# Check if frontend is running
if lsof -ti:3000 > /dev/null; then
    echo "   ✅ Frontend started successfully"
else
    echo "   ❌ Frontend failed to start"
    exit 1
fi

echo ""
echo "✅ All services started successfully!"
echo ""
echo "📊 Service URLs:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "📝 Process IDs:"
echo "   Backend:   $BACKEND_PID"
echo "   Frontend:  $FRONTEND_PID"
echo ""
echo "🛑 To stop all services, run: ./stop_all.sh"
echo "📋 Logs are in: logs/backend.log and logs/frontend.log"
echo ""
