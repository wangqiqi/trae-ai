#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trae AI 增强控制台 - 模板自动化集成版

功能：
1. 模板自动应用和智能生成
2. AI智能体深度集成
3. 一键项目创建和初始化
4. 智能需求分析和方案生成
5. 跨平台模板管理

作者：Trae AI团队
版本：v3.0
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import argparse
import subprocess
from typing import Dict, List, Optional, Any

class TraeEnhancedConsole:
    """Trae AI 增强控制台 - 模板集成版"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.agents_dir = self.base_dir / "agent"
        self.templates_dir = self.base_dir / "templates"
        self.user_data_dir = self.base_dir / "user-data"
        self.workflows_dir = self.base_dir / "workflows"
        
        self.user_data_dir.mkdir(exist_ok=True)
        self.agents = self._load_agents()
        self.templates = self._load_templates()
        
    def _load_agents(self) -> Dict[str, Any]:
        """加载智能体配置"""
        agents = {}
        if not self.agents_dir.exists():
            return agents
            
        for agent_file in self.agents_dir.glob("*.json"):
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    agent_config = json.load(f)
                    
                name = agent_config.get('name', '')
                role = agent_config.get('role', agent_file.stem)
                
                if name:
                    agents[name] = {
                        'config': agent_config,
                        'file': agent_file,
                        'role': role
                    }
                    
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
    
    def display_welcome(self):
        """显示欢迎界面"""
        print("\n" + "="*60)
        print("🚀 Trae AI 增强控制台 - 模板自动化集成")
        print("="*60)
        print("💡 智能模板 + AI专家 = 高效开发！")
        print("\n🎯 快速开始：")
        print("  • 模板应用: template apply")
        print("  • 项目创建: project create")
        print("  • AI协作: ai collaborate")
        print("  • 帮助: help")
    
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
  1. 自动应用: python .trae/workflows/template-manager.py auto
  2. 交互应用: python .trae/workflows/template-manager.py interactive
  3. 创建项目: python .trae/workflows/template-manager.py create --name MyApp --type vue3
  4. AI增强: python .trae/workflows/ai-template-integration.py kit --project MyApp --type fastapi
        """)
    
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
    
    def create_project_with_templates(self, project_name: str, project_type: str, features: List[str]):
        """使用模板创建项目"""
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
        project_info = {
            "name": Path.cwd().name,
            "type": "custom",
            "tech_stack": ["待确定"],
            "features": []
        }
        
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
    
    def display_help(self):
        """显示帮助"""
        print("""
🎯 Trae AI 增强控制台 - 完整帮助

=== 模板自动化 ===
template auto     - 自动识别并应用模板
template list     - 查看可用模板
template apply    - 交互式模板应用

=== 项目创建 ===
project create    - 创建新项目
project kit       - 创建完整项目套件

=== AI协作 ===
ai collaborate    - AI协作模式
ai enhance        - AI增强模板内容

=== 快速开始 ===
quick vue3        - 快速创建Vue3项目
quick react       - 快速创建React项目
quick fastapi     - 快速创建FastAPI项目

=== 示例 ===
"创建一个Vue3电商网站，需要用户登录、商品管理、购物车、支付功能"
"@产品经理 设计Vue3任务管理系统的需求文档"
"@系统架构师 设计微服务架构方案"
        """)
    
    def interactive_mode(self):
        """交互模式"""
        self.display_welcome()
        
        while True:
            try:
                user_input = input("\n🎯 Trae> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 再见！")
                    break
                
                if user_input.lower() == 'help':
                    self.display_help()
                    continue
                
                if user_input.lower() == 'template auto':
                    self.auto_apply_templates()
                    continue
                
                if user_input.lower() == 'template list':
                    self.display_templates_help()
                    continue
                
                if user_input.lower() == 'template apply':
                    self.interactive_template_selection()
                    continue
                
                if user_input.lower().startswith('project create'):
                    parts = user_input.split()
                    if len(parts) >= 3:
                        project_name = parts[2]
                        project_type = input("项目类型 (vue3/react/fastapi/flutter/node): ").strip()
                        features = input("功能特性 (用空格分隔): ").strip().split()
                        self.create_project_with_templates(project_name, project_type, features)
                    else:
                        print("用法: project create <项目名>")
                    continue
                
                if user_input.lower() == 'ai collaborate':
                    self.ai_collaboration_mode()
                    continue
                
                # 检测@智能体调用
                if '@' in user_input:
                    self.handle_agent_call(user_input)
                else:
                    # AI协作模式
                    self.ai_collaboration_mode_from_input(user_input)
                
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
    
    def handle_agent_call(self, user_input: str):
        """处理智能体调用"""
        # 这里可以集成实际的智能体调用逻辑
        print(f"🤖 AI智能体正在处理: {user_input}")
        
    def ai_collaboration_mode_from_input(self, requirement: str):
        """从输入启动AI协作模式"""
        print(f"\n🤖 AI分析需求: {requirement}")
        
        project_type = self.detect_project_type(requirement)
        features = self.extract_features(requirement)
        
        print(f"\n💡 项目建议:")
        print(f"  类型: {project_type}")
        print(f"  功能: {', '.join(features)}")
        
        confirm = input("\n是否创建项目? (y/n): ").strip().lower()
        if confirm == 'y':
            project_name = input("项目名称: ").strip() or f"ai_project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.create_project_with_templates(project_name, project_type, features)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Trae AI 增强控制台')
    parser.add_argument('action', nargs='?', 
                       choices=['template', 'project', 'ai', 'quick', 'help'])
    parser.add_argument('--name', help='项目名称')
    parser.add_argument('--type', choices=['vue3', 'react', 'fastapi', 'flutter', 'node'])
    parser.add_argument('--features', nargs='*', help='功能特性')
    
    args = parser.parse_args()
    
    console = TraeEnhancedConsole()
    
    if not args.action:
        console.interactive_mode()
    elif args.action == 'template':
        console.interactive_template_selection()
    elif args.action == 'project':
        if args.name and args.type:
            console.create_project_with_templates(args.name, args.type, args.features or [])
        else:
            print("用法: project --name <项目名> --type <类型>")
    elif args.action == 'ai':
        console.ai_collaboration_mode()
    elif args.action == 'quick':
        if args.type:
            project_name = args.name or f"quick_{args.type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            console.create_project_with_templates(project_name, args.type, args.features or [])
        else:
            print("用法: quick --type <类型>")
    elif args.action == 'help':
        console.display_help()

if __name__ == "__main__":
    main()