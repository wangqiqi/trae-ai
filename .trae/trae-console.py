#!/usr/bin/env python3
"""
Trae AI 统一控制台
整合项目管理、智能体管理、交互式操作于一体
版本：v3.0-统一版
"""

import os
import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import webbrowser
import re
from datetime import datetime

class TraeAIConsole:
    """Trae AI 统一控制台"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.agents_dir = self.base_dir / "agents"
        self.scripts_dir = self.base_dir / "scripts"
        self.templates_dir = self.base_dir / "templates"
        
        # 用户数据目录（迁移到根目录）
        self.user_data_dir = self.base_dir.parent / "user-data"
        self.user_data_dir.mkdir(exist_ok=True)
        
        # 确保系统目录存在
        for dir_path in [self.agents_dir, self.scripts_dir, self.templates_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # 初始化数据文件（新位置）
        self.projects_file = self.user_data_dir / "projects.json"
        self._init_data()
    
    # ====================
    # 数据初始化
    # ====================
    def _init_data(self):
        """初始化数据文件"""
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
                }
            ]
            
            with open(self.projects_file, 'w', encoding='utf-8') as f:
                json.dump(default_projects, f, ensure_ascii=False, indent=2)
    
    # ====================
    # 智能体管理功能
    # ====================
    def list_agents(self) -> List[Dict[str, Any]]:
        """列出所有智能体"""
        agents = []
        for agent_file in self.agents_dir.glob("*.json"):
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                agents.append({
                    'file': agent_file.name,
                    'name': config.get('name', '未知'),
                    'role': config.get('role', '未知'),
                    'description': config.get('description', '无描述'),
                    'capabilities': config.get('capabilities', [])
                })
            except Exception as e:
                print(f"⚠️ 读取失败 {agent_file}: {e}")
        return agents
    
    def add_agent(self, config: Dict[str, Any], filename: str = None) -> str:
        """添加新智能体"""
        if not filename:
            filename = f"{config.get('role', 'new-agent')}.json"
        
        agent_file = self.agents_dir / filename
        
        # 验证必要字段
        required_fields = ['name', 'role', 'description', 'prompt']
        missing = [f for f in required_fields if f not in config]
        if missing:
            raise ValueError(f"缺少必要字段: {', '.join(missing)}")
        
        with open(agent_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        return str(agent_file)
    
    def remove_agent(self, name_or_filename: str) -> bool:
        """删除智能体"""
        if name_or_filename.endswith('.json'):
            agent_file = self.agents_dir / name_or_filename
        else:
            # 根据名称查找文件
            for agent_file in self.agents_dir.glob("*.json"):
                try:
                    with open(agent_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    if config.get('name') == name_or_filename:
                        break
                except:
                    continue
            else:
                return False
        
        if agent_file.exists():
            agent_file.unlink()
            return True
        return False
    
    def update_agent(self, name_or_filename: str, updates: Dict[str, Any]) -> bool:
        """更新智能体配置"""
        if name_or_filename.endswith('.json'):
            agent_file = self.agents_dir / name_or_filename
        else:
            for agent_file in self.agents_dir.glob("*.json"):
                try:
                    with open(agent_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    if config.get('name') == name_or_filename:
                        break
                except:
                    continue
            else:
                return False
        
        if not agent_file.exists():
            return False
        
        try:
            with open(agent_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            config.update(updates)
            
            with open(agent_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception:
            return False
    
    # ====================
    # 项目管理功能
    # ====================
    def list_projects(self) -> List[Dict[str, Any]]:
        """列出所有项目"""
        try:
            with open(self.projects_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    
    def create_project(self, requirement: str) -> Dict[str, Any]:
        """根据需求创建项目"""
        project_spec = self._parse_requirement(requirement)
        
        # 保存项目
        projects = self.list_projects()
        projects.append(project_spec)
        
        with open(self.projects_file, 'w', encoding='utf-8') as f:
            json.dump(projects, f, ensure_ascii=False, indent=2)
        
        return project_spec
    
    def _parse_requirement(self, requirement: str) -> Dict[str, Any]:
        """解析需求为项目规范"""
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
        
        project_type = "web"
        tech_stack = []
        features = []
        timeline = "2-4周"
        risk_level = "low"
        
        req_lower = requirement.lower()
        
        # 检测项目类型
        for type_key, type_keywords in keywords.items():
            if any(keyword in req_lower for keyword in type_keywords):
                if type_key in ["todo", "blog", "ecommerce", "ai"]:
                    project_type = type_key
                break
        
        # 智能技术栈推荐
        if "vue" in req_lower or "vue3" in req_lower:
            tech_stack = ["Vue3", "FastAPI", "SQLite"]
        elif "react" in req_lower:
            tech_stack = ["React", "Node.js", "MongoDB"]
        elif "flutter" in req_lower:
            tech_stack = ["Flutter", "FastAPI", "SQLite"]
        elif "miniprogram" in req_lower or "小程序" in req_lower:
            tech_stack = ["uni-app", "FastAPI", "MySQL"]
        else:
            tech_stack = ["Vue3", "FastAPI", "SQLite"]
        
        # 功能检测
        if "用户" in requirement or "登录" in requirement:
            features.append("用户认证")
        if "管理" in requirement:
            features.append("后台管理")
        if "支付" in requirement:
            features.append("支付集成")
            risk_level = "medium"
        if "响应式" in requirement or "手机" in requirement:
            features.append("响应式设计")
        if "ai" in req_lower or "智能" in requirement:
            features.append("AI功能")
            risk_level = "medium"
        
        # 时间检测
        timeline_match = re.search(r'(\d+)[\s]*[周天月]', requirement)
        if timeline_match:
            timeline = f"{timeline_match.group(1)}周"
        
        return {
            "id": f"{project_type}_{datetime.now().strftime('%m%d_%H%M')}",
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
        timestamp = datetime.now().strftime("%m%d")
        return f"{base_name}_{timestamp}"
    
    # ====================
    # 交互式界面
    # ====================
    def interactive_mode(self):
        """统一交互式界面"""
        print("🎯 Trae AI 统一控制台 v3.0")
        print("=" * 50)
        print("💡 可用命令：")
        print("  项目相关：")
        print("    - '创建项目：我想做xxx'")
        print("    - '查看项目列表' 或 'list projects'")
        print("  智能体相关：")
        print("    - '查看智能体' 或 'list agents'")
        print("    - '添加智能体' 或 'add agent'")
        print("    - '删除智能体' 或 'remove agent'")
        print("  其他：")
        print("    - '退出' 或 'exit'")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n🤖 请输入命令：").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', '退出', 'q']:
                    print("👋 感谢使用！再见！")
                    break
                
                # 项目列表
                elif user_input.lower() in ['list projects', '查看项目', '项目列表']:
                    projects = self.list_projects()
                    if projects:
                        print("\n📋 项目列表：")
                        for i, project in enumerate(projects, 1):
                            print(f"{i}. {project['name']} ({project['status']}) - {project['progress']}%")
                            print(f"   技术栈：{' + '.join(project['tech_stack'])}")
                            print(f"   功能：{', '.join(project['features'])}")
                    else:
                        print("❌ 暂无项目")
                
                # 智能体列表
                elif user_input.lower() in ['list agents', '查看智能体', '智能体列表']:
                    agents = self.list_agents()
                    if agents:
                        print("\n🤖 智能体列表：")
                        for i, agent in enumerate(agents, 1):
                            print(f"{i}. {agent['name']} ({agent['role']})")
                            print(f"   {agent['description']}")
                            if agent['capabilities']:
                                print(f"   能力：{', '.join(agent['capabilities'])}")
                    else:
                        print("❌ 暂无智能体")
                
                # 创建项目
                elif any(keyword in user_input.lower() for keyword in ['创建项目', '创建', '项目']):
                    requirement = user_input.replace('创建项目', '').replace('创建', '').strip()
                    if requirement:
                        project = self.create_project(requirement)
                        print(f"\n✅ 项目创建成功！")
                        print(f"   名称：{project['name']}")
                        print(f"   技术栈：{' + '.join(project['tech_stack'])}")
                        print(f"   预计时间：{project['timeline']}")
                    else:
                        print("❌ 请描述项目需求")
                
                # 智能体管理
                elif user_input.lower().startswith('add agent') or user_input.lower().startswith('添加智能体'):
                    print("💡 请使用命令行模式添加智能体")
                    print("   python .trae/trae-console.py add-agent --name 智能体名称")
                
                else:
                    # 默认为创建项目
                    project = self.create_project(user_input)
                    print(f"\n✅ 项目创建成功！")
                    print(f"   名称：{project['name']}")
                    print(f"   技术栈：{' + '.join(project['tech_stack'])}")
                    
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"❌ 错误：{e}")
                print("💡 请重新输入")
    
    # ====================
    # 命令行接口
    # ====================
    def run_cli(self):
        """命令行接口"""
        parser = argparse.ArgumentParser(description="Trae AI 统一控制台")
        subparsers = parser.add_subparsers(dest='command', help='可用命令')
        
        # 项目命令
        project_parser = subparsers.add_parser('create-project', help='创建新项目')
        project_parser.add_argument('requirement', help='项目需求描述')
        
        list_parser = subparsers.add_parser('list-projects', help='列出所有项目')
        
        # 智能体命令
        agent_parser = subparsers.add_parser('list-agents', help='列出所有智能体')
        
        add_parser = subparsers.add_parser('add-agent', help='添加智能体')
        add_parser.add_argument('--name', required=True, help='智能体名称')
        add_parser.add_argument('--role', required=True, help='智能体角色')
        add_parser.add_argument('--description', required=True, help='智能体描述')
        add_parser.add_argument('--prompt', required=True, help='智能体提示词')
        add_parser.add_argument('--capabilities', nargs='*', help='智能体能力')
        
        remove_parser = subparsers.add_parser('remove-agent', help='删除智能体')
        remove_parser.add_argument('--name', required=True, help='智能体名称或文件名')
        
        # 交互模式
        subparsers.add_parser('interactive', help='启动交互模式')
        
        args = parser.parse_args()
        
        if not args.command:
            # 默认启动交互模式
            self.interactive_mode()
            return
        
        try:
            if args.command == 'create-project':
                project = self.create_project(args.requirement)
                print(json.dumps(project, ensure_ascii=False, indent=2))
            
            elif args.command == 'list-projects':
                projects = self.list_projects()
                print(json.dumps(projects, ensure_ascii=False, indent=2))
            
            elif args.command == 'list-agents':
                agents = self.list_agents()
                print(json.dumps(agents, ensure_ascii=False, indent=2))
            
            elif args.command == 'add-agent':
                config = {
                    'name': args.name,
                    'role': args.role,
                    'description': args.description,
                    'prompt': args.prompt,
                    'capabilities': args.capabilities or []
                }
                filename = self.add_agent(config)
                print(f"✅ 智能体已添加：{filename}")
            
            elif args.command == 'remove-agent':
                if self.remove_agent(args.name):
                    print(f"✅ 智能体已删除：{args.name}")
                else:
                    print(f"❌ 未找到智能体：{args.name}")
            
            elif args.command == 'interactive':
                self.interactive_mode()
                
        except Exception as e:
            print(f"❌ 错误：{e}", file=sys.stderr)
            sys.exit(1)

def main():
    """主入口"""
    console = TraeAIConsole()
    console.run_cli()

if __name__ == "__main__":
    main()