#!/bin/bash
# DermaFast Quick Restart Script (Shell Version)
# Simple bash script to kill and restart servers

echo "🚀 DermaFast Quick Restart"
echo "=========================="

# Configuration
BACKEND_PORT=8000
FRONTEND_PORT=5173
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}$message${NC}"
}

# Kill processes on specific ports
kill_port() {
    local port=$1
    local service=$2
    
    print_message $BLUE "Killing $service processes on port $port..."
    
    # Find and kill processes
    local pids=$(lsof -ti:$port 2>/dev/null)
    
    if [ -z "$pids" ]; then
        print_message $GREEN "No $service processes found on port $port"
    else
        echo "Found processes: $pids"
        echo $pids | xargs kill -TERM 2>/dev/null || true
        sleep 2
        
        # Force kill if still running
        local remaining=$(lsof -ti:$port 2>/dev/null)
        if [ ! -z "$remaining" ]; then
            print_message $YELLOW "Force killing remaining processes..."
            echo $remaining | xargs kill -9 2>/dev/null || true
        fi
        
        print_message $GREEN "$service processes killed"
    fi
}

# Start backend server
start_backend() {
    print_message $BLUE "Starting backend server..."
    
    cd "$BACKEND_DIR" || {
        print_message $RED "Failed to change to backend directory"
        exit 1
    }
    
    # Check if virtual environment exists
    if [ ! -f "venv/bin/activate" ]; then
        print_message $RED "Virtual environment not found. Please create it first:"
        print_message $RED "cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
        exit 1
    fi
    
    # Start backend
    nohup bash -c "source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port $BACKEND_PORT" > backend.log 2>&1 &
    
    sleep 3
    
    # Check if backend started
    if curl -s "http://localhost:$BACKEND_PORT/health" > /dev/null 2>&1; then
        print_message $GREEN "✅ Backend started successfully on port $BACKEND_PORT"
    else
        print_message $YELLOW "⚠️  Backend may be starting (check backend.log for details)"
    fi
}

# Start frontend server  
start_frontend() {
    print_message $BLUE "Starting frontend server..."
    
    cd "$FRONTEND_DIR" || {
        print_message $RED "Failed to change to frontend directory" 
        exit 1
    }
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        print_message $YELLOW "Installing frontend dependencies..."
        npm install
    fi
    
    # Start frontend
    nohup npm run dev > frontend.log 2>&1 &
    
    sleep 3
    
    # Check if frontend started
    if curl -s "http://localhost:$FRONTEND_PORT" > /dev/null 2>&1; then
        print_message $GREEN "✅ Frontend started successfully on port $FRONTEND_PORT"
    else
        print_message $YELLOW "⚠️  Frontend may be starting (check frontend.log for details)"
    fi
}

# Main execution
main() {
    # Kill existing processes
    kill_port $BACKEND_PORT "backend"
    kill_port $FRONTEND_PORT "frontend"
    
    # Wait before starting
    print_message $BLUE "Waiting 2 seconds before starting servers..."
    sleep 2
    
    # Start servers
    start_backend
    start_frontend
    
    # Final status
    echo "=========================="
    print_message $GREEN "🎉 DermaFast servers restarted!"
    print_message $GREEN "🐍 Backend:  http://localhost:$BACKEND_PORT"
    print_message $GREEN "⚛️  Frontend: http://localhost:$FRONTEND_PORT"
    echo "=========================="
    
    print_message $BLUE "Servers are running in background."
    print_message $BLUE "Check logs: tail -f backend/backend.log frontend/frontend.log"
    print_message $BLUE "To stop: lsof -ti:8000 | xargs kill && lsof -ti:5173 | xargs kill"
}

# Run with error handling
if main "$@"; then
    exit 0
else
    print_message $RED "Script failed with errors"
    exit 1
fi
