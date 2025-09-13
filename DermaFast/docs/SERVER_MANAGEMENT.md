# 🚀 DermaFast Server Management

This directory contains several scripts to help you manage the DermaFast backend and frontend servers.

## 📋 Available Scripts

### 1. `restart_servers_simple.py` ⭐ **RECOMMENDED**
**Simple Python script with no external dependencies**

```bash
cd /Users/tamardufourdror/Projects/DermaFast
python3 restart_servers_simple.py
```

**Features:**
- ✅ Kills existing backend/frontend processes
- ✅ Starts both servers automatically  
- ✅ Tests connectivity after startup
- ✅ Clean colored output
- ✅ No external dependencies required

### 2. `restart_servers.py` 
**Advanced Python script with process monitoring**

```bash
cd /Users/tamardufourdror/Projects/DermaFast
pip install psutil  # Required dependency
python3 restart_servers.py
```

**Features:**
- ✅ All features of simple version
- ✅ Advanced process monitoring with psutil
- ✅ Keeps running and monitors server health
- ✅ Graceful shutdown on Ctrl+C
- ⚠️ Requires `pip install psutil`

### 3. `quick_restart.sh`
**Bash shell script for quick restarts**

```bash
cd /Users/tamardufourdror/Projects/DermaFast
./quick_restart.sh
```

**Features:**
- ✅ Pure bash, no Python required
- ✅ Logs output to files (backend.log, frontend.log)
- ✅ Checks for dependencies
- ✅ Colorful terminal output

## 🎯 Quick Commands

### One-liner restart command:
```bash
cd /Users/tamardufourdror/Projects/DermaFast && python3 restart_servers_simple.py
```

### Manual server management:
```bash
# Kill both servers
lsof -ti:8000 | xargs kill && lsof -ti:5173 | xargs kill

# Start backend only
cd backend && source venv/bin/activate && uvicorn app.main:app --reload &

# Start frontend only  
cd frontend && npm run dev &
```

### Check server status:
```bash
# Check what's running on the ports
lsof -i:8000    # Backend
lsof -i:5173    # Frontend

# Test connectivity
curl http://localhost:8000/health    # Backend health
curl http://localhost:5173           # Frontend
```

## 🔧 Troubleshooting

### Common Issues:

1. **Virtual environment not found**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Frontend dependencies missing**
   ```bash
   cd frontend
   npm install
   ```

3. **Ports already in use**
   ```bash
   # Force kill processes on ports
   sudo lsof -ti:8000 | xargs kill -9
   sudo lsof -ti:5173 | xargs kill -9
   ```

4. **Permission denied**
   ```bash
   chmod +x restart_servers_simple.py
   chmod +x quick_restart.sh
   ```

## 📊 Server URLs

After starting the servers:

- **Backend API**: http://localhost:8000
- **Backend Health**: http://localhost:8000/health  
- **Backend Docs**: http://localhost:8000/docs
- **Frontend App**: http://localhost:5173

## 💡 Pro Tips

1. **Add alias to your shell**:
   ```bash
   # Add to ~/.zshrc or ~/.bashrc
   alias derma-restart="cd /Users/tamardufourdror/Projects/DermaFast && python3 restart_servers_simple.py"
   
   # Then use:
   derma-restart
   ```

2. **Quick status check**:
   ```bash
   # Check if servers are running
   curl -s http://localhost:8000/health && echo "Backend OK" || echo "Backend DOWN"
   curl -s http://localhost:5173 >/dev/null && echo "Frontend OK" || echo "Frontend DOWN"
   ```

3. **View logs in real-time** (when using shell script):
   ```bash
   tail -f backend/backend.log frontend/frontend.log
   ```

## 🎉 Usage Examples

```bash
# Method 1: Simple Python script (recommended)
cd /Users/tamardufourdror/Projects/DermaFast
python3 restart_servers_simple.py

# Method 2: Shell script with logging
./quick_restart.sh

# Method 3: Manual restart
lsof -ti:8000,5173 | xargs kill
cd backend && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
cd ../frontend && npm run dev &
```

Choose the method that works best for your workflow! 🚀
