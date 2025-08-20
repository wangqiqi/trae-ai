#!/usr/bin/env python3
"""
批量升级 .trae\agents2 目录下的所有智能体到v2.0标准
作者：AI助手
功能：将旧版智能体升级到100分合规的v2.0版本
"""

import os
import json
import shutil
from pathlib import Path
import subprocess
import sys
from datetime import datetime

class AgentUpgrader:
    def __init__(self, agents_dir, script_path):
        self.agents_dir = Path(agents_dir)
        self.script_path = Path(script_path)
        self.backup_dir = self.agents_dir / "backup" / datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def scan_agents(self):
        """扫描所有需要升级的智能体文件"""
        agents = []
        for file in self.agents_dir.glob("*-engineer-v2.json"):
            if file.is_file():
                agents.append(file)
        return agents
    
    def check_compliance(self, agent_file):
        """检查单个智能体的合规性"""
        try:
            cmd = [sys.executable, str(self.script_path), "check", str(agent_file)]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.agents_dir.parent.parent)
            
            # 尝试解析JSON输出
            try:
                output = json.loads(result.stdout)
                return output
            except:
                # 如果输出不是JSON，返回基本结果
                return {
                    "file": agent_file.name,
                    "v2_compliant": False,
                    "score": 0,
                    "error": "无法解析输出"
                }
        except Exception as e:
            return {
                "file": agent_file.name,
                "v2_compliant": False,
                "score": 0,
                "error": str(e)
            }
    
    def backup_agents(self, agents):
        """备份原始文件"""
        if not agents:
            return
            
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 创建备份目录: {self.backup_dir}")
        
        for agent_file in agents:
            backup_file = self.backup_dir / agent_file.name
            shutil.copy2(agent_file, backup_file)
            print(f"💾 备份: {agent_file.name}")
    
    def extract_tech_stack(self, agent_file):
        """从文件名提取技术栈"""
        # 从文件名提取技术栈，例如：angular-engineer-v2.json -> angular
        name = agent_file.stem  # 去掉扩展名
        tech_stack = name.replace("-engineer-v2", "")
        return tech_stack
    
    def regenerate_agent(self, agent_file):
        """重新生成单个智能体"""
        tech_stack = self.extract_tech_stack(agent_file)
        
        try:
            cmd = [sys.executable, str(self.script_path), "generate", tech_stack]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.agents_dir.parent.parent)
            
            if result.returncode == 0:
                return True, f"✅ 成功重新生成 {tech_stack} 智能体"
            else:
                return False, f"❌ 重新生成失败: {result.stderr}"
        except Exception as e:
            return False, f"❌ 错误: {str(e)}"
    
    def upgrade_all(self):
        """执行完整的批量升级流程"""
        print("🚀 开始批量升级智能体...")
        print("=" * 50)
        
        # 1. 扫描文件
        agents = self.scan_agents()
        if not agents:
            print("⚠️ 没有找到需要升级的智能体文件")
            return
        
        print(f"📊 发现 {len(agents)} 个智能体文件")
        
        # 2. 检查当前合规性
        need_upgrade = []
        for agent_file in agents:
            result = self.check_compliance(agent_file)
            score = result.get("score", 0)
            compliant = result.get("v2_compliant", False)
            
            print(f"📄 {agent_file.name}: {score}分 {'✅' if compliant else '❌'}")
            
            if not compliant or score < 100:
                need_upgrade.append(agent_file)
        
        if not need_upgrade:
            print("🎉 所有智能体已经是100分合规版本！")
            return
        
        print(f"🔧 需要升级 {len(need_upgrade)} 个智能体")
        
        # 3. 备份原始文件
        self.backup_agents(need_upgrade)
        
        # 4. 逐个重新生成
        success_count = 0
        for agent_file in need_upgrade:
            print(f"\n🔄 正在升级: {agent_file.name}")
            success, message = self.regenerate_agent(agent_file)
            print(f"   {message}")
            
            if success:
                success_count += 1
        
        # 5. 验证升级结果
        print("\n📋 验证升级结果...")
        final_results = []
        for agent_file in need_upgrade:
            result = self.check_compliance(agent_file)
            final_results.append({
                "file": agent_file.name,
                "score": result.get("score", 0),
                "compliant": result.get("v2_compliant", False)
            })
        
        print("\n" + "=" * 50)
        print(f"📊 升级完成统计:")
        print(f"   总文件数: {len(agents)}")
        print(f"   升级成功: {success_count}")
        print(f"   备份位置: {self.backup_dir}")
        
        # 显示最终结果
        print("\n🎯 最终合规性检查结果:")
        for result in final_results:
            status = "✅" if result["compliant"] else "❌"
            print(f"   {result['file']}: {result['score']}分 {status}")

def main():
    # 设置路径
    agents_dir = "e:\\study\\learn_trae\\.trae\\agents2"
    script_path = "e:\\study\\learn_trae\\.trae\\scripts\\agent-suitev2.py"
    
    # 检查路径是否存在
    if not os.path.exists(agents_dir):
        print(f"❌ 智能体目录不存在: {agents_dir}")
        return
    
    if not os.path.exists(script_path):
        print(f"❌ 脚本文件不存在: {script_path}")
        return
    
    # 执行升级
    upgrader = AgentUpgrader(agents_dir, script_path)
    upgrader.upgrade_all()

if __name__ == "__main__":
    main()