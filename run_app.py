"""Script to run the AI Travel Assistant application."""
import os
import subprocess
import time
import sys
import signal
import platform

def check_api_key():
    """Check if the API key is set."""
    if not os.environ.get("GOOGLE_API_KEY"):
        print("\nWARNING: GOOGLE_API_KEY environment variable is not set.")
        print("The application will not function correctly without a valid API key.")
        api_key = input("Enter your Google API Key to continue (or press Enter to exit): ")
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
        else:
            print("Exiting...")
            sys.exit(1)

def kill_existing_servers():
    """Kill any existing servers on the same ports."""
    if platform.system() == "Windows":
        # Kill processes on port 8000 (backend)
        subprocess.run("FOR /F \"tokens=5\" %P IN ('netstat -ano ^| findstr :8000') DO taskkill /F /PID %P", shell=True)
        # Kill processes on port 7860 (frontend)
        subprocess.run("FOR /F \"tokens=5\" %P IN ('netstat -ano ^| findstr :7860') DO taskkill /F /PID %P", shell=True)
    else:
        # Unix-based systems
        subprocess.run("lsof -ti:8000 | xargs kill -9", shell=True)
        subprocess.run("lsof -ti:7860 | xargs kill -9", shell=True)

def run_backend():
    """Run the backend server."""
    print("Starting backend server...")
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", "127.0.0.1", "--port", "8000"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )

def run_frontend():
    """Run the frontend server."""
    print("Starting frontend server...")
    return subprocess.Popen(
        [sys.executable, "frontend/gradio_app.py"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )

def main():
    """Main function."""
    # Kill existing servers
    kill_existing_servers()
    
    # Check API key
    check_api_key()
    
    # Run backend
    backend_process = run_backend()
    
    # Wait for backend to start
    print("Waiting for backend to start...")
    time.sleep(3)
    
    # Run frontend
    frontend_process = run_frontend()
    
    # Wait for user to press Ctrl+C
    print("\nPress Ctrl+C to stop the servers...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Servers stopped.")

if __name__ == "__main__":
    main()
