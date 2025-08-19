#!/usr/bin/env python3
"""
SOLO智能开发控制台快速启动脚本
一键启动整个系统，包括API服务器和Web界面
"""

import os
import sys
import time
import webbrowser
import subprocess
from pathlib import Path

def check_dependencies():
    """检查必要的依赖"""
    try:
        import fastapi
        import uvicorn
        print("✅ 依赖检查通过")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("正在安装依赖...")
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "python-multipart"])
        return True

def setup_data_directory():
    """设置数据目录"""
    data_dir = Path(".trae/data")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建示例数据文件
    projects_file = data_dir / "projects.json"
    if not projects_file.exists():
        projects_file.write_text('[]', encoding='utf-8')
    
    risks_file = data_dir / "risks.json"
    if not risks_file.exists():
        risks_file.write_text('[]', encoding='utf-8')
    
    print("✅ 数据目录设置完成")

def start_api_server():
    """启动API服务器"""
    print("🚀 正在启动API服务器...")
    
    # 设置Python路径
    script_dir = Path(".trae/scripts").absolute()
    sys.path.insert(0, str(script_dir))
    
    try:
        from solo_api_server import SOLOAPIServer
        server = SOLOAPIServer()
        
        import uvicorn
        print("✅ API服务器启动成功！")
        print("📱 Web界面: http://localhost:8000")
        
        # 打开浏览器
        webbrowser.open("http://localhost:8000")
        
        # 启动服务器
        uvicorn.run(
            server.app,
            host="0.0.0.0",
            port=8000,
            reload=False
        )
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("尝试简化启动...")
        
        # 简化启动
        os.chdir(str(Path(__file__).parent))
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "solo_api_server:SOLOAPIServer.app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload", "False"
        ], cwd=".trae/scripts")

def main():
    """主函数"""
    print("🎯 SOLO智能开发控制台 v2.0")
    print("=" * 50)
    
    # 检查依赖
    check_dependencies()
    
    # 设置数据目录
    setup_data_directory()
    
    # 启动服务器
    start_api_server()

if __name__ == "__main__":
    main()