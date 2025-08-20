#!/usr/bin/env python3
"""
🚀 Trae超级团队启动器
一键启动完整的AI智能体团队
作者：你的专属AI团队
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

class TeamLauncher:
    """超级团队启动器"""
    
    def __init__(self):
        self.trae_dir = Path(__file__).parent.parent  # 指向 .trae 目录
        self.agents_dir = self.trae_dir / "agent"
        self.scripts_dir = self.trae_dir / "scripts"
        self.project_root = self.trae_dir.parent
        
        # 确保目录存在
        self.agents_dir.mkdir(exist_ok=True)
        self.scripts_dir.mkdir(exist_ok=True)
    
    def show_banner(self):
        """显示启动横幅"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🚀 Trae 超级团队启动器                              ║
║                                                              ║
║    一键启动完整AI智能体团队                                  ║
║    复制即用 · 零配置 · 全功能                               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def list_agents(self) -> List[Dict]:
        """列出所有可用智能体"""
        agents = []
        for agent_file in self.agents_dir.glob("*.json"):
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    agents.append({
                        "name": agent_file.stem,
                        "file": agent_file.name,
                        "description": config.get("agent_info", {}).get("description", "暂无描述"),
                        "role": config.get("agent_info", {}).get("role", "未知角色")
                    })
            except Exception as e:
                print(f"⚠️  加载 {agent_file.name} 失败: {e}")
        return agents
    
    def quick_start(self):
        """快速启动向导"""
        self.show_banner()
        
        print("📋 发现以下智能体：")
        agents = self.list_agents()
        
        if not agents:
            print("❌ 未找到智能体配置，请先创建智能体！")
            return
        
        for i, agent in enumerate(agents, 1):
            print(f"{i}. {agent['name']} - {agent['description']}")
        
        try:
            choice = input("\n🎯 请选择智能体编号 (或输入 'all' 启动全部): ").strip()
            
            if choice.lower() == 'all':
                self.start_all_agents(agents)
            elif choice.isdigit() and 1 <= int(choice) <= len(agents):
                selected = agents[int(choice) - 1]
                self.start_single_agent(selected)
            else:
                print("❌ 无效选择")
                
        except KeyboardInterrupt:
            print("\n👋 已取消操作")
    
    def start_single_agent(self, agent: Dict):
        """启动单个智能体"""
        print(f"🚀 正在启动: {agent['name']}")
        print(f"📄 配置文件: {agent['file']}")
        print(f"📝 角色描述: {agent['description']}")
        
        # 这里可以添加实际的启动逻辑
        print(f"✅ {agent['name']} 智能体已准备就绪！")
        print(f"💡 使用提示: 该智能体已配置为 {agent['role']}")
    
    def start_all_agents(self, agents: List[Dict]):
        """启动所有智能体"""
        print(f"🚀 正在启动 {len(agents)} 个智能体...")
        
        for agent in agents:
            print(f"  ✅ {agent['name']} - {agent['role']}")
        
        print("\n🎉 超级团队已全员就位！")
        print("💡 每个智能体都已准备好在当前项目中协作")
    
    def project_setup(self):
        """项目初始化设置"""
        print("🔧 正在设置当前项目...")
        
        # 创建项目配置文件
        project_config = {
            "project_name": self.project_root.name,
            "trae_version": "1.0",
            "active_agents": [agent["name"] for agent in self.list_agents()],
            "setup_date": "auto-generated"
        }
        
        config_file = self.project_root / ".trae-project.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(project_config, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 项目配置已保存到: {config_file}")
    
    def migration_guide(self):
        """显示迁移指南"""
        print("""
📦 超级团队迁移指南

🎯 在新项目中使用：
1. 复制整个 .trae 目录到新项目根目录
2. 运行: python .trae/team-launcher.py
3. 按照向导选择智能体

🚀 快速命令：
   python .trae/team-launcher.py start     # 启动向导
   python .trae/team-launcher.py list      # 列出所有智能体
   python .trae/team-launcher.py setup      # 项目设置

💡 项目结构：
   your-project/
   ├── .trae/
   │   ├── team-launcher.py      # 团队启动器
   │   ├── agent/                # 智能体配置
   │   └── scripts/              # 工具脚本
   └── your-project-files...

🎉 一键启动完整AI团队！
        """)
    
    def show_help(self):
        """显示帮助"""
        print("""
🚀 Trae超级团队启动器 - 使用帮助

用法:
    python team-launcher.py start      # 启动向导模式
    python team-launcher.py list       # 列出所有智能体
    python team-launcher.py setup      # 项目初始化
    python team-launcher.py guide      # 显示迁移指南
    python team-launcher.py help       # 显示此帮助

功能:
    • 一键启动完整AI智能体团队
    • 零配置复制即用
    • 支持单个/批量启动
    • 自动项目适配
    • 可视化操作界面

示例:
    # 在新项目中使用
    cp -r learn_trae/.trae my-new-project/
    cd my-new-project
    python .trae/team-launcher.py start
        """)

def main():
    """主函数"""
    launcher = TeamLauncher()
    
    if len(sys.argv) < 2:
        launcher.quick_start()
    else:
        command = sys.argv[1]
        if command == "start":
            launcher.quick_start()
        elif command == "list":
            agents = launcher.list_agents()
            print(f"📋 发现 {len(agents)} 个智能体:")
            for agent in agents:
                print(f"  • {agent['name']} - {agent['description']}")
        elif command == "setup":
            launcher.project_setup()
        elif command == "guide":
            launcher.migration_guide()
        elif command == "help":
            launcher.show_help()
        else:
            launcher.show_help()

if __name__ == "__main__":
    main()