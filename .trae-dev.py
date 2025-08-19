#!/usr/bin/env python3
"""
Trae AI 开发助手 - 极简入口
所有功能都在 .trae 目录下
直接在对话框使用：@产品经理 我想创建Vue3任务管理应用
"""
import os
import sys
import json
from pathlib import Path

class SimpleTraeAI:
    """简化版Trae AI助手 - 支持动态加载"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent / ".trae"
        self.agents = self._load_agents_dynamically()
        
    def _load_agents_dynamically(self):
        """动态加载所有智能体"""
        agents_dir = self.base_dir / "agents"
        agents = {}
        
        if not agents_dir.exists():
            print(f"❌ 智能体目录不存在: {agents_dir}")
            return agents
            
        for agent_file in agents_dir.glob("*.json"):
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    agent_config = json.load(f)
                    
                # 从文件名提取角色名
                role_key = agent_file.stem
                
                # 从配置中提取中文名和英文名
                chinese_name = agent_config.get('name', '')
                english_name = agent_config.get('role', role_key)
                
                # 建立映射关系
                if chinese_name:
                    agents[chinese_name] = role_key
                agents[english_name] = role_key
                    
            except Exception as e:
                print(f"⚠️ 加载智能体失败 {agent_file}: {e}")
                
        return agents
        
    def process_command(self, command):
        """处理自然语言命令"""
        command = command.strip()
        
        # 使用动态加载的智能体映射
        
        # 项目类型映射
        templates = {
            "任务管理": "todo",
            "电商": "ecommerce", 
            "博客": "blog",
            "AI": "ai"
        }
        
        # 分析命令 - 使用动态智能体
        for agent_name, agent_key in self.agents.items():
            if f"@{agent_name}" in command:
                return self.call_agent(agent_key, command.replace(f"@{agent_name}", "").strip())
                
        # 如果没有找到匹配的智能体，显示可用列表
        if "@" in command and not any(f"@{name}" in command for name in self.agents.keys()):
            print("📋 可用智能体：")
            for name, key in self.agents.items():
                if "工程师" in name or "经理" in name:  # 显示中文名
                    print(f"  @{name}")
                
        # 项目模式
        for project_type, template in templates.items():
            if project_type in command:
                return self.create_project(command, template)
                
        # 默认处理
        return self.create_project(command, "web")
        
    def call_agent(self, agent_name, requirement):
        """调用智能体"""
        agent_file = self.base_dir / "agents" / f"{agent_name}.json"
        
        if agent_file.exists():
            with open(agent_file, 'r', encoding='utf-8') as f:
                agent_config = json.load(f)
                
            print(f"🎯 正在调用 @{agent_config['name']} 智能体...")
            print(f"📋 需求: {requirement}")
            
            # 这里模拟智能体响应
            response = {
                "agent": agent_config['name'],
                "requirement": requirement,
                "plan": agent_config.get('default_plan', '分析需求 -> 设计方案 -> 实现代码'),
                "next_steps": [
                    "1. 详细分析需求",
                    "2. 设计技术方案", 
                    "3. 生成代码框架",
                    "4. 实现核心功能"
                ]
            }
            
            return response
        else:
            return {"error": f"智能体 {agent_name} 不存在"}
            
    def create_project(self, description, template="web"):
        """创建项目"""
        print(f"🚀 创建项目: {description}")
        print(f"📦 模板: {template}")
        
        # 模拟项目创建
        project_info = {
            "name": f"{description.split()[0]}项目",
            "description": description,
            "template": template,
            "status": "created",
            "files": [
                "README.md",
                "package.json",
                "src/main.js",
                "src/components/",
                "src/views/"
            ]
        }
        
        return project_info

def main():
    """主函数"""
    if len(sys.argv) > 1:
        # 命令行模式
        command = " ".join(sys.argv[1:])
    else:
        # 交互模式
        command = input("🎯 请输入你的需求: ")
        
    ai = SimpleTraeAI()
    result = ai.process_command(command)
    
    if "error" in result:
        print(f"❌ {result['error']}")
    else:
        print("✅ 处理完成！")
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()