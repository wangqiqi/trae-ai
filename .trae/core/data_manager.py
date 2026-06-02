#!/usr/bin/env python3
"""
Trae AI 数据目录管理器
管理 .trae-data/ 目录的创建和初始化
"""
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class TraeDataManager:
    """Trae AI 数据管理器"""
    
    def __init__(self):
        self.data_dir = Path('.trae-data')
        self.config_file = self.data_dir / 'config.json'
        self.stats_file = self.data_dir / 'stats.json'
        self.learning_file = self.data_dir / 'learning.json'
        
    def init(self):
        """初始化数据目录"""
        # 创建目录结构
        dirs = [
            'logs',
            'cache',
            'learning',
            'stats',
            'temp'
        ]
        
        for d in dirs:
            (self.data_dir / d).mkdir(parents=True, exist_ok=True)
        
        # 创建配置文件
        self._init_config()
        
        # 创建统计文件
        self._init_stats()
        
        # 创建学习文件
        self._init_learning()
        
        # 创建 .gitignore
        self._create_gitignore()
        
        print("✅ .trae-data/ 目录初始化完成")
        
    def _init_config(self):
        """初始化配置文件"""
        if not self.config_file.exists():
            config = {
                "version": "5.0",
                "created_at": datetime.now().isoformat(),
                "trae_version": "5.0",
                "settings": {
                    "auto_detect": True,
                    "log_level": "info",
                    "cache_enabled": True,
                    "learning_enabled": True
                }
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
    def _init_stats(self):
        """初始化统计文件"""
        if not self.stats_file.exists():
            stats = {
                "skills_used": {},
                "commands_executed": 0,
                "projects_created": 0,
                "templates_applied": 0,
                "last_updated": datetime.now().isoformat()
            }
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
                
    def _init_learning(self):
        """初始化学习文件"""
        if not self.learning_file.exists():
            learning = {
                "user_preferences": {},
                "project_patterns": {},
                "skill_recommendations": [],
                "last_learning": datetime.now().isoformat()
            }
            with open(self.learning_file, 'w', encoding='utf-8') as f:
                json.dump(learning, f, indent=2, ensure_ascii=False)
                
    def _create_gitignore(self):
        """创建 .gitignore"""
        gitignore_path = self.data_dir / '.gitignore'
        if not gitignore_path.exists():
            gitignore_content = """# Trae AI 私有数据 - 请勿提交到版本控制

# 日志文件
*.log
logs/

# 缓存
*.cache
*.tmp
cache/

# 学习数据
learning/
stats/

# 临时文件
temp/
*.bak
*.swp

# 个人配置
personal/
"""
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
    
    def record_skill_usage(self, skill_name: str):
        """记录技能使用"""
        if self.stats_file.exists():
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                stats = json.load(f)
        else:
            stats = {"skills_used": {}}
            
        if skill_name not in stats["skills_used"]:
            stats["skills_used"][skill_name] = 0
        stats["skills_used"][skill_name] += 1
        stats["last_updated"] = datetime.now().isoformat()
        
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计数据"""
        if self.stats_file.exists():
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def clean_cache(self):
        """清理缓存"""
        cache_dir = self.data_dir / 'cache'
        if cache_dir.exists():
            for f in cache_dir.glob('*'):
                f.unlink()
            print("✅ 缓存已清理")
    
    def get_size(self) -> int:
        """获取数据目录大小（字节）"""
        total = 0
        for f in self.data_dir.rglob('*'):
            if f.is_file():
                total += f.stat().st_size
        return total

def main():
    """主函数"""
    import sys
    
    manager = TraeDataManager()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == 'init':
            manager.init()
        elif cmd == 'stats':
            stats = manager.get_stats()
            print(json.dumps(stats, indent=2, ensure_ascii=False))
        elif cmd == 'clean':
            manager.clean_cache()
        elif cmd == 'size':
            size = manager.get_size()
            print(f"数据目录大小: {size / 1024 / 1024:.2f} MB")
        else:
            print(f"未知命令: {cmd}")
            print("可用命令: init, stats, clean, size")
    else:
        manager.init()

if __name__ == '__main__':
    main()
