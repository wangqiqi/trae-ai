#!/usr/bin/env python3
# 🎯 项目助手 - 合并版
# 统一的项目管理和开发助手
# 替代: advanced-toolkit.py + interactive-enhancer.py + universal-quick-checklist.py

import os
import json
import platform
import glob
import subprocess
import sys
import shutil
from pathlib import Path
from datetime import datetime

class ProjectAssistant:
    """
    项目助手
    职责：项目生命周期管理、环境验证、模板应用
    边界：专注于项目相关功能，不涉及系统级优化
    """
    
    def __init__(self):
        self.system = platform.system()
        self.project_root = Path.cwd()
        self.trae_path = self.project_root / ".trae"
        self.user_preferences_file = self.trae_path / "user_preferences.json"
        self.load_user_preferences()
    
    def load_user_preferences(self):
        """加载用户偏好设置"""
        if self.user_preferences_file.exists():
            with open(self.user_preferences_file, 'r', encoding='utf-8') as f:
                self.preferences = json.load(f)
        else:
            self.preferences = {
                "theme": "auto",
                "skill_level": "intermediate",
                "favorite_tools": [],
                "last_project": None,
                "auto_suggestions": True
            }
            self.save_preferences()
    
    def save_preferences(self):
        """保存用户偏好"""
        self.trae_path.mkdir(exist_ok=True)
        with open(self.user_preferences_file, 'w', encoding='utf-8') as f:
            json.dump(self.preferences, f, indent=2, ensure_ascii=False)
    
    def check_project_structure(self):
        """检查项目目录结构完整性"""
        print("📁 检查项目结构...")
        
        standard_structure = {
            "directories": ["src", "tests", "docs", "config", "scripts", ".git"],
            "files": {
                "README.md": "项目说明文档",
                "requirements.txt": "Python依赖列表",
                ".gitignore": "Git忽略文件",
                ".trae-project.json": "Trae项目配置",
                "PRD.md": "产品需求文档"
            }
        }
        
        results = {
            "directories": {"found": [], "missing": []},
            "files": {"found": [], "missing": []},
            "score": 0
        }
        
        # 检查目录
        for dir_name in standard_structure["directories"]:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                results["directories"]["found"].append(dir_name)
            else:
                results["directories"]["missing"].append(dir_name)
        
        # 检查文件
        for filename, description in standard_structure["files"].items():
            file_path = self.project_root / filename
            if file_path.exists():
                results["files"]["found"].append({"name": filename, "desc": description})
            else:
                results["files"]["missing"].append({"name": filename, "desc": description})
        
        # 计算评分
        dir_score = len(results["directories"]["found"]) / len(standard_structure["directories"]) * 50
        file_score = len(results["files"]["found"]) / len(standard_structure["files"]) * 50
        results["score"] = dir_score + file_score
        
        return results
    
    def check_python_environment(self):
        """检查Python开发环境"""
        print("🐍 检查Python环境...")
        
        checks = {
            "python_version": platform.python_version(),
            "pip_available": False,
            "venv_exists": False,
            "requirements_installed": False,
            "git_available": False,
            "git_initialized": False
        }
        
        # 检查pip
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                                  capture_output=True, text=True)
            checks["pip_available"] = result.returncode == 0
        except:
            checks["pip_available"] = False
        
        # 检查虚拟环境
        venv_names = ["venv", ".venv", "env", ".env"]
        for venv_name in venv_names:
            if (self.project_root / venv_name).exists():
                checks["venv_exists"] = True
                break
        
        # 检查requirements.txt
        req_file = self.project_root / "requirements.txt"
        if req_file.exists():
            try:
                with open(req_file) as f:
                    requirements = [line.strip() for line in f 
                                  if line.strip() and not line.startswith("#")]
                
                installed_count = 0
                for req in requirements:
                    try:
                        package_name = req.split("==")[0].split(">=")[0]
                        __import__(package_name)
                        installed_count += 1
                    except ImportError:
                        pass
                
                checks["requirements_installed"] = installed_count == len(requirements)
            except:
                pass
        
        # 检查Git
        try:
            result = subprocess.run(["git", "--version"], 
                                  capture_output=True, text=True)
            checks["git_available"] = result.returncode == 0
            
            if checks["git_available"]:
                result = subprocess.run(["git", "rev-parse", "--git-dir"], 
                                      capture_output=True, text=True, cwd=self.project_root)
                checks["git_initialized"] = result.returncode == 0
        except:
            pass
        
        # 计算环境评分
        score_checks = [
            checks["pip_available"],
            checks["venv_exists"],
            checks["requirements_installed"],
            checks["git_available"],
            checks["git_initialized"]
        ]
        checks["score"] = sum(score_checks) / len(score_checks) * 100
        
        return checks
    
    def check_available_templates(self):
        """检查可用模板"""
        print("📋 检查可用模板...")
        
        template_dir = self.trae_path / "templates"
        if not template_dir.exists():
            return {"count": 0, "templates": []}
        
        templates = list(template_dir.glob("*.md"))
        return {
            "count": len(templates),
            "templates": [t.name for t in templates]
        }
    
    def generate_project_report(self):
        """生成项目状态报告"""
        structure = self.check_project_structure()
        environment = self.check_python_environment()
        templates = self.check_available_templates()
        
        overall_score = (structure["score"] + environment["score"]) / 2
        
        report = f"""
🎯 项目状态报告
{'='*50}
📊 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
📁 项目路径: {self.project_root}
🎯 总体评分: {overall_score:.1f}/100

📁 项目结构:
"""
        
        if structure["directories"]["missing"]:
            report += f"缺失目录: {', '.join(structure['directories']['missing'])}\n"
        if structure["files"]["missing"]:
            missing_files = [f["name"] for f in structure["files"]["missing"]]
            report += f"缺失文件: {', '.join(missing_files)}\n"
        
        report += f"""

🐍 Python环境:
- Python版本: {environment['python_version']}
- pip可用: {'✅' if environment['pip_available'] else '❌'}
- 虚拟环境: {'✅' if environment['venv_exists'] else '❌'}
- 依赖安装: {'✅' if environment['requirements_installed'] else '❌'}
- Git可用: {'✅' if environment['git_available'] else '❌'}
- Git初始化: {'✅' if environment['git_initialized'] else '❌'}

📋 可用模板: {templates['count']}个
{chr(10).join(f"- {t}" for t in templates['templates'])}

"""
        
        # 改进建议
        if overall_score < 80:
            report += "🚀 改进建议:\n"
            if not environment["venv_exists"]:
                report += "- 创建虚拟环境: python -m venv venv\n"
            if structure["files"]["missing"]:
                report += "- 创建缺失的项目文件\n"
            if not environment["requirements_installed"]:
                report += "- 安装依赖: pip install -r requirements.txt\n"
        
        return report
    
    def create_project_scaffold(self, project_name, project_type):
        """创建项目脚手架"""
        print(f"🚀 创建项目脚手架: {project_name} ({project_type})")
        
        project_dir = self.project_root / project_name
        project_dir.mkdir(exist_ok=True)
        
        # 标准目录结构
        directories = {
            "web": ["src", "templates", "static", "tests", "docs", "config"],
            "api": ["src", "tests", "docs", "config", "scripts"],
            "mobile": ["src", "tests", "docs", "assets", "config"],
            "cli": ["src", "tests", "docs", "scripts"]
        }
        
        structure = directories.get(project_type, directories["web"])
        for dir_name in structure:
            (project_dir / dir_name).mkdir(exist_ok=True)
        
        # 创建项目配置文件
        project_config = {
            "project_name": project_name,
            "project_type": project_type,
            "created_at": datetime.now().isoformat(),
            "structure": structure,
            "next_steps": [
                f"cd {project_name}",
                "python -m venv venv",
                "source venv/bin/activate" if self.system != "Windows" else ".\\venv\\Scripts\\activate",
                "pip install -r requirements.txt"
            ]
        }
        
        with open(project_dir / ".trae-project.json", 'w') as f:
            json.dump(project_config, f, indent=2)
        
        # 复制模板文件
        template_dir = self.trae_path / "templates"
        if template_dir.exists():
            for template in template_dir.glob("*.md"):
                if "requirements" in template.name or "deployment" in template.name:
                    shutil.copy2(template, project_dir)
        
        return project_config
    
    def get_personalized_welcome(self):
        """获取个性化欢迎信息"""
        skill_level = self.preferences["skill_level"]
        last_project = self.preferences["last_project"]
        
        messages = {
            "beginner": """
🌱 欢迎回到.trae！
作为新手，让我来引导你：
1. 📊 运行项目状态检查
2. 🚀 创建第一个项目脚手架
3. 📚 查看项目模板
4. ❓ 需要帮助时查看原则速查表
            """,
            "intermediate": """
🚀 欢迎回来！
上次项目: {last_project}
这次推荐：
1. 📊 检查当前项目状态
2. 🎯 创建新项目脚手架
3. 📋 使用项目模板
4. 🔍 优化项目结构
            """,
            "expert": """
🎯 大师级用户！
你的项目: {last_project}
高级功能：
1. 🏗️ 自定义项目脚手架
2. 📊 深度项目分析
3. 🚀 批量模板应用
4. ⚙️ 项目配置优化
            """
        }
        
        return messages[skill_level].format(last_project=last_project or "暂无")
    
    def run_interactive_mode(self):
        """运行交互模式"""
        print(self.get_personalized_welcome())
        
        while True:
            menu = """
🎯 项目助手交互菜单
========================
1. 📊 项目状态检查
2. 🚀 创建新项目
3. 📋 查看可用模板
4. 🏗️ 创建项目脚手架
5. ⚙️ 项目配置管理
6. ❓ 帮助与教程
7. 🚪 退出

请选择 (1-7): """
            
            choice = input(menu).strip()
            
            if choice == "1":
                print(self.generate_project_report())
            elif choice == "2":
                project_name = input("🎯 输入项目名称: ").strip()
                project_type = input("📱 选择项目类型 (web/api/mobile/cli): ").strip()
                config = self.create_project_scaffold(project_name, project_type)
                print(f"✅ 项目 '{project_name}' 创建完成！")
                print("下一步:")
                for step in config["next_steps"]:
                    print(f"  {step}")
            elif choice == "3":
                templates = self.check_available_templates()
                print(f"📋 可用模板 ({templates['count']}个):")
                for template in templates['templates']:
                    print(f"  - {template}")
            elif choice == "4":
                project_name = input("🎯 输入项目名称: ").strip()
                project_type = input("📱 选择项目类型: ").strip()
                self.create_project_scaffold(project_name, project_type)
            elif choice == "5":
                print("⚙️ 项目配置管理开发中...")
            elif choice == "6":
                print("❓ 查看 .trae/principles.md 获取完整帮助")
            elif choice == "7":
                print("👋 再见！")
                break
            else:
                print("❌ 无效选择，请重新输入")

# 使用示例
if __name__ == "__main__":
    assistant = ProjectAssistant()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--report":
            print(assistant.generate_project_report())
        elif sys.argv[1] == "--scaffold" and len(sys.argv) > 3:
            assistant.create_project_scaffold(sys.argv[2], sys.argv[3])
    else:
        assistant.run_interactive_mode()