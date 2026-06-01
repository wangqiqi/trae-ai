#!/usr/bin/env python3
"""
代码分析技能
分析项目代码结构和质量
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List


def execute(**kwargs) -> Dict[str, Any]:
    """
    执行代码分析
    
    Args:
        target_path: 分析目标路径 (默认当前目录)
        languages: 语言列表 (默认 ['python', 'javascript']
        analysis_depth: 分析深度
        
    Returns:
        分析结果
    """
    target_path = Path(kwargs.get("target_path", "."))
    languages = kwargs.get("languages", ["python", "javascript"])
    analysis_depth = kwargs.get("analysis_depth", "basic")
    
    if not target_path.exists():
        return {
            "success": False,
            "message": f"路径不存在: {target_path}"
        }
    
    results = {
        "success": True,
        "path": str(target_path),
        "summary": {},
        "files": [],
        "recommendations": []
    }
    
    # 统计文件
    all_files = list(target_path.rglob("*"))
    code_files = []
    
    for f in all_files:
        if f.is_file():
            ext = f.suffix.lower()
            file_info = {
                "path": str(f.relative_to(target_path)),
                "size": f.stat().st_size,
                "ext": ext
            }
            
            if ext in [".py", ".js", ".ts", ".jsx", ".tsx", ".vue", ".html", ".css"]:
                code_files.append(file_info)
                
                # 简单分析
                if ext == ".py":
                    file_info["language"] = "Python"
                elif ext in [".js", ".jsx"]:
                    file_info["language"] = "JavaScript"
                elif ext in [".ts", ".tsx"]:
                    file_info["language"] = "TypeScript"
                elif ext == ".vue":
                    file_info["language"] = "Vue"
                
                results["files"].append(file_info)
    
    # 统计
    results["summary"] = {
        "total_files": len(all_files),
        "code_files": len(code_files),
        "languages": _count_languages(code_files),
        "total_size": sum(f["size"] for f in code_files)
    }
    
    # 生成建议
    if len(code_files) > 50:
        results["recommendations"].append("项目规模较大，考虑模块化")
    
    if ".git" not in [d.name for d in target_path.iterdir() if d.is_dir()]:
        results["recommendations"].append("建议初始化 git 仓库")
    
    if not any(f["path"].startswith("tests/") or f["path"].startswith("test_") for f in code_files):
        results["recommendations"].append("建议添加测试文件")
    
    return results


def _count_languages(files: List[Dict]) -> Dict[str, int]:
    """统计语言分布"""
    counts = {}
    for f in files:
        lang = f.get("language", "Other")
        counts[lang] = counts.get(lang, 0) + 1
    return counts


if __name__ == "__main__":
    # 测试运行
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    result = execute(target_path=path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
