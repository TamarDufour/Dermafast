#!/usr/bin/env python3
"""
Ultra-Simple DermaFast Restart
Just run: python3 restart.py
"""
import os, subprocess, time

print("🚀 DermaFast Restart")
print("===================")

# Kill existing processes
print("🔄 Stopping servers...")
os.system("lsof -ti:8000 | xargs kill 2>/dev/null || true")
os.system("lsof -ti:5173 | xargs kill 2>/dev/null || true")
time.sleep(2)

# Start backend
print("🐍 Starting backend...")
os.system("cd backend && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 &")
time.sleep(3)

# Start frontend  
print("⚛️  Starting frontend...")
os.system("cd frontend && npm run dev > frontend.log 2>&1 &")
time.sleep(3)

# Test servers
backend_ok = os.system("curl -s http://localhost:8000/health >/dev/null 2>&1") == 0
frontend_ok = os.system("curl -s http://localhost:5173 >/dev/null 2>&1") == 0

print("===================")
print(f"Backend:  {'✅ OK' if backend_ok else '❌ FAIL'} - http://localhost:8000")
print(f"Frontend: {'✅ OK' if frontend_ok else '❌ FAIL'} - http://localhost:5173")
print("===================")
