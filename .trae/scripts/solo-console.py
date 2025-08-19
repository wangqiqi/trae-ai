#!/usr/bin/env python3
"""
SOLO智能开发控制台启动器
一键启动完整的SOLO开发环境
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path
import argparse

class SOLOConsole:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent.parent
        self.scripts_dir = Path(__file__).parent
        self.data_dir = self.scripts_dir.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        
    def print_banner(self):
        """打印启动横幅"""
        banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🚀 SOLO智能开发控制台 v2.0                                ║
║   智能项目开发 & 风险监控 & Web管理界面                        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def check_dependencies(self):
        """检查依赖"""
        required_packages = [
            "fastapi", "uvicorn", "python-multipart", "aiofiles"
        ]
        
        print("📦 检查依赖...")
        for package in required_packages:
            try:
                __import__(package)
                print(f"✅ {package}")
            except ImportError:
                print(f"❌ 缺少依赖: {package}")
                print("正在安装...")
                subprocess.run([sys.executable, "-m", "pip", "install", package])
    
    def start_api_server(self):
        """启动API服务器"""
        print("🔧 启动API服务器...")
        cmd = [
            sys.executable, 
            str(self.scripts_dir / "solo-api-server.py")
        ]
        
        # 使用subprocess.Popen启动服务器
        process = subprocess.Popen(
            cmd,
            cwd=str(self.root_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("⏳ 等待服务器启动...")
        time.sleep(3)
        
        # 检查服务器是否成功启动
        if process.poll() is None:
            print("✅ API服务器启动成功")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ API服务器启动失败: {stderr}")
            return None
    
    def start_web_dashboard(self):
        """启动Web管理界面"""
        print("🌐 启动Web管理界面...")
        dashboard_url = "http://localhost:8000"
        
        try:
            webbrowser.open(dashboard_url)
            print(f"✅ 管理界面已打开: {dashboard_url}")
            return True
        except Exception as e:
            print(f"⚠️  无法自动打开浏览器: {e}")
            print(f"请手动访问: {dashboard_url}")
            return False
    
    def setup_demo_data(self):
        """设置演示数据"""
        print("📊 设置演示数据...")
        
        # 创建演示项目
        demo_projects = [
            {
                "id": "demo_todo_2024",
                "name": "智能Todo应用",
                "description": "基于Vue3和FastAPI的现代化Todo应用",
                "type": "web_application",
                "status": "completed",
                "tech_stack": {"frontend": "vue", "backend": "fastapi", "database": "sqlite"},
                "timeline": "1-2周",
                "created_at": "2024-01-15T10:00:00",
                "risk_score": 25,
                "risk_level": "低风险"
            },
            {
                "id": "demo_ai_2024",
                "name": "AI图像识别系统",
                "description": "支持1000类物体识别的AI系统",
                "type": "ai_system",
                "status": "active",
                "tech_stack": {"frontend": "vue", "backend": "fastapi", "ai": "tensorflow"},
                "timeline": "6-8周",
                "created_at": "2024-01-20T14:30:00",
                "risk_score": 65,
                "risk_level": "中风险"
            }
        ]
        
        # 保存演示项目
        projects_file = self.data_dir / "projects.json"
        with open(projects_file, 'w', encoding='utf-8') as f:
            import json
            json.dump(demo_projects, f, ensure_ascii=False, indent=2)
        
        print("✅ 演示数据已设置")
    
    def show_quick_commands(self):
        """显示快速命令"""
        print("\n🎯 快速命令:")
        print("  python .trae/scripts/solo-console.py --help    显示帮助")
        print("  python .trae/scripts/solo-console.py start     启动完整环境")
        print("  python .trae/scripts/solo-console.py api       仅启动API")
        print("  python .trae/scripts/solo-console.py demo       设置演示数据")
    
    def run_interactive_mode(self):
        """运行交互模式"""
        self.print_banner()
        
        while True:
            print("\n" + "="*50)
            print("选择操作:")
            print("1. 启动完整SOLO环境")
            print("2. 仅启动API服务器")
            print("3. 设置演示数据")
            print("4. 显示帮助")
            print("5. 退出")
            
            choice = input("\n请输入选项 (1-5): ").strip()
            
            if choice == "1":
                self.start_full_environment()
                break
            elif choice == "2":
                self.start_api_only()
                break
            elif choice == "3":
                self.setup_demo_data()
            elif choice == "4":
                self.show_quick_commands()
            elif choice == "5":
                print("👋 再见！")
                break
            else:
                print("❌ 无效选项，请重试")
    
    def start_full_environment(self):
        """启动完整环境"""
        print("🚀 启动完整SOLO环境...")
        
        # 检查依赖
        self.check_dependencies()
        
        # 设置演示数据
        self.setup_demo_data()
        
        # 启动API服务器
        api_process = self.start_api_server()
        if api_process:
            # 启动Web界面
            self.start_web_dashboard()
            
            print("\n" + "="*50)
            print("🎉 SOLO环境启动成功！")
            print("📊 管理界面: http://localhost:8000")
            print("🔧 API文档: http://localhost:8000/docs")
            print("\n💡 按 Ctrl+C 停止服务")
            
            try:
                api_process.wait()
            except KeyboardInterrupt:
                print("\n🛑 正在停止服务...")
                api_process.terminate()
                api_process.wait()
                print("✅ 服务已停止")
        else:
            print("❌ 启动失败，请检查错误信息")
    
    def start_api_only(self):
        """仅启动API服务器"""
        print("🔧 仅启动API服务器...")
        self.start_api_server()
        
        print("\n" + "="*50)
        print("📊 API服务器启动成功！")
        print("🔧 API文档: http://localhost:8000/docs")
        print("\n💡 按 Ctrl+C 停止服务")
    
    def main(self):
        """主函数"""
        parser = argparse.ArgumentParser(description="SOLO智能开发控制台")
        parser.add_argument("command", nargs="?", choices=["start", "api", "demo", "help"])
        parser.add_argument("-i", "--interactive", action="store_true", help="交互模式")
        
        args = parser.parse_args()
        
        if args.interactive or not args.command:
            self.run_interactive_mode()
        elif args.command == "start":
            self.start_full_environment()
        elif args.command == "api":
            self.start_api_only()
        elif args.command == "demo":
            self.setup_demo_data()
        elif args.command == "help":
            self.show_quick_commands()

if __name__ == "__main__":
    console = SOLOConsole()
    console.main()