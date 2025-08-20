#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trae AI v2.0 智能开发助手
独立的v2.0系统，只支持v2.0标准智能体
"""
import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional

class TraeDevV2:
    """Trae AI v2.0 智能开发助手 - 纯v2.0版本"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent / ".trae"
        self.agents_dir = self.base_dir / "agents2"  # 仅v2.0目录
        self.agents = self._load_v2_agents()
        
    def _load_v2_agents(self) -> Dict[str, Any]:
        """仅加载v2.0智能体"""
        agents = {}
        
        if not self.agents_dir.exists():
            print("⚠️  v2.0智能体目录不存在")
            return agents
        
        for agent_file in self.agents_dir.glob("*-v2.json"):
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    agent_config = json.load(f)
                
                name = agent_config.get('name', '')
                role = agent_config.get('role', agent_file.stem.replace('-v2', ''))
                
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
    
    def get_system_info(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            'agents_count': len(self.agents),
            'agents_dir': str(self.agents_dir),
            'version': '2.0'
        }
    
    def process_command(self, command: str) -> Dict[str, Any]:
        """处理命令"""
        command = command.strip()
        
        if not command:
            return {"error": "请输入需求描述"}
        
        # 智能体调用
        agent_match = self._detect_agent_call(command)
        if agent_match:
            return self.call_agent(agent_match['agent'], agent_match['requirement'])
        
        # 项目创建
        return self.create_project(command)
    
    def _detect_agent_call(self, command: str) -> Optional[Dict[str, str]]:
        """检测@智能体调用"""
        for agent_name in self.agents:
            if f"@{agent_name}" in command:
                requirement = command.replace(f"@{agent_name}", "").strip()
                return {
                    'agent': agent_name,
                    'requirement': requirement
                }
        return None
    
    def call_agent(self, agent_name: str, requirement: str) -> Dict[str, Any]:
        """调用智能体"""
        if agent_name not in self.agents:
            return {
                "error": f"智能体 '{agent_name}' 不存在",
                "available_agents": [name for name in self.agents.keys() if "工程师" in name or "经理" in name]
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
    
    def create_project(self, description: str) -> Dict[str, Any]:
        """创建项目"""
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
    
    def display_help(self) -> Dict[str, Any]:
        """显示帮助"""
        agents_list = [name for name in self.agents.keys() if "工程师" in name or "经理" in name]
        
        return {
            "help": "Trae AI v2.0 智能助手",
            "usage": {
                "智能体调用": "@智能体名 需求描述",
                "项目创建": "直接描述需求"
            },
            "available_agents": agents_list,
            "examples": [
                "@产品经理 创建Vue3任务管理应用",
                "@Vue工程师 实现响应式界面",
                "创建Python数据分析项目"
            ]
        }

def main():
    """主函数"""
    if len(sys.argv) > 1:
        command = " ".join(sys.argv[1:])
    else:
        print("🤖 Trae AI v2.0 智能助手")
        print("=" * 40)
        print("💡 使用方法：")
        print("   • @产品经理 创建Vue3任务管理应用")
        print("   • 创建React电商网站")
        print("   • 输入 'help' 查看更多信息")
        print("=" * 40)
        command = input("🎯 请输入需求: ")
    
    if command.lower() in ['help', 'h', '?']:
        ai = TraeDevV2()
        result = ai.display_help()
    else:
        ai = TraeDevV2()
        result = ai.process_command(command)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()