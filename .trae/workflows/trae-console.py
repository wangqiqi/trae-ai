#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trae AI 控制台
整合.trae-dev.py功能的统一控制台系统
支持智能体调用、项目管理和需求处理
新增模板自动化集成和AI协作功能
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime
import argparse
import subprocess
from typing import Dict, List, Optional, Any

class TraeConsole:
    """Trae AI 控制台 - 整合版"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent  # 指向 .trae 目录
        self.agents_dir = self.base_dir / "agent"
        self.templates_dir = self.base_dir / "templates"
        self.user_data_dir = self.base_dir / "user-data"
        self.workflows_dir = self.base_dir / "workflows"
        self.projects_file = self.user_data_dir / "projects.json"
        self.mcp_config_file = self.base_dir / "mcp-config.json"
        self.trae_config_file = self.base_dir / ".trae-config.json"
        self.cursor_rules_dir = self.base_dir / "rules" / "cursor"
        
        self.user_data_dir.mkdir(exist_ok=True)
        self.init_projects_data()
        self.agents = self._load_agents()
        self.templates = self._load_templates()
        self.mcp_config = self._load_mcp_config()
        self.trae_config = self._load_trae_config()
        self.cursor_rules = self._load_cursor_rules()
        self.cursor_constitution = self._load_cursor_constitution()
    
    def _load_mcp_config(self) -> Dict[str, Any]:
        """加载MCP配置"""
        try:
            if self.mcp_config_file.exists():
                with open(self.mcp_config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ 加载MCP配置失败: {e}")
        
        return {"mcp_config": {"enabled": False}}
    
    def _load_trae_config(self) -> Dict[str, Any]:
        """加载Trae配置"""
        try:
            if self.trae_config_file.exists():
                with open(self.trae_config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ 加载Trae配置失败: {e}")
        
        return {"trae_ai_assistant": {"version": "4.0"}}
    
    def _load_cursor_rules(self) -> Dict[str, Any]:
        """加载Cursor规则"""
        try:
            if self.cursor_rules_dir.exists():
                rules = {}
                for rule_dir in self.cursor_rules_dir.iterdir():
                    if rule_dir.is_dir():
                        rule_file = rule_dir / "RULE.md"
                        if rule_file.exists():
                            with open(rule_file, 'r', encoding='utf-8') as f:
                                rules[rule_dir.name] = f.read()
                return rules
        except Exception as e:
            print(f"⚠️ 加载Cursor规则失败: {e}")
        
        return {}
    
    def _load_cursor_constitution(self) -> Dict[str, Any]:
        """加载Cursor宪法"""
        try:
            if 'cursor_constitution' in self.trae_config.get('trae_ai_assistant', {}):
                return self.trae_config['trae_ai_assistant']['cursor_constitution']
        except Exception as e:
            print(f"⚠️ 加载Cursor宪法失败: {e}")
        
        return {}
    
    def init_projects_data(self):
        """初始化项目数据"""
        if not self.projects_file.exists():
            default_data = {
                "version": "4.0",
                "created_at": datetime.now().isoformat(),
                "trae_version": "4.0",
                "projects": [],
                "stats": {
                    "total_projects": 0,
                    "completed_projects": 0
                },
                "mcp_enabled": True,
                "context_management": {
                    "web_context": True,
                    "doc_context": True
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
    
    def _load_agents(self) -> Dict[str, Any]:
        """加载智能体配置（来自.trae-dev.py）"""
        agents = {}
        if not self.agents_dir.exists():
            return agents
        
        for agent_file in self.agents_dir.glob("*.json"):
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    agent_config = json.load(f)
                
                name = agent_config.get('name', '')
                role = agent_config.get('role', agent_file.stem)
                
                # 建立映射
                if name:
                    agents[name] = {
                        'config': agent_config,
                        'file': agent_file,
                        'role': role
                    }
                
                # 角色名映射
                agents[role] = {
                    'config': agent_config,
                    'file': agent_file,
                    'role': role
                }
                
            except Exception as e:
                print(f"⚠️ 加载智能体失败 {agent_file.name}: {e}")
        
        return agents

    def _load_templates(self) -> Dict[str, Any]:
        """加载模板配置"""
        templates = {}
        if not self.templates_dir.exists():
            return templates
            
        for template_file in self.templates_dir.glob("*.md"):
            if template_file.stem == "README":
                continue
                
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                templates[template_file.stem] = {
                    'path': template_file,
                    'content': content,
                    'type': self._detect_template_type(template_file.stem),
                    'description': self._extract_description(content)
                }
                
            except Exception as e:
                print(f"⚠️ 加载模板失败 {template_file.name}: {e}")
                
        return templates

    def _detect_template_type(self, template_name: str) -> str:
        """检测模板类型"""
        type_mapping = {
            "project-init": "初始化",
            "requirements": "需求",
            "api-spec": "API",
            "database-design": "数据库",
            "test-plan": "测试",
            "deployment": "部署",
            "code-review": "代码审查",
            "tech-choice": "技术选型"
        }
        
        for key, value in type_mapping.items():
            if key in template_name:
                return value
                
        return "通用"

    def _extract_description(self, content: str) -> str:
        """提取模板描述"""
        lines = content.split('\n')
        for line in lines[:10]:
            if line.strip().startswith('#') and '模板' in line:
                return line.replace('#', '').strip()
        return "项目模板"

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
        print("\n" + "="*60)
        print("🚀 Trae AI 控制台 - 模板自动化集成")
        print("="*60)
        print("💡 智能模板 + AI专家 = 高效开发！")
        print(f"📊 已加载 {len(self.agents)} 个智能体, {len(self.templates)} 个模板")
        print("\n🎯 快速开始：")
        print("  • 模板应用: template")
        print("  • 项目创建: create")
        print("  • AI协作: ai")
        print("  • 帮助: help")

    def display_help(self):
        """显示帮助（来自.trae-dev.py）"""
        agents_list = [name for name in self.agents.keys() if "工程师" in name or "经理" in name]
        
        print("""
