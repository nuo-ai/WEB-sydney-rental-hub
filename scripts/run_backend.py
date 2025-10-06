from __future__ import annotations

import subprocess
import sys
from pathlib import Path

def _resolve_env_file(project_root: Path, backend_path: Path) -> Path | None:
    candidates = [project_root / ".env", backend_path / ".env"]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None

def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    backend_path = project_root / "apps" / "backend"

    if not backend_path.exists():
        raise FileNotFoundError(f"Backend directory not found at {backend_path}")

    env_file_path = _resolve_env_file(project_root, backend_path)

    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "backend.main:app",
        "--reload",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
    ]

    if env_file_path is not None:
        cmd.extend(["--env-file", str(env_file_path)])

    try:
        subprocess.run(
            cmd,
            cwd=str(project_root),
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        print(f"Backend server failed to start with exit code {exc.returncode}")
        sys.exit(exc.returncode or 1)
    except Exception as exc:  # pragma: no cover - defensive logging
        print(f"An error occurred: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    main()
