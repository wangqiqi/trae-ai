#!/bin/bash
cd "$(dirname "$0")"
python3 trae.py "$@"

# 确保脚本有执行权限
chmod +x "$0" 2>/dev/null || true