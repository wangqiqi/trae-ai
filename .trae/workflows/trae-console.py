#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trae AI 控制台
独立的系统，专注于智能体管理和项目协作
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime
import argparse
from typing import Dict, List, Optional, Any

class TraeConsole:
    """Trae AI 控制台"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent  # 指向 .trae 目录
        self.agents_dir = self.base_dir / "agent"
        self.user_data_dir = self.base_dir / "user-data"
        self.projects_file = self.user_data_dir / "projects.json"
        
        self.user_data_dir.mkdir(exist_ok=True)
        self.init_projects_data()
    
    def init_projects_data(self):
        """初始化项目数据"""
        if not self.projects_file.exists():
            default_data = {
                "version": "2.0.0",
                "created_at": datetime.now().isoformat(),
                "projects": [],
                "stats": {
                    "total_projects": 0,
                    "completed_projects": 0
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
        """获取所有智能体"""
        agents = []
        if not self.agents_dir.exists():
            return agents
        
        for agent_file in self.agents_dir.glob("*.json"):
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    agent_data = json.load(f)
                    agent_data['filename'] = agent_file.name
                    agents.append(agent_data)
            except Exception as e:
                print(f"⚠️ 加载失败: {e}")
        
        return sorted(agents, key=lambda x: x.get('name', ''))
    
    def display_welcome(self):
        """显示欢迎界面"""
        print("\n" + "="*50)
        print("🤖 Trae AI 控制台")
        print("="*50)
        print("💡 描述需求，让AI专家为你服务！")
    
    def create_project(self, project_name: str):
        """创建项目"""
        if not project_name.strip():
            print("❌ 项目名称不能为空")
            return
        
        project_data = {
            "id": f"proj_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "name": project_name,
            "created_at": datetime.now().isoformat(),
            "status": "planning"
        }
        
        data = self.load_projects_data()
        data["projects"].append(project_data)
        data["stats"]["total_projects"] += 1
        self.save_projects_data(data)
        
        print(f"✅ 项目 '{project_name}' 已创建")
    
    def list_projects(self):
        """列出项目"""
        data = self.load_projects_data()
        projects = data.get("projects", [])
        
        if not projects:
            print("📋 暂无项目")
            return
        
        print(f"\n📋 项目列表 ({len(projects)}个)")
        for project in projects:
            created = datetime.fromisoformat(project["created_at"]).strftime("%m-%d %H:%M")
            print(f"  • {project['name']} ({created})")
    
    def interactive_mode(self):
        """交互模式"""
        self.display_welcome()
        
        agents = self.get_all_agents()
        if agents:
            print(f"📊 已加载 {len(agents)} 个智能体")
        
        while True:
            try:
                user_input = input("\n🎯 需求: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 再见！")
                    break
                
                if user_input.lower() == 'help':
                    print("📖 帮助：直接描述需求或@智能体名")
                    continue
                
                print(f"🚀 处理: {user_input}")
                
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Trae AI 控制台')
    parser.add_argument('action', nargs='?', choices=['create', 'list'])
    parser.add_argument('name', nargs='?')
    
    args = parser.parse_args()
    console = TraeConsole()
    
    if not args.action:
        console.interactive_mode()
    elif args.action == 'create':
        project_name = args.name or input("项目名称: ")
        console.create_project(project_name)
    elif args.action == 'list':
        console.list_projects()

if __name__ == "__main__":
    main()