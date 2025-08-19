#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trae IDE AI开发助手
直接在Trae对话框中使用的AI驱动开发助手
版本：v2.0-Trae集成版
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import subprocess
import webbrowser
import re
from datetime import datetime

class TraeAIDevelopmentAssistant:
    """Trae IDE内AI开发助手"""
    
    def __init__(self):
        self.workspace = Path.cwd()
        self.config_dir = self.workspace / ".trae"
        self.agents_dir = self.config_dir / "agents"
        self.templates_dir = self.config_dir / "templates"
        self.data_dir = self.config_dir / "data"
        
        # 确保目录存在
        self.config_dir.mkdir(exist_ok=True)
        self.agents_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
        
        # 初始化项目数据
        self.projects_file = self.data_dir / "projects.json"
        self._init_project_data()
        
    def _init_project_data(self):
        """初始化项目数据"""
        if not self.projects_file.exists():
            default_projects = [
                {
                    "id": "demo-todo",
                    "name": "智能Todo管理应用",
                    "type": "web",
                    "description": "基于Vue3+FastAPI的现代化任务管理系统",
                    "status": "in_progress",
                    "progress": 65,
                    "risk_level": "low",
                    "timeline": "1-2周",
                    "tech_stack": ["Vue3", "FastAPI", "SQLite", "Docker"],
                    "features": ["任务CRUD", "用户认证", "分类管理", "优先级", "响应式设计"],
                    "created_at": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat()
                },
                {
                    "id": "demo-blog",
                    "name": "个人技术博客系统",
                    "type": "web",
                    "description": "React+Node.js驱动的现代化博客平台",
                    "status": "planning",
                    "progress": 15,
                    "risk_level": "medium",
                    "timeline": "3-4周",
                    "tech_stack": ["React", "Node.js", "MongoDB", "Redis"],
                    "features": ["文章管理", "评论系统", "SEO优化", "Markdown编辑器", "响应式设计"],
                    "created_at": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat()
                },
                {
                    "id": "demo-ecommerce",
                    "name": "精品电商小程序",
                    "type": "miniprogram",
                    "description": "uni-app多端电商解决方案",
                    "status": "completed",
                    "progress": 100,
                    "risk_level": "medium",
                    "timeline": "4-6周",
                    "tech_stack": ["uni-app", "FastAPI", "MySQL", "微信支付", "支付宝"],
                    "features": ["商品展示", "购物车", "订单管理", "支付集成", "多端发布"],
                    "created_at": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat()
                }
            ]
            
            with open(self.projects_file, 'w', encoding='utf-8') as f:
                json.dump(default_projects, f, ensure_ascii=False, indent=2)
    
    def parse_natural_language_requirement(self, requirement: str) -> Dict[str, Any]:
        """将自然语言需求解析为项目规范"""
        
        # 关键词匹配
        keywords = {
            "todo": ["任务", "todo", "待办", "清单", "任务管理"],
            "blog": ["博客", "文章", "发布", "写作", "内容"],
            "ecommerce": ["电商", "购物", "商品", "订单", "支付"],
            "ai": ["ai", "人工智能", "识别", "机器学习", "深度学习"],
            "miniprogram": ["小程序", "微信", "支付宝", "uni-app"],
            "vue": ["vue", "vue3", "前端", "界面"],
            "react": ["react", "reactjs", "前端"],
            "fastapi": ["fastapi", "python", "后端", "api"],
            "nodejs": ["nodejs", "node", "javascript", "后端"],
            "flutter": ["flutter", "移动", "app", "跨平台"]
        }
        
        # 分析需求类型
        project_type = "web"  # 默认
        tech_stack = []
        features = []
        timeline = "2-4周"
        risk_level = "low"
        
        requirement_lower = requirement.lower()
        
        # 检测项目类型
        for type_key, type_keywords in keywords.items():
            if any(keyword in requirement_lower for keyword in type_keywords):
                if type_key in ["todo", "blog", "ecommerce", "ai"]:
                    project_type = type_key
                break
        
        # 检测技术栈
        if "vue" in requirement_lower or "vue3" in requirement_lower:
            tech_stack.append("Vue3")
            tech_stack.append("FastAPI")
        elif "react" in requirement_lower:
            tech_stack.append("React")
            tech_stack.append("Node.js")
        elif "flutter" in requirement_lower:
            tech_stack.append("Flutter")
            tech_stack.append("FastAPI")
        elif "miniprogram" in requirement_lower or "小程序" in requirement_lower:
            tech_stack.append("uni-app")
            tech_stack.append("FastAPI")
        else:
            # 智能推荐
            if project_type == "ai":
                tech_stack = ["Vue3", "FastAPI", "Python AI", "TensorFlow"]
            elif project_type == "ecommerce":
                tech_stack = ["Vue3", "FastAPI", "MySQL", "Docker"]
            else:
                tech_stack = ["Vue3", "FastAPI", "SQLite"]
        
        # 检测功能需求
        if "用户" in requirement or "登录" in requirement:
            features.append("用户认证")
        if "管理" in requirement:
            features.append("后台管理")
        if "支付" in requirement:
            features.append("支付集成")
            risk_level = "medium"
        if "响应式" in requirement or "手机" in requirement:
            features.append("响应式设计")
        if "ai" in requirement_lower or "智能" in requirement:
            features.append("AI功能")
            risk_level = "medium"
        
        # 检测时间要求
        timeline_match = re.search(r'(\d+)[\s]*[周天月]', requirement)
        if timeline_match:
            timeline = f"{timeline_match.group(1)}周"
        
        # 生成项目规范
        project_spec = {
            "name": self._generate_project_name(project_type, requirement),
            "type": project_type,
            "description": requirement,
            "tech_stack": tech_stack,
            "features": features,
            "timeline": timeline,
            "risk_level": risk_level,
            "status": "planning",
            "progress": 0,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
        return project_spec
    
    def _generate_project_name(self, project_type: str, requirement: str) -> str:
        """生成项目名称"""
        names = {
            "todo": "智能任务管理系统",
            "blog": "个人博客平台",
            "ecommerce": "精品电商平台",
            "ai": "AI智能识别系统",
            "miniprogram": "多端小程序应用"
        }
        
        base_name = names.get(project_type, "创新项目")
        
        # 添加时间戳避免重复
        timestamp = datetime.now().strftime("%m%d")
        return f"{base_name}_{timestamp}"
    
    def create_project(self, requirement: str) -> Dict[str, Any]:
        """根据需求创建项目"""
        print("🤖 正在分析您的需求...")
        
        # 解析需求
        project_spec = self.parse_natural_language_requirement(requirement)
        
        print(f"📋 项目分析结果：")
        print(f"   项目名称：{project_spec['name']}")
        print(f"   项目类型：{project_spec['type']}")
        print(f"   技术栈：{' + '.join(project_spec['tech_stack'])}")
        print(f"   开发周期：{project_spec['timeline']}")
        print(f"   风险等级：{project_spec['risk_level']}")
        print(f"   核心功能：{', '.join(project_spec['features'])}")
        
        # 保存项目
        with open(self.projects_file, 'r', encoding='utf-8') as f:
            projects = json.load(f)
        
        projects.append(project_spec)
        
        with open(self.projects_file, 'w', encoding='utf-8') as f:
            json.dump(projects, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 项目已创建！项目ID: {project_spec['type']}_{len(projects)}")
        
        # 生成下一步建议
        self._generate_next_steps(project_spec)
        
        return project_spec
    
    def _generate_next_steps(self, project_spec: Dict[str, Any]):
        """生成下一步操作建议"""
        print("\n🎯 下一步操作：")
        print("1. 启动开发环境：python .trae/scripts/solo-console.py start")
        print("2. 打开Web界面：http://localhost:8000")
        print("3. 查看项目详情：在Web界面中查看项目进度")
        print("4. 开始开发：根据技术栈选择对应的开发模式")
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """列出所有项目"""
        with open(self.projects_file, 'r', encoding='utf-8') as f:
            projects = json.load(f)
        return projects
    
    def get_project_status(self, project_id: str) -> Optional[Dict[str, Any]]:
        """获取项目状态"""
        projects = self.list_projects()
        for project in projects:
            if project.get('id') == project_id or project.get('name') == project_id:
                return project
        return None
    
    def start_development(self, project_id: str = None):
        """启动开发环境"""
        print("🚀 正在启动SOLO开发环境...")
        
        # 启动API服务器
        api_script = self.config_dir / "scripts" / "solo-api-server.py"
        if api_script.exists():
            print("✅ API服务器已就绪")
            webbrowser.open("http://localhost:8000")
            print("📱 Web界面已打开：http://localhost:8000")
        else:
            print("⚠️  API服务器脚本不存在，尝试启动简化模式...")
            self._start_simplified_mode()
    
    def _start_simplified_mode(self):
        """启动简化模式"""
        print("🎯 启动简化开发模式...")
        print("1. 打开终端")
        print("2. 运行：python .trae/scripts/solo-console.py start")
        print("3. 访问：http://localhost:8000")
    
    def interactive_mode(self):
        """交互式模式"""
        print("🎯 Trae IDE AI开发助手 v2.0")
        print("=" * 50)
        print("💡 使用方法：")
        print("   直接告诉我你想要什么，我来帮你完成！")
        print("   例如：")
        print("   - '我想做一个任务管理应用'")
        print("   - '创建一个Vue3的博客系统'")
        print("   - '启动电商小程序项目'")
        print("   - '查看我的项目列表'")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n🤖 请描述你的需求：").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', '退出']:
                    print("👋 感谢使用！再见！")
                    break
                
                if user_input.lower() in ['list', '列表', '项目']:
                    projects = self.list_projects()
                    print("\n📋 项目列表：")
                    for i, project in enumerate(projects, 1):
                        print(f"{i}. {project['name']} ({project['status']}) - {project['progress']}%")
                    continue
                
                if '启动' in user_input or '开始' in user_input:
                    self.start_development()
                    continue
                
                # 创建项目
                self.create_project(user_input)
                
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"❌ 出现错误：{e}")
                print("💡 请重新描述你的需求")

def main():
    """主函数"""
    assistant = TraeAIDevelopmentAssistant()
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "interactive":
            assistant.interactive_mode()
        elif command == "list":
            projects = assistant.list_projects()
            for project in projects:
                print(f"{project['name']} - {project['status']} - {project['progress']}%")
        elif command == "start":
            assistant.start_development()
        else:
            # 将剩余参数作为需求
            requirement = " ".join(sys.argv[1:])
            assistant.create_project(requirement)
    else:
        # 交互式模式
        assistant.interactive_mode()

if __name__ == "__main__":
    main()