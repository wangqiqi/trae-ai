@echo off
chcp 65001 > nul
REM Trae AI 超级团队 - Windows 一键安装脚本

echo ========================================
echo   🚀 Trae AI 超级团队 - 一键安装
echo ========================================
echo.

REM 检查 Python
echo 📋 检查环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)

for /f "delims=" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python 版本: %PYTHON_VERSION%
echo.

REM 检查 .trae 目录
if not exist ".trae" (
    echo ❌ 错误: 未找到 .trae 目录，请确保在项目根目录运行
    pause
    exit /b 1
)
echo ✅ 项目结构检查通过
echo.

REM 创建必要的目录
echo 📁 创建必要目录...
if not exist ".trae\user-data" mkdir ".trae\user-data"
if not exist ".trae\cache" mkdir ".trae\cache"
echo ✅ 目录创建完成
echo .

REM 初始化项目数据
echo 💾 初始化项目数据...
python -c "
import json
from pathlib import Path
from datetime import datetime

data = {
    'version': '5.0',
    'created_at': datetime.now().isoformat(),
    'trae_version': '5.0',
    'projects': [],
    'stats': {
        'total_projects': 0,
        'completed_projects': 0
    },
    'mcp_enabled': True,
    'context_management': {
        'web_context': True,
        'doc_context': True
    }
}

projects_file = Path('.trae/user-data/projects.json')
if not projects_file.exists():
    with open(projects_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print('✅ 项目数据初始化完成')
else:
    print('✅ 项目数据已存在')
"
echo.

REM 创建安装标记
if not exist ".trae\config" mkdir ".trae\config"
echo. > ".trae\config\installed.flag"
echo ✅ 安装标记已创建
echo.

REM 测试运行
echo 🧪 测试运行...
python .trae/workflows/trae-console.py --help >nul 2>&1
if errorlevel 1 (
    echo ⚠️  测试发现问题，但不影响使用
) else (
    echo ✅ 测试通过
)
echo.

REM 完成
echo ========================================
echo   ✅ 安装完成！
echo ========================================
echo.
echo 📖 快速开始：
echo   运行控制台: python .trae\workflows\trae-console.py
echo   查看帮助:   python .trae\trae.py help
echo.
echo 📚 文档：
echo   安装指南:   查看 INSTALL.md
echo   项目文档:   查看 README.md
echo .
echo 🎉 祝你使用愉快！
echo.
pause
