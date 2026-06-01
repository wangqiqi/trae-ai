"""
Trae AI Skills 技能系统
"""

import sys
import importlib.util
from pathlib import Path
from typing import Dict, Any, List, Optional


class SkillManager:
    """技能管理器"""
    
    def __init__(self, skills_dir: Optional[Path] = None):
        if skills_dir is None:
            skills_dir = Path(__file__).parent
        
        self.skills_dir = skills_dir
        self.skills = self._discover_skills()
    
    def _discover_skills(self) -> Dict[str, Any]:
        """发现并加载所有可用技能"""
        skills = {}
        
        for skill_file in self.skills_dir.glob("*.py"):
            if skill_file.name == "__init__.py":
                continue
            
            skill_name = skill_file.stem
            try:
                # 动态加载模块
                spec = importlib.util.spec_from_file_location(skill_name, skill_file)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # 检查是否有 execute 函数
                    if hasattr(module, "execute") and callable(module.execute):
                        skills[skill_name] = module
                        print(f"✅ 加载技能: {skill_name}")
            except Exception as e:
                print(f"❌ 加载技能失败 {skill_name}: {e}")
        
        return skills
    
    def list_skills(self) -> List[str]:
        """列出所有可用技能"""
        return list(self.skills.keys())
    
    def execute_skill(self, skill_name: str, **kwargs) -> Dict[str, Any]:
        """执行指定技能"""
        if skill_name not in self.skills:
            return {
                "success": False,
                "message": f"技能不存在: {skill_name}",
                "available_skills": self.list_skills()
            }
        
        try:
            module = self.skills[skill_name]
            result = module.execute(**kwargs)
            return result
        except Exception as e:
            return {
                "success": False,
                "message": f"执行技能失败: {e}"
            }


# 全局技能管理器实例
_skill_manager: Optional[SkillManager] = None


def get_skill_manager() -> SkillManager:
    """获取技能管理器单例"""
    global _skill_manager
    if _skill_manager is None:
        _skill_manager = SkillManager()
    return _skill_manager


def use_skill(skill_name: str, **kwargs) -> Dict[str, Any]:
    """使用指定技能"""
    manager = get_skill_manager()
    return manager.execute_skill(skill_name, **kwargs)


def list_available_skills() -> List[str]:
    """列出所有可用技能"""
    manager = get_skill_manager()
    return manager.list_skills()


if __name__ == "__main__":
    print("🎯 Trae AI Skills")
    print("=" * 40)
    
    manager = get_skill_manager()
    skills = manager.list_skills()
    
    print(f"\n📦 可用技能 ({len(skills)}):")
    for skill in skills:
        print(f"  - {skill}")
    
    print("\n💡 使用示例:")
    print("  use_skill('project_scaffold', project_type='vue', project_name='my-app')")