🎯 Trae AI 控制台 - 完整帮助

=== 模板自动化 ===
template          - 交互式模板选择
auto              - 自动识别并应用模板
list              - 查看可用模板

=== 项目创建 ===
create <name>     - 创建新项目
project <type>    - 使用模板创建项目 (vue3/react/fastapi/flutter/node)

=== AI协作 ===
ai                - AI协作模式

=== 智能体调用 ===
@智能体名 需求      - 直接调用智能体
描述需求          - AI自动分析并建议

=== 可用智能体 ===
管理类: @产品经理 @系统架构师 @项目经理 @项目协调员
前端: @Vue工程师 @React工程师 @Angular工程师 @Uniapp工程师 @Flutter工程师
后端: @Python工程师 @FastAPI工程师 @Node工程师 @Go工程师 @Rust工程师
专项: @测试工程师 @DevOps工程师 @UI/UX设计师 @技术文档工程师

=== 示例 ===
"创建一个Vue3电商网站，需要用户登录、商品管理、购物车、支付功能"
"@产品经理 设计Vue3任务管理系统的需求文档"
"@系统架构师 设计微服务架构方案"
        """)

    def display_templates_help(self):
        """显示模板帮助"""
        print("""
📋 模板自动化系统

可用模板类别：
  🎯 项目启动类
    • project-init-template     - 项目初始化指南
    • requirements-template     - 需求分析文档
    • tech-choice-template      - 技术选型对比
  
  🏗️ 系统设计类
    • api-spec-template         - API接口规范
    • database-design-template  - 数据库设计
    • deployment-template       - 部署方案
  
  ✅ 质量保证类
    • test-plan-template        - 测试计划
    • code-review-template      - 代码审查

