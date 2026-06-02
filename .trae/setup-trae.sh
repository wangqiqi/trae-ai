#!/bin/bash
# Trae AI 一键集成脚本
# 自动配置当前项目为 Trae AI 兼容项目

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  🔧 Trae AI 一键集成${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查 .trae 目录
if [ ! -d ".trae" ]; then
    echo -e "${RED}❌ 错误: 未找到 .trae 目录${NC}"
    exit 1
fi

# 创建 .trae/rules 目录
echo -e "${YELLOW}📁 创建 Trae 规则目录...${NC}"
mkdir -p .trae/rules

# 复制规则文件
echo -e "${YELLOW}📋 复制 Trae 规则文件...${NC}"
if [ -d ".trae/templates" ]; then
    cp -r .trae/templates/* .trae/rules/ 2>/dev/null || true
fi

# 创建项目配置
echo -e "${YELLOW}⚙️ 创建项目配置...${NC}"
cat > .trae-project.json << 'EOF'
{
  "project_name": "$(basename $PWD)",
  "trae_version": "5.0",
  "skills_enabled": true,
  "auto_detect": true,
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

# 创建 .gitignore 规则
echo -e "${YELLOW}🔒 配置 .gitignore...${NC}"
if [ -f ".gitignore" ]; then
    if ! grep -q "# Trae AI" .gitignore; then
        echo "" >> .gitignore
        echo "# Trae AI" >> .gitignore
        echo ".trae/cache/" >> .gitignore
        echo ".trae-user/" >> .gitignore
        echo "*.pyc" >> .gitignore
        echo "__pycache__/" >> .gitignore
    fi
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ✅ Trae AI 集成完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}📖 下一步：${NC}"
echo -e "   1. 运行控制台: ${YELLOW}python3 .trae/workflows/trae-console.py${NC}"
echo -e "   2. 启动智能检测: ${YELLOW}python3 .trae/workflows/trae-console.py${NC}"
echo ""
echo -e "${BLUE}🎯 智能功能：${NC}"
echo -e "   • 自动检测项目类型"
echo -e "   • 推荐合适的技能"
echo -e "   • 零配置开箱即用"
echo ""
