#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trae IDE AI开发助手 - 一键启动版
直接在Trae中使用自然语言开发
"""

import sys
import os
from pathlib import Path

# 添加路径
sys.path.insert(0, str(Path(__file__).parent / ".trae" / "agents"))

try:
    from trae_ai_assistant import TraeAIDevelopmentAssistant
    
    def main():
        assistant = TraeAIDevelopmentAssistant()
        
        if len(sys.argv) > 1:
            # 命令行模式
            command = " ".join(sys.argv[1:])
            if command.lower() in ['list', '项目列表']:
                projects = assistant.list_projects()
                print("📋 当前项目列表：")
                for i, project in enumerate(projects, 1):
                    status_emoji = {
                        "planning": "📋",
                        "in_progress": "🚀", 
                        "completed": "✅",
                        "on_hold": "⏸️"
                    }
                    emoji = status_emoji.get(project['status'], "❓")
                    print(f"{i}. {emoji} {project['name']} - {project['progress']}% - {project['timeline']}")
            elif command.lower() in ['start', '启动']:
                assistant.start_development()
            else:
                # 直接创建项目
                assistant.create_project(command)
        else:
            # 交互式欢迎
            print("🎯 Trae IDE AI开发助手已就绪！")
            print("💡 使用方法：")
            print("   python trae-dev.py '你的需求描述'")
            print("   python trae-dev.py list  # 查看项目")
            print("   python trae-dev.py start # 启动开发环境")
            print("\n🚀 示例：")
            print("   python trae-dev.py '我想做一个任务管理应用'")
            print("   python trae-dev.py '创建Vue3电商网站，支持微信支付'")
            print("   python trae-dev.py '启动AI图像识别项目'")
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"⚠️  导入错误: {e}")
    print("正在初始化AI助手...")
    
    # 确保目录结构
    os.makedirs(".trae/agents", exist_ok=True)
    os.makedirs(".trae/data", exist_ok=True)
    
    print("✅ 初始化完成！请重新运行：")
    print("python trae-dev.py '你的需求描述'")