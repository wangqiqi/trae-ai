#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trae AI 快速启动脚本

一键启动Trae AI增强控制台，集成模板自动化功能
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """主函数"""
    base_dir = Path(__file__).parent
    console_script = base_dir / "workflows" / "trae-console-enhanced.py"
    
    if not console_script.exists():
        print("❌ 找不到增强控制台脚本")
        return
    
    try:
        # 启动增强控制台
        subprocess.run([sys.executable, str(console_script)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 启动失败: {e}")
    except KeyboardInterrupt:
        print("\n👋 再见！")

if __name__ == "__main__":
    main()