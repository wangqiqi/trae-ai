#!/usr/bin/env python3
"""
环境检测技能 - 自动检测项目技术栈和环境
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, List

def execute(**kwargs) -> Dict[str, Any]:
    """
    检测项目环境
    
    Args:
        target_path: 检测目录（默认当前目录）
        deep_scan: 深度扫描（yes/no）
    
    Returns:
        检测结果
    """
    target_path = kwargs.get('target_path', '.')
    deep_scan = kwargs.get('deep_scan', 'no').lower() == 'yes'
    
    try:
        project_path = Path(target_path)
        
        # 基础检测
        results = {
            'success': True,
            'project_type': None,
            'tech_stack': [],
            'recommended_skills': [],
            'missing_dependencies': [],
            'suggestions': []
        }
        
        # 1. 检测项目类型
        results['project_type'] = detect_project_type(project_path)
        
        # 2. 检测技术栈
        results['tech_stack'] = detect_tech_stack(project_path)
        
        # 3. 推荐技能
        results['recommended_skills'] = recommend_skills(results['project_type'], results['tech_stack'])
        
        # 4. 检测缺失的依赖
        results['missing_dependencies'] = check_dependencies(project_path)
        
        # 5. 生成建议
        results['suggestions'] = generate_suggestions(results)
        
        return results
        
    except Exception as e:
        return {
            'success': False,
            'message': f'检测失败: {e}'
        }

def detect_project_type(path: Path) -> str:
    """检测项目类型"""
    
    # 检测关键文件
    if (path / 'package.json').exists():
        # 读取 package.json
        try:
            with open(path / 'package.json', 'r', encoding='utf-8') as f:
                pkg = json.load(f)
                deps = pkg.get('dependencies', {})
                dev_deps = pkg.get('devDependencies', {})
                
                if 'vue' in str(deps) or 'vue' in str(dev_deps):
                    return 'vue'
                elif '@angular/core' in str(deps) or '@angular/core' in str(dev_deps):
                    return 'angular'
                elif 'next' in str(deps):
                    return 'next'
                else:
                    return 'react'  # 默认为 React
        except:
            return 'node'
    
    elif (path / 'requirements.txt').exists() or (path / 'setup.py').exists():
        # 检测 Python 项目
        try:
            with open(path / 'requirements.txt', 'r', encoding='utf-8') as f:
                content = f.read()
                if 'fastapi' in content:
                    return 'fastapi'
                elif 'django' in content:
                    return 'django'
                elif 'flask' in content:
                    return 'flask'
                else:
                    return 'python'
        except:
            return 'python'
    
    elif (path / 'Cargo.toml').exists():
        return 'rust'
    
    elif (path / 'go.mod').exists():
        return 'go'
    
    elif (path / 'pubspec.yaml').exists():
        return 'flutter'
    
    else:
        return 'unknown'

def detect_tech_stack(path: Path) -> List[str]:
    """检测技术栈"""
    stack = []
    
    # 检测配置文件
    if (path / 'package.json').exists():
        stack.append('Node.js')
    if (path / 'requirements.txt').exists():
        stack.append('Python')
    if (path / 'Cargo.toml').exists():
        stack.append('Rust')
    if (path / 'go.mod').exists():
        stack.append('Go')
    if (path / 'pom.xml').exists() or (path / 'build.gradle').exists():
        stack.append('Java')
    if (path / 'docker-compose.yml').exists():
        stack.append('Docker')
    if (path / '.git').exists():
        stack.append('Git')
    
    # 检测前端框架
    try:
        if (path / 'package.json').exists():
            with open(path / 'package.json', 'r', encoding='utf-8') as f:
                content = f.read()
                if 'vue' in content:
                    stack.append('Vue.js')
                if 'react' in content:
                    stack.append('React')
                if 'angular' in content:
                    stack.append('Angular')
    except:
        pass
    
    # 检测后端框架
    if (path / 'requirements.txt').exists():
        try:
            with open(path / 'requirements.txt', 'r', encoding='utf-8') as f:
                content = f.read()
                if 'fastapi' in content:
                    stack.append('FastAPI')
                if 'django' in content:
                    stack.append('Django')
                if 'flask' in content:
                    stack.append('Flask')
        except:
            pass
    
    return stack

def recommend_skills(project_type: str, tech_stack: List[str]) -> List[str]:
    """推荐适合的技能"""
    skills = ['code_analyzer']  # 基础推荐
    
    if project_type == 'unknown':
        skills.append('project_scaffold')
        skills.append('readme_generator')
        return skills
    
    # 根据项目类型推荐
    if 'vue' in project_type or 'react' in project_type or 'angular' in project_type:
        skills.extend(['git_initializer'])
        skills.append('docker_generator')
    
    elif 'fastapi' in project_type or 'django' in project_type or project_type == 'python':
        skills.extend(['git_initializer'])
        skills.append('docker_generator')
    
    skills.append('readme_generator')
    
    return skills

def check_dependencies(path: Path) -> List[str]:
    """检查缺失的依赖"""
    missing = []
    
    # Git 检查
    if not (path / '.git').exists():
        missing.append('⚠️  未检测到 Git 仓库，建议初始化')
    
    # README 检查
    if not (path / 'README.md').exists():
        missing.append('⚠️  缺少 README.md 文档')
    
    # Docker 检查（如果有 Web 服务）
    if (path / 'package.json').exists() or (path / 'requirements.txt').exists():
        if not (path / 'Dockerfile').exists():
            missing.append('💡 建议添加 Dockerfile 用于部署')
    
    return missing

def generate_suggestions(results: Dict[str, Any]) -> List[str]:
    """生成建议"""
    suggestions = []
    
    if results['project_type'] == 'unknown':
        suggestions.append('🤔 未检测到明确的项目类型，建议创建 README 文档')
    
    if not results['tech_stack']:
        suggestions.append('⚠️  未检测到技术栈，请确保依赖文件存在')
    
    # 根据项目类型给出建议
    if 'fastapi' in str(results['tech_stack']):
        suggestions.append('🚀 检测到 FastAPI 项目，推荐使用 Uvicorn 运行')
    
    if 'vue' in str(results['tech_stack']) or 'react' in str(results['tech_stack']):
        suggestions.append('🎨 检测到前端项目，可以使用 docker_generator 快速配置部署')
    
    if results['recommended_skills']:
        suggestions.append(f'✅ 推荐使用技能: {", ".join(results["recommended_skills"])}')
    
    return suggestions
