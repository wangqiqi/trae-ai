#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trae AI v2.0 开发助手 - 极简入口
兼容v1和v2.0标准，智能识别目录结构
所有功能都在 .trae 目录下
直接在对话框使用：@产品经理 我想创建Vue3任务管理应用
"""
import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional

class TraeDevV2:
    """Trae AI v2.0 开发助手 - 兼容v1和v2.0"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent / ".trae"
        self.agents_v1_dir = self.base_dir / "agents"      # v1目录（旧）
        self.agents_v2_dir = self.base_dir / "agents2"    # v2目录（新）
        self.agents = self._load_agents_intelligently()
        
    def _load_agents_intelligently(self) -> Dict[str, Any]:
        """智能加载所有智能体（兼容v1和v2.0）"""
        agents = {}
        
        # 优先加载v2.0智能体
        if self.agents_v2_dir.exists():
            agents.update(self._load_v2_agents())
            
        # 回退加载v1智能体（如果存在）
        if self.agents_v1_dir.exists():
            v1_agents = self._load_v1_agents()
            # 只添加v2.0中没有的智能体
            for name, config in v1_agents.items():
                if name not in agents:
                    agents[name] = config
        
        return agents
    
    def _load_v2_agents(self) -> Dict[str, Any]:
        """加载v2.0智能体"""
        agents = {}
        
        for agent_file in self.agents_v2_dir.glob("*-v2.json"):
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    agent_config = json.load(f)
                
                # v2.0格式处理
                name = agent_config.get('name', '')
                role = agent_config.get('role', agent_file.stem.replace('-v2', ''))
                
                # 建立多重映射
                if name:
                    agents[name] = {
                        'type': 'v2.0',
                        'file': agent_file,
                        'config': agent_config,
                        'role': role
                    }
                
                # 英文角色名映射
                agents[role] = {
                    'type': 'v2.0', 
                    'file': agent_file,
                    'config': agent_config,
                    'role': role
                }
                
            except Exception as e:
                print(f"⚠️ 加载v2.0智能体失败 {agent_file.name}: {e}")
        
        return agents
    
    def _load_v1_agents(self) -> Dict[str, Any]:
        """加载v1智能体（向后兼容）"""
        agents = {}
        
        for agent_file in self.agents_v1_dir.glob("*.json"):
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    agent_config = json.load(f)
                
                # v1格式处理
                name = agent_config.get('name', '')
                role = agent_config.get('role', agent_file.stem)
                
                agents[name] = {
                    'type': 'v1',
                    'file': agent_file,
                    'config': agent_config,
                    'role': role
                }
                
                agents[role] = {
                    'type': 'v1',
                    'file': agent_file,
                    'config': agent_config,
                    'role': role
                }
                
            except Exception as e:
                print(f"⚠️ 加载v1智能体失败 {agent_file.name}: {e}")
        
        return agents
    
    def get_system_info(self) -> Dict[str, Any]:
        """获取系统状态信息"""
        info = {
            'v2_agents_count': len(list(self.agents_v2_dir.glob("*-v2.json"))) if self.agents_v2_dir.exists() else 0,
            'v1_agents_count': len(list(self.agents_v1_dir.glob("*.json"))) if self.agents_v1_dir.exists() else 0,
            'total_agents': len(self.agents),
            'base_dir': str(self.base_dir)
        }
        return info
    
    def process_command(self, command: str) -> Dict[str, Any]:
        """智能处理自然语言命令"""
        command = command.strip()
        
        if not command:
            return {"error": "请输入需求描述"}
        
        # 智能体调用检测
        agent_match = self._detect_agent_call(command)
        if agent_match:
            return self.call_agent(agent_match['agent'], agent_match['requirement'])
        
        # 项目模板检测
        template_match = self._detect_project_template(command)
        if template_match:
            return self.create_project(command, template_match)
        
        # 默认项目创建
        return self.create_project(command, "web")
    
    def _detect_agent_call(self, command: str) -> Optional[Dict[str, str]]:
        """检测智能体调用模式"""
        # 检测@智能体调用
        for agent_name, agent_info in self.agents.items():
            if f"@{agent_name}" in command:
                requirement = command.replace(f"@{agent_name}", "").strip()
                return {
                    'agent': agent_name,
                    'requirement': requirement,
                    'agent_info': agent_info
                }
        
        return None
    
    def _detect_project_template(self, command: str) -> Optional[str]:
        """检测项目模板"""
        templates = {
            "任务管理": "todo",
            "todo": "todo", 
            "电商": "ecommerce",
            "购物": "ecommerce",
            "商城": "ecommerce",
            "博客": "blog",
            "文章": "blog",
            "写作": "blog",
            "AI": "ai",
            "人工智能": "ai",
            "识别": "ai",
            "小程序": "miniprogram",
            "移动": "mobile",
            "Flutter": "flutter",
            "Vue": "vue",
            "React": "react",
            "Python": "python",
            "FastAPI": "fastapi",
            "Node": "nodejs"
        }
        
        command_lower = command.lower()
        for keyword, template in templates.items():
            if keyword.lower() in command_lower:
                return template
        
        return None
    
    def call_agent(self, agent_name: str, requirement: str) -> Dict[str, Any]:
        """调用指定智能体"""
        if agent_name not in self.agents:
            return {
                "error": f"智能体 '{agent_name}' 不存在",
                "available_agents": list(set([name for name in self.agents.keys() if "工程师" in name or "经理" in name]))
            }
        
        agent_info = self.agents[agent_name]
        config = agent_info['config']
        
        # 构建响应
        response = {
            "agent": agent_name,
            "agent_type": agent_info['type'],
            "requirement": requirement,
            "system_info": self.get_system_info(),
            "agent_config": {
                "name": config.get('name', agent_name),
                "role": config.get('role', agent_name),
                "description": config.get('description', '暂无描述'),
                "capabilities": config.get('capabilities', [])
            },
            "plan": self._generate_plan(config, requirement),
            "next_steps": [
                "1. 详细分析需求",
                "2. 设计技术方案",
                "3. 生成代码框架",
                "4. 实现核心功能",
                "5. 测试和优化"
            ]
        }
        
        return response
    
    def _generate_plan(self, agent_config: Dict[str, Any], requirement: str) -> str:
        """根据智能体配置生成计划"""
        role = agent_config.get('role', '通用智能体')
        
        plans = {
            '产品经理': '需求分析 → 功能规划 → 原型设计 → 需求文档',
            '系统架构师': '技术调研 → 架构设计 → 技术选型 → 架构文档',
            'Vue工程师': '需求理解 → 组件设计 → 页面开发 → 功能测试',
            'React工程师': '需求理解 → 组件设计 → 页面开发 → 功能测试',
            'Python工程师': '需求分析 → API设计 → 后端开发 → 接口测试',
            'Node工程师': '需求分析 → API设计 → 后端开发 → 接口测试',
            '测试工程师': '需求分析 → 测试计划 → 测试用例 → 自动化测试',
            'DevOps工程师': '环境配置 → 部署方案 → CI/CD配置 → 监控设置'
        }
        
        return plans.get(role, '需求分析 → 方案设计 → 代码实现 → 测试验证')
    
    def create_project(self, description: str, template: str = "web") -> Dict[str, Any]:
        """智能创建项目"""
        # 项目模板配置
        templates = {
            "todo": {
                "name": "智能任务管理系统",
                "tech_stack": ["Vue3", "FastAPI", "SQLite"],
                "features": ["任务CRUD", "用户认证", "拖拽排序", "状态管理"]
            },
            "ecommerce": {
                "name": "精品电商平台", 
                "tech_stack": ["React", "Node.js", "MongoDB", "支付集成"],
                "features": ["商品管理", "购物车", "订单系统", "支付功能"]
            },
            "blog": {
                "name": "个人博客系统",
                "tech_stack": ["Vue3", "FastAPI", "Markdown"],
                "features": ["文章发布", "分类管理", "评论系统", "SEO优化"]
            },
            "ai": {
                "name": "AI智能识别系统",
                "tech_stack": ["Python", "FastAPI", "TensorFlow"],
                "features": ["图像识别", "文本分析", "模型训练", "API服务"]
            },
            "vue": {
                "name": "Vue3应用",
                "tech_stack": ["Vue3", "TypeScript", "Vite"],
                "features": ["组件化开发", "状态管理", "路由管理"]
            },
            "react": {
                "name": "React应用", 
                "tech_stack": ["React18", "TypeScript", "Vite"],
                "features": ["函数式组件", "Hooks", "状态管理"]
            },
            "python": {
                "name": "Python后端API",
                "tech_stack": ["Python", "FastAPI", "SQLAlchemy"],
                "features": ["RESTful API", "数据库操作", "身份验证"]
            }
        }
        
        template_info = templates.get(template, {
            "name": f"{template}项目",
            "tech_stack": ["Vue3", "FastAPI", "SQLite"],
            "features": ["基础功能"]
        })
        
        project_info = {
            "project_name": template_info["name"],
            "description": description,
            "template": template,
            "tech_stack": template_info["tech_stack"],
            "features": template_info["features"],
            "status": "created",
            "files": [
                "README.md",
                "package.json",
                "requirements.txt",
                "src/main.py",
                "src/components/",
                "src/views/",
                "tests/"
            ],
            "system_info": self.get_system_info(),
            "next_steps": [
                "1. 创建项目目录结构",
                "2. 初始化代码仓库",
                "3. 安装依赖包",
                "4. 开始开发",
                "5. 运行测试"
            ]
        }
        
        return project_info
    
    def display_help(self) -> Dict[str, Any]:
        """显示帮助信息"""
        v2_agents = [name for name, info in self.agents.items() 
                    if info['type'] == 'v2.0' and ("工程师" in name or "经理" in name)]
        
        return {
            "help": "Trae AI v2.0 开发助手",
            "usage": {
                "智能体调用": "@智能体名 需求描述",
                "项目创建": "直接描述需求",
                "模板创建": "包含关键词如'Vue'、'React'、'任务管理'"
            },
            "available_agents": list(set(v2_agents))[:10],  # 显示前10个
            "system_status": self.get_system_info(),
            "examples": [
                "@产品经理 我想创建一个Vue3任务管理系统",
                "创建React电商网站",
                "用Python做RESTful API",
                "帮我设计Flutter移动应用"
            ]
        }

def main():
    """主函数"""
    if len(sys.argv) > 1:
        # 命令行模式
        command = " ".join(sys.argv[1:])
    else:
        # 交互模式
        print("🤖 Trae AI v2.0 开发助手")
        print("=" * 40)
        print("💡 支持自然语言输入！")
        print("🎯 示例：")
        print("   • @产品经理 创建Vue3任务管理应用")
        print("   • 创建React电商网站")
        print("   • 用Python做RESTful API")
        print("   • 输入 'help' 查看更多信息")
        print("=" * 40)
        command = input("🎯 请输入需求: ")
    
    if command.lower() in ['help', 'h', '?']:
        ai = TraeDevV2()
        result = ai.display_help()
    else:
        ai = TraeDevV2()
        result = ai.process_command(command)
    
    # 美化输出
    if "error" in result:
        print(f"❌ {result['error']}")
        if "available_agents" in result:
            print("📋 可用智能体：")
            for agent in result["available_agents"]:
                print(f"   • {agent}")
    else:
        print("✅ 处理完成！")
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()