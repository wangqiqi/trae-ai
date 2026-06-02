#!/usr/bin/env python3
"""
Trae AI 自学习系统
自动学习和适应用户偏好
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

class TraeLearner:
    """Trae AI 学习器"""
    
    def __init__(self):
        self.data_dir = Path('.trae-data')
        self.learning_file = self.data_dir / 'learning.json'
        self.preferences_file = self.data_dir / 'preferences.json'
        self.patterns_file = self.data_dir / 'patterns.json'
        
        # 确保目录存在
        self.data_dir.mkdir(exist_ok=True)
        
        # 初始化文件
        self._init_files()
    
    def _init_files(self):
        """初始化学习文件"""
        # 学习记录
        if not self.learning_file.exists():
            self._save_json(self.learning_file, {
                'user_preferences': {},
                'skill_usage_history': [],
                'command_history': [],
                'project_patterns': {},
                'last_learning': datetime.now().isoformat()
            })
        
        # 用户偏好
        if not self.preferences_file.exists():
            self._save_json(self.preferences_file, {
                'preferred_persona': 'professional_assistant',
                'preferred_skill': None,
                'code_style': 'standard',
                'communication_tone': 'formal',
                'learning_enabled': True
            })
        
        # 模式记录
        if not self.patterns_file.exists():
            self._save_json(self.patterns_file, {
                'project_types': {},
                'tech_stacks': {},
                'common_tasks': [],
                'successful_patterns': []
            })
    
    def _load_json(self, filepath: Path) -> Dict[str, Any]:
        """加载 JSON 文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_json(self, filepath: Path, data: Dict[str, Any]):
        """保存 JSON 文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def learn_skill_usage(self, skill_name: str, success: bool, context: str = ''):
        """学习技能使用"""
        data = self._load_json(self.learning_file)
        
        # 记录技能使用
        data['skill_usage_history'].append({
            'skill': skill_name,
            'success': success,
            'context': context,
            'timestamp': datetime.now().isoformat()
        })
        
        # 只保留最近 100 条记录
        data['skill_usage_history'] = data['skill_usage_history'][-100:]
        
        # 更新最后学习时间
        data['last_learning'] = datetime.now().isoformat()
        
        self._save_json(self.learning_file, data)
        
        # 更新模式
        self._update_pattern('skill_usage', skill_name)
    
    def learn_command(self, command: str, args: List[str]):
        """学习命令使用"""
        data = self._load_json(self.learning_file)
        
        # 记录命令
        data['command_history'].append({
            'command': command,
            'args': args,
            'timestamp': datetime.now().isoformat()
        })
        
        # 只保留最近 100 条记录
        data['command_history'] = data['command_history'][-100:]
        
        self._save_json(self.learning_file, data)
        
        # 更新模式
        self._update_pattern('command_usage', command)
    
    def learn_project_type(self, project_type: str):
        """学习项目类型"""
        self._update_pattern('project_type', project_type)
    
    def learn_tech_stack(self, tech_stack: List[str]):
        """学习技术栈"""
        for tech in tech_stack:
            self._update_pattern('tech_stack', tech)
    
    def _update_pattern(self, pattern_type: str, value: str):
        """更新模式"""
        patterns = self._load_json(self.patterns_file)
        
        if pattern_type not in patterns:
            patterns[pattern_type] = {}
        
        if value not in patterns[pattern_type]:
            patterns[pattern_type][value] = 0
        
        patterns[pattern_type][value] += 1
        
        self._save_json(self.patterns_file, patterns)
    
    def get_recommendations(self) -> Dict[str, Any]:
        """获取推荐"""
        recommendations = {
            'skills': [],
            'persona': None,
            'next_actions': []
        }
        
        # 分析最常用的技能
        patterns = self._load_json(self.patterns_file)
        if 'skill_usage' in patterns:
            sorted_skills = sorted(
                patterns['skill_usage'].items(),
                key=lambda x: x[1],
                reverse=True
            )
            recommendations['skills'] = [s[0] for s in sorted_skills[:5]]
        
        # 获取用户偏好人格
        prefs = self._load_json(self.preferences_file)
        recommendations['persona'] = prefs.get('preferred_persona')
        
        # 获取推荐的下一步操作
        if 'command_usage' in patterns:
            sorted_commands = sorted(
                patterns['command_usage'].items(),
                key=lambda x: x[1],
                reverse=True
            )
            recommendations['next_actions'] = [c[0] for c in sorted_commands[:3]]
        
        return recommendations
    
    def update_preference(self, key: str, value: Any):
        """更新偏好"""
        prefs = self._load_json(self.preferences_file)
        prefs[key] = value
        self._save_json(self.preferences_file, prefs)
    
    def get_preferences(self) -> Dict[str, Any]:
        """获取所有偏好"""
        return self._load_json(self.preferences_file)
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """获取学习统计"""
        patterns = self._load_json(self.patterns_file)
        learning = self._load_json(self.learning_file)
        
        return {
            'total_skills_used': sum(patterns.get('skill_usage', {}).values()),
            'total_commands': sum(patterns.get('command_usage', {}).values()),
            'project_types_learned': len(patterns.get('project_type', {})),
            'tech_stacks_learned': len(patterns.get('tech_stack', {})),
            'last_learning': learning.get('last_learning'),
            'learning_enabled': self._load_json(self.preferences_file).get('learning_enabled', True)
        }
    
    def suggest_improvements(self) -> List[str]:
        """建议改进"""
        suggestions = []
        patterns = self._load_json(self.patterns_file)
        prefs = self._load_json(self.preferences_file)
        
        # 检查是否开启了学习
        if not prefs.get('learning_enabled'):
            suggestions.append("💡 建议开启学习功能以获得更好的个性化推荐")
        
        # 检查是否使用了多种技能
        skill_count = len(patterns.get('skill_usage', {}))
        if skill_count < 3:
            suggestions.append("💡 你可以尝试使用更多技能来提高效率")
        
        # 检查是否分析了多个项目
        project_count = len(patterns.get('project_type', {}))
        if project_count < 2:
            suggestions.append("💡 建议使用项目检测功能来让系统更好地了解你的项目")
        
        # 检查人格设置
        if not prefs.get('preferred_persona'):
            suggestions.append("💡 建议设置一个人格角色以获得更个性化的体验")
        
        if not suggestions:
            suggestions.append("✅ 学习系统运行良好！继续保持")
        
        return suggestions


def main():
    """主函数"""
    import sys
    
    learner = TraeLearner()
    
    if len(sys.argv) < 2:
        print("❌ 请提供操作")
        print("可用操作: learn, recommend, stats, improve")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == 'learn':
        if len(sys.argv) < 3:
            print("❌ 请提供学习内容")
            sys.exit(1)
        
        content_type = sys.argv[2]
        if content_type == 'skill':
            learner.learn_skill_usage(sys.argv[3] if len(sys.argv) > 3 else 'unknown')
            print("✅ 已学习技能使用")
        elif content_type == 'command':
            learner.learn_command(sys.argv[2], sys.argv[3:])
            print("✅ 已学习命令使用")
        else:
            print(f"❌ 未知学习类型: {content_type}")
    
    elif action == 'recommend':
        recs = learner.get_recommendations()
        print(json.dumps(recs, indent=2, ensure_ascii=False))
    
    elif action == 'stats':
        stats = learner.get_learning_stats()
        print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    elif action == 'improve':
        suggestions = learner.suggest_improvements()
        for s in suggestions:
            print(s)
    
    elif action == 'prefs':
        prefs = learner.get_preferences()
        print(json.dumps(prefs, indent=2, ensure_ascii=False))
    
    else:
        print(f"❌ 未知操作: {action}")


if __name__ == '__main__':
    main()
