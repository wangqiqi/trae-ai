#!/usr/bin/env python3
"""
智能需求澄清AI工程师
基于实测经验：主动询问需求，提供选择方案
"""

import json
import os
from pathlib import Path

class SmartRequirementsClarifier:
    def __init__(self):
        self.requirements = {}
        self.project_type = None
        self.conversation_state = 'initial'
    
    def start_requirements_clarification(self, user_input=None):
        """启动需求澄清流程"""
        print("🎯 需求澄清AI工程师启动...")
        
        if not user_input:
            return self.ask_initial_questions()
        
        return self.process_user_input(user_input)
    
    def ask_initial_questions(self):
        """询问初始问题"""
        questions = [
            {
                "question": "请描述您的项目类型：",
                "options": [
                    "Web应用 (Vue/React/Angular)",
                    "移动应用 (Flutter/Uniapp)",
                    "API服务 (FastAPI/Node.js)",
                    "全栈应用 (前后端)",
                    "其他类型"
                ],
                "field": "project_type"
            },
            {
                "question": "项目规模预期：",
                "options": [
                    "小型项目 (1-3天)",
                    "中型项目 (1-2周)",
                    "大型项目 (1个月+)",
                    "长期项目"
                ],
                "field": "project_scale"
            },
            {
                "question": "主要功能需求：",
                "options": [
                    "用户认证系统",
                    "数据管理系统",
                    "电商功能",
                    "社交功能",
                    "内容管理系统",
                    "实时通讯",
                    "文件上传下载",
                    "数据分析",
                    "支付集成",
                    "其他"
                ],
                "field": "main_features"
            }
        ]
        
        return {
            "state": "clarifying",
            "current_question": 0,
            "questions": questions,
            "message": "让我帮您澄清项目需求，这样我们可以提供更精准的解决方案。"
        }
    
    def process_user_input(self, user_input):
        """处理用户输入"""
        # 分析项目类型
        self.detect_project_type(user_input)
        
        # 生成技术方案
        technical_options = self.generate_technical_options()
        
        # 创建需求文档模板
        requirements_template = self.create_requirements_template()
        
        return {
            "state": "options_provided",
            "project_type": self.project_type,
            "technical_options": technical_options,
            "requirements_template": requirements_template,
            "next_actions": [
                "选择技术方案",
                "确认功能需求",
                "开始项目初始化",
                "继续细化需求"
            ]
        }
    
    def detect_project_type(self, user_input):
        """智能检测项目类型"""
        keywords = {
            'vue': ['vue', 'vue3', 'vite'],
            'react': ['react', 'nextjs', 'jsx'],
            'angular': ['angular', 'typescript'],
            'flutter': ['flutter', 'dart', 'mobile'],
            'uniapp': ['uniapp', '小程序', '跨平台'],
            'fastapi': ['fastapi', 'python', 'api'],
            'node': ['node', 'express', 'nestjs']
        }
        
        user_input_lower = user_input.lower()
        for project_type, keys in keywords.items():
            if any(key in user_input_lower for key in keys):
                self.project_type = project_type
                break
        
        if not self.project_type:
            self.project_type = 'generic'
    
    def generate_technical_options(self):
        """生成技术方案选项"""
        options = {
            'vue': {
                'stack': 'Vue3 + TypeScript + Vite + Pinia + FastAPI',
                'features': ['响应式设计', '状态管理', '路由管理', 'API集成'],
                'timeline': '3-5天',
                'complexity': '中等'
            },
            'react': {
                'stack': 'React18 + Next.js + TypeScript + Redux + Node.js',
                'features': ['SSR支持', '状态管理', 'SEO优化', 'API集成'],
                'timeline': '4-6天',
                'complexity': '中高'
            },
            'fastapi': {
                'stack': 'FastAPI + SQLAlchemy + PostgreSQL + Redis',
                'features': ['RESTful API', '数据库ORM', '缓存', '认证授权'],
                'timeline': '2-3天',
                'complexity': '中等'
            },
            'flutter': {
                'stack': 'Flutter + Dart + Firebase + REST API',
                'features': ['跨平台', '实时数据', '推送通知', '离线支持'],
                'timeline': '5-7天',
                'complexity': '中高'
            }
        }
        
        return options.get(self.project_type, options['vue'])
    
    def create_requirements_template(self):
        """创建需求文档模板"""
        template = {
            "项目概述": {
                "项目名称": "待填写",
                "项目描述": "简要描述项目目标和价值",
                "目标用户": "描述主要用户群体",
                "核心功能": ["功能1", "功能2", "功能3"]
            },
            "技术规格": {
                "前端技术": "根据选择的技术方案",
                "后端技术": "根据选择的技术方案",
                "数据库": "SQLite/PostgreSQL/MySQL",
                "部署方式": "本地/Docker/云服务器"
            },
            "功能需求": {
                "用户故事": [
                    "作为[用户角色]，我想[功能需求]，以便[业务价值]"
                ],
                "功能清单": [
                    "用户注册登录",
                    "数据CRUD操作",
                    "权限管理",
                    "数据展示"
                ]
            },
            "非功能需求": {
                "性能要求": "页面响应时间<2秒",
                "安全要求": "用户数据加密存储",
                "兼容性": "支持主流浏览器",
                "可扩展性": "支持功能模块化扩展"
            }
        }
        
        return template
    
    def save_requirements(self, final_requirements):
        """保存最终需求"""
        with open('project_requirements.json', 'w', encoding='utf-8') as f:
            json.dump(final_requirements, f, indent=2, ensure_ascii=False)
        
        # 生成markdown文档
        markdown_content = self.generate_markdown_requirements(final_requirements)
        with open('REQUIREMENTS.md', 'w', encoding='utf-8') as f:
            f.write(markdown_content)
    
    def generate_markdown_requirements(self, requirements):
        """生成markdown格式的需求文档"""
        return f"""# 项目需求文档

## 项目概述
- **项目名称**: {requirements.get('project_name', '未命名')}
- **项目类型**: {requirements.get('project_type', '未指定')}
- **技术方案**: {requirements.get('technical_stack', '待确定')}

## 功能需求
{chr(10).join(f"- {feature}" for feature in requirements.get('features', []))}

## 技术要求
- 前端: {requirements.get('frontend', '待确定')}
- 后端: {requirements.get('backend', '待确定')}
- 数据库: {requirements.get('database', '待确定')}

## 验收标准
{chr(10).join(f"- {criteria}" for criteria in requirements.get('acceptance_criteria', []))}

## 时间计划
- **预计完成时间**: {requirements.get('timeline', '待评估')}
- **关键里程碑**: {requirements.get('milestones', '待制定')}
"""

    def interactive_clarification(self):
        """交互式需求澄清"""
        print("🎯 让我们一步步澄清您的需求")
        
        questions = [
            "您的项目主要解决什么问题？",
            "目标用户是谁？",
            "最重要的3个功能是什么？",
            "有特定的技术偏好吗？",
            "项目预期完成时间？",
            "是否需要用户认证？",
            "数据存储需求？",
            "是否需要移动端支持？"
        ]
        
        answers = {}
        for i, question in enumerate(questions, 1):
            print(f"\n[{i}/8] {question}")
            answer = input("> ").strip()
            if answer:
                answers[question] = answer
        
        return self.generate_final_requirements(answers)
    
    def generate_final_requirements(self, answers):
        """生成最终需求"""
        requirements = {
            'project_name': answers.get('您的项目主要解决什么问题？', '未命名')[:20],
            'project_type': self.detect_type_from_answers(answers),
            'technical_stack': self.suggest_tech_stack(answers),
            'features': self.extract_features(answers),
            'timeline': self.estimate_timeline(answers),
            'acceptance_criteria': self.generate_acceptance_criteria(answers)
        }
        
        self.save_requirements(requirements)
        return requirements
    
    def detect_type_from_answers(self, answers):
        """从回答中检测项目类型"""
        # 简单实现，可以根据需要扩展
        return 'web'
    
    def suggest_tech_stack(self, answers):
        """建议技术栈"""
        return 'Vue3 + FastAPI + SQLite'
    
    def extract_features(self, answers):
        """提取功能需求"""
        features_text = answers.get('最重要的3个功能是什么？', '')
        return [f.strip() for f in features_text.split(',') if f.strip()]
    
    def estimate_timeline(self, answers):
        """估算时间"""
        return "3-5天"
    
    def generate_acceptance_criteria(self, answers):
        """生成验收标准"""
        return [
            "所有功能正常运行",
            "代码无语法错误",
            "环境配置正确",
            "文档完整"
        ]

if __name__ == "__main__":
    clarifier = SmartRequirementsClarifier()
    
    # 示例使用
    user_input = "我想做一个Vue3的待办事项管理系统"
    result = clarifier.start_requirements_clarification(user_input)
    print(json.dumps(result, indent=2, ensure_ascii=False))