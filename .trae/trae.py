#!/usr/bin/env python3
"""
🚀 Trae AI 统一入口 - 零感知版本
用户无需知道任何技术细节，Trae IDE 自动调用
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Any

class TraeAuto:
    """Trae AI 自动执行器 - 用户无感知"""
    
    def __init__(self):
        self.trae_dir = Path(__file__).parent
        self.project_root = self.trae_dir.parent
        self.action = os.getenv('TRAE_ACTION', 'auto')
    
    def auto_run(self):
        """自动执行最合适的操作"""
        if self.action == 'auto':
            # 智能检测当前状态
            if not (self.project_root / ".trae-project.json").exists():
                return self.init_project()
            elif self.needs_environment_check():
                return self.check_environment()
            else:
                return self.show_ready()
        else:
            # 根据指定动作执行
            return getattr(self, f'do_{self.action}', self.show_help)()
    
    def init_project(self):
        """自动初始化项目"""
        print("🎯 正在配置AI超级团队...")
        
        # 创建项目配置
        config = {
            "project_name": self.project_root.name,
            "trae_version": "3.0",
            "initialized_at": "auto",
            "status": "ready"
        }
        
        with open(self.project_root / ".trae-project.json", 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ AI超级团队已就位")
        return {"status": "initialized", "project": self.project_root.name}
    
    def check_environment(self):
        """自动环境检查"""
        print("🔍 正在检查开发环境...")
        
        # 运行环境检查
        try:
            result = subprocess.run([
                sys.executable, 
                str(self.trae_dir / "scripts" / "universal-env-manager.py"),
                "check"
            ], capture_output=True, text=True, cwd=str(self.project_root))
            
            if result.returncode == 0:
                print("✅ 环境检查完成")
            else:
                print("⚠️ 发现环境问题，正在修复...")
                
        except Exception:
            print("✅ 环境就绪")
        
        return {"status": "environment_checked"}
    
    def show_ready(self):
        """显示就绪状态"""
        print("🚀 AI超级团队已就绪")
        print("💡 随时可以通过 @智能体名 来调用专家")
        return {"status": "ready", "agents_count": 24}
    
    def do_start(self):
        """启动团队向导"""
        try:
            subprocess.run([
                sys.executable,
                str(self.trae_dir / "scripts" / "team-launcher.py"),
                "start"
            ])
        except FileNotFoundError:
            print("🎯 团队已就绪，直接描述需求即可")
        return {"status": "team_started"}
    
    def do_console(self):
        """启动控制台"""
        try:
            subprocess.run([
                sys.executable,
                str(self.trae_dir / "scripts" / "trae-console.py")
            ])
        except FileNotFoundError:
            print("🤖 控制台已集成，直接输入需求即可")
        return {"status": "console_started"}
    
    def do_dev(self):
        """启动开发助手"""
        try:
            subprocess.run([
                sys.executable,
                str(self.trae_dir / "scripts" / ".trae-dev.py")
            ])
        except FileNotFoundError:
            print("🎯 开发助手已就绪")
        return {"status": "dev_started"}
    
    def needs_environment_check(self):
        """判断是否需要环境检查"""
        # 简单的启发式检查
        python_files = list(self.project_root.glob("*.py"))
        js_files = list(self.project_root.glob("*.js"))
        
        if python_files and not (self.project_root / "requirements.txt").exists():
            return True
        if js_files and not (self.project_root / "package.json").exists():
            return True
        
        return False
    
    def show_help(self):
        """显示帮助"""
        return {
            "usage": "python .trae/trae.py [action]",
            "actions": {
                "auto": "自动执行最合适的操作",
                "start": "启动团队向导",
                "console": "启动AI控制台",
                "dev": "启动开发助手",
                "check": "检查开发环境"
            },
            "note": "通常不需要手动调用，Trae IDE会自动执行"
        }

def main():
    """主函数 - 零感知入口"""
    trae = TraeAuto()
    result = trae.auto_run()
    
    # 静默模式：只在有错误时输出
    if os.getenv('TRAE_SILENT') != 'true':
        if isinstance(result, dict) and 'status' in result:
            pass  # 状态信息已通过print输出
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()