#!/usr/bin/env python3
"""
Trae AI 集成工具 - 自动配置 Trae AI 环境
"""
import os
import shutil
from pathlib import Path
from typing import Dict, Any

def execute(**kwargs) -> Dict[str, Any]:
    """
    配置 Trae AI 环境
    
    Args:
        action: 操作类型 (setup/check/clean)
        target_dir: 目标目录
    
    Returns:
        配置结果
    """
    action = kwargs.get('action', 'setup')
    target_dir = kwargs.get('target_dir', '.')
    
    results = {
        'success': True,
        'message': '',
        'files_created': [],
        'files_copied': []
    }
    
    try:
        if action == 'setup':
            results = setup_trae(target_dir, results)
        elif action == 'check':
            results = check_trae(target_dir, results)
        elif action == 'clean':
            results = clean_trae(target_dir, results)
        else:
            results['success'] = False
            results['message'] = f'未知操作: {action}'
    
    except Exception as e:
        results['success'] = False
        results['message'] = f'操作失败: {e}'
    
    return results

def setup_trae(target_dir: str, results: Dict[str, Any]) -> Dict[str, Any]:
    """设置 Trae AI 环境"""
    
    target_path = Path(target_dir)
    trae_dir = Path('.trae')
    
    # 检查 .trae 目录
    if not trae_dir.exists():
        results['success'] = False
        results['message'] = '❌ 未找到 .trae 目录，请确保在项目根目录运行'
        return results
    
    # 创建必要的目录
    rules_dir = target_path / '.trae' / 'rules'
    rules_dir.mkdir(parents=True, exist_ok=True)
    results['files_created'].append(str(rules_dir))
    
    # 复制规则文件
    if (trae_dir / 'rules').exists():
        for rule_file in (trae_dir / 'rules').rglob('*.md'):
            if rule_file.is_file():
                dest = target_path / '.trae' / rule_file.relative_to(trae_dir)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(rule_file, dest)
                results['files_copied'].append(str(dest))
    
    # 创建项目配置文件
    project_config = target_path / '.trae-project.json'
    if not project_config.exists():
        config_content = {
            "project_name": target_path.name,
            "trae_version": "5.0",
            "skills_enabled": True,
            "auto_detect": True
        }
        import json
        with open(project_config, 'w', encoding='utf-8') as f:
            json.dump(config_content, f, indent=2, ensure_ascii=False)
        results['files_created'].append(str(project_config))
    
    results['message'] = f'✅ Trae AI 环境配置完成！创建/复制了 {len(results["files_created"]) + len(results["files_copied"])} 个文件'
    return results

def check_trae(target_dir: str, results: Dict[str, Any]) -> Dict[str, Any]:
    """检查 Trae AI 环境"""
    
    target_path = Path(target_dir)
    checks = []
    
    # 检查规则目录
    rules_dir = target_path / '.trae' / 'rules'
    if rules_dir.exists():
        checks.append('✅ 规则目录存在')
    else:
        checks.append('❌ 规则目录不存在')
    
    # 检查项目配置
    project_config = target_path / '.trae-project.json'
    if project_config.exists():
        checks.append('✅ 项目配置文件存在')
    else:
        checks.append('❌ 项目配置文件不存在')
    
    # 检查 Skills 目录
    skills_dir = target_path / '.trae' / 'skills'
    if skills_dir.exists():
        skill_count = len(list(skills_dir.glob('*.py')))
        checks.append(f'✅ Skills 目录存在 ({skill_count} 个技能)')
    else:
        checks.append('❌ Skills 目录不存在')
    
    results['message'] = '\n'.join(checks)
    return results

def clean_trae(target_dir: str, results: Dict[str, Any]) -> Dict[str, Any]:
    """清理 Trae AI 配置"""
    
    target_path = Path(target_dir)
    
    # 删除规则目录
    rules_dir = target_path / '.trae' / 'rules'
    if rules_dir.exists():
        shutil.rmtree(rules_dir)
        results['files_copied'].append(f'已删除: {rules_dir}')
    
    # 删除项目配置
    project_config = target_path / '.trae-project.json'
    if project_config.exists():
        project_config.unlink()
        results['files_copied'].append(f'已删除: {project_config}')
    
    results['message'] = '✅ Trae AI 配置已清理'
    return results
