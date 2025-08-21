#!/usr/bin/env python3
"""
🎯 项目初始化器
为新项目快速配置超级团队
"""

import os
import json
import shutil
import sys
from pathlib import Path

class ProjectInitializer:
    """项目初始化器"""
    
    def __init__(self):
        self.source_dir = Path(__file__).parent.parent  # 指向 .trae 目录
        self.target_dir = Path.cwd()
    
    def init_new_project(self, project_name: str = None):
        """初始化新项目"""
        project_name = project_name or self.target_dir.name
        
        print(f"🎯 正在初始化项目: {project_name}")
        
        # 1. 复制 .trae 目录
        target_trae = self.target_dir / ".trae"
        if target_trae.exists():
            print("⚠️  .trae 目录已存在，跳过复制")
        else:
            shutil.copytree(self.source_dir, target_trae)
            print("✅ .trae 超级团队已复制")
        
        # 2. 创建项目配置文件
        self.create_project_config(project_name)
        
        # 3. 初始化Git忽略
        self.setup_gitignore()
        
        # 4. 项目设置（来自team-launcher.py的setup功能）
        self.setup_project_agents()
        
        print(f"\n🎉 项目 {project_name} 初始化完成！")
        print(f"💡 运行: python .trae/workflows/trae-console.py 启动AI控制台")
    
    def create_project_config(self, project_name: str):
        """创建项目配置"""
        config = {
            "project_name": project_name,
            "trae_version": "3.0",
            "initialized_at": "auto-generated",
            "features": {
                "ai_agents": True,
                "environment_management": True,
                "deployment_tools": True,
                "monitoring": True
            }
        }
        
        config_file = self.target_dir / ".trae-project.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print("✅ 项目配置已创建")
    
    def setup_gitignore(self):
        """设置Git忽略文件"""
        gitignore_path = self.target_dir / ".gitignore"
        
        ignore_content = """
# Trae AI 超级团队
.trae/logs/
.trae/temp/
.trae/cache/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
        
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(ignore_content.strip())
        
        print("✅ .gitignore 已配置")

    def setup_project_agents(self):
        """项目智能体设置（来自team-launcher.py的setup功能）"""
        print("🎯 正在配置项目智能体...")
        
        # 创建项目专用配置
        project_config = {
            "project_name": self.target_dir.name,
            "created_at": "auto-generated",
            "agents_enabled": True,
            "auto_start": False,
            "team_config": {
                "mode": "project",
                "members": ["产品经理", "系统架构师", "项目经理", "项目协调员"]
            }
        }
        
        config_path = self.target_dir / ".trae-project.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(project_config, f, ensure_ascii=False, indent=2)
        
        print("✅ 项目智能体配置完成")
    
    def quick_setup(self):
        """快速设置向导"""
        print("""
🎯 Trae超级团队 - 项目初始化向导

这个工具将帮助你在新项目中快速配置完整的AI智能体团队。
        """)
        
        project_name = input("请输入项目名称 (留空使用当前目录名): ").strip()
        if not project_name:
            project_name = self.target_dir.name
        
        confirm = input(f"确认初始化项目 '{project_name}' ? (y/n): ").strip().lower()
        if confirm == 'y':
            self.init_new_project(project_name)
        else:
            print("❌ 已取消")

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        initializer = ProjectInitializer()
        initializer.quick_setup()
    else:
        print("""
🎯 Trae超级团队 - 项目初始化器

用法:
    python project-init.py quick     # 交互式初始化
    python project-init.py auto      # 自动初始化当前项目

示例:
    # 在新项目中使用
    cd my-new-project
    python /path/to/learn_trae/.trae/project-init.py quick
        """)

if __name__ == "__main__":
    main()