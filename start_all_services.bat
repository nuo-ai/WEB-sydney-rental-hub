@echo off
echo ========================================
echo 悉尼租房平台 - 一键启动
echo ========================================
echo.

echo [1/4] 检查Python环境...
C:\Python313\python.exe --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：指定的Python (C:\Python313\python.exe) 不存在
    echo 请确认Python安装路径
    pause
    exit /b 1
)
echo ✅ Python已找到

echo.
echo [2/4] 安装必要的包...
C:\Python313\python.exe -m pip install -r requirements.txt
echo ✅ 依赖包安装完成

echo.
echo [3/4] 启动后端服务...
start cmd /k "cd backend && C:\Python313\python.exe main.py"
timeout /t 5 >nul

echo.
echo [4/4] 启动前端服务...
start cmd /k "cd frontend && C:\Python313\python.exe -m http.server 8080"
timeout /t 3 >nul

echo.
echo ========================================
echo ✅ 所有服务已启动！
echo.
echo 前端地址: http://localhost:8080
echo 后端地址: http://localhost:8000
echo.
echo 按任意键打开网站...
echo ========================================
pause >nul

start http://localhost:8080
