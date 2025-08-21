#!/bin/bash
# 启动Trae AI系统

# 切换到脚本所在目录
cd "$(dirname "$0")"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] Python3未安装"
    echo "请安装Python 3.8+"
    exit 1
fi

# 检查Python版本
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "检测到Python版本: $python_version"

# 启动主程序
python3 trae.py "$@"