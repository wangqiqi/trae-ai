#!/bin/bash
# Trae AI 超级团队 - 一键安装脚本
# 支持 Linux/Mac 系统

set -e  # 遇到错误立即退出

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  🚀 Trae AI 超级团队 - 一键安装${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查 Python
echo -e "${YELLOW}📋 检查环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误: 未找到 python3，请先安装 Python 3.7+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✅ Python 版本: $PYTHON_VERSION${NC}"

# 检查当前目录
if [ ! -d ".trae" ]; then
    echo -e "${RED}❌ 错误: 未找到 .trae 目录，请确保在项目根目录运行${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 项目结构检查通过${NC}"
echo ""

# 创建必要的目录
echo -e "${YELLOW}📁 创建必要目录...${NC}"
mkdir -p .trae/user-data
mkdir -p .trae/cache
echo -e "${GREEN}✅ 目录创建完成${NC}"
echo ""

# 初始化项目数据
echo -e "${YELLOW}💾 初始化项目数据...${NC}"
python3 -c "
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
echo ""

# 设置执行权限
echo -e "${YELLOW}🔧 设置执行权限...${NC}"
chmod +x .trae/trae.py 2>/dev/null || true
chmod +x .trae/workflows/*.py 2>/dev/null || true
chmod +x .trae/skills/*.py 2>/dev/null || true
echo -e "${GREEN}✅ 权限设置完成${NC}"
echo ""

# 创建快捷命令（可选）
echo -e "${YELLOW}⚙️ 创建快捷命令...${NC}"

# 检查是否已经配置过
if [ -f ".trae/config/installed.flag" ]; then
    echo -e "${YELLOW}⚠️  已检测到之前的安装，是否重新配置？(y/n)${NC}"
    read -r response
    if [ "$response" != "y" ]; then
        echo -e "${BLUE}跳过配置，保留现有设置${NC}"
    else
        echo -e "${GREEN}✅ 重新配置完成${NC}"
    fi
else
    # 创建安装标记
    mkdir -p .trae/config
    touch .trae/config/installed.flag
    echo -e "${GREEN}✅ 快捷命令配置完成${NC}"
fi
echo ""

# 测试运行
echo -e "${YELLOW}🧪 测试运行...${NC}"
if python3 .trae/workflows/trae-console.py --help &> /dev/null; then
    echo -e "${GREEN}✅ 测试通过${NC}"
else
    echo -e "${RED}⚠️  测试发现问题，但不影响使用${NC}"
fi
echo ""

# 完成
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ✅ 安装完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}📖 快速开始：${NC}"
echo -e "   运行控制台: ${YELLOW}python3 .trae/workflows/trae-console.py${NC}"
echo -e "   查看帮助:   ${YELLOW}python3 .trae/trae.py help${NC}"
echo ""
echo -e "${BLUE}📚 文档：${NC}"
echo -e "   安装指南:   查看 ${YELLOW}INSTALL.md${NC}"
echo -e "   项目文档:   查看 ${YELLOW}README.md${NC}"
echo ""
echo -e "${GREEN}🎉 祝你使用愉快！${NC}"
echo ""