使用方式：
  1. 自动应用: python .trae/workflows/trae-console.py auto
  2. 交互选择: python .trae/workflows/trae-console.py template
  3. 创建项目: python .trae/workflows/trae-console.py create MyApp
        """)
    
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

    def auto_apply_templates(self):
        """自动应用模板"""
        print("🔍 正在分析项目...")
        
        # 调用模板管理器
        cmd = [
            sys.executable,
            str(self.workflows_dir / "template-manager.py"),
            "auto"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ 模板自动应用完成")
            else:
                print(f"❌ 模板应用失败: {result.stderr}")
        except Exception as e:
            print(f"❌ 执行失败: {e}")

    def interactive_template_selection(self):
        """交互式模板选择"""
        print("\n📋 模板选择向导")
        print("-" * 40)
        
        # 显示模板分类
        categories = {}
        for name, template in self.templates.items():
            category = template['type']
            if category not in categories:
                categories[category] = []
            categories[category].append((name, template['description']))
        
        for category, templates in categories.items():
            print(f"\n🎯 {category}类模板:")
            for i, (name, desc) in enumerate(templates, 1):
                print(f"  {i}. {name} - {desc}")
        
        # 用户选择
        choices = input("\n选择模板编号 (用逗号分隔): ").strip()
        selected = []
        
        try:
            for choice in choices.split(","):
                idx = int(choice.strip()) - 1
                all_templates = [(k, v) for k, v in self.templates.items()]
                if 0 <= idx < len(all_templates):
                    selected.append(all_templates[idx][0])
        except ValueError:
            print("❌ 无效选择")
            return
        
        if selected:
            print(f"✅ 已选择: {', '.join(selected)}")
            self.apply_selected_templates(selected)

    def apply_selected_templates(self, template_names: List[str]):
        """应用选中的模板"""
        for template_name in template_names:
            cmd = [
                sys.executable,
                str(self.workflows_dir / "template-manager.py"),
                "auto"
            ]
            
            try:
                subprocess.run(cmd, check=True)
                print(f"✅ 已应用: {template_name}")
            except subprocess.CalledProcessError:
                print(f"❌ 应用失败: {template_name}")

    def create_project_with_templates(self, project_name: str, project_type: str, features: List[str] = None):
        """使用模板创建项目"""
        if not features:
            features = []
            
        print(f"🚀 创建项目: {project_name} ({project_type})")
        
        # 调用AI模板集成
        cmd = [
            sys.executable,
            str(self.workflows_dir / "ai-template-integration.py"),
            "kit",
            "--project", project_name,
            "--type", project_type
        ]
        
        if features:
            cmd.extend(["--features"] + features)
            
        try:
            result = subprocess.run(cmd, capture_output=False, text=True)
            if result.returncode == 0:
                print(f"✅ 项目 {project_name} 创建完成")
            else:
                print(f"❌ 项目创建失败")
        except Exception as e:
            print(f"❌ 执行失败: {e}")
    
    def _detect_agent_call(self, command: str) -> Optional[Dict[str, str]]:
        """检测@智能体调用（来自.trae-dev.py）"""
        for agent_name in self.agents:
            if f"@{agent_name}" in command:
                requirement = command.replace(f"@{agent_name}", "").strip()
                return {
                    'agent': agent_name,
                    'requirement': requirement
                }
        return None

    def call_agent(self, agent_name: str, requirement: str) -> Dict[str, Any]:
        """调用智能体（来自.trae-dev.py）"""
        if agent_name not in self.agents:
            available_agents = [name for name in self.agents.keys() if "工程师" in name or "经理" in name]
            return {
                "error": f"智能体 '{agent_name}' 不存在",
                "available_agents": available_agents
            }
        
        agent_info = self.agents[agent_name]
        config = agent_info['config']
        
        return {
            "agent": agent_name,
            "requirement": requirement,
            "agent_config": {
                "name": config.get('name', agent_name),
                "role": config.get('role', agent_name),
                "description": config.get('description', '暂无描述')
            },
            "response": f"🎯 {config.get('name', agent_name)} 正在处理您的需求...",
            "next_steps": [
                "分析需求",
                "设计方案", 
                "生成代码",
                "测试验证"
            ]
        }

    def create_project_from_description(self, description: str) -> Dict[str, Any]:
        """从描述创建项目（来自.trae-dev.py）"""
        return {
            "project_name": f"项目_{description[:20]}...",
            "description": description,
            "status": "created",
            "suggested_agents": [name for name in self.agents.keys() if "工程师" in name][:3],
            "next_steps": [
                "选择合适的技术栈",
                "创建项目结构",
                "开始开发",
                "测试部署"
            ]
        }

    def ai_collaboration_mode(self):
        """AI协作模式"""
        print("\n🤖 AI协作模式")
        print("描述你的需求，AI将自动选择合适的模板和智能体")
        
        requirement = input("\n💡 项目需求: ").strip()
        if not requirement:
            return
        
        # 智能分析需求
        project_type = self.detect_project_type(requirement)
        features = self.extract_features(requirement)
        
        print(f"\n🔍 分析结果:")
        print(f"  项目类型: {project_type}")
        print(f"  功能特性: {', '.join(features)}")
        
        # 生成建议
        suggestions = self.generate_project_suggestions(project_type, features)
        
        print(f"\n💡 AI建议:")
        for suggestion in suggestions:
            print(f"  • {suggestion}")
        
        # 确认创建
        confirm = input("\n是否创建项目? (y/n): ").strip().lower()
        if confirm == 'y':
            project_name = input("项目名称: ").strip() or f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.create_project_with_templates(project_name, project_type, features)

    def detect_project_type(self, requirement: str) -> str:
        """检测项目类型"""
        keywords = {
            "vue": ["vue", "vue3", "vuetify"],
            "react": ["react", "react18", "nextjs"],
            "flutter": ["flutter", "dart", "mobile"],
            "fastapi": ["fastapi", "python", "api"],
            "node": ["node", "nodejs", "express"]
        }
        
        requirement_lower = requirement.lower()
        
        for project_type, keywords_list in keywords.items():
            if any(keyword in requirement_lower for keyword in keywords_list):
                return project_type
        
        return "vue3"  # 默认

    def extract_features(self, requirement: str) -> List[str]:
        """提取功能特性"""
        features = []
        
        feature_keywords = {
            "用户认证": ["登录", "注册", "认证", "权限"],
            "数据管理": ["CRUD", "增删改查", "数据", "管理"],
            "实时通信": ["实时", "聊天", "消息", "通知"],
            "支付功能": ["支付", "订单", "购物车"],
            "文件上传": ["上传", "文件", "图片", "视频"],
            "搜索功能": ["搜索", "筛选", "过滤"],
            "移动端适配": ["移动", "响应式", "适配"]
        }
        
        requirement_lower = requirement.lower()
        
        for feature, keywords in feature_keywords.items():
            if any(keyword in requirement_lower for keyword in keywords):
                features.append(feature)
        
        return features or ["基础功能"]

    def generate_project_suggestions(self, project_type: str, features: List[str]) -> List[str]:
        """生成项目建议"""
        suggestions = []
        
        # 技术栈建议
        tech_stacks = {
            "vue3": "Vue3 + TypeScript + Vite + Pinia",
            "react": "React18 + TypeScript + Next.js + Redux",
            "fastapi": "FastAPI + SQLAlchemy + PostgreSQL + Docker",
            "flutter": "Flutter + Dart + Firebase + Provider",
            "node": "Node.js + Express + MongoDB + Docker"
        }
        
        suggestions.append(f"技术栈: {tech_stacks.get(project_type, '通用技术栈')}")
        
        # 模板建议
        template_suggestions = {
            "vue3": ["项目初始化", "需求文档", "测试计划"],
            "react": ["项目初始化", "需求文档", "测试计划"],
            "fastapi": ["项目初始化", "API规范", "数据库设计", "测试计划", "部署方案"],
            "flutter": ["项目初始化", "需求文档", "测试计划"],
            "node": ["项目初始化", "API规范", "测试计划", "部署方案"]
        }
        
        templates = template_suggestions.get(project_type, ["项目初始化", "需求文档"])
        suggestions.append(f"推荐模板: {', '.join(templates)}")
        
        # 开发建议
        suggestions.append("开发周期: 2-4周")
        suggestions.append("团队协作: 建议产品经理先行设计需求")
        
        return suggestions

    def interactive_mode(self):
        """交互模式"""
        while True:
            self.display_welcome()
            
            choice = input("\n选择操作 (1-9): ").strip()
            
            if choice == '1':
                self.list_projects()
                input("\n按回车键继续...")
            elif choice == '2':
                agents = self.get_all_agents()
                print(f"📊 已加载 {len(agents)} 个智能体")
                for agent in agents:
                    print(f"  • {agent.get('name', '未知')} - {agent.get('description', '暂无描述')}")
                input("\n按回车键继续...")
            elif choice == '3':
                project_name = input("项目名称: ").strip()
                if project_name:
                    self.create_project(project_name)
                input("\n按回车键继续...")
            elif choice == '4':
                agent_name = input("智能体名称 (@开头): ").strip()
                requirement = input("需求描述: ").strip()
                if agent_name and requirement:
                    result = self.call_agent(agent_name.lstrip('@'), requirement)
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                input("\n按回车键继续...")
            elif choice == '5':
                description = input("项目需求描述: ").strip()
                if description:
                    result = self.create_project_from_description(description)
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                input("\n按回车键继续...")
            elif choice == '6':
                self.auto_apply_templates()
                input("\n按回车键继续...")
            elif choice == '7':
                self.interactive_template_selection()
                input("\n按回车键继续...")
            elif choice == '8':
                self.ai_collaboration_mode()
                input("\n按回车键继续...")
            elif choice == '9':
                self.display_help()
                input("\n按回车键继续...")
            elif choice == '0':
                print("👋 再见！")
                break
            else:
                print("❌ 无效选择，请重试")
                input("\n按回车键继续...")

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