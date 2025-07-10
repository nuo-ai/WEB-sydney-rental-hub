@echo off
echo [1/2] 安装/检查必要的包...
C:\Python313\python.exe -m pip install -r requirements.txt
echo ✅ 依赖包安装/检查完成

echo.
echo [2/2] 开始测试自动更新...
C:\Python313\python.exe scripts/automated_data_update.py --once
pause
