#!/usr/bin/env python3
"""
DermaFast Server Management Script
Kills existing backend and frontend processes and restarts them.
"""

import os
import sys
import time
import signal
import subprocess
import psutil
from pathlib import Path

# Configuration
BACKEND_PORT = 8000
FRONTEND_PORT = 5173
PROJECT_ROOT = Path(__file__).parent.absolute()
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
VENV_PATH = BACKEND_DIR / "venv" / "bin" / "activate"

def print_status(message, status="INFO"):
    """Print colored status messages"""
    colors = {
        "INFO": "\033[94m",      # Blue
        "SUCCESS": "\033[92m",   # Green
        "WARNING": "\033[93m",   # Yellow
        "ERROR": "\033[91m",     # Red
        "RESET": "\033[0m"       # Reset
    }
    print(f"{colors.get(status, '')}{status}: {message}{colors['RESET']}")

def find_processes_by_port(port):
    """Find all processes using a specific port"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            for conn in proc.connections():
                if conn.laddr.port == port:
                    processes.append(proc)
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

def kill_processes_by_port(port, service_name):
    """Kill all processes using a specific port"""
    print_status(f"Looking for {service_name} processes on port {port}...")
    
    processes = find_processes_by_port(port)
    
    if not processes:
        print_status(f"No {service_name} processes found on port {port}")
        return True
    
    print_status(f"Found {len(processes)} {service_name} process(es) to kill")
    
    # Try graceful termination first
    for proc in processes:
        try:
            print_status(f"Terminating process {proc.pid} ({proc.name()})")
            proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Wait for graceful termination
    time.sleep(2)
    
    # Force kill if still running
    remaining_processes = find_processes_by_port(port)
    for proc in remaining_processes:
        try:
            print_status(f"Force killing process {proc.pid} ({proc.name()})", "WARNING")
            proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Final check
    time.sleep(1)
    if find_processes_by_port(port):
        print_status(f"Failed to kill all {service_name} processes", "ERROR")
        return False
    else:
        print_status(f"All {service_name} processes killed successfully", "SUCCESS")
        return True

def check_directories():
    """Check if required directories exist"""
    if not BACKEND_DIR.exists():
        print_status(f"Backend directory not found: {BACKEND_DIR}", "ERROR")
        return False
    
    if not FRONTEND_DIR.exists():
        print_status(f"Frontend directory not found: {FRONTEND_DIR}", "ERROR")
        return False
    
    if not VENV_PATH.exists():
        print_status(f"Virtual environment not found: {VENV_PATH}", "ERROR")
        print_status("Please create virtual environment first: python -m venv backend/venv", "ERROR")
        return False
    
    return True

def start_backend():
    """Start the backend server"""
    print_status("Starting backend server...")
    
    try:
        # Create activation script
        activate_script = f"source {VENV_PATH} && cd {BACKEND_DIR} && uvicorn app.main:app --reload --host 0.0.0.0 --port {BACKEND_PORT}"
        
        # Start backend process
        backend_process = subprocess.Popen(
            activate_script,
            shell=True,
            executable='/bin/bash',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid  # Create new process group
        )
        
        # Wait a moment and check if process started successfully
        time.sleep(3)
        
        if backend_process.poll() is None:
            print_status(f"Backend server started successfully (PID: {backend_process.pid})", "SUCCESS")
            print_status(f"Backend running on: http://localhost:{BACKEND_PORT}", "SUCCESS")
            return backend_process
        else:
            stdout, stderr = backend_process.communicate()
            print_status("Backend failed to start", "ERROR")
            print_status(f"Error: {stderr.decode()}", "ERROR")
            return None
            
    except Exception as e:
        print_status(f"Failed to start backend: {str(e)}", "ERROR")
        return None

def start_frontend():
    """Start the frontend server"""
    print_status("Starting frontend server...")
    
    try:
        # Start frontend process
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=FRONTEND_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid  # Create new process group
        )
        
        # Wait a moment and check if process started successfully
        time.sleep(3)
        
        if frontend_process.poll() is None:
            print_status(f"Frontend server started successfully (PID: {frontend_process.pid})", "SUCCESS")
            print_status(f"Frontend running on: http://localhost:{FRONTEND_PORT}", "SUCCESS")
            return frontend_process
        else:
            stdout, stderr = frontend_process.communicate()
            print_status("Frontend failed to start", "ERROR")
            print_status(f"Error: {stderr.decode()}", "ERROR")
            return None
            
    except Exception as e:
        print_status(f"Failed to start frontend: {str(e)}", "ERROR")
        return None

def test_servers():
    """Test if servers are responding"""
    import urllib.request
    import urllib.error
    
    print_status("Testing server connectivity...")
    
    # Test backend
    try:
        response = urllib.request.urlopen(f"http://localhost:{BACKEND_PORT}/health", timeout=5)
        if response.status == 200:
            print_status("✅ Backend health check passed", "SUCCESS")
        else:
            print_status(f"❌ Backend health check failed (status: {response.status})", "WARNING")
    except Exception as e:
        print_status(f"❌ Backend health check failed: {str(e)}", "WARNING")
    
    # Test frontend (just check if port is responding)
    try:
        response = urllib.request.urlopen(f"http://localhost:{FRONTEND_PORT}", timeout=5)
        if response.status == 200:
            print_status("✅ Frontend responding", "SUCCESS")
        else:
            print_status(f"❌ Frontend not responding (status: {response.status})", "WARNING")
    except Exception as e:
        print_status(f"❌ Frontend not responding: {str(e)}", "WARNING")

def main():
    """Main function"""
    print_status("=" * 60)
    print_status("DermaFast Server Management Script", "INFO")
    print_status("=" * 60)
    
    # Check directories
    if not check_directories():
        sys.exit(1)
    
    # Kill existing processes
    backend_killed = kill_processes_by_port(BACKEND_PORT, "backend")
    frontend_killed = kill_processes_by_port(FRONTEND_PORT, "frontend")
    
    if not (backend_killed and frontend_killed):
        print_status("Failed to kill some processes. Manual intervention may be required.", "ERROR")
        sys.exit(1)
    
    # Wait a moment before starting
    print_status("Waiting 2 seconds before starting servers...")
    time.sleep(2)
    
    # Start servers
    backend_process = start_backend()
    if not backend_process:
        print_status("Failed to start backend server", "ERROR")
        sys.exit(1)
    
    frontend_process = start_frontend()
    if not frontend_process:
        print_status("Failed to start frontend server", "ERROR")
        # Kill backend since frontend failed
        try:
            os.killpg(os.getpgid(backend_process.pid), signal.SIGTERM)
        except:
            pass
        sys.exit(1)
    
    # Wait for servers to fully start
    print_status("Waiting for servers to fully initialize...")
    time.sleep(5)
    
    # Test connectivity
    test_servers()
    
    print_status("=" * 60)
    print_status("🎉 DermaFast servers started successfully!", "SUCCESS")
    print_status(f"🐍 Backend:  http://localhost:{BACKEND_PORT}", "SUCCESS")
    print_status(f"⚛️  Frontend: http://localhost:{FRONTEND_PORT}", "SUCCESS")
    print_status("=" * 60)
    print_status("Press Ctrl+C to stop all servers", "INFO")
    
    # Keep script running and handle Ctrl+C gracefully
    try:
        while True:
            # Check if processes are still running
            if backend_process.poll() is not None:
                print_status("Backend process died unexpectedly", "ERROR")
                break
            if frontend_process.poll() is not None:
                print_status("Frontend process died unexpectedly", "ERROR")
                break
            time.sleep(5)
    
    except KeyboardInterrupt:
        print_status("\nStopping servers...", "INFO")
        
        # Kill both processes
        try:
            print_status("Stopping backend server...")
            os.killpg(os.getpgid(backend_process.pid), signal.SIGTERM)
        except:
            pass
            
        try:
            print_status("Stopping frontend server...")
            os.killpg(os.getpgid(frontend_process.pid), signal.SIGTERM)
        except:
            pass
        
        print_status("Servers stopped", "SUCCESS")

if __name__ == "__main__":
    main()
