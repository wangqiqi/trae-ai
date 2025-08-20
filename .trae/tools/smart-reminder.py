#!/usr/bin/env python3
# 🧠 .trae 智能提示系统
# 使用方法: python .\.trae\tools\smart-reminder.py [场景]

import sys
import os
from datetime import datetime

class SmartReminder:
    def __init__(self):
        self.context_rules = {
            "start": {
                "message": "🚀 开发开始提醒",
                "checks": [
                    "✅ 需求文档是否已创建？",
                    "🔍 技术选型是否已对比？",
                    "⚙️ 开发环境是否已配置？"
                ],
                "next_action": "运行 .\.trae\tools\quick-checklist.ps1"
            },
            "coding": {
                "message": "⚡ 开发中提醒",
                "checks": [
                    "📝 是否同步更新文档？",
                    "🎯 是否按阶段实施？",
                    "🚫 是否避免了终端操作？"
                ],
                "next_action": "查看 .\.trae\tools\principles-cheat-sheet.md"
            },
            "deploy": {
                "message": "🚀 部署前提醒",
                "checks": [
                    "✅ 代码审查是否完成？",
                    "📋 文档是否更新完毕？",
                    "🧪 功能测试是否通过？"
                ],
                "next_action": "运行最终验收清单"
            }
        }
    
    def get_reminder(self, context="start"):
        if context not in self.context_rules:
            context = "start"
        
        rule = self.context_rules[context]
        
        print(f"\n{rule['message']}")
        print("=" * 30)
        
        for check in rule['checks']:
            print(f"{check}")
        
        print(f"\n📋 下一步: {rule['next_action']}")
        
        # 记录使用日志
        self.log_usage(context)
    
    def log_usage(self, context):
        log_file = ".trae/tools/usage.log"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} - 触发场景: {context}\n")

if __name__ == "__main__":
    context = sys.argv[1] if len(sys.argv) > 1 else "start"
    reminder = SmartReminder()
    reminder.get_reminder(context)