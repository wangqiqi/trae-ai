#!/usr/bin/env python3
"""
自动环境管理AI工程师
基于实测经验优化：主动检测、自动修复、零交互
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class AutoEnvironmentManager:
    def __init__(self):
        self.project_root = Path.cwd()
        self.env_config = {}
        self.issues_found = []
        self.auto_fixes = []
        
    def detect_project_type(self):
        """智能检测项目类型"""
        indicators = {
            'vue': ['package.json', 'vite.config.ts', 'vue'],
            'react': ['package.json', 'react', 'next.config.js'],
            'fastapi': ['requirements.txt', 'main.py', 'fastapi'],
            'django': ['manage.py', 'requirements.txt', 'django'],
            'node': ['package.json', 'node_modules'],
            'python': ['requirements.txt', 'main.py']
        }
        
        detected = []
        for project_type, files in indicators.items():
            matches = sum(1 for f in files if any(Path(self.project_root).rglob(f"*{f}*")))
            if matches >= 2:
                detected.append(project_type)
        
        return detected[0] if detected else 'generic'
    
    def auto_check_environment(self):
        """主动环境检查，无需用户确认"""
        print("🤖 环境管理AI工程师启动...")
        
        # Python环境检查
        self.check_python()
        
        # Node.js环境检查
        self.check_node()
        
        # 项目依赖检查
        self.check_dependencies()
        
        # 配置文件检查
        self.check_configs()
        
        # 自动修复
        self.auto_fix_issues()
        
        return {
            'status': 'completed',
            'issues': self.issues_found,
            'fixes': self.auto_fixes,
            'recommendations': self.get_recommendations()
        }
    
    def check_python(self):
        """Python环境检查"""
        try:
            result = subprocess.run([sys.executable, '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ Python环境: {version}")
            else:
                self.issues_found.append("Python环境异常")
        except Exception as e:
            self.issues_found.append(f"Python检查失败: {e}")
    
    def check_node(self):
        """Node.js环境检查"""
        try:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ Node.js环境: {version}")
            else:
                self.issues_found.append("Node.js环境异常")
        except:
            self.issues_found.append("Node.js未安装或不在PATH中")
    
    def check_dependencies(self):
        """依赖检查"""
        # 检查Python依赖
        if (self.project_root / "requirements.txt").exists():
            self.check_python_deps()
        
        # 检查Node依赖
        if (self.project_root / "package.json").exists():
            self.check_node_deps()
    
    def check_python_deps(self):
        """Python依赖检查"""
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '--dry-run'],
                          capture_output=True, check=True)
            print("✅ Python依赖检查通过")
        except:
            self.issues_found.append("Python依赖需要安装")
            self.auto_fixes.append("pip install -r requirements.txt")
    
    def check_node_deps(self):
        """Node依赖检查"""
        if not (self.project_root / "node_modules").exists():
            self.issues_found.append("Node依赖未安装")
            self.auto_fixes.append("npm install")
    
    def check_configs(self):
        """配置文件检查"""
        configs = [
            'tsconfig.json',
            'vite.config.ts',
            'package.json',
            'requirements.txt'
        ]
        
        for config in configs:
            config_path = self.project_root / config
            if config_path.exists():
                try:
                    with open(config_path) as f:
                        json.load(f) if config.endswith('.json') else f.read()
                    print(f"✅ {config} 配置有效")
                except:
                    self.issues_found.append(f"{config} 配置错误")
    
    def auto_fix_issues(self):
        """自动修复发现的问题"""
        for fix in self.auto_fixes:
            if "pip install" in fix:
                print("🔄 自动安装Python依赖...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            elif "npm install" in fix:
                print("🔄 自动安装Node依赖...")
                subprocess.run(['npm', 'install'])
    
    def get_recommendations(self):
        """基于检查结果给出建议"""
        project_type = self.detect_project_type()
        return {
            'project_type': project_type,
            'next_steps': [
                f"项目类型识别: {project_type}",
                "运行测试验证代码完整性",
                "启动开发服务器"
            ]
        }

if __name__ == "__main__":
    manager = AutoEnvironmentManager()
    result = manager.auto_check_environment()
    print(json.dumps(result, indent=2, ensure_ascii=False))