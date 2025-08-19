@echo off
echo 正在启动SOLO智能开发控制台...
echo.

REM 设置环境变量
set PYTHONPATH=%cd%\.trae\scripts

REM 启动API服务器
echo 启动API服务器...
start cmd /k "cd /d %~dp0 && python .trae\scripts\solo-api-server.py"

REM 等待服务器启动
timeout /t 3 /nobreak > nul

REM 打开浏览器
echo 正在打开Web界面...
start http://localhost:8000

echo.
echo SOLO智能开发控制台已启动！
echo Web界面: http://localhost:8000
echo.
echo 按任意键退出...
pause > nul