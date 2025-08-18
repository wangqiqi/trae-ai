#!/usr/bin/env python3
"""
项目启动标准化脚本
确保每个项目都按统一决策流程执行
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

class ProjectInitCommander:
    def __init__(self):
        self.base_path = Path("e:/study/learn_trae")
        self.config_path = self.base_path / ".trae"
        self.checklist_file = self.config_path / "templates" / "project-decision-checklist.json"
        
    def load_checklist(self):
        """加载决策检查清单"""
        with open(self.checklist_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def interactive_decision_flow(self):
        """交互式决策流程"""
        checklist = self.load_checklist()
        decisions = {
            "project_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "decisions": [],
            "timestamp": datetime.now().isoformat()
        }
        
        print("🚀 项目启动决策流程")
        print("=" * 50)
        
        # 需求确认阶段
        self._phase_requirement_confirmation(checklist, decisions)
        
        # 团队组建阶段  
        self._phase_team_assembly(checklist, decisions)
        
        # 里程碑确认阶段
        self._phase_milestone_confirmation(checklist, decisions)
        
        # 保存决策记录
        self._save_decisions(decisions)
        
        return decisions
    
    def _phase_requirement_confirmation(self, checklist, decisions):
        """需求确认阶段"""
        checkpoint = checklist["decision_checkpoints"][0]
        print(f"\n📋 {checkpoint['checkpoint']} (Phase 1)")
        print("-" * 30)
        
        answers = {}
        for question in checkpoint["questions"]:
            print(f"\n❓ {question}")
            if "项目类型" in question:
                print("选项: Web应用 | 移动应用 | 小程序 | AI系统")
                answer = input("您的选择: ").strip()
            elif "技术栈" in question:
                print("选项: FastAPI+Vue3 | Node.js+React | Go+Flutter")
                answer = input("您的选择: ").strip()
            elif "项目规模" in question:
                print("选项: 入门级 | 中级 | 高级")
                answer = input("您的选择: ").strip()
            elif "开发周期" in question:
                print("选项: 1周 | 2-4周 | 1-2个月")
                answer = input("您的选择: ").strip()
            elif "团队配置" in question:
                print("选项: 精简版 | 标准版 | 完整版")
                answer = input("您的选择: ").strip()
            else:
                answer = input("您的回答: ").strip()
            
            answers[question] = answer
        
        decisions["decisions"].append({
            "checkpoint": "需求确认",
            "answers": answers,
            "phase": "启动前"
        })
    
    def _phase_team_assembly(self, checklist, decisions):
        """团队组建阶段"""
        checkpoint = checklist["decision_checkpoints"][1]
        print(f"\n👥 {checkpoint['checkpoint']} (Phase 2)")
        print("-" * 30)
        
        templates = checkpoint["selection_interface"]["team_templates"]
        print("\n可选团队模板:")
        for template_name, members in templates.items():
            print(f"  {template_name}: {', '.join(members)}")
        
        selected_template = input("\n选择团队模板 (精简团队/标准团队/完整团队): ").strip()
        
        # 个性化调整
        print("\n个性化调整:")
        custom_members = []
        for member_type in templates.get(selected_template, templates["标准团队"]):
            include = input(f"是否包含 {member_type}? (y/n): ").strip().lower()
            if include == 'y':
                custom_members.append(member_type)
        
        decisions["decisions"].append({
            "checkpoint": "团队组建",
            "selected_template": selected_template,
            "final_team": custom_members
        })
    
    def _phase_milestone_confirmation(self, checklist, decisions):
        """里程碑确认阶段"""
        checkpoint = checklist["decision_checkpoints"][2]
        print(f"\n🎯 {checkpoint['checkpoint']} (Phase 3)")
        print("-" * 30)
        
        milestones = checkpoint["milestones"]
        selected_milestones = []
        
        print("\n项目里程碑:")
        for i, milestone in enumerate(milestones, 1):
            include = input(f"{i}. {milestone} (y/n): ").strip().lower()
            if include == 'y':
                selected_milestones.append(milestone)
        
        # 自定义选项
        print("\n自定义选项:")
        customization = {}
        for option in checkpoint["customization_options"]:
            answer = input(f"{option} (y/n): ").strip().lower()
            customization[option] = answer == 'y'
        
        decisions["decisions"].append({
            "checkpoint": "里程碑确认",
            "selected_milestones": selected_milestones,
            "customization": customization
        })
    
    def _save_decisions(self, decisions):
        """保存决策记录"""
        project_path = self.base_path / f"project-{decisions['project_id']}"
        project_path.mkdir(exist_ok=True)
        
        decisions_file = project_path / "project-decisions.md"
        
        with open(decisions_file, 'w', encoding='utf-8') as f:
            f.write(f"# 项目启动决策记录\n\n")
            f.write(f"**项目ID**: {decisions['project_id']}\n")
            f.write(f"**决策时间**: {decisions['timestamp']}\n\n")
            
            for decision in decisions["decisions"]:
                f.write(f"## {decision['checkpoint']}\n\n")
                
                if 'answers' in decision:
                    for q, a in decision['answers'].items():
                        f.write(f"- **{q}**: {a}\n")
                
                if 'selected_template' in decision:
                    f.write(f"- **团队模板**: {decision['selected_template']}\n")
                    f.write(f"- **最终团队**: {', '.join(decision['final_team'])}\n")
                
                if 'selected_milestones' in decision:
                    f.write(f"- **里程碑**: {', '.join(decision['selected_milestones'])}\n")
                    f.write(f"- **自定义配置**: {json.dumps(decision['customization'], ensure_ascii=False)}\n")
                
                f.write("\n")
        
        print(f"\n✅ 决策记录已保存: {decisions_file}")
        return str(project_path)

if __name__ == "__main__":
    commander = ProjectInitCommander()
    decisions = commander.interactive_decision_flow()
    print(f"\n🎉 项目启动决策完成！")
    print(f"项目ID: {decisions['project_id']}")
    print(f"现在可以开始项目开发流程...")