#!/usr/bin/env python3
"""
Git 初始化技能 - 快速设置 Git 仓库
"""
import os
import subprocess
from pathlib import Path
from typing import Dict, Any

def execute(**kwargs) -> Dict[str, Any]:
    """
    初始化 Git 仓库
    
    Args:
        gitignore_template: gitignore 模板类型 (python, node, vue, react 等)
        init: 是否执行 git init (yes/no)
        first_commit: 是否创建初始提交 (yes/no)
    
    Returns:
        执行结果
    """
    gitignore_type = kwargs.get('gitignore_template', 'python')
    do_init = kwargs.get('init', 'yes').lower() == 'yes'
    do_commit = kwargs.get('first_commit', 'yes').lower() == 'yes'
    
    results = {
        'success': True,
        'steps': [],
        'message': ''
    }
    
    try:
        # 1. 创建 .gitignore
        gitignore_content = generate_gitignore(gitignore_type)
        gitignore_path = Path('.gitignore')
        
        if not gitignore_path.exists():
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            results['steps'].append(f'✅ 创建 .gitignore ({gitignore_type})')
        else:
            results['steps'].append(f'⚠️  .gitignore 已存在')
        
        # 2. Git init
        if do_init and not Path('.git').exists():
            subprocess.run(['git', 'init'], capture_output=True, text=True)
            results['steps'].append('✅ 执行 git init')
        elif Path('.git').exists():
            results['steps'].append('⚠️  Git 仓库已存在')
        
        # 3. Initial commit
        if do_commit and Path('.git').exists():
            try:
                subprocess.run(['git', 'add', '.'], capture_output=True, text=True)
                result = subprocess.run(
                    ['git', 'commit', '-m', 'Initial commit'],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    results['steps'].append('✅ 创建初始提交')
                else:
                    results['steps'].append('⚠️  没有文件可提交')
            except Exception as e:
                results['steps'].append(f'⚠️  提交失败: {e}')
        
        results['message'] = 'Git 初始化完成！'
        
    except Exception as e:
        results['success'] = False
        results['message'] = f'初始化失败: {e}'
    
    return results

def generate_gitignore(template: str) -> str:
    """生成 gitignore 内容"""
    
    templates = {
        'python': '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.env
.venv
env/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
''',
        'node': '''# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*
.env
.env.local
.env.*.local

# Build
dist/
build/
.next/
.nuxt/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
''',
        'vue': '''# Vue
node_modules/
dist/
.nuxt/
.next/
.cache/
.vuepress/dist/
serverless/
.serverless/
.DS_Store
*.swp
*.swo

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# IDE
.vscode/
.idea/
''',
        'react': '''# React
node_modules/
/build
/.pnp
.pnp.js

# Testing
/coverage

# Production
/build

# Misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode/
.idea/
'''
    }
    
    return templates.get(template.lower(), templates['python'])
