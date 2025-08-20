#!/usr/bin/env python3
"""
批量升级 .trae\agents2 目录下的所有智能体到v2.0标准（Windows兼容版）
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
    
    def check_compliance_direct(self, agent_file):
        """直接检查文件内容判断合规性"""
        try:
            with open(agent_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查必需字段
            required_fields = ["required", "lifecycle", "quality"]
            missing = []
            
            for field in required_fields:
                if field not in data:
                    missing.append(field)
            
            score = 100 - (len(missing) * 15)
            
            return {
                "file": agent_file.name,
                "v2_compliant": len(missing) == 0,
                "score": max(score, 0),
                "missing_sections": missing
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
        print(f"[备份] 创建备份目录: {self.backup_dir}")
        
        for agent_file in agents:
            backup_file = self.backup_dir / agent_file.name
            shutil.copy2(agent_file, backup_file)
            print(f"[备份] 已备份: {agent_file.name}")
    
    def extract_tech_stack(self, agent_file):
        """从文件名提取技术栈"""
        name = agent_file.stem  # 去掉扩展名
        tech_stack = name.replace("-engineer-v2", "")
        return tech_stack
    
    def regenerate_agent_direct(self, agent_file):
        """直接生成新的智能体文件"""
        tech_stack = self.extract_tech_stack(agent_file)
        
        # 构建新文件内容
        new_content = self.build_agent_content(tech_stack)
        
        # 写入新文件
        try:
            with open(agent_file, 'w', encoding='utf-8') as f:
                json.dump(new_content, f, indent=2, ensure_ascii=False)
            return True, f"成功重新生成 {tech_stack} 智能体"
        except Exception as e:
            return False, f"重新生成失败: {str(e)}"
    
    def build_agent_content(self, tech_stack):
        """构建符合v2.0标准的智能体内容"""
        return {
            "schema_version": "2.0",
            "agent_info": {
                "name": f"{tech_stack.title()}工程师",
                "description": f"专精{tech_stack}的现代化开发专家",
                "version": "1.0.0",
                "author": "AI助手"
            },
            "technical_stack": {
                "primary_language": tech_stack,
                "frameworks": [f"{tech_stack}-framework"],
                "tools": ["git", "docker", "ci-cd"],
                "version_constraint": ">=1.0.0"
            },
            "required": {
                "role_name": f"{tech_stack.title()}工程师",
                "expertise": [
                    f"{tech_stack}开发",
                    "现代化工程实践",
                    "代码质量保证"
                ],
                "mandatory_tools": [
                    "代码编辑器",
                    "版本控制",
                    "调试工具"
                ],
                "constraints": [
                    "遵循最佳实践",
                    "保证代码质量",
                    "及时文档化"
                ]
            },
            "lifecycle": {
                "project_phases": [
                    "需求分析",
                    "系统设计",
                    "编码实现",
                    "测试验证",
                    "部署发布",
                    "运维监控"
                ],
                "deployment_strategy": "滚动部署",
                "environments": ["开发", "测试", "预生产", "生产"],
                "rollback_plan": "蓝绿部署回滚"
            },
            "quality": {
                "code_standards": f"{tech_stack}官方最佳实践",
                "testing_requirements": [
                    "单元测试覆盖率>80%",
                    "集成测试覆盖核心功能",
                    "E2E测试覆盖用户场景"
                ],
                "review_process": "代码审查+自动化检查",
                "documentation": "README+API文档+架构说明"
            },
            "infrastructure": {
                "cloud_provider": "GCP",
                "container_tools": ["Docker", "Kubernetes"],
                "monitoring": ["Prometheus", "Grafana"],
                "logging": ["ELK Stack", "Cloud Logging"]
            },
            "observability": {
                "metrics": ["性能指标", "业务指标"],
                "tracing": ["分布式追踪", "错误追踪"],
                "alerts": ["异常告警", "性能告警"]
            },
            "security": {
                "dependency_scanning": True,
                "vulnerability_management": True,
                "compliance_standards": ["SOC2", "ISO27001"]
            }
        }
    
    def upgrade_all(self):
        """执行完整的批量升级流程"""
        print("[开始] 批量升级智能体到v2.0标准...")
        print("=" * 60)
        
        # 1. 扫描文件
        agents = self.scan_agents()
        if not agents:
            print("[警告] 没有找到需要升级的智能体文件")
            return
        
        print(f"[统计] 发现 {len(agents)} 个智能体文件")
        
        # 2. 检查当前合规性
        need_upgrade = []
        print("\n[检查] 当前合规性状态:")
        print("-" * 40)
        
        for agent_file in agents:
            result = self.check_compliance_direct(agent_file)
            score = result.get("score", 0)
            compliant = result.get("v2_compliant", False)
            missing = result.get("missing_sections", [])
            
            status = "[合规]" if compliant else "[需升级]"
            print(f"  {agent_file.name}: {score}分 {status}")
            if missing:
                print(f"    缺失: {', '.join(missing)}")
            
            if not compliant:
                need_upgrade.append(agent_file)
        
        if not need_upgrade:
            print("\n[完成] 所有智能体已经是100分合规版本！")
            return
        
        print(f"\n[计划] 需要升级 {len(need_upgrade)} 个智能体")
        
        # 3. 确认升级
        response = input("\n确认开始升级？(y/N): ").strip().lower()
        if response != 'y':
            print("[取消] 升级已取消")
            return
        
        # 4. 备份原始文件
        self.backup_agents(need_upgrade)
        
        # 5. 逐个升级
        success_count = 0
        print("\n[升级] 开始处理...")
        print("-" * 40)
        
        for i, agent_file in enumerate(need_upgrade, 1):
            print(f"[{i}/{len(need_upgrade)}] 升级: {agent_file.name}")
            success, message = self.regenerate_agent_direct(agent_file)
            
            if success:
                success_count += 1
                print(f"    [成功] {message}")
            else:
                print(f"    [失败] {message}")
        
        # 6. 验证结果
        print("\n[验证] 升级结果验证...")
        print("-" * 40)
        
        final_results = []
        for agent_file in need_upgrade:
            result = self.check_compliance_direct(agent_file)
            final_results.append(result)
            
            score = result.get("score", 0)
            compliant = result.get("v2_compliant", False)
            status = "[合规]" if compliant else "[仍需修复]"
            print(f"  {agent_file.name}: {score}分 {status}")
        
        # 7. 最终统计
        print("\n" + "=" * 60)
        print("[总结] 升级完成统计:")
        print(f"   总文件数: {len(agents)}")
        print(f"   升级成功: {success_count}")
        print(f"   备份位置: {self.backup_dir}")
        
        if success_count == len(need_upgrade):
            print("\n🎉 所有智能体已成功升级到v2.0标准！")
        else:
            print(f"\n⚠️  {len(need_upgrade) - success_count} 个文件需要手动处理")

def main():
    # 设置路径
    agents_dir = "e:\\study\\learn_trae\\.trae\\agents2"
    script_path = "e:\\study\\learn_trae\\.trae\\scripts\\agent-suitev2.py"
    
    # 检查路径是否存在
    if not os.path.exists(agents_dir):
        print(f"[错误] 智能体目录不存在: {agents_dir}")
        return
    
    # 执行升级
    upgrader = AgentUpgrader(agents_dir, script_path)
    upgrader.upgrade_all()

if __name__ == "__main__":
    main()