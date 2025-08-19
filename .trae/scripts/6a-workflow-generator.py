#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
6A超级工作流文档生成器
读取模板文件生成项目文档，避免Python字符串格式问题
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
import argparse

class SixAWorkflowGenerator:
    def __init__(self, base_path=None):
        self.base_path = Path(base_path or os.getcwd())
        self.template_dir = self.base_path / ".trae" / "templates" / "6a-docs"
        self.output_dir = None
        
    def create_project_structure(self, project_name):
        """创建项目目录结构"""
        safe_name = "".join(c for c in project_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '-')
        
        self.output_dir = self.base_path / "projects" / safe_name
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建子目录
        subdirs = [
            "docs/6a-workflow",
            "src/frontend",
            "src/backend",
            "tests",
            "scripts",
            "configs"
        ]
        
        for subdir in subdirs:
            (self.output_dir / subdir).mkdir(parents=True, exist_ok=True)
            
        return self.output_dir
    
    def read_template(self, template_name):
        """读取模板文件"""
        template_file = self.template_dir / f"{template_name}-template.md"
        if template_file.exists():
            return template_file.read_text(encoding='utf-8')
        else:
            return f"# 模板文件不存在: {template_name}"
    
    def render_template(self, template_content, context):
        """渲染模板内容"""
        # 使用简单的字符串替换，避免格式问题
        for key, value in context.items():
            placeholder = f"{{{key}}}"
            template_content = template_content.replace(placeholder, str(value))
        return template_content
    
    def generate_alignment_doc(self, project_name, project_description):
        """生成需求对齐文档"""
        template = self.read_template("01-alignment")
        context = {
            "project_name": project_name,
            "project_description": project_description,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        content = self.render_template(template, context)
        
        output_file = self.output_dir / "docs" / "6a-workflow" / "01-requirement-alignment.md"
        output_file.write_text(content, encoding='utf-8')
        return output_file
    
    def generate_consensus_doc(self, project_name):
        """生成需求共识文档"""
        template = self.read_template("02-consensus")
        context = {
            "project_name": project_name
        }
        content = self.render_template(template, context)
        
        output_file = self.output_dir / "docs" / "6a-workflow" / "02-requirement-consensus.md"
        output_file.write_text(content, encoding='utf-8')
        return output_file
    
    def generate_design_doc(self, project_name):
        """生成架构设计文档"""
        template = self.read_template("03-design")
        context = {
            "project_name": project_name
        }
        content = self.render_template(template, context)
        
        output_file = self.output_dir / "docs" / "6a-workflow" / "03-architecture-design.md"
        output_file.write_text(content, encoding='utf-8')
        return output_file
    
    def generate_task_doc(self, project_name):
        """生成任务分解文档"""
        template = self.read_template("04-task")
        context = {
            "project_name": project_name
        }
        content = self.render_template(template, context)
        
        output_file = self.output_dir / "docs" / "6a-workflow" / "04-task-breakdown.md"
        output_file.write_text(content, encoding='utf-8')
        return output_file
    
    def create_tasksync_config(self, project_name):
        """创建TaskSync监控配置"""
        config = {
            "project": project_name,
            "created": datetime.now().isoformat(),
            "workflow": "6a-super-workflow",
            "stages": [
                "需求对齐", "需求共识", "架构设计", "任务分解", 
                "开发实现", "测试验证", "部署上线", "项目验收"
            ],
            "current_stage": "需求对齐",
            "status": "active",
            "milestones": [
                {
                    "name": "需求确认",
                    "target_date": "",
                    "status": "pending"
                },
                {
                    "name": "设计完成", 
                    "target_date": "",
                    "status": "pending"
                },
                {
                    "name": "开发完成",
                    "target_date": "", 
                    "status": "pending"
                }
            ]
        }
        
        config_file = self.output_dir / "configs" / "tasksync-config.json"
        config_file.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding='utf-8')
        return config_file
    
    def create_readme(self, project_name):
        """创建项目README"""
        readme_content = f"""# {project_name}

## 🎯 项目简介
{project_name} 项目采用6A超级工作流开发

## 📁 项目结构
```
{project_name}/
├── docs/6a-workflow/          # 6A工作流文档
│   ├── 01-requirement-alignment.md
│   ├── 02-requirement-consensus.md
│   ├── 03-architecture-design.md
│   └── 04-task-breakdown.md
├── src/
│   ├── frontend/              # 前端代码
│   └── backend/               # 后端代码
├── tests/                     # 测试代码
├── scripts/                   # 脚本文件
└── configs/                   # 配置文件
```

## 🚀 快速开始

### 1. 查看工作流文档
打开 `docs/6a-workflow/` 目录查看完整的6A工作流文档

### 2. 启动开发环境
```bash
# 安装依赖
npm install
pip install -r requirements.txt

# 启动开发服务器
npm run dev
```

## 📋 开发规范
- 遵循6A工作流各阶段规范
- 代码提交前需通过测试
- 每日更新TaskSync状态

## 📞 联系信息
- 项目经理：
- 技术负责人：
- 创建时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        readme_file = self.output_dir / "README.md"
        readme_file.write_text(readme_content, encoding='utf-8')
        return readme_file
    
    def generate_all_docs(self, project_name, project_description=""):
        """生成所有6A工作流文档"""
        print(f"🚀 开始生成6A工作流文档...")
        
        # 创建项目结构
        project_dir = self.create_project_structure(project_name)
        print(f"✅ 项目目录创建完成: {project_dir}")
        
        # 生成各个阶段文档
        docs = []
        docs.append(self.generate_alignment_doc(project_name, project_description))
        print("✅ 需求对齐文档生成完成")
        
        docs.append(self.generate_consensus_doc(project_name))
        print("✅ 需求共识文档生成完成")
        
        docs.append(self.generate_design_doc(project_name))
        print("✅ 架构设计文档生成完成")
        
        docs.append(self.generate_task_doc(project_name))
        print("✅ 任务分解文档生成完成")
        
        # 创建TaskSync配置
        tasksync_config = self.create_tasksync_config(project_name)
        print("✅ TaskSync配置创建完成")
        
        # 创建项目README
        readme = self.create_readme(project_name)
        print("✅ 项目README创建完成")
        
        return {
            "project_dir": project_dir,
            "docs": docs,
            "tasksync_config": tasksync_config,
            "readme": readme
        }

def main():
    parser = argparse.ArgumentParser(description='6A超级工作流文档生成器')
    parser.add_argument('project_name', help='项目名称')
    parser.add_argument('description', nargs='?', default='', help='项目描述')
    
    args = parser.parse_args()
    
    generator = SixAWorkflowGenerator()
    result = generator.generate_all_docs(args.project_name, args.description)
    
    print(f"\n🎉 6A工作流项目创建成功！")
    print(f"📁 项目路径: {result['project_dir']}")
    print(f"📋 生成文档: {len(result['docs'])} 个")
    print(f"\n下一步操作：")
    print(f"1. 查看文档: cd {result['project_dir']} && start docs\\6a-workflow")
    print(f"2. 启动开发: 按照 README.md 指引开始")
    print(f"3. 更新状态: 修改 configs/tasksync-config.json 跟踪进度")

if __name__ == "__main__":
    main()