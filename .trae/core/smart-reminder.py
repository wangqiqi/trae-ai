#!/usr/bin/env python3
# 🔔 智能提醒工具 - 重构版
# 提供开发各阶段的关键提醒

import os
import platform
from datetime import datetime

class SmartReminder:
    """智能提醒系统"""
    
    def __init__(self):
        self.system = platform.system()
        self.reminders = {
            "start": {
                "title": "🚀 开发开始提醒",
                "checks": [
                    "✅ 需求文档是否已创建？",
                    "🔍 技术选型是否已对比？",
                    "⚙️ 开发环境是否已配置？"
                ],
                "next_action": "运行 python .trae/tools/project-assistant.py --report"
            },
            "developing": {
                "title": "💻 开发中提醒",
                "checks": [
                    "🔄 代码是否已提交？",
                    "📝 文档是否已更新？",
                    "🧪 测试是否已编写？"
                ],
                "next_action": "查看 python .trae/tools/smart-cleanup.py --analyze"
            },
            "deploy": {
                "title": "🚀 部署前提醒",
                "checks": [
                    "🧪 测试是否全部通过？",
                    "📊 性能是否已优化？",
                    "🔒 安全检查是否完成？"
                ],
                "next_action": "查看 .trae/principles.md"
            }
        }
    
    def show_reminder(self, phase="start"):
        """显示指定阶段的提醒"""
        reminder = self.reminders.get(phase, self.reminders["start"])
        
        print(f"\n{reminder['title']}")
        print("=" * 30)
        for check in reminder["checks"]:
            print(check)
        print(f"\n📋 下一步: {reminder['next_action']}")

if __name__ == "__main__":
    import sys
    phase = sys.argv[1] if len(sys.argv) > 1 else "start"
    reminder = SmartReminder()
    reminder.show_reminder(phase)