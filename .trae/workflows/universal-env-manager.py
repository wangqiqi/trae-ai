#!/usr/bin/env python3
"""
通用环境管理器 - 可迁移到任何项目
基于AI环境管理专家知识库
支持：Python/Node.js/Java/Go/任何技术栈
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

class UniversalEnvironmentManager:
    """
    通用环境管理器
    
    特点：
    1. 技术栈无关 - 支持任何语言和框架
    2. 配置驱动 - 通过JSON配置适配不同项目
    3. 插件化架构 - 易于扩展新功能
    4. 零依赖迁移 - 复制文件即可使用
    """
    
    def __init__(self, project_root: Optional[str] = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.config_file = self.project_root / "env-config.json"
        self.logs_dir = self.project_root / "logs"
        self.backups_dir = self.project_root / "backups"
        
        # 确保必要的目录存在
        self.logs_dir.mkdir(exist_ok=True)
        self.backups_dir.mkdir(exist_ok=True)
        
        # 加载配置
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载或创建环境配置"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 创建默认配置模板
            default_config = {
                "project_name": self.project_root.name,
                "tech_stack": "auto-detect",  # auto/python/node/java/go/rust
                "environments": {
                    "development": {"port": 3000, "debug": True},
                    "staging": {"port": 3001, "debug": False},
                    "production": {"port": 80, "debug": False}
                },
                "dependencies": {
                    "package_manager": "auto-detect",
                    "install_command": "auto-detect",
                    "requirements_file": "auto-detect"
                },
                "docker": {
                    "enabled": False,
                    "compose_file": "docker-compose.yml"
                },
                "scripts": {
                    "start": "auto-detect",
                    "test": "auto-detect",
                    "build": "auto-detect"
                }
            }
            
            # 自动检测技术栈
            detected = self.detect_tech_stack()
            default_config.update(detected)
            
            # 保存配置
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config: Dict[str, Any]):
        """保存配置到文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def detect_tech_stack(self) -> Dict[str, Any]:
        """自动检测项目技术栈"""
        detected = {
            "tech_stack": "unknown",
            "dependencies": {},
            "scripts": {}
        }
        
        # 检测文件特征
        files = list(self.project_root.glob("*"))
        file_names = [f.name.lower() for f in files]
        
        # Python项目检测
        if "requirements.txt" in file_names or "pyproject.toml" in file_names:
            detected.update({
                "tech_stack": "python",
                "dependencies": {
                    "package_manager": "pip",
                    "install_command": "pip install -r requirements.txt",
                    "requirements_file": "requirements.txt"
                },
                "scripts": {
                    "start": "python main.py",
                    "test": "python -m pytest",
                    "build": "python setup.py build"
                },
                "docker": {
                    "enabled": True,
                    "compose_file": "docker-compose.yml",
                    "dockerfile": "Dockerfile"
                }
            })
        
        # Node.js项目检测
        elif "package.json" in file_names:
            detected.update({
                "tech_stack": "node",
                "dependencies": {
                    "package_manager": "npm",
                    "install_command": "npm install",
                    "requirements_file": "package.json"
                },
                "scripts": {
                    "start": "npm start",
                    "test": "npm test",
                    "build": "npm run build"
                },
                "docker": {
                    "enabled": True,
                    "compose_file": "docker-compose.yml",
                    "dockerfile": "Dockerfile"
                }
            })
        
        # Java项目检测
        elif any(f.suffix == ".java" for f in files) or "pom.xml" in file_names:
            detected.update({
                "tech_stack": "java",
                "dependencies": {
                    "package_manager": "maven",
                    "install_command": "mvn install",
                    "requirements_file": "pom.xml"
                },
                "scripts": {
                    "start": "mvn spring-boot:run",
                    "test": "mvn test",
                    "build": "mvn package"
                }
            })
        
        # Go项目检测
        elif "go.mod" in file_names:
            detected.update({
                "tech_stack": "go",
                "dependencies": {
                    "package_manager": "go mod",
                    "install_command": "go mod download",
                    "requirements_file": "go.mod"
                },
                "scripts": {
                    "start": "go run main.go",
                    "test": "go test ./...",
                    "build": "go build -o app"
                }
            })
        
        return detected
    
    def universal_check(self) -> Dict[str, Any]:
        """通用环境检查"""
        print(f"🔍 正在检查 {self.config['tech_stack']} 项目环境...")
        
        checks = {}
        
        # 基础工具检查
        base_tools = {
            "git": "git --version",
            "curl": "curl --version",
            "docker": "docker --version"
        }
        
        for tool, command in base_tools.items():
            try:
                result = subprocess.run(command, shell=True, 
                                      capture_output=True, text=True)
                checks[tool] = {
                    "installed": result.returncode == 0,
                    "version": result.stdout.split('\n')[0] if result.returncode == 0 else "未安装"
                }
            except Exception as e:
                checks[tool] = {"installed": False, "error": str(e)}
        
        # 技术栈特定检查
        if self.config["tech_stack"] == "python":
            checks.update(self.check_python())
        elif self.config["tech_stack"] == "node":
            checks.update(self.check_node())
        elif self.config["tech_stack"] == "java":
            checks.update(self.check_java())
        
        return checks
    
    def check_python(self) -> Dict[str, Any]:
        """Python环境检查"""
        checks = {}
        
        # Python版本
        try:
            result = subprocess.run("python --version", shell=True, 
                                  capture_output=True, text=True)
            checks["python"] = {
                "installed": True,
                "version": result.stdout.strip()
            }
        except:
            checks["python"] = {"installed": False}
        
        # pip
        try:
            subprocess.run("pip --version", shell=True, check=True)
            checks["pip"] = {"installed": True}
        except:
            checks["pip"] = {"installed": False}
        
        return checks
    
    def check_node(self) -> Dict[str, Any]:
        """Node.js环境检查"""
        checks = {}
        
        # Node版本
        try:
            result = subprocess.run("node --version", shell=True, 
                                  capture_output=True, text=True)
            checks["node"] = {
                "installed": True,
                "version": result.stdout.strip()
            }
        except:
            checks["node"] = {"installed": False}
        
        # npm
        try:
            subprocess.run("npm --version", shell=True, check=True)
            checks["npm"] = {"installed": True}
        except:
            checks["npm"] = {"installed": False}
        
        return checks
    
    def check_java(self) -> Dict[str, Any]:
        """Java环境检查"""
        checks = {}
        
        # Java版本
        try:
            result = subprocess.run("java -version", shell=True, 
                                  capture_output=True, text=True)
            checks["java"] = {
                "installed": True,
                "version": result.stderr.split('\n')[0] if result.stderr else "未知"
            }
        except:
            checks["java"] = {"installed": False}
        
        return checks
    
    def create_environment_template(self, tech_stack: str = None) -> bool:
        """创建环境模板"""
        tech = tech_stack or self.config["tech_stack"]
        
        templates = {
            "python": {
                "requirements.txt": "fastapi==0.104.1\nuvicorn[standard]==0.24.0\npython-dotenv==1.0.0",
                "main.py": '''from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)''',
                "Dockerfile": '''FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]''',
                "docker-compose.yml": '''version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=development'''
            },
            "node": {
                "package.json": '''{
  "name": "myapp",
  "version": "1.0.0",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js"
  },
  "dependencies": {
    "express": "^4.18.0"
  },
  "devDependencies": {
    "nodemon": "^3.0.0"
  }
}''',
                "index.js": '''const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.json({ message: 'Hello World' });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});''',
                "Dockerfile": '''FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]''',
                "docker-compose.yml": '''version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development'''
            }
        }
        
        if tech in templates:
            for filename, content in templates[tech].items():
                file_path = self.project_root / filename
                if not file_path.exists():
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ 创建: {filename}")
            return True
        
        return False
    
    def migrate_project(self, source_path: str, target_path: str) -> bool:
        """项目迁移功能"""
        try:
            source = Path(source_path)
            target = Path(target_path)
            
            if not source.exists():
                print(f"❌ 源路径不存在: {source}")
                return False
            
            # 复制环境管理器
            manager_file = source / "universal-env-manager.py"
            if manager_file.exists():
                import shutil
                shutil.copy2(manager_file, target / "universal-env-manager.py")
            
            # 复制配置文件模板
            config_file = source / "env-config.json"
            if config_file.exists():
                shutil.copy2(config_file, target / "env-config.json")
            
            print(f"✅ 环境管理器已迁移到: {target}")
            return True
            
        except Exception as e:
            print(f"❌ 迁移失败: {e}")
            return False
    
    def show_help(self):
        """显示帮助信息"""
        print("""
🎯 通用环境管理器 - 零依赖迁移版

使用方法:
    python universal-env-manager.py check                    # 环境检查
    python universal-env-manager.py init [tech_stack]        # 初始化项目
    python universal-env-manager.py template [python|node|java] # 创建模板
    python universal-env-manager.py migrate [source] [target]  # 项目迁移

技术栈支持:
    python  - FastAPI/Django/Flask
    node    - Express/Vue/React
    java    - Spring Boot
    go      - Gin/Echo
    rust    - Actix/Rocket

特点:
    ✅ 零依赖 - 复制即可使用
    ✅ 自动检测 - 智能识别技术栈
    ✅ 通用配置 - JSON驱动适配
    ✅ 一键迁移 - 项目间无缝转移
    ✅ 插件架构 - 易于扩展

示例:
    python universal-env-manager.py check
    python universal-env-manager.py init python
    python universal-env-manager.py template node
    python universal-env-manager.py migrate ./project1 ./project2
        """)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        UniversalEnvironmentManager().show_help()
        return
    
    manager = UniversalEnvironmentManager()
    command = sys.argv[1]
    
    if command == "check":
        results = manager.universal_check()
        print("\n📊 环境检查结果:")
        for tool, info in results.items():
            status = "✅" if info.get("installed") else "❌"
            print(f"{status} {tool}: {info.get('version', '未安装')}")
    
    elif command == "init":
        tech_stack = sys.argv[2] if len(sys.argv) > 2 else None
        if tech_stack:
            manager.config["tech_stack"] = tech_stack
            manager.save_config(manager.config)
        print(f"✅ 项目已初始化为 {manager.config['tech_stack']} 技术栈")
    
    elif command == "template":
        tech_stack = sys.argv[2] if len(sys.argv) > 2 else manager.config["tech_stack"]
        if manager.create_environment_template(tech_stack):
            print(f"✅ {tech_stack} 环境模板已创建")
        else:
            print(f"❌ 不支持 {tech_stack} 技术栈")
    
    elif command == "migrate" and len(sys.argv) >= 4:
        source = sys.argv[2]
        target = sys.argv[3]
        manager.migrate_project(source, target)
    
    else:
        manager.show_help()

if __name__ == "__main__":
    main()