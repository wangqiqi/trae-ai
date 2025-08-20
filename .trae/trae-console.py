#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trae AI v2.0 统一控制台
作者：Trae AI 团队
版本：v2.0.0
描述：一站式管理和操作所有v2.0智能体
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import subprocess
import argparse
from typing import Dict, List, Optional, Any

class TraeConsole:
    """Trae AI v2.0 统一控制台"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.agents_dir = self.base_dir / "agents2"
        self.user_data_dir = self.base_dir / "user-data"
        self.projects_file = self.user_data_dir / "projects.json"
        
        # 确保用户数据目录存在
        self.user_data_dir.mkdir(exist_ok=True)
        
        # 初始化项目数据
        self.init_projects_data()
    
    def init_projects_data(self):
        """初始化项目数据文件"""
        if not self.projects_file.exists():
            default_data = {
                "version": "2.0.0",
                "created_at": datetime.now().isoformat(),
                "projects": [],
                "stats": {
                    "total_projects": 0,
                    "completed_projects": 0,
                    "active_agents": 0
                }
            }
            self.save_projects_data(default_data)
    
    def load_projects_data(self) -> Dict[str, Any]:
        """加载项目数据"""
        try:
            with open(self.projects_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.init_projects_data()
            return self.load_projects_data()
    
    def save_projects_data(self, data: Dict[str, Any]):
        """保存项目数据"""
        with open(self.projects_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """获取所有v2.0智能体"""
        agents = []
        if not self.agents_dir.exists():
            return agents
        
        for agent_file in self.agents_dir.glob("*-v2.json"):
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    agent_data = json.load(f)
                    agent_data['filename'] = agent_file.name
                    agents.append(agent_data)
            except Exception as e:
                print(f"⚠️  加载智能体 {agent_file.name} 失败: {e}")
        
        return sorted(agents, key=lambda x: x.get('name', ''))
    
    def display_welcome(self):
        """显示欢迎界面"""
        print("\n" + "="*60)
        print("🤖 Trae AI v2.0 统一控制台")
        print("="*60)
        print("💡 提示：直接输入需求，让19个AI专家为你服务！")
        print("📋 示例：")
        print("   - 我想做一个Vue3+TypeScript的任务管理系统")
        print("   - 用React18+Next.js14做电商网站")
        print("   - 用Python+FastAPI做RESTful API")
        print()
    
    def display_agents_summary(self):
        """显示智能体概览"""
        agents = self.get_all_agents()
        if not agents:
            print("⚠️  未找到v2.0智能体文件")
            return
        
        print(f"\n📊 v2.0智能体概览 (共 {len(agents)} 个)")
        print("-" * 40)
        
        # 按类别分组
        categories = {}
        for agent in agents:
            category = agent.get('category', '其他')
            if category not in categories:
                categories[category] = []
            categories[category].append(agent)
        
        for category, category_agents in sorted(categories.items()):
            print(f"\n{category} ({len(category_agents)}个):")
            for agent in category_agents:
                name = agent.get('name', '未知')
                description = agent.get('description', '')[:50]
                if len(description) == 50:
                    description += "..."
                print(f"  • {name} - {description}")
    
    def create_project_interactive(self, project_name: str = None):
        """交互式创建项目"""
        if not project_name:
            project_name = input("\n🎯 请输入项目名称：").strip()
        
        if not project_name:
            print("❌ 项目名称不能为空")
            return
        
        print(f"\n🚀 正在为项目 '{project_name}' 生成技术方案...")
        
        # 创建项目记录
        project_data = {
            "id": f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "name": project_name,
            "description": project_name,
            "created_at": datetime.now().isoformat(),
            "status": "planning",
            "agents_involved": [],
            "progress": 0
        }
        
        # 保存项目
        data = self.load_projects_data()
        data["projects"].append(project_data)
        data["stats"]["total_projects"] += 1
        self.save_projects_data(data)
        
        print(f"✅ 项目 '{project_name}' 已创建！")
        print("📋 下一步建议：")
        print("   1. 查看适合的AI智能体")
        print("   2. 与项目经理或项目协调员对话")
        print("   3. 开始技术方案设计")
    
    def list_projects(self):
        """列出所有项目"""
        data = self.load_projects_data()
        projects = data.get("projects", [])
        
        if not projects:
            print("📋 暂无项目")
            return
        
        print(f"\n📋 项目列表 (共 {len(projects)} 个)")
        print("-" * 50)
        
        for project in projects:
            created = datetime.fromisoformat(project["created_at"]).strftime("%Y-%m-%d %H:%M")
            status = project.get("status", "unknown")
            progress = project.get("progress", 0)
            
            status_icons = {
                "planning": "📋",
                "developing": "🚀",
                "testing": "🧪",
                "completed": "✅",
                "cancelled": "❌"
            }
            
            icon = status_icons.get(status, "❓")
            print(f"{icon} {project['name']}")
            print(f"   📅 {created} | 🎯 {status} | 📊 {progress}%")
            print()
    
    def interactive_mode(self):
        """交互模式"""
        self.display_welcome()
        self.display_agents_summary()
        
        while True:
            try:
                user_input = input("\n🎯 请输入需求 (输入 'help' 查看帮助，'quit' 退出): ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 感谢使用 Trae AI v2.0！")
                    break
                
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                if user_input.lower() in ['list', 'list agents', 'agents']:
                    self.display_agents_summary()
                    continue
                
                if user_input.lower().startswith('create project'):
                    project_name = user_input[14:].strip()
                    self.create_project_interactive(project_name)
                    continue
                
                # 处理普通需求
                self.handle_user_request(user_input)
                
            except KeyboardInterrupt:
                print("\n👋 感谢使用 Trae AI v2.0！")
                break
            except Exception as e:
                print(f"❌ 发生错误: {e}")
    
    def handle_user_request(self, request: str):
        """处理用户请求"""
        print(f"\n🎯 处理需求：{request}")
        print("="*50)
        
        # 创建项目
        project_name = f"需求_{datetime.now().strftime('%m%d_%H%M')}"
        self.create_project_interactive(project_name)
        
        # 智能体推荐
        agents = self.get_all_agents()
        recommended = self.recommend_agents(request, agents)
        
        print("\n🎭 推荐的AI专家：")
        for agent in recommended[:3]:
            print(f"   • {agent['name']} - {agent.get('description', '')}")
        
        print(f"\n💡 建议：")
        print(f"   1. 与 {recommended[0]['name']} 对话开始")
        print(f"   2. 或运行：python trae-console.py create-project \"{request}\"")
    
    def recommend_agents(self, request: str, agents: List[Dict]) -> List[Dict]:
        """根据需求推荐智能体"""
        request_lower = request.lower()
        keywords = {
            'react': ['react', '前端', 'web'],
            'vue': ['vue', '前端', 'web'],
            'angular': ['angular', '前端', 'web'],
            'python': ['python', '后端', 'api', 'ai'],
            'node': ['node', 'javascript', '后端'],
            'go': ['go', 'golang', '后端'],
            'rust': ['rust', '后端', '系统'],
            'flutter': ['flutter', '移动', 'app'],
            'uniapp': ['uniapp', '小程序', '移动'],
            'ui': ['ui', '设计', '界面'],
            '架构': ['架构', '系统', '设计'],
            '测试': ['测试', 'qa', '质量'],
            '部署': ['部署', 'devops', '运维'],
            '文档': ['文档', '写作', '技术']
        }
        
        scored_agents = []
        for agent in agents:
            score = 0
            name_lower = agent.get('name', '').lower()
            desc_lower = agent.get('description', '').lower()
            
            # 关键词匹配
            for keyword_list in keywords.values():
                for keyword in keyword_list:
                    if keyword in request_lower or keyword in name_lower or keyword in desc_lower:
                        score += 2
            
            # 精确匹配
            if any(kw in request_lower for kw in [name_lower, desc_lower]):
                score += 5
            
            scored_agents.append((score, agent))
        
        return [agent for _, agent in sorted(scored_agents, key=lambda x: x[0], reverse=True)]
    
    def show_help(self):
        """显示帮助信息"""
        print("\n📖 Trae AI v2.0 帮助")
        print("-" * 30)
        print("🎯 基本用法：")
        print("   直接输入需求 → 让AI专家为你服务")
        print("   例如：我想做一个Vue3+TypeScript的任务管理系统")
        print()
        print("🛠️ 命令：")
        print("   help          - 显示帮助")
        print("   list          - 查看所有v2.0智能体")
        print("   quit          - 退出")
        print()
        print("📋 项目管理：")
        print("   create project <名称>  - 创建新项目")
        print("   python trae-console.py list-projects  - 查看项目")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Trae AI v2.0 统一控制台')
    parser.add_argument('action', nargs='?', help='操作：create-project, list-projects, list-agents')
    parser.add_argument('name', nargs='?', help='项目名称')
    
    args = parser.parse_args()
    
    console = TraeConsole()
    
    if not args.action:
        # 无参数，启动交互模式
        console.interactive_mode()
    elif args.action == 'create-project':
        if args.name:
            console.create_project_interactive(args.name)
        else:
            console.create_project_interactive()
    elif args.action == 'list-projects':
        console.list_projects()
    elif args.action == 'list-agents':
        console.display_agents_summary()
    else:
        print(f"❌ 未知操作: {args.action}")
        print("💡 使用: python trae-console.py [create-project|list-projects|list-agents]")

if __name__ == "__main__":
    main()