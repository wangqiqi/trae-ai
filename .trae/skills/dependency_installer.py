#!/usr/bin/env python3
"""
依赖安装技能 - 智能安装项目依赖
"""
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, List

def execute(**kwargs) -> Dict[str, Any]:
    """
    安装项目依赖
    
    Args:
        package_manager: 包管理器 (auto/npm/pip/yarn/pnpm)
        install_optional: 安装可选依赖 (yes/no)
    
    Returns:
        安装结果
    """
    package_manager = kwargs.get('package_manager', 'auto')
    install_optional = kwargs.get('install_optional', 'no').lower() == 'yes'
    
    results = {
        'success': True,
        'installed': [],
        'failed': [],
        'skipped': [],
        'message': ''
    }
    
    try:
        # 自动检测包管理器
        if package_manager == 'auto':
            package_manager = detect_package_manager()
        
        if not package_manager:
            results['success'] = False
            results['message'] = '❌ 未检测到任何包管理器，请确保在项目目录运行'
            return results
        
        # 执行安装
        if package_manager == 'npm':
            install_npm(results, install_optional)
        elif package_manager == 'yarn':
            install_yarn(results)
        elif package_manager == 'pnpm':
            install_pnpm(results)
        elif package_manager == 'pip':
            install_pip(results)
        elif package_manager == 'poetry':
            install_poetry(results)
        
        # 生成结果消息
        if results['failed']:
            results['message'] = f'⚠️  安装完成，但有 {len(results["failed"])} 个失败'
            results['success'] = False
        else:
            results['message'] = f'✅ 安装完成！成功 {len(results["installed"])} 个'
        
    except Exception as e:
        results['success'] = False
        results['message'] = f'❌ 安装失败: {e}'
    
    return results

def detect_package_manager() -> str:
    """自动检测包管理器"""
    path = Path('.')
    
    if (path / 'package.json').exists():
        # 检查锁文件
        if (path / 'pnpm-lock.yaml').exists():
            return 'pnpm'
        elif (path / 'yarn.lock').exists():
            return 'yarn'
        else:
            return 'npm'
    
    elif (path / 'requirements.txt').exists():
        if (path / 'pyproject.toml').exists():
            return 'poetry'
        else:
            return 'pip'
    
    return None

def install_npm(results: Dict[str, Any], install_optional: bool):
    """安装 npm 依赖"""
    try:
        cmd = ['npm', 'install']
        
        # 检查是否已经安装过
        if not Path('node_modules').exists():
            results['installed'].append('node_modules (首次安装)')
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # 统计安装的包
            if Path('node_modules').exists():
                pkg_count = len(list(Path('node_modules').iterdir()))
                results['installed'].append(f'{pkg_count} 个 npm 包')
        else:
            results['failed'].append(f'npm install: {result.stderr}')
            
    except FileNotFoundError:
        results['failed'].append('npm 未安装')
    except Exception as e:
        results['failed'].append(f'npm: {e}')

def install_yarn(results: Dict[str, Any]):
    """安装 yarn 依赖"""
    try:
        cmd = ['yarn', 'install']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            results['installed'].append('yarn 依赖')
        else:
            results['failed'].append(f'yarn: {result.stderr}')
            
    except FileNotFoundError:
        results['failed'].append('yarn 未安装')
    except Exception as e:
        results['failed'].append(f'yarn: {e}')

def install_pnpm(results: Dict[str, Any]):
    """安装 pnpm 依赖"""
    try:
        cmd = ['pnpm', 'install']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            results['installed'].append('pnpm 依赖')
        else:
            results['failed'].append(f'pnpm: {result.stderr}')
            
    except FileNotFoundError:
        results['failed'].append('pnpm 未安装')
    except Exception as e:
        results['failed'].append(f'pnpm: {e}')

def install_pip(results: Dict[str, Any]):
    """安装 pip 依赖"""
    try:
        # 使用 pip install
        cmd = ['pip', 'install', '-r', 'requirements.txt']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # 统计安装的包
            with open('requirements.txt', 'r') as f:
                pkg_count = len([l for l in f if l.strip() and not l.startswith('#')])
            results['installed'].append(f'{pkg_count} 个 pip 包')
        else:
            results['failed'].append(f'pip: {result.stderr}')
            
    except FileNotFoundError:
        results['failed'].append('pip 未安装')
    except Exception as e:
        results['failed'].append(f'pip: {e}')

def install_poetry(results: Dict[str, Any]):
    """安装 Poetry 依赖"""
    try:
        cmd = ['poetry', 'install']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            results['installed'].append('poetry 依赖')
        else:
            results['failed'].append(f'poetry: {result.stderr}')
            
    except FileNotFoundError:
        results['failed'].append('poetry 未安装')
    except Exception as e:
        results['failed'].append(f'poetry: {e}')
