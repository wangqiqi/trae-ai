@echo off
chcp 65001 > nul
echo.
echo ======================================
echo 🚀 Trae AI 模板系统一键配置
echo ======================================
echo.

REM 检查Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.7+
    echo 📥 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python已安装

REM 检查目录结构
echo.
echo 📁 检查目录结构...
if not exist ".trae\templates" (
    echo ❌ 错误: 模板目录不存在
    exit /b 1
)

if not exist ".trae\workflows" (
    echo ❌ 错误: 工作流目录不存在
    exit /b 1
)

echo ✅ 目录结构完整

REM 检查关键文件
echo.
echo 🔍 检查关键文件...
set files_to_check=
set files_to_check=%files_to_check% .trae\templates\project-init-template.md
set files_to_check=%files_to_check% .trae\templates\requirements-template.md
set files_to_check=%files_to_check% .trae\templates\api-spec-template.md
set files_to_check=%files_to_check% .trae\templates\database-design-template.md
set files_to_check=%files_to_check% .trae\templates\test-plan-template.md
set files_to_check=%files_to_check% .trae\workflows\template-manager.py
set files_to_check=%files_to_check% .trae\workflows\trae-console-enhanced.py
set files_to_check=%files_to_check% .trae\quick-start.py

set all_files_exist=true
for %%f in (%files_to_check%) do (
    if not exist "%%f" (
        echo ❌ 缺失: %%f
        set all_files_exist=false
    )
)

if "%all_files_exist%"=="false" (
    echo ❌ 部分文件缺失，请检查安装包
    pause
    exit /b 1
)

echo ✅ 所有关键文件存在

REM 测试脚本语法
echo.
echo 🧪 测试脚本语法...
python -m py_compile .trae\workflows\template-manager.py
if %errorlevel% neq 0 (
    echo ❌ template-manager.py 语法错误
    pause
    exit /b 1
)

python -m py_compile .trae\workflows\trae-console-enhanced.py
if %errorlevel% neq 0 (
    echo ❌ trae-console-enhanced.py 语法错误
    pause
    exit /b 1
)

python -m py_compile .trae\quick-start.py
if %errorlevel% neq 0 (
    echo ❌ quick-start.py 语法错误
    pause
    exit /b 1
)

echo ✅ 所有脚本语法正确

REM 运行测试
echo.
echo 🧪 运行系统测试...
python test-template-system.py

if %errorlevel% neq 0 (
    echo ❌ 系统测试失败
    pause
    exit /b 1
)

echo.
echo ======================================
echo 🎉 配置完成！模板系统已就绪
echo ======================================
echo.
echo 🚀 快速开始：
echo   1. python .trae\quick-start.py          (启动控制台)
echo   2. python demo-template-usage.py demo   (运行演示)
echo   3. python test-template-system.py      (运行测试)
echo.
echo 📚 查看文档：
echo   - 打开 .trae\TEMPLATES-GUIDE.md        (完整指南)
echo   - 打开 README.md                     (项目说明)
echo.
echo 💡 提示：
echo   - 支持中文界面，无需额外配置
echo   - 支持所有主流技术栈
echo   - 支持一键生成完整项目
pause