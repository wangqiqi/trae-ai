@echo off
setlocal enabledelayedexpansion

echo 🎯 Trae AI 系统级配置应用工具
echo =================================

:: 检查管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 需要管理员权限，请右键以管理员身份运行
    pause
    exit /b 1
)

:: 设置变量
set SYSTEM_RULES_PATH=%USERPROFILE%\.trae-cn\user_rules.md
set BACKUP_PATH=%USERPROFILE%\.trae-cn\user_rules.md.backup
set TEMPLATE_PATH=%~dp0system-level-user-rules-template.md

echo 📁 系统规则路径: %SYSTEM_RULES_PATH%

:: 备份现有配置
if exist "%SYSTEM_RULES_PATH%" (
    echo 📦 备份现有配置...
    copy "%SYSTEM_RULES_PATH%" "%BACKUP_PATH%" >nul
    echo ✅ 已备份到: %BACKUP_PATH%
)

:: 应用新的系统级配置
echo 🚀 应用系统级配置...
if exist "%TEMPLATE_PATH%" (
    copy "%TEMPLATE_PATH%" "%SYSTEM_RULES_PATH%" >nul
    echo ✅ 系统级配置已更新
) else (
    echo ❌ 模板文件不存在: %TEMPLATE_PATH%
    pause
    exit /b 1
)

:: 验证配置
echo 🔍 验证配置...
if exist "%SYSTEM_RULES_PATH%" (
    echo ✅ 配置文件已创建
    echo 📊 文件大小: 
    for %%F in ("%SYSTEM_RULES_PATH%") do echo    %%~zF bytes
) else (
    echo ❌ 配置应用失败
    pause
    exit /b 1
)

echo.
echo 🎉 系统级配置应用完成！
echo 💡 现在你可以：
echo    1. 重新启动 Trae IDE
echo    2. 在任何项目中使用全局AI规则
echo    3. 享受标准化的开发体验

echo.
echo 🔧 如需恢复，请运行: 
echo    copy "%BACKUP_PATH%" "%SYSTEM_RULES_PATH%"

pause