#!/usr/bin/env python3
"""
文件搜索技能 - 快速搜索项目文件
"""
import os
from pathlib import Path
from typing import Dict, Any, List

def execute(**kwargs) -> Dict[str, Any]:
    """
    搜索文件
    
    Args:
        pattern: 搜索模式（文件名或扩展名）
        search_type: 搜索类型 (name/ext/content)
        directory: 搜索目录（默认当前目录）
        max_results: 最大结果数
    
    Returns:
        搜索结果
    """
    pattern = kwargs.get('pattern', '')
    search_type = kwargs.get('search_type', 'name')
    directory = kwargs.get('directory', '.')
    max_results = int(kwargs.get('max_results', 20))
    
    if not pattern:
        return {
            'success': False,
            'message': '请提供搜索模式'
        }
    
    try:
        matches = []
        search_path = Path(directory)
        
        for item in search_path.rglob('*'):
            if len(matches) >= max_results:
                break
            
            if item.is_file():
                if search_type == 'name' and pattern.lower() in item.name.lower():
                    matches.append(str(item.relative_to(search_path)))
                elif search_type == 'ext' and item.suffix.lower() == pattern.lower():
                    matches.append(str(item.relative_to(search_path)))
                elif search_type == 'content':
                    try:
                        with open(item, 'r', encoding='utf-8') as f:
                            if pattern in f.read():
                                matches.append(str(item.relative_to(search_path)))
                    except:
                        pass
        
        return {
            'success': True,
            'message': f'找到 {len(matches)} 个匹配项',
            'matches': matches,
            'count': len(matches)
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'搜索失败: {e}'
        }
