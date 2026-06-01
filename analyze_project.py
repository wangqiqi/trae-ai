#!/usr/bin/env python3
"""
分析项目当前状态
"""
import sys
from pathlib import Path

# 导入技能系统
sys.path.insert(0, str(Path(__file__).parent))
from .trae.skills import use_skill

print("🎯 项目分析报告")
print("=" * 50)

# 1. 代码分析
print("\n📊 代码结构分析...")
result = use_skill('code_analyzer', target_path='.')

if result.get('success'):
    print(f"\n✅ 分析成功！")
    print(f"总文件数: {result['summary']['total_files']}")
    print(f"代码文件: {result['summary']['code_files']}")
    print(f"语言分布: {result['summary']['languages']}")
    print(f"\n💡 建议:")
    for rec in result.get('recommendations', []):
        print(f"  - {rec}")
else:
    print(f"❌ 分析失败: {result}")

# 2. 检查技能系统
print("\n" + "=" * 50)
print("🎯 技能系统检查")
from .trae.skills import list_available_skills, get_skill_manager

skills = list_available_skills()
print(f"📦 已加载技能: {len(skills)}")
for skill in skills:
    print(f"  - {skill}")

print("\n✨ 项目分析完成！")
