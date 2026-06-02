#!/usr/bin/env python3
# 🎯 团队协作工程师
# 多人AI协作开发，协调团队工作流程

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class TeamCollaborationEngineer:
    """
    团队协作工程师
    职责：协调团队工作流程，促进多人协作
    功能：任务管理、进度跟踪、团队沟通、会议组织
    """
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.trae_path = self.project_root / ".trae"
        self.team_data_path = self.trae_path / "team-data"
        self.team_data_path.mkdir(exist_ok=True)
        self.tasks_file = self.team_data_path / "tasks.json"
        self.team_file = self.team_data_path / "team.json"
        self.meetings_file = self.team_data_path / "meetings.json"
        self.load_data()
    
    def load_data(self):
        """加载团队数据"""
        if self.tasks_file.exists():
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                self.tasks = json.load(f)
        else:
            self.tasks = []
        
        if self.team_file.exists():
            with open(self.team_file, 'r', encoding='utf-8') as f:
                self.team_members = json.load(f)
        else:
            self.team_members = []
        
        if self.meetings_file.exists():
            with open(self.meetings_file, 'r', encoding='utf-8') as f:
                self.meetings = json.load(f)
        else:
            self.meetings = []
    
    def save_data(self):
        """保存团队数据"""
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=2, ensure_ascii=False)
        
        with open(self.team_file, 'w', encoding='utf-8') as f:
            json.dump(self.team_members, f, indent=2, ensure_ascii=False)
        
        with open(self.meetings_file, 'w', encoding='utf-8') as f:
            json.dump(self.meetings, f, indent=2, ensure_ascii=False)
    
    def add_team_member(self, name: str, role: str, skills: List[str]):
        """添加团队成员"""
        member = {
            "id": len(self.team_members) + 1,
            "name": name,
            "role": role,
            "skills": skills,
            "joined_at": datetime.now().isoformat(),
            "tasks_count": 0
        }
        self.team_members.append(member)
        self.save_data()
        return member
    
    def create_task(self, title: str, description: str, assignee: str = None, priority: str = "medium", status: str = "pending"):
        """创建任务"""
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "assignee": assignee,
            "priority": priority,
            "status": status,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.save_data()
        return task
    
    def update_task_status(self, task_id: int, status: str):
        """更新任务状态"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = status
                task["updated_at"] = datetime.now().isoformat()
                self.save_data()
                return True
        return False
    
    def schedule_meeting(self, title: str, date: str, time: str, participants: List[str], agenda: List[str]):
        """安排会议"""
        meeting = {
            "id": len(self.meetings) + 1,
            "title": title,
            "date": date,
            "time": time,
            "participants": participants,
            "agenda": agenda,
            "status": "scheduled",
            "created_at": datetime.now().isoformat()
        }
        self.meetings.append(meeting)
        self.save_data()
        return meeting
    
    def get_team_report(self) -> str:
        """生成团队状态报告"""
        report = f"""
🎯 团队协作报告
{'='*60}
📊 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
📁 项目路径: {self.project_root}

👥 团队成员 ({len(self.team_members)}人)
--------------
"""
        
        for member in self.team_members:
            report += f"👤 {member['name']} - {member['role']}\n"
            report += f"   技能: {', '.join(member['skills'])}\n"
            report += f"   加入时间: {member['joined_at'][:10]}\n"
        
        report += f"""

📋 任务统计
-----------
- 总任务数: {len(self.tasks)}
- 待处理: {sum(1 for t in self.tasks if t['status'] == 'pending')}
- 进行中: {sum(1 for t in self.tasks if t['status'] == 'in_progress')}
- 已完成: {sum(1 for t in self.tasks if t['status'] == 'completed')}
"""
        
        if self.tasks:
            report += "\n📝 当前任务列表:\n"
            for task in self.tasks[:5]:
                status_icon = {
                    "pending": "⏳",
                    "in_progress": "🔄",
                    "completed": "✅"
                }.get(task["status"], "❓")
                report += f"   {status_icon} [{task['priority'].upper()}] {task['title']}"
                if task['assignee']:
                    report += f" - {task['assignee']}"
                report += "\n"
        
        report += f"""

