#!/usr/bin/env python3
"""
DermaFast Simple Server Restart Script
Simple version using basic subprocess calls (no psutil dependency)
"""

import os
import sys
import time
import subprocess
import signal
from pathlib import Path

# Configuration
BACKEND_PORT = 8000
FRONTEND_PORT = 5173
PROJECT_ROOT = Path(__file__).parent.absolute()
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"

def print_status(message, status="INFO"):
    """Print colored status messages"""
    colors = {
        "INFO": "\033[94m",
        "SUCCESS": "\033[92m",
        "WARNING": "\033[93m", 
        "ERROR": "\033[91m",
        "RESET": "\033[0m"
    }
    print(f"{colors.get(status, '')}{status}: {message}{colors['RESET']}")

def kill_port_processes(port, service_name):
    """Kill processes using lsof and kill commands"""
    print_status(f"Killing {service_name} processes on port {port}...")
    
    try:
        # Find processes using the port
        result = subprocess.run(
            ["lsof", "-t", f"-i:{port}"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0 and result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            print_status(f"Found {len(pids)} {service_name} process(es): {', '.join(pids)}")
            
            # Kill each process
            for pid in pids:
                try:
                    subprocess.run(["kill", "-TERM", pid], check=True)
                    print_status(f"Terminated process {pid}")
                except subprocess.CalledProcessError:
                    try:
                        subprocess.run(["kill", "-9", pid], check=True)
                        print_status(f"Force killed process {pid}", "WARNING")
                    except subprocess.CalledProcessError:
                        print_status(f"Failed to kill process {pid}", "ERROR")
            
            # Wait for processes to die
            time.sleep(2)
            print_status(f"{service_name} processes killed", "SUCCESS")
        else:
            print_status(f"No {service_name} processes found on port {port}")
            
    except Exception as e:
        print_status(f"Error killing {service_name} processes: {str(e)}", "ERROR")

def check_backend_dependencies():
    """Check if backend dependencies are properly installed"""
    print_status("Checking backend dependencies...")
    
    try:
        # Check if virtual environment exists
        venv_path = BACKEND_DIR / "venv"
        if not venv_path.exists():
            print_status("Virtual environment not found", "ERROR")
            return False
        
        # Check critical dependencies
        cmd = f"cd {BACKEND_DIR} && source venv/bin/activate && python -c 'import faiss; import torch; import fastapi; print(\"Dependencies OK\")'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print_status("✅ All backend dependencies available", "SUCCESS")
            return True
        else:
            print_status(f"❌ Missing dependencies: {result.stderr.strip()}", "ERROR")
            print_status("Run: pip install -r requirements.txt", "INFO")
            return False
            
    except Exception as e:
        print_status(f"Error checking dependencies: {str(e)}", "ERROR")
        return False

def start_backend():
    """Start backend server"""
    print_status("Starting backend server...")
    
    try:
        # Start backend in background
        cmd = f"cd {BACKEND_DIR} && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port {BACKEND_PORT}"
        
        process = subprocess.Popen(
            cmd,
            shell=True,
            executable='/bin/bash',
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid
        )
        
        # Wait and check if it started
        time.sleep(3)
        if process.poll() is None:
            print_status(f"Backend started (PID: {process.pid})", "SUCCESS")
            return process
        else:
            print_status("Backend failed to start", "ERROR")
            return None
            
    except Exception as e:
        print_status(f"Error starting backend: {str(e)}", "ERROR")
        return None

def start_frontend():
    """Start frontend server"""
    print_status("Starting frontend server...")
    
    try:
        process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=FRONTEND_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid
        )
        
        # Wait and check if it started
        time.sleep(3)
        if process.poll() is None:
            print_status(f"Frontend started (PID: {process.pid})", "SUCCESS")
            return process
        else:
            print_status("Frontend failed to start", "ERROR")
            return None
            
    except Exception as e:
        print_status(f"Error starting frontend: {str(e)}", "ERROR")
        return None

def test_connectivity():
    """Test server connectivity and new features"""
    print_status("Testing server connectivity...")
    
    # Test backend health
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", f"http://localhost:{BACKEND_PORT}/health"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.stdout == "200":
            print_status("✅ Backend health check passed", "SUCCESS")
        else:
            print_status(f"⚠️  Backend returned status: {result.stdout}", "WARNING")
    except Exception:
        print_status("⚠️  Backend health check failed", "WARNING")
    
    # Test backend root endpoint
    try:
        result = subprocess.run(
            ["curl", "-s", f"http://localhost:{BACKEND_PORT}/"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if '"message":"Welcome to DermaFast API"' in result.stdout:
            print_status("✅ Backend API responding correctly", "SUCCESS")
        else:
            print_status("⚠️  Backend API response unexpected", "WARNING")
    except Exception:
        print_status("⚠️  Backend API test failed", "WARNING")
    
    # Test frontend
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", f"http://localhost:{FRONTEND_PORT}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.stdout == "200":
            print_status("✅ Frontend responding", "SUCCESS")
        else:
            print_status(f"⚠️  Frontend returned status: {result.stdout}", "WARNING")
    except Exception:
        print_status("⚠️  Frontend connectivity check failed", "WARNING")

def test_faiss_functionality():
    """Test FAISS functionality"""
    print_status("Testing FAISS similarity search...")
    
    try:
        cmd = f"""cd {BACKEND_DIR} && source venv/bin/activate && python -c "
from app.faiss_service import faiss_service
from app.supabase_client import supabase_client as supabase
import asyncio

async def test():
    try:
        # Check embedding records
        response = supabase.table('ham_metadata').select('image_id', count='exact').not_.is_('embedding', 'null').execute()
        print(f'Embedding records available: {{response.count}}')
        
        if response.count and response.count > 0:
            # Test FAISS loading
            result = await faiss_service.load_embeddings()
            if result:
                print('FAISS service: Ready')
                print(f'Indexed images: {{len(faiss_service.image_ids)}}')
            else:
                print('FAISS service: Failed to load')
        else:
            print('No embedding records found - FAISS will be unavailable')
    except Exception as e:
        print(f'FAISS test error: {{str(e)}}')

asyncio.run(test())
"
"""
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            output_lines = result.stdout.strip().split('\n')
            for line in output_lines:
                if line.strip():
                    if 'Ready' in line:
                        print_status(f"✅ {line}", "SUCCESS")
                    elif 'error' in line.lower() or 'failed' in line.lower():
                        print_status(f"⚠️  {line}", "WARNING")
                    else:
                        print_status(f"ℹ️  {line}", "INFO")
        else:
            print_status(f"⚠️  FAISS test failed: {result.stderr.strip()}", "WARNING")
            
    except Exception as e:
        print_status(f"⚠️  FAISS functionality test error: {str(e)}", "WARNING")

def main():
    """Main execution function"""
    print_status("=" * 60)
    print_status("🚀 DermaFast Server Restart (Enhanced)", "INFO")
    print_status("=" * 60)
    
    # Check backend dependencies first
    if not check_backend_dependencies():
        print_status("❌ Backend dependencies check failed", "ERROR")
        print_status("Please install missing dependencies and try again", "ERROR")
        sys.exit(1)
    
    # Kill existing processes
    kill_port_processes(BACKEND_PORT, "backend")
    kill_port_processes(FRONTEND_PORT, "frontend")
    
    # Wait before starting
    print_status("Waiting 2 seconds...")
    time.sleep(2)
    
    # Start servers
    backend_proc = start_backend()
    frontend_proc = start_frontend()
    
    if not backend_proc or not frontend_proc:
        print_status("Failed to start servers", "ERROR")
        sys.exit(1)
    
    # Wait for full startup
    print_status("Waiting for servers to initialize...")
    time.sleep(5)
    
    # Test connectivity
    test_connectivity()
    
    # Test FAISS functionality
    test_faiss_functionality()
    
    # Success message
    print_status("=" * 60)
    print_status("🎉 Servers restarted successfully!", "SUCCESS")
    print_status(f"🐍 Backend:  http://localhost:{BACKEND_PORT}", "SUCCESS")
    print_status(f"   📋 API Docs: http://localhost:{BACKEND_PORT}/docs", "INFO")
    print_status(f"   ❤️  Health: http://localhost:{BACKEND_PORT}/health", "INFO")
    print_status(f"⚛️  Frontend: http://localhost:{FRONTEND_PORT}", "SUCCESS")
    print_status("=" * 60)
    
    # Enhanced instructions
    print_status("🔧 Server Management:", "INFO")
    print_status("  • Stop servers: lsof -ti:8000 | xargs kill && lsof -ti:5173 | xargs kill", "INFO")
    print_status("  • Run tests: cd backend && python test_comprehensive.py", "INFO")
    print_status("  • Debug tokens: cd backend && python debug_token.py", "INFO")
    print_status("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_status("\nScript interrupted by user", "WARNING")
        sys.exit(1)
    except Exception as e:
        print_status(f"Unexpected error: {str(e)}", "ERROR")
        sys.exit(1)
