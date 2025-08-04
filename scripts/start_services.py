import subprocess
import time
import sys
import os

# --- Configuration ---
# Define commands for each service
commands = {
    "backend": {
        "command": [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"],
        "cwd": "..", # Run from the project root
        "name": "Backend (FastAPI)"
    },
    "frontend": {
        "command": [sys.executable, "-m", "http.server", "8080", "--directory", "frontend"],
        "cwd": "..", # Run from the project root
        "name": "Frontend (http.server)"
    },
    "mcp_server": {
        "command": ["npm", "start", "--prefix", "mcp-server"],
        "cwd": "..", # Run from the project root
        "name": "MCP Server",
        "enabled": True
    }
}

# --- Main Execution ---
def main():
    """
    Starts all configured services as separate processes and waits for user interruption
    to terminate them.
    """
    print("="*50)
    print("🚀 Starting All Services...")
    print("="*50)

    processes = []
    
    # Start all enabled services
    for service, config in commands.items():
        if config.get("enabled", True):
            print(f"🔄 Starting {config['name']}...")
            try:
                # Adjust cwd to be relative to this script's location
                script_dir = os.path.dirname(os.path.abspath(__file__))
                cwd_path = os.path.join(script_dir, config['cwd'])

                process = subprocess.Popen(
                    config['command'],
                    cwd=cwd_path,
                    shell=sys.platform == 'win32' # Use shell=True on Windows for npm commands
                )
                processes.append((process, config['name']))
                print(f"✅ {config['name']} started successfully (PID: {process.pid}).")
            except FileNotFoundError:
                print(f"❌ ERROR: Command not found for {config['name']}. Is it installed and in your PATH?")
                print(f"   Failed command: {' '.join(config['command'])}")
            except Exception as e:
                print(f"❌ ERROR: Failed to start {config['name']}: {e}")
    
    print("\n" + "="*50)
    print("🎉 All services are launching.")
    print("   Backend: http://localhost:8000")
    print("   Frontend: http://localhost:8080")
    if commands['mcp_server'].get('enabled', True):
        print("   MCP Server: http://localhost:3002 (default)")
    print("\n👉 Press CTRL+C to stop all services.")
    print("="*50)

    try:
        # Wait for interruption
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 SIGINT received, stopping all services...")
    finally:
        for process, name in processes:
            print(f"   Terminating {name} (PID: {process.pid})...")
            process.terminate()
            try:
                # Wait for a bit for graceful shutdown
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if it doesn't terminate
                print(f"   {name} did not terminate gracefully, force killing.")
                process.kill()
        print("\n✅ All services stopped.")

if __name__ == "__main__":
    main()
