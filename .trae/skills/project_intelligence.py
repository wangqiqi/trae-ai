#!/usr/bin/env python3
"""
项目智能助手 - 自动识别项目并推荐操作
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, List

def execute(**kwargs) -> Dict[str, Any]:
    """
    项目智能分析
    
    Args:
        target_path: 项目路径（默认当前目录）
        mode: 模式 (detect/recommend/full)
    
    Returns:
        分析结果
    """
    target_path = kwargs.get('target_path', '.')
    mode = kwargs.get('mode', 'full')
    
    try:
        project_path = Path(target_path)
        
        # 完整分析
        results = {
            'success': True,
            'project_info': {},
            'recommended_skills': [],
            'next_steps': [],
            'message': ''
        }
        
        # 1. 检测项目信息
        results['project_info'] = detect_project(project_path)
        
        # 2. 推荐技能
        results['recommended_skills'] = recommend_skill(results['project_info'])
        
        # 3. 生成下一步建议
        results['next_steps'] = suggest_next_steps(results['project_info'])
        
        # 生成总结
        project_type = results['project_info'].get('type', 'unknown')
        stack = results['project_info'].get('tech_stack', [])
        
        results['message'] = f"✅ 项目分析完成！检测到 {project_type} 项目，使用 {', '.join(stack[:3]) if stack else '未知技术栈'}"
        
        return results
        
    except Exception as e:
        return {
            'success': False,
            'message': f'分析失败: {e}'
        }

def detect_project(path: Path) -> Dict[str, Any]:
    """检测项目信息"""
    info = {
        'type': 'unknown',
        'name': path.name,
        'tech_stack': [],
        'has_git': False,
        'has_readme': False,
        'has_docker': False,
        'has_tests': False,
        'package_manager': None
    }
    
    # 项目类型
    info['type'] = detect_type(path)
    
    # 技术栈
    info['tech_stack'] = detect_stack(path)
    
    # Git
    info['has_git'] = (path / '.git').exists()
    
    # README
    info['has_readme'] = (path / 'README.md').exists()
    
    # Docker
    info['has_docker'] = (path / 'Dockerfile').exists() or (path / 'docker-compose.yml').exists()
    
    # 测试
    info['has_tests'] = any([
        (path / 'tests').exists(),
        (path / 'test').exists(),
        (path / '__tests__').exists(),
        list(path.glob('*.test.js')),
        list(path.glob('*_test.py'))
    ])
    
    # 包管理器
    info['package_manager'] = detect_package_manager(path)
    
    return info

def detect_type(path: Path) -> str:
    """检测项目类型"""
    
    # Node.js 项目
    if (path / 'package.json').exists():
        try:
            with open(path / 'package.json', 'r', encoding='utf-8') as f:
                pkg = json.load(f)
                deps = str(pkg.get('dependencies', {})) + str(pkg.get('devDependencies', {}))
                
                if 'vue' in deps:
                    return 'vue'
                elif '@angular/core' in deps:
                    return 'angular'
                elif 'next' in deps:
                    return 'next'
                elif '@nestjs/core' in deps:
                    return 'nestjs'
                else:
                    return 'react'
        except:
            return 'node'
    
    # Python 项目
    if (path / 'requirements.txt').exists() or (path / 'setup.py').exists() or (path / 'pyproject.toml').exists():
        try:
            req_file = path / 'requirements.txt'
            if req_file.exists():
                with open(req_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'fastapi' in content:
                        return 'fastapi'
                    elif 'django' in content:
                        return 'django'
                    elif 'flask' in content:
                        return 'flask'
            return 'python'
        except:
            return 'python'
    
    # Rust
    if (path / 'Cargo.toml').exists():
        return 'rust'
    
    # Go
    if (path / 'go.mod').exists():
        return 'go'
    
    # Java
    if (path / 'pom.xml').exists() or (path / 'build.gradle').exists():
        return 'java'
    
    # Flutter
    if (path / 'pubspec.yaml').exists():
        return 'flutter'
    
    return 'unknown'

def detect_stack(path: Path) -> List[str]:
    """检测技术栈"""
    stack = []
    
    # 语言运行时
    if (path / 'package.json').exists():
        stack.append('Node.js')
    if (path / 'requirements.txt').exists() or (path / 'setup.py').exists():
        stack.append('Python')
    if (path / 'Cargo.toml').exists():
        stack.append('Rust')
    if (path / 'go.mod').exists():
        stack.append('Go')
    if (path / 'pubspec.yaml').exists():
        stack.append('Dart')
    
    # 前端框架
    if (path / 'package.json').exists():
        try:
            with open(path / 'package.json', 'r', encoding='utf-8') as f:
                content = f.read()
                if "'vue'" in content or '"vue"' in content:
                    stack.append('Vue.js')
                if "'react'" in content or '"react"' in content:
                    stack.append('React')
                if "'angular'" in content or '"angular"' in content:
                    stack.append('Angular')
        except:
            pass
    
    # 后端框架
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
    
    # 工具
    if (path / 'docker-compose.yml').exists():
        stack.append('Docker')
    if (path / '.git').exists():
        stack.append('Git')
    
    return stack

def detect_package_manager(path: Path) -> str:
    """检测包管理器"""
    if (path / 'package.json').exists():
        if (path / 'pnpm-lock.yaml').exists():
            return 'pnpm'
        elif (path / 'yarn.lock').exists():
            return 'yarn'
        else:
            return 'npm'
    
    if (path / 'requirements.txt').exists():
        if (path / 'poetry.lock').exists():
            return 'poetry'
        else:
            return 'pip'
    
    return None

def recommend_skill(info: Dict[str, Any]) -> List[str]:
    """推荐技能"""
    skills = []
    
    # 基础推荐
    skills.append('code_analyzer')
    
    # 根据项目类型推荐
    project_type = info['type']
    
    if project_type == 'unknown':
        skills.extend(['project_scaffold', 'readme_generator'])
    
    if project_type in ['vue', 'react', 'angular', 'next']:
        skills.extend(['git_initializer'])
        if not info['has_docker']:
            skills.append('docker_generator')
    
    if project_type in ['fastapi', 'django', 'flask', 'python', 'nestjs']:
        skills.extend(['git_initializer'])
        if not info['has_docker']:
            skills.append('docker_generator')
        if not info['has_readme']:
            skills.append('readme_generator')
    
    if info['package_manager']:
        skills.append('dependency_installer')
    
    # 如果没有 README
    if not info['has_readme']:
        skills.append('readme_generator')
    
    # 去重
    return list(dict.fromkeys(skills))

def suggest_next_steps(info: Dict[str, Any]) -> List[str]:
    """生成下一步建议"""
    steps = []
    
    # Git
    if not info['has_git']:
        steps.append('🔧 初始化 Git 仓库: git_initializer')
    
    # README
    if not info['has_readme']:
        steps.append('📝 生成 README: readme_generator')
    
    # Docker
    if not info['has_docker'] and info['type'] != 'unknown':
        steps.append('🐳 添加 Docker 配置: docker_generator')
    
    # 依赖
    if info['package_manager']:
        steps.append(f'📦 安装依赖: dependency_installer')
    
    # 测试
    if not info['has_tests']:
        steps.append('🧪 建议添加测试文件')
    
    return steps
