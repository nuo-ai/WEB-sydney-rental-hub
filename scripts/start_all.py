#!/usr/bin/env python3
"""
统一启动脚本 - 启动所有服务
适配新的项目目录结构
"""
import subprocess
import sys
import time
import signal
from pathlib import Path
from threading import Thread

def start_backend():
    """启动后端API服务"""
    print("🚀 启动后端API服务...")
    backend_path = Path(__file__).parent.parent / "backend"
    
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "main:app", 
        "--reload", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ]
    
    try:
        process = subprocess.Popen(cmd, cwd=str(backend_path))
        print("✅ 后端API启动成功 - http://localhost:8000")
        return process
    except Exception as e:
        print(f"❌ 后端API启动失败: {e}")
        return None

def start_frontend():
    """启动前端开发服务器"""
    print("🚀 启动前端服务...")
    frontend_path = Path(__file__).parent.parent / "frontend"
    
    cmd = [sys.executable, "-m", "http.server", "8080"]
    
    try:
        process = subprocess.Popen(cmd, cwd=str(frontend_path))
        print("✅ 前端服务启动成功 - http://localhost:8080")
        return process
    except Exception as e:
        print(f"❌ 前端服务启动失败: {e}")
        return None

def start_mcp_server():
    """启动MCP服务器"""
    print("🚀 启动MCP服务器...")
    mcp_path = Path(__file__).parent.parent / "mcp-server"
    
    # 首先确保已经编译
    build_cmd = ["npm", "run", "build"]
    try:
        subprocess.run(build_cmd, cwd=str(mcp_path), shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ MCP服务器编译失败: {e}")
        return None

    cmd = ["node", "build/index.js"]
    
    try:
        process = subprocess.Popen(cmd, cwd=str(mcp_path), shell=True)
        print("✅ MCP服务器启动成功")
        return process
    except Exception as e:
        print(f"❌ MCP服务器启动失败: {e}")
        return None

def main():
    print("🎯 Sydney Rental Platform - 启动所有服务")
    print("=" * 50)
    
    processes = []
    
    # 启动后端
    backend_process = start_backend()
    if backend_process:
        processes.append(backend_process)
    
    # 等待一下让后端启动
    time.sleep(5)
    
    # 启动前端
    frontend_process = start_frontend()
    if frontend_process:
        processes.append(frontend_process)
        
    # 等待一下让前端启动
    time.sleep(2)
    
    # 启动MCP服务器
    mcp_process = start_mcp_server()
    if mcp_process:
        processes.append(mcp_process)
    
    if not processes:
        print("❌ 没有服务启动成功")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 所有服务启动完成！")
    print("📱 前端: http://localhost:8080")
    print("🔧 后端API: http://localhost:8000")
    print("🤖 MCP服务器: 已启动")
    print("\n按 Ctrl+C 停止所有服务")
    
    def signal_handler(sig, frame):
        print("\n🛑 正在停止所有服务...")
        for process in processes:
            try:
                process.terminate()
            except:
                pass
        print("✅ 所有服务已停止")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # 等待所有进程
    for process in processes:
        try:
            process.wait()
        except:
            pass

if __name__ == "__main__":
    main()
