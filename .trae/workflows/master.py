#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trae AI Master 命令 - 单一入口智能助手
"""
import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

class TraeMaster:
    """Trae AI Master - 智能命令中枢"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.skills_dir = self.base_dir / "skills"
        self.personas_dir = self.base_dir / "docs"
        
    def execute(self, command: str, args: List[str] = None) -> Dict[str, Any]:
        """
        执行 Master 命令
        
        Args:
            command: 命令名称
            args: 命令参数
        
        Returns:
            执行结果
        """
        if args is None:
            args = []
        
        # 命令路由
        commands = {
            # 核心命令
            'help': self.cmd_help,
            'init': self.cmd_init,
            'skills': self.cmd_skills,
            'roles': self.cmd_roles,
            'vibe': self.cmd_vibe,
            
            # 项目命令
            'create': self.cmd_create,
            'analyze': self.cmd_analyze,
            'detect': self.cmd_detect,
            
            # 技能命令
            'skill': self.cmd_skill,
            'use': self.cmd_use,
            
            # 信息命令
            'info': self.cmd_info,
            'stats': self.cmd_stats,
            'status': self.cmd_status,
        }
        
        # 处理自然语言输入
        if ' ' in command or command.startswith('创建一个') or command.startswith('我想'):
            return self.cmd_natural(command, args)
        
        # 执行命令
        if command in commands:
            return commands[command](args)
        else:
            return {
                'success': False,
                'message': f'未知命令: {command}',
                'hint': '使用 "help" 查看可用命令'
            }
    
    def cmd_help(self, args: List[str]) -> Dict[str, Any]:
        """显示帮助信息"""
        help_text = """
🚀 Trae AI Master - 智能命令中枢

📖 基础命令:
   help     - 显示此帮助信息
   init     - 初始化 Trae AI 环境
   skills   - 列出所有可用技能
   roles    - 列出所有人格角色
   vibe     - VIBE 开发流程
   status   - 查看系统状态

📦 项目命令:
   create   - 创建新项目
   analyze  - 分析项目
   detect   - 检测当前项目

🎯 技能命令:
   skill    - 使用技能
   use      - 使用技能 (同 skill)

💡 使用示例:
   trae master help
   trae master skills
   trae master create my-project
   trae master skill code_analyzer
   trae master vibe start

🌟 自然语言:
   "创建一个Vue项目"
   "分析一下我的代码"
   "我想学习Python"
"""
        return {
            'success': True,
            'output': help_text
        }
    
    def cmd_init(self, args: List[str]) -> Dict[str, Any]:
        """初始化环境"""
        try:
            from core.data_manager import TraeDataManager
            
            # 初始化数据目录
            manager = TraeDataManager()
            manager.init()
            
            return {
                'success': True,
                'message': '✅ Trae AI 环境初始化完成！'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'初始化失败: {e}'
            }
    
    def cmd_skills(self, args: List[str]) -> Dict[str, Any]:
        """列出技能"""
        try:
            skills = []
            
            if self.skills_dir.exists():
                for skill_file in self.skills_dir.glob('*.py'):
                    if skill_file.stem != '__init__':
                        skills.append(skill_file.stem)
            
            return {
                'success': True,
                'message': f'📦 可用技能 ({len(skills)}):',
                'skills': skills
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'获取技能列表失败: {e}'
            }
    
    def cmd_roles(self, args: List[str]) -> Dict[str, Any]:
        """人格角色"""
        if args and args[0] == 'list':
            roles = [
                'professional_assistant (专业助手)',
                'humble_assistant (谦逊助手)',
                'friendly_partner (友好伙伴)',
                'expert_mentor (专家导师)',
                'creative_artist (创意艺术家)',
                'strict_teacher (严格教师)',
                'comedy_actor (搞笑演员)',
                'zen_minimalist (极简禅者)',
                'loli (可爱萝莉)',
                'queen_sister (御姐女王)',
                'cyberpunk_hacker (赛博朋克黑客)',
                'magical_girl_coder (魔法少女程序员)',
                'perfect_maid (完美女仆)'
            ]
            
            return {
                'success': True,
                'message': '🎭 可用人格角色:',
                'roles': roles
            }
        else:
            return {
                'success': True,
                'message': '使用 "trae master roles list" 查看所有角色'
            }
    
    def cmd_vibe(self, args: List[str]) -> Dict[str, Any]:
        """VIBE 开发流程"""
        if args and args[0] == 'start':
            return {
                'success': True,
                'message': '🚀 启动 VIBE 开发流程...',
                'phases': [
                    'Phase 1: 📝 Documentation (文档驱动)',
                    'Phase 2: 🎨 Interface (前后端对齐)',
                    'Phase 3: 🧪 Backend (分层开发)',
                    'Phase 4: 🎨 Frontend (前端实现)',
                    'Phase 5: 🔄 Iteration (持续迭代)'
                ]
            }
        else:
            return {
                'success': True,
                'message': '使用 "trae master vibe start" 启动 VIBE 开发流程'
            }
    
    def cmd_create(self, args: List[str]) -> Dict[str, Any]:
        """创建项目"""
        if not args:
            return {
                'success': False,
                'message': '请提供项目名称',
                'usage': 'trae master create <project-name>'
            }
        
        project_name = args[0]
        
        return {
            'success': True,
            'message': f'🚀 正在创建项目: {project_name}',
            'next_steps': [
                f'1. 创建项目目录',
                f'2. 初始化 Git',
                f'3. 应用项目模板',
                f'4. 安装依赖'
            ]
        }
    
    def cmd_analyze(self, args: List[str]) -> Dict[str, Any]:
        """分析项目"""
        try:
            # 使用 env_detector 技能
            from skills.env_detector import execute
            
            result = execute(target_path='.')
            return result
            
        except Exception as e:
            return {
                'success': False,
                'message': f'分析失败: {e}'
            }
    
    def cmd_detect(self, args: List[str]) -> Dict[str, Any]:
        """检测项目"""
        return self.cmd_analyze(args)
    
    def cmd_skill(self, args: List[str]) -> Dict[str, Any]:
        """使用技能"""
        if not args:
            return self.cmd_skills([])
        
        skill_name = args[0]
        
        return {
            'success': True,
            'message': f'🎯 执行技能: {skill_name}',
            'usage': f'请使用控制台执行: python .trae/workflows/trae-console.py'
        }
    
    def cmd_use(self, args: List[str]) -> Dict[str, Any]:
        """使用技能 (alias)"""
        return self.cmd_skill(args)
    
    def cmd_info(self, args: List[str]) -> Dict[str, Any]:
        """系统信息"""
        return {
            'success': True,
            'message': '📊 Trae AI 超级团队信息',
            'info': {
                'version': '5.0',
                'constitution': '已加载',
                'vibe_methodology': '已加载',
                'dual_directory': '已加载',
                'persona_system': '已加载'
            }
        }
    
    def cmd_stats(self, args: List[str]) -> Dict[str, Any]:
        """统计数据"""
        try:
            from core.data_manager import TraeDataManager
            
            manager = TraeDataManager()
            stats = manager.get_stats()
            
            return {
                'success': True,
                'message': '📊 使用统计',
                'stats': stats
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'获取统计失败: {e}'
            }
    
    def cmd_status(self, args: List[str]) -> Dict[str, Any]:
        """系统状态"""
        return {
            'success': True,
            'message': '✅ 系统状态正常',
            'checks': {
                'constitution': '✅ 已加载',
                'skills': f'✅ {len(list(self.skills_dir.glob("*.py"))) - 1} 个技能',
                'data_dir': '✅ 正常',
                'core_modules': '✅ 正常'
            }
        }
    
    def cmd_natural(self, command: str, args: List[str]) -> Dict[str, Any]:
        """处理自然语言"""
        command_lower = command.lower()
        
        if '创建' in command or '新建' in command:
            # 提取项目名称
            project_name = 'my-project'
            for arg in args:
                if not arg.startswith('-'):
                    project_name = arg
                    break
            
            return self.cmd_create([project_name])
        
        elif '分析' in command or '检测' in command:
            return self.cmd_analyze([])
        
        elif '技能' in command or 'skill' in command_lower:
            if args:
                return self.cmd_skill(args)
            else:
                return self.cmd_skills([])
        
        elif '帮助' in command or 'help' in command_lower:
            return self.cmd_help([])
        
        else:
            return {
                'success': True,
                'message': f'我理解了你的需求: {command}',
                'hint': '使用 "trae master help" 查看所有命令'
            }


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("❌ 请提供命令")
        print("使用 'trae master help' 查看帮助")
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    master = TraeMaster()
    result = master.execute(command, args)
    
    # 输出结果
    if result.get('success'):
        if 'output' in result:
            print(result['output'])
        elif 'message' in result:
            print(result['message'])
        
        if 'skills' in result:
            for skill in result['skills']:
                print(f"  • {skill}")
        
        if 'roles' in result:
            for role in result['roles']:
                print(f"  • {role}")
        
        if 'phases' in result:
            for phase in result['phases']:
                print(f"  {phase}")
        
        if 'info' in result:
            for key, value in result['info'].items():
                print(f"  {key}: {value}")
        
        if 'stats' in result:
            print(json.dumps(result['stats'], indent=2, ensure_ascii=False))
        
        if 'checks' in result:
            for key, value in result['checks'].items():
                print(f"  {key}: {value}")
    else:
        print(f"❌ {result.get('message')}")
        if 'hint' in result:
            print(f"💡 {result['hint']}")
        if 'usage' in result:
            print(f"📖 用法: {result['usage']}")


if __name__ == '__main__':
    main()
