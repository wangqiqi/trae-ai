@echo off
cd /d %~dp0

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python未安装或未添加到PATH
    echo 请安装Python 3.8+ 并确保已添加到系统PATH
    pause
    exit /b 1
)

:: 运行主程序
python trae.py %*