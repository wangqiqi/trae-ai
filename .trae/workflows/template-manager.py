#!/usr/bin/env python3
"""
Trae AI 超级团队 - 模板自动化管理器

功能：
1. 自动识别项目类型并应用相应模板
2. 智能填充模板内容
3. 一键生成完整项目骨架
4. 模板版本管理和更新
5. 与AI智能体深度集成

作者：Trae AI团队
版本：v3.0
"""

import os
import json
import shutil
import argparse
from datetime import datetime
from pathlib import Path
import sys

class TemplateManager:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.templates_path = self.base_path / "templates"
        self.project_root = Path.cwd()
        self.config_file = self.base_path / "config" / "template-config.json"
        
    def get_project_info(self):
        """智能识别项目信息"""
        info = {
            "name": self.project_root.name,
            "type": "unknown",
            "tech_stack": [],
            "detected_files": [],
            "suggested_templates": []
        }
        
        # 检测项目文件
        files = list(self.project_root.glob("*"))
        
        # 前端项目检测
        if any(f.name == "package.json" for f in files):
            with open(self.project_root / "package.json") as f:
                package_data = json.load(f)
                deps = package_data.get("dependencies", {})
                
                if "vue" in deps:
                    info["type"] = "vue3"
                    info["tech_stack"] = ["Vue3", "JavaScript", "Vite"]
                    info["suggested_templates"] = ["project-init-template", "requirements-template"]
                elif "react" in deps:
                    info["type"] = "react"
                    info["tech_stack"] = ["React18", "JavaScript", "Next.js"]
                    info["suggested_templates"] = ["project-init-template", "requirements-template"]
        
        # 后端项目检测
        elif any(f.name == "requirements.txt" for f in files):
            info["type"] = "python"
            info["tech_stack"] = ["Python", "FastAPI", "PostgreSQL"]
            info["suggested_templates"] = ["project-init-template", "api-spec-template", "database-design-template"]
            
        # Flutter项目检测
        elif any(f.name == "pubspec.yaml" for f in files):
            info["type"] = "flutter"
            info["tech_stack"] = ["Flutter", "Dart", "Firebase"]
            info["suggested_templates"] = ["project-init-template", "requirements-template"]
        
        # 通用模板
        if info["type"] == "unknown":
            info["suggested_templates"] = ["project-init-template", "requirements-template", "test-plan-template"]
            
        return info
    
    def apply_template(self, template_name, project_info, custom_data=None):
        """应用模板到项目"""
        template_file = self.templates_path / f"{template_name}.md"
        
        if not template_file.exists():
            print(f"❌ 模板文件不存在: {template_name}")
            return False
            
        # 读取模板内容
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 智能填充变量
        filled_content = self.fill_template_variables(content, project_info, custom_data)
        
        # 生成目标文件
        target_file = self.get_target_filename(template_name)
        output_path = self.project_root / target_file
        
        # 创建目录
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(filled_content)
            
        print(f"✅ 已生成: {output_path}")
        return True
    
    def fill_template_variables(self, content, project_info, custom_data=None):
        """智能填充模板变量"""
        variables = {
            "{{PROJECT_NAME}}": project_info["name"],
            "{{PROJECT_TYPE}}": project_info["type"],
            "{{TECH_STACK}}": ", ".join(project_info["tech_stack"]),
            "{{CURRENT_DATE}}": datetime.now().strftime("%Y-%m-%d"),
            "{{CURRENT_YEAR}}": str(datetime.now().year),
            "{{AUTHOR}}": os.getenv("USER", "Trae AI团队"),
            "{{PROJECT_DESCRIPTION}}": f"基于{', '.join(project_info['tech_stack'])}的{project_info['name']}项目"
        }
        
        # 添加自定义数据
        if custom_data:
            variables.update(custom_data)
            
        # 替换变量
        for key, value in variables.items():
            content = content.replace(key, str(value))
            
        return content
    
    def get_target_filename(self, template_name):
        """根据模板类型确定目标文件名"""
        filename_map = {
            "project-init-template": "docs/project-init.md",
            "requirements-template": "docs/requirements.md",
            "api-spec-template": "docs/api-spec.md",
            "database-design-template": "docs/database-design.md",
            "test-plan-template": "docs/test-plan.md",
            "code-review-template": "docs/code-review.md",
            "deployment-template": "docs/deployment.md"
        }
        
        return filename_map.get(template_name, f"docs/{template_name}.md")
    
    def auto_apply_templates(self, project_type=None):
        """自动识别并应用模板"""
        project_info = self.get_project_info()
        
        if project_type:
            project_info["type"] = project_type
            
        print(f"🔍 检测到项目类型: {project_info['type']}")
        print(f"📋 技术栈: {', '.join(project_info['tech_stack'])}")
        
        applied_count = 0
        for template in project_info["suggested_templates"]:
            if self.apply_template(template, project_info):
                applied_count += 1
                
        print(f"✅ 成功应用 {applied_count} 个模板")
        return applied_count
    
    def interactive_apply(self):
        """交互式模板应用"""
        print("🎨 Trae AI 模板应用向导")
        print("=" * 50)
        
        project_info = self.get_project_info()
        
        print(f"项目: {project_info['name']}")
        print(f"类型: {project_info['type']}")
        
        # 显示可用模板
        templates = [f.stem for f in self.templates_path.glob("*.md") 
                    if f.stem != "README"]
        
        print("\n📋 可用模板:")
        for i, template in enumerate(templates, 1):
            print(f"  {i}. {template}")
            
        # 用户选择
        choices = input("\n选择要应用的模板 (用逗号分隔数字，或按Enter自动选择): ").strip()
        
        if not choices:
            return self.auto_apply_templates()
            
        selected_templates = []
        for choice in choices.split(","):
            try:
                idx = int(choice.strip()) - 1
                if 0 <= idx < len(templates):
                    selected_templates.append(templates[idx])
            except ValueError:
                continue
                
        # 应用选中的模板
        for template in selected_templates:
            self.apply_template(template, project_info)
            
    def create_project_with_templates(self, project_name, project_type):
        """使用模板创建新项目"""
        new_project_path = Path.cwd() / project_name
        
        if new_project_path.exists():
            print(f"❌ 项目目录已存在: {new_project_path}")
            return False
            
        # 创建项目目录
        new_project_path.mkdir(parents=True)
        
        # 切换到新项目目录
        os.chdir(new_project_path)
        
        # 设置项目信息
        project_info = {
            "name": project_name,
            "type": project_type,
            "tech_stack": self.get_tech_stack_for_type(project_type),
            "suggested_templates": self.get_templates_for_type(project_type)
        }
        
        # 应用模板
        for template in project_info["suggested_templates"]:
            self.apply_template(template, project_info)
            
        print(f"✅ 项目 {project_name} 创建完成！")
        print(f"📁 路径: {new_project_path}")
        
        # 生成项目结构
        self.create_project_structure(project_type, new_project_path)
        
        return True
    
    def get_tech_stack_for_type(self, project_type):
        """根据项目类型返回技术栈"""
        tech_stacks = {
            "vue3": ["Vue3", "TypeScript", "Vite", "Pinia", "Vue Router"],
            "react": ["React18", "TypeScript", "Next.js", "Redux", "React Router"],
            "fastapi": ["Python", "FastAPI", "SQLAlchemy", "PostgreSQL", "Docker"],
            "flutter": ["Flutter", "Dart", "Firebase", "Provider", "GetX"],
            "node": ["Node.js", "Express", "TypeScript", "MongoDB", "Docker"]
        }
        return tech_stacks.get(project_type, ["通用技术栈"])
    
    def get_templates_for_type(self, project_type):
        """根据项目类型返回推荐模板"""
        template_sets = {
            "vue3": ["project-init-template", "requirements-template", "test-plan-template"],
            "react": ["project-init-template", "requirements-template", "test-plan-template"],
            "fastapi": ["project-init-template", "api-spec-template", "database-design-template", "test-plan-template"],
            "flutter": ["project-init-template", "requirements-template", "test-plan-template"],
            "node": ["project-init-template", "api-spec-template", "test-plan-template"]
        }
        return template_sets.get(project_type, ["project-init-template", "requirements-template"])
    
    def create_project_structure(self, project_type, project_path):
        """创建项目目录结构"""
        structures = {
            "vue3": ["src", "public", "tests", "docs", ".github/workflows"],
            "react": ["src", "public", "tests", "docs", ".github/workflows"],
            "fastapi": ["app", "tests", "docs", "scripts", ".github/workflows"],
            "flutter": ["lib", "test", "docs", ".github/workflows"],
            "node": ["src", "tests", "docs", "scripts", ".github/workflows"]
        }
        
        dirs = structures.get(project_type, ["src", "tests", "docs"])
        
        for dir_name in dirs:
            (project_path / dir_name).mkdir(parents=True, exist_ok=True)
            
        print(f"📁 已创建项目目录结构")

def main():
    parser = argparse.ArgumentParser(description="Trae AI 模板自动化管理器")
    parser.add_argument("action", choices=["auto", "interactive", "create", "list"], 
                       help="操作类型")
    parser.add_argument("--name", help="项目名称 (用于create)")
    parser.add_argument("--type", choices=["vue3", "react", "fastapi", "flutter", "node"], 
                       help="项目类型 (用于create)")
    parser.add_argument("--template", help="指定模板名称")
    
    args = parser.parse_args()
    
    manager = TemplateManager()
    
    if args.action == "auto":
        manager.auto_apply_templates()
    elif args.action == "interactive":
        manager.interactive_apply()
    elif args.action == "create":
        if not args.name or not args.type:
            print("❌ 创建项目需要指定 --name 和 --type")
            sys.exit(1)
        manager.create_project_with_templates(args.name, args.type)
    elif args.action == "list":
        templates = [f.stem for f in manager.templates_path.glob("*.md") 
                    if f.stem != "README"]
        print("📋 可用模板:")
        for template in templates:
            print(f"  - {template}")

if __name__ == "__main__":
    main()