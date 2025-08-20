#!/usr/bin/env python3
# 🎨 .trae 交互体验深度优化工具
# 升级用户交互体验，提供更智能的引导

import os
import json
import platform
from datetime import datetime

class InteractiveEnhancer:
    def __init__(self):
        self.system = platform.system()
        self.user_data_file = ".trae/user_preferences.json"
        self.load_user_preferences()
    
    def load_user_preferences(self):
        """加载用户偏好设置"""
        if os.path.exists(self.user_data_file):
            with open(self.user_data_file, 'r', encoding='utf-8') as f:
                self.preferences = json.load(f)
        else:
            self.preferences = {
                "theme": "auto",
                "notifications": True,
                "auto_suggestions": True,
                "last_interaction": str(datetime.now()),
                "favorite_tools": [],
                "skill_level": "intermediate"
            }
            self.save_preferences()
    
    def save_preferences(self):
        """保存用户偏好"""
        os.makedirs(os.path.dirname(self.user_data_file), exist_ok=True)
        with open(self.user_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.preferences, f, indent=2, ensure_ascii=False)
    
    def get_welcome_message(self):
        """获取个性化欢迎信息"""
        level = self.preferences["skill_level"]
        
        messages = {
            "beginner": """
🌱 欢迎回到.trae！
看起来你是新手，让我来引导你：
1. 运行 `.\.trae\tools\quick-checklist-fixed.ps1` 检查项目状态
2. 查看 `.\.trae\templates\requirements-template.md` 学习写需求
3. 需要帮助时输入 `.\.trae\tools\interactive-enhancer.py help`
""",
            "intermediate": """
🚀 欢迎回来！
上次你使用了这些工具：{tools}
这次推荐：
1. 运行性能监控：`.\.trae\tools\performance-monitor.py`
2. 优化Windows：`.\.trae\tools\windows-enhancer.ps1`
3. 快速开始新项目：使用需求模板
""",
            "expert": """
🎯 大师级用户！
你的工具使用记录：{tools}
高级功能：
1. 自定义模板：`.\.trae\templates\`
2. 跨平台适配：`.\.trae\tools\cross-platform-adapter.py`
3. 深度优化：`.\.trae\tools\performance-monitor.py`
"""
        }
        
        tools = ", ".join(self.preferences["favorite_tools"][-3:]) if self.preferences["favorite_tools"] else "暂无"
        return messages[level].format(tools=tools)
    
    def get_smart_suggestions(self, context):
        """基于上下文提供智能建议"""
        suggestions = []
        
        # 根据项目状态提供建议
        if context == "new_project":
            suggestions = [
                "📋 使用需求模板开始项目规划",
                "🔍 进行技术选型对比",
                "✅ 运行项目状态检查"
            ]
        elif context == "development":
            suggestions = [
                "🎯 使用代码审查模板",
                "⚡ 运行性能监控",
                "📝 同步更新文档"
            ]
        elif context == "deployment":
            suggestions = [
                "🚀 使用部署指南模板",
                "✅ 运行最终验收清单",
                "🔍 检查系统性能"
            ]
        
        return suggestions
    
    def create_project_starter(self, project_name, project_type):
        """创建项目启动器"""
        starter_config = {
            "project_name": project_name,
            "project_type": project_type,
            "created_at": str(datetime.now()),
            "next_steps": [
                f"📁 创建 {project_name} 目录结构",
                f"📋 复制 {project_type} 需求模板",
                f"🔍 运行项目初始化检查",
                f"🚀 启动开发环境"
            ],
            "templates_to_use": {
                "web": ["requirements-template.md", "tech-choice-template.md"],
                "mobile": ["requirements-template.md", "deployment-template.md"],
                "api": ["requirements-template.md", "code-review-template.md"]
            }
        }
        
        # 保存项目配置
        config_path = f".trae/projects/{project_name}.json"
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(starter_config, f, indent=2, ensure_ascii=False)
        
        return starter_config
    
    def show_interactive_menu(self):
        """显示交互式菜单"""
        menu = """
🎨 .trae 交互体验中心
========================
1. 🚀 新项目快速启动
2. 📊 系统性能监控
3. 🧹 一键系统优化
4. 📚 模板快速选择
5. ⚙️ 个性化设置
6. ❓ 帮助与教程

请输入数字选择功能 (1-6): """
        
        print(menu)
        return input().strip()
    
    def run_interactive_mode(self):
        """运行交互模式"""
        print(self.get_welcome_message())
        
        while True:
            choice = self.show_interactive_menu()
            
            if choice == "1":
                project_name = input("🎯 输入项目名称: ").strip()
                project_type = input("📱 选择项目类型 (web/mobile/api): ").strip()
                config = self.create_project_starter(project_name, project_type)
                print(f"🚀 项目 '{project_name}' 启动配置已创建!")
                for step in config["next_steps"]:
                    print(f"  {step}")
            
            elif choice == "2":
                os.system("python .\.trae\tools\performance-monitor.py")
            
            elif choice == "3":
                if self.system == "Windows":
                    os.system("powershell -ExecutionPolicy Bypass -File .\.trae\tools\windows-enhancer.ps1")
                else:
                    print("🌍 跨平台优化工具开发中...")
            
            elif choice == "4":
                print("📚 可用模板:")
                templates = ["requirements", "tech-choice", "code-review", "deployment"]
                for i, template in enumerate(templates, 1):
                    print(f"{i}. {template}-template.md")
            
            elif choice == "5":
                print("⚙️ 个性化设置功能开发中...")
            
            elif choice == "6":
                print("❓ 帮助文档: .\.trae\principles-v2.md")
                break
            
            else:
                print("❌ 无效选择，请重新输入")
            
            continue_choice = input("\n继续操作? (y/n): ").strip().lower()
            if continue_choice != 'y':
                break

# 使用示例
if __name__ == "__main__":
    enhancer = InteractiveEnhancer()
    enhancer.run_interactive_mode()