#!/usr/bin/env python3
"""
Trae AI 超级团队 - 模板自动化管理器（集成AI增强版）

功能：
1. 自动识别项目类型并应用相应模板
2. AI智能填充和增强模板内容
3. 一键生成完整项目骨架
4. 与20个AI专家智能体深度集成
5. 智能需求分析和项目建议

作者：Trae AI团队
版本：v3.1 - 集成AI增强功能
"""

import os
import json
import shutil
import argparse
from datetime import datetime
from pathlib import Path
import sys
import subprocess

class TemplateManager:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.templates_path = self.base_path / "templates"
        self.project_root = Path.cwd()
        # 配置文件路径已移除，使用默认配置
        self.config = {}
        
    def _run_ai_integration(self, action, **kwargs):
        """调用AI集成模块（通过trae-console.py）"""
        try:
            cmd = [
                sys.executable,
                "trae-console.py",
                "--ai-mode",
                action
            ]
            
            # 添加参数
            for key, value in kwargs.items():
                if value:
                    cmd.extend([f"--{key}", str(value)])
            
            result = subprocess.run(
                cmd,
                cwd=str(Path(__file__).parent),
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            return False, "", "AI集成模块超时"
        except Exception as e:
            return False, "", f"AI集成不可用: {e}"
        
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
        
        # HTML组合式设计项目检测
        elif any(f.suffix in ['.html', '.css', '.js'] for f in files[:10]):
            info["type"] = "html-composition"
            info["tech_stack"] = ["HTML5", "CSS3", "JavaScript", "Vanilla JS"]
            info["suggested_templates"] = ["html-composition-template", "project-init-template", "requirements-template"]
            
        # 通用模板
        if info["type"] == "unknown":
            info["suggested_templates"] = ["project-init-template", "requirements-template", "test-plan-template"]
            
        return info
    
    def apply_template(self, template_name, project_info, custom_data=None, use_ai_enhance=True):
        """应用模板到项目（支持AI增强）"""
        template_file = self.templates_path / f"{template_name}.md"
        
        if not template_file.exists():
            print(f"❌ 模板文件不存在: {template_name}")
            return False
            
        # 读取模板内容
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 基础变量填充
        filled_content = self.fill_template_variables(content, project_info, custom_data)
        
        # AI增强处理
        if use_ai_enhance:
            print(f"🤖 AI正在增强模板: {template_name}")
            enhanced_content = self._enhance_with_ai(template_name, project_info)
            if enhanced_content:
                filled_content = enhanced_content
        
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
        
    def _enhance_with_ai(self, template_name, project_info):
        """使用AI增强模板内容"""
        try:
            # 构建项目上下文
            project_context = {
                "name": project_info["name"],
                "type": project_info["type"],
                "tech_stack": project_info["tech_stack"],
                "features": project_info.get("features", []),
                "target_users": "end_users",
                "timeline": "4 weeks"
            }
            
            # 调用AI集成模块
            success, stdout, stderr = self._run_ai_integration(
                "enhance",
                template=template_name,
                project=json.dumps(project_context, ensure_ascii=False)
            )
            
            if success and stdout:
                return stdout.strip()
            else:
                print(f"⚠️ AI增强失败，使用基础模板: {stderr}")
                return None
                
        except Exception as e:
            print(f"⚠️ AI增强异常: {e}")
            return None
    
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
            "deployment-template": "docs/deployment.md",
            "html-composition-template": "docs/html-composition-guide.md"
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
            
    def interactive_create(self):
        """交互式创建项目（AI增强版）"""
        print("\n🎯 交互式项目创建")
        print("=" * 50)
        
        # 项目名称
        project_name = input("项目名称: ").strip()
        if not project_name:
            print("❌ 项目名称不能为空")
            return
            
        # 项目类型
        print("\n📋 选择项目类型:")
        project_types = ["vue3", "react", "fastapi", "flutter", "node"]
        for i, ptype in enumerate(project_types, 1):
            print(f"{i}. {ptype}")
            
        try:
            choice = int(input("选择: ")) - 1
            project_type = project_types[choice]
        except (ValueError, IndexError):
            print("❌ 无效选择")
            return
            
        # 是否使用AI增强
        use_ai = input("\n🤖 是否使用AI增强创建？(y/n): ").strip().lower() == 'y'
        
        features = []
        if use_ai:
            # 输入项目功能需求
            print("\n✨ 请输入项目功能需求（用逗号分隔）:")
            features_input = input("例如: 用户认证, 数据管理, 实时通信: ").strip()
            features = [f.strip() for f in features_input.split(",") if f.strip()]
            
            if not features:
                print("⚠️ 未输入功能需求，将使用基础模板")
                use_ai = False
        
        # 创建项目
        self.create_project_with_templates(
            project_name, 
            project_type, 
            features=features,
            use_ai_enhance=True
        )
        
        # 返回原目录
        os.chdir(self.project_root)

    def create_project_with_templates(self, project_name, project_type, features=None, use_ai_enhance=False, use_ai_kit=False):
        """使用模板创建新项目（支持AI完整套件）"""
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
            "features": features or [],
            "suggested_templates": self.get_templates_for_type(project_type)
        }
        
        if use_ai_enhance and features:
            # 使用AI创建完整项目套件
            print(f"🚀 使用AI创建 {project_name} 完整项目套件...")
            self._create_ai_project_kit(project_name, project_type, features)
        else:
            # 传统模板应用
            for template in project_info["suggested_templates"]:
                self.apply_template(template, project_info, use_ai_enhance=use_ai_enhance)
                
        print(f"✅ 项目 {project_name} 创建完成！")
        print(f"📁 路径: {new_project_path}")
        
        # 生成项目结构
        self.create_project_structure(project_type, new_project_path)
        
        return True
        
    def _create_ai_project_kit(self, project_name, project_type, features):
        """使用AI集成模块创建完整项目套件"""
        try:
            success, stdout, stderr = self._run_ai_integration(
                "kit",
                project=project_name,
                type=project_type,
                features=" ".join(features)
            )
            
            if success:
                print(f"✅ AI项目套件创建成功")
                return True
            else:
                print(f"⚠️ AI套件创建失败: {stderr}")
                return False
                
        except Exception as e:
            print(f"⚠️ AI套件创建异常: {e}")
            return False
    
    def get_tech_stack_for_type(self, project_type):
        """根据项目类型返回技术栈"""
        tech_stacks = {
            "vue3": ["Vue3", "TypeScript", "Vite", "Pinia", "Vue Router"],
            "react": ["React18", "TypeScript", "Next.js", "Redux", "React Router"],
            "fastapi": ["Python", "FastAPI", "SQLAlchemy", "PostgreSQL", "Docker"],
            "flutter": ["Flutter", "Dart", "Firebase", "Provider", "GetX"],
            "node": ["Node.js", "Express", "TypeScript", "MongoDB", "Docker"],
            "html-composition": ["HTML5", "CSS3", "JavaScript", "Vanilla JS", "Web Components"]
        }
        return tech_stacks.get(project_type, ["通用技术栈"])
    
    def get_templates_for_type(self, project_type):
        """根据项目类型返回推荐模板"""
        template_sets = {
            "vue3": ["project-init-template", "requirements-template", "test-plan-template"],
            "react": ["project-init-template", "requirements-template", "test-plan-template"],
            "fastapi": ["project-init-template", "api-spec-template", "database-design-template", "test-plan-template"],
            "flutter": ["project-init-template", "requirements-template", "test-plan-template"],
            "node": ["project-init-template", "api-spec-template", "test-plan-template"],
            "html-composition": ["html-composition-template", "project-init-template", "requirements-template"]
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
    parser = argparse.ArgumentParser(description="Trae AI 模板自动化管理器（集成AI增强版）")
    parser.add_argument("action", choices=["auto", "interactive", "create", "list", "ai-create"], 
                       help="操作类型")
    parser.add_argument("--name", help="项目名称 (用于create)")
    parser.add_argument("--type", choices=["vue3", "react", "fastapi", "flutter", "node"], 
                       help="项目类型 (用于create)")
    parser.add_argument("--template", help="指定模板名称")
    parser.add_argument("--features", help="项目功能需求，用逗号分隔 (用于ai-create)")
    parser.add_argument("--no-ai", action="store_true", 
                       help="禁用AI增强，使用基础模板")
    
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
        manager.create_project_with_templates(args.name, args.type, use_ai_enhance=not args.no_ai)
    elif args.action == "ai-create":
        if not args.name or not args.type or not args.features:
            print("❌ AI创建需要指定 --name, --type 和 --features")
            sys.exit(1)
        features = [f.strip() for f in args.features.split(",") if f.strip()]
        manager.create_project_with_templates(
            args.name, 
            args.type, 
            features=features,
            use_ai_enhance=True
        )
    elif args.action == "list":
        templates = [f.stem for f in manager.templates_path.glob("*.md") 
                    if f.stem != "README"]
        print("📋 可用模板:")
        for template in templates:
            print(f"  - {template}")
    
    print("\n💡 使用提示:")
    print("  python template-manager.py ai-create --name myapp --type vue3 --features '用户认证,数据管理,图表展示'")
    print("  python template-manager.py create --name myapp --type vue3")
    print("  python template-manager.py interactive")

if __name__ == "__main__":
    main()