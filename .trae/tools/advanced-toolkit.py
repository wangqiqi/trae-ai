#!/usr/bin/env python3
# 🔧 .trae 高级工具包 - 功能深度增强
# 集成所有高级功能，提供一站式开发体验

import os
import json
import subprocess
import platform
from datetime import datetime
from pathlib import Path

class AdvancedToolkit:
    def __init__(self):
        self.system = platform.system()
        self.base_dir = Path(".trae")
        self.config_file = self.base_dir / "advanced_config.json"
        self.load_config()
    
    def load_config(self):
        """加载高级配置"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "auto_backup": True,
                "performance_alerts": True,
                "cross_platform": True,
                "development_mode": False,
                "last_optimization": str(datetime.now())
            }
            self.save_config()
    
    def save_config(self):
        """保存配置"""
        self.config_file.parent.mkdir(exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def run_system_health_check(self):
        """运行系统健康检查"""
        print("🔍 运行系统健康检查...")
        
        checks = []
        
        # 检查工具完整性
        tools_dir = self.base_dir / "tools"
        required_tools = [
            "cross-platform-adapter.py",
            "performance-monitor.py",
            "windows-enhancer.ps1",
            "interactive-enhancer.py",
            "smart-cleanup.py"
        ]
        
        for tool in required_tools:
            tool_path = tools_dir / tool
            if tool_path.exists():
                checks.append(f"✅ {tool} - 已就绪")
            else:
                checks.append(f"❌ {tool} - 缺失")
        
        # 检查模板完整性
        templates_dir = self.base_dir / "templates"
        required_templates = [
            "requirements-template.md",
            "tech-choice-template.md",
            "code-review-template.md",
            "deployment-template.md"
        ]
        
        for template in required_templates:
            template_path = templates_dir / template
            if template_path.exists():
                checks.append(f"✅ {template} - 已就绪")
            else:
                checks.append(f"❌ {template} - 缺失")
        
        return checks
    
    def create_project_scaffold(self, project_name, project_type="web"):
        """创建项目脚手架"""
        print(f"🏗️ 创建 {project_name} 项目脚手架...")
        
        project_dir = Path(project_name)
        project_dir.mkdir(exist_ok=True)
        
        # 创建标准目录结构
        directories = [
            "src",
            "tests",
            "docs",
            "config",
            "scripts",
            "assets"
        ]
        
        for directory in directories:
            (project_dir / directory).mkdir(exist_ok=True)
        
        # 复制模板文件
        templates_dir = self.base_dir / "templates"
        for template in ["requirements-template.md", "deployment-template.md"]:
            src = templates_dir / template
            dst = project_dir / "docs" / template
            if src.exists():
                dst.write_text(src.read_text(encoding='utf-8'), encoding='utf-8')
        
        # 创建项目配置文件
        project_config = {
            "name": project_name,
            "type": project_type,
            "created": str(datetime.now()),
            "tools": {
                "cross_platform": True,
                "performance_monitor": True,
                "auto_backup": True
            }
        }
        
        config_path = project_dir / ".trae-project.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(project_config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 项目脚手架创建完成: {project_dir}")
        return project_dir
    
    def run_performance_benchmark(self):
        """运行性能基准测试"""
        print("⚡ 运行性能基准测试...")
        
        # 测试工具启动时间
        tools = [
            ("cross-platform-adapter", "python .trae/tools/cross-platform-adapter.py --version"),
            ("performance-monitor", "python .trae/tools/performance-monitor.py --quick"),
            ("smart-cleanup", "python .trae/tools/smart-cleanup.py --check")
        ]
        
        results = []
        for tool_name, command in tools:
            try:
                start = datetime.now()
                subprocess.run(command, shell=True, capture_output=True, text=True)
                duration = (datetime.now() - start).total_seconds()
                results.append(f"{tool_name}: {duration:.2f}s")
            except Exception as e:
                results.append(f"{tool_name}: 错误 - {e}")
        
        return results
    
    def generate_optimization_report(self):
        """生成优化报告"""
        print("📊 生成优化报告...")
        
        report = {
            "timestamp": str(datetime.now()),
            "system": self.system,
            "health_check": self.run_system_health_check(),
            "performance": self.run_performance_benchmark(),
            "recommendations": [
                "定期运行系统健康检查",
                "使用性能监控工具优化",
                "保持模板和工具更新",
                "利用跨平台适配器确保兼容性"
            ]
        }
        
        report_path = self.base_dir / "reports" / f"optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report
    
    def show_toolkit_menu(self):
        """显示工具包菜单"""
        menu = """
🔧 .trae 高级工具包
========================
1. 🏗️ 创建项目脚手架
2. 🔍 系统健康检查
3. ⚡ 性能基准测试
4. 📊 生成优化报告
5. 🎯 一键项目启动
6. 🔄 系统全面优化
7. ❓ 帮助信息

请输入选择 (1-7): """
        
        print(menu)
        return input().strip()
    
    def run_toolkit(self):
        """运行工具包"""
        print("🚀 启动.trae高级工具包...")
        
        while True:
            choice = self.show_toolkit_menu()
            
            if choice == "1":
                name = input("🎯 输入项目名称: ").strip()
                ptype = input("📱 项目类型 (web/mobile/api): ").strip() or "web"
                self.create_project_scaffold(name, ptype)
            
            elif choice == "2":
                health = self.run_system_health_check()
                for check in health:
                    print(f"  {check}")
            
            elif choice == "3":
                perf = self.run_performance_benchmark()
                for result in perf:
                    print(f"  {result}")
            
            elif choice == "4":
                report = self.generate_optimization_report()
                print(f"📊 报告已生成: {report['timestamp']}")
            
            elif choice == "5":
                print("🎯 一键项目启动功能开发中...")
            
            elif choice == "6":
                print("🔄 运行系统全面优化...")
                os.system("python .trae/tools/performance-monitor.py")
                if self.system == "Windows":
                    os.system("powershell -ExecutionPolicy Bypass -File .trae/tools/windows-enhancer.ps1")
            
            elif choice == "7":
                print("❓ 查看 .trae/principles-v2.md 获取详细帮助")
                break
            
            else:
                print("❌ 无效选择")
            
            cont = input("\n继续操作? (y/n): ").strip().lower()
            if cont != 'y':
                break

# 使用示例
if __name__ == "__main__":
    toolkit = AdvancedToolkit()
    toolkit.run_toolkit()