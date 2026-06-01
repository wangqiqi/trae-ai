#!/usr/bin/env python3
"""
项目脚手架生成技能
快速生成常用项目的基础结构
"""

import os
from pathlib import Path
from typing import Dict, Any


def execute(**kwargs) -> Dict[str, Any]:
    """
    执行项目脚手架生成
    
    Args:
        project_type: 项目类型 (vue/react/fastapi/flutter/node
        project_name: 项目名称
        output_dir: 输出目录
        
    Returns:
        执行结果
    """
    project_type = kwargs.get("project_type", "vue")
    project_name = kwargs.get("project_name", "my-project")
    output_dir = Path(kwargs.get("output_dir", "."))
    
    project_path = output_dir / project_name
    
    if project_path.exists():
        return {
            "success": False,
            "message": f"项目目录已存在: {project_path}"
        }
    
    # 创建项目目录
    project_path.mkdir(parents=True)
    
    # 根据项目类型配置
    project_configs = {
        "vue": _generate_vue_project,
        "react": _generate_react_project, 
        "fastapi": _generate_fastapi_project,
        "node": _generate_node_project,
    }
    
    generator = project_configs.get(project_type, _generate_default_project)
    generator(project_path, project_name)
    
    return {
        "success": True,
        "message": f"{project_type} 项目脚手架已生成: {project_path}",
        "path": str(project_path)
    }


def _generate_vue_project(path: Path, name: str):
    """生成Vue项目结构"""
    (path / "src").mkdir()
    (path / "public").mkdir()
    (path / "tests").mkdir()
    
    with open(path / "package.json", "w", encoding="utf-8") as f:
        f.write('''{
  "name": "%s",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}''' % name)
    
    with open(path / "README.md", "w", encoding="utf-8") as f:
        f.write(f"# {name}\n\nVue 项目")


def _generate_react_project(path: Path, name: str):
    """生成React项目结构"""
    (path / "src").mkdir()
    (path / "public").mkdir()
    
    with open(path / "package.json", "w", encoding="utf-8") as f:
        f.write('''{
  "name": "%s",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  }
}''' % name)


def _generate_fastapi_project(path: Path, name: str):
    """生成FastAPI项目结构"""
    (path / "app").mkdir()
    (path / "tests").mkdir()
    
    with open(path / "requirements.txt", "w", encoding="utf-8") as f:
        f.write("fastapi>=0.104.0\nuvicorn>=0.24.0\n")
    
    with open(path / "main.py", "w", encoding="utf-8") as f:
        f.write('''from fastapi import FastAPI

app = FastAPI(title="%s")

@app.get("/")
async def root():
    return {"message": "Hello World"}
''' % name)


def _generate_node_project(path: Path, name: str):
    """生成Node.js项目结构"""
    (path / "src").mkdir()
    (path / "tests").mkdir()
    
    with open(path / "package.json", "w", encoding="utf-8") as f:
        f.write('''{
  "name": "%s",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "start": "node src/index.js"
  }
}''' % name)


def _generate_default_project(path: Path, name: str):
    """生成默认项目结构"""
    (path / "src").mkdir()
    with open(path / "README.md", "w", encoding="utf-8") as f:
        f.write(f"# {name}\n\n项目")


if __name__ == "__main__":
    # 独立运行测试
    import sys
    result = execute(
        project_type=sys.argv[1] if len(sys.argv) > 1 else "vue",
        project_name=sys.argv[2] if len(sys.argv) > 2 else "test-project"
    )
    print(result)
