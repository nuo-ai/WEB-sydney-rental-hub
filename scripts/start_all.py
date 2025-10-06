#!/usr/bin/env python3
"""
统一启动脚本 - 启动所有服务
适配新的项目目录结构
"""
from __future__ import annotations

import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional


def _resolve_env_file(project_root: Path, backend_path: Path) -> Optional[Path]:
    for candidate in (project_root / ".env", backend_path / ".env"):
        if candidate.exists():
            return candidate
    return None


def _node_runner() -> Optional[str]:
    for candidate in ("pnpm", "npm"):
        if shutil.which(candidate):
            return candidate
    return None


def start_backend(project_root: Path) -> Optional[subprocess.Popen[bytes]]:
    """启动后端API服务"""
    print("🚀 启动后端API服务...")
    backend_path = project_root / "apps" / "backend"

    if not backend_path.exists():
        print(f"❌ 后端目录不存在: {backend_path}")
        return None

    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "backend.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
    ]

    env_file = _resolve_env_file(project_root, backend_path)
    if env_file is not None:
        cmd.extend(["--env-file", str(env_file)])

    try:
        process = subprocess.Popen(cmd, cwd=str(project_root))
        print("✅ 后端API启动成功 - http://localhost:8000")
        return process
    except Exception as exc:  # pragma: no cover - defensive logging
        print(f"❌ 后端API启动失败: {exc}")
        return None


def start_frontend(project_root: Path) -> tuple[Optional[subprocess.Popen[bytes]], str]:
    """启动前端开发服务器"""
    print("🚀 启动前端服务...")
    frontend_path = project_root / "vue-frontend"

    default_target = "http://localhost:5173"
    if not frontend_path.exists():
        print(f"❌ 找不到前端目录: {frontend_path}")
        return None, default_target

    runner = _node_runner()
    if runner is not None:
        cmd = [runner, "run", "dev"]
        target = default_target
    else:
        print("⚠️ 未检测到 pnpm/npm，将回退到 Python 静态服务器 (仅供调试)。")
        cmd = [sys.executable, "-m", "http.server", "8080"]
        target = "http://localhost:8080"

    try:
        process = subprocess.Popen(cmd, cwd=str(frontend_path))
        print(f"✅ 前端服务启动成功 - {target}")
        return process, target
    except Exception as exc:  # pragma: no cover - defensive logging
        print(f"❌ 前端服务启动失败: {exc}")
        return None, default_target


def start_mcp_server(project_root: Path) -> Optional[subprocess.Popen[bytes]]:
    """启动MCP服务器"""
    print("🚀 启动MCP服务器...")
    mcp_path = project_root / "mcp-server"

    is_windows = sys.platform == "win32"

    # 1. 编译
    print("    - 正在编译MCP服务器...")
    build_cmd = ["npm", "run", "build"]
    try:
        subprocess.run(build_cmd, cwd=str(mcp_path), check=True, shell=is_windows)
        print("    - MCP服务器编译完成。")
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"❌ MCP服务器编译失败: {exc}")
        return None

    # 2. 启动
    # 直接用node运行编译后的文件，而不是npm start
    start_cmd = ["node", "build/api/index.js"]
    try:
        process = subprocess.Popen(start_cmd, cwd=str(mcp_path), shell=is_windows)
        print("✅ MCP服务器启动成功 - http://localhost:3002")
        return process
    except Exception as exc:  # pragma: no cover - defensive logging
        print(f"❌ MCP服务器启动失败: {exc}")
        return None


def main() -> None:
    print("🎯 Sydney Rental Platform - 启动所有服务")
    print("=" * 50)

    project_root = Path(__file__).resolve().parent.parent
    processes: list[subprocess.Popen[bytes]] = []

    # 启动后端
    backend_process = start_backend(project_root)
    if backend_process:
        processes.append(backend_process)

    # 等待一下让后端启动
    time.sleep(5)

    # 启动前端
    frontend_process, frontend_url = start_frontend(project_root)
    if frontend_process:
        processes.append(frontend_process)

    # 等待一下让前端启动
    time.sleep(2)

    # 启动MCP服务器
    mcp_process = start_mcp_server(project_root)
    if mcp_process:
        processes.append(mcp_process)

    if not processes:
        print("❌ 没有服务启动成功")
        sys.exit(1)

    backend_url = "http://localhost:8000" if backend_process else "未启动"
    frontend_url_display = frontend_url if frontend_process else "未启动"
    mcp_url = "http://localhost:3002" if mcp_process else "未启动"

    print()
    print("=" * 50)
    print("🎉 所有服务启动完成！")
    print(f"📱 前端: {frontend_url_display}")
    print(f"🔧 后端API: {backend_url}")
    print(f"🤖 MCP服务器: {mcp_url}")
    print()
    print("按 Ctrl+C 停止所有服务")

    def signal_handler(sig: int, frame) -> None:  # type: ignore[override]
        print()
        print("🛑 正在停止所有服务...")
        for process in processes:
            try:
                process.terminate()
            except Exception:
                pass
        print("✅ 所有服务已停止")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # 等待所有进程
    for process in processes:
        try:
            process.wait()
        except Exception:
            pass


if __name__ == "__main__":
    main()
