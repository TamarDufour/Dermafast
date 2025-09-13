#!/bin/bash

echo "🔧 Starting DermaFast Application..."

# Kill any existing processes on these ports
echo "📋 Stopping existing servers..."
kill $(lsof -t -i:5173) 2>/dev/null
kill $(lsof -t -i:8000) 2>/dev/null
sleep 2

# Start backend with virtual environment
echo "🐍 Starting Backend Server..."
cd /Users/tamardufourdror/Projects/DermaFast/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "⚛️  Starting Frontend Server..."
cd /Users/tamardufourdror/Projects/DermaFast/frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ DermaFast is starting up!"
echo "📊 Backend:  http://localhost:8000"
echo "🌐 Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
wait
