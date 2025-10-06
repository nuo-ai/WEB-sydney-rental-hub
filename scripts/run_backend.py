import subprocess
import sys
from pathlib import Path


def main():
    repo_root = Path(__file__).resolve().parent.parent

    cmd = [
        "pnpm",
        "--filter",
        "@web-sydney/backend",
        "dev",
    ]

    try:
        subprocess.run(
            cmd,
            cwd=str(repo_root),
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Backend server failed to start with exit code {e.returncode}")
        sys.exit(1)
    except FileNotFoundError:
        print("pnpm command not found. Please install pnpm to run the backend server.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