📅 近期会议 ({len(self.meetings)}个)
------------------
"""
        
        for meeting in self.meetings[:3]:
            report += f"📅 {meeting['title']}\n"
            report += f"   时间: {meeting['date']} {meeting['time']}\n"
            report += f"   参会人员: {', '.join(meeting['participants'])}\n"
        
        return report
    
    def generate_meeting_agenda(self, topic: str) -> List[str]:
        """生成会议议程"""
        agendas = {
            "项目进度": ["上周工作总结", "本周工作计划", "问题与障碍", "资源需求"],
            "技术方案": ["方案介绍", "技术选型讨论", "风险评估", "实施计划"],
            "代码审查": ["PR概述", "代码质量评估", "安全审查", "改进建议"],
            "需求评审": ["需求介绍", "优先级讨论", "工作量估算", "排期确认"]
        }
        
        return agendas.get(topic, ["会议目标", "讨论内容", "下一步行动", "时间安排"])
    
    def run_interactive(self):
        """运行交互模式"""
        while True:
            menu = """
🎯 团队协作控制台
==================
1. 👥 查看团队成员
2. ➕ 添加团队成员
3. 📋 查看任务列表
4. ✅ 创建新任务
5. 🔄 更新任务状态
6. 📅 安排会议
7. 📊 生成团队报告
8. ❓ 帮助
9. 🚪 退出

请选择 (1-9): """
            
            choice = input(menu).strip()
            
            if choice == "1":
                print("\n👥 团队成员:")
                for member in self.team_members:
                    print(f"   {member['id']}. {member['name']} - {member['role']}")
            elif choice == "2":
                name = input("👤 成员姓名: ").strip()
                role = input("📝 角色: ").strip()
                skills = input("💡 技能(逗号分隔): ").strip().split(',')
                self.add_team_member(name, role, [s.strip() for s in skills])
                print("✅ 成员添加成功!")
            elif choice == "3":
                print("\n📋 任务列表:")
                for task in self.tasks:
                    print(f"   {task['id']}. [{task['status']}] {task['title']}")
            elif choice == "4":
                title = input("📝 任务标题: ").strip()
                desc = input("📄 任务描述: ").strip()
                assignee = input("👤 负责人(可选): ").strip()
                priority = input("⚡ 优先级(low/medium/high): ").strip() or "medium"
                self.create_task(title, desc, assignee if assignee else None, priority)
                print("✅ 任务创建成功!")
            elif choice == "5":
                task_id = int(input("🔢 任务ID: ").strip())
                status = input("📊 新状态(pending/in_progress/completed): ").strip()
                if self.update_task_status(task_id, status):
                    print("✅ 任务状态更新成功!")
                else:
                    print("❌ 任务未找到!")
            elif choice == "6":
                title = input("📅 会议主题: ").strip()
                date = input("📆 日期(YYYY-MM-DD): ").strip()
                time = input("⏰ 时间(HH:MM): ").strip()
                participants = input("👥 参会人员(逗号分隔): ").strip().split(',')
                agenda = self.generate_meeting_agenda(title)
                self.schedule_meeting(title, date, time, [p.strip() for p in participants], agenda)
                print("✅ 会议安排成功!")
            elif choice == "7":
                print(self.get_team_report())
            elif choice == "8":
                print("\n❓ 帮助信息:")
                print("   团队协作工程师帮助您管理团队任务和会议")
                print("   支持: 成员管理、任务管理、会议安排")
            elif choice == "9":
                print("👋 再见!")
                break
            else:
                print("❌ 无效选择，请重新输入")
    
    def run(self):
        """运行团队协作工程师"""
        if len(sys.argv) > 1 and sys.argv[1] == "--report":
            print(self.get_team_report())
        else:
            self.run_interactive()

if __name__ == "__main__":
    engineer = TeamCollaborationEngineer()
    engineer.run()