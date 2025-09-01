import subprocess
import sys
from pathlib import Path

def main():
    # 更新为新的backend目录结构
    backend_path = Path(__file__).parent.parent / "backend"
    
    # Define the path to the .env file in the project root
    env_file_path = backend_path.parent / ".env"

    cmd = [
        sys.executable, "-m", "uvicorn", 
        "main:app", 
        "--reload", 
        "--host", "0.0.0.0", 
        "--port", "8000",
        "--env-file", str(env_file_path)
    ]
    
    try:
        subprocess.run(
            cmd,
            cwd=str(backend_path),
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Backend server failed to start with exit code {e.returncode}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
