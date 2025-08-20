@echo off
echo.
echo 🎯 .trae 原则驱动开发系统启动中...
echo.
echo 📋 当前启用的核心原则：
echo    ✅ PRINCIPLE-001 - 需求澄清原则
echo    ✅ PRINCIPLE-002 - 技术选型对比原则
echo    ✅ PRINCIPLE-003 - 文档驱动开发原则
echo    ✅ PRINCIPLE-004 - 渐进式实施原则
echo.
echo 🛠️ 可用命令：
echo    python scripts/team-launcher.py !principle 需求描述
echo    python scripts/trae-console.py --principle-mode
echo.
echo 📚 查看完整原则文档：
echo    打开 .trae/principles.md
echo.

:: 启动原则模式下的控制台
python scripts/trae-console.py --principle-mode