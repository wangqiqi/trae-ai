#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能需求解析引擎
实现自然语言到项目规格的自动转换
"""

import json
import re
import os
from pathlib import Path
from typing import Dict, List, Any
import datetime

class IntelligentProjectParser:
    """智能项目需求解析器"""
    
    def __init__(self):
        self.base_path = Path(os.getcwd())
        self.config_path = self.base_path / ".trae" / "config"
        self.templates_path = self.base_path / ".trae" / "templates"
        
        # 技术栈关键词映射
        self.tech_keywords = {
            "前端": {
                "vue": ["vue", "vue3", "vue.js"],
                "react": ["react", "react.js", "next.js"],
                "angular": ["angular", "angular.js"],
                "flutter": ["flutter", "dart"],
                "uniapp": ["uni-app", "uniapp", "小程序"]
            },
            "后端": {
                "fastapi": ["fastapi", "python", "flask"],
                "nodejs": ["nodejs", "node.js", "express"],
                "go": ["go", "golang", "gin"],
                "rust": ["rust", "actix"]
            },
            "数据库": {
                "postgresql": ["postgresql", "postgres", "pg"],
                "mysql": ["mysql", "mariadb"],
                "sqlite": ["sqlite", "sqlite3"],
                "mongodb": ["mongodb", "mongo"]
            },
            "ai": {
                "python_ai": ["ai", "机器学习", "深度学习", "pytorch", "tensorflow"],
                "cpp_deployment": ["c++", "部署", "推理", "tensorrt"]
            }
        }
        
        # 项目类型关键词
        self.project_types = {
            "mvp_web": ["mvp", "最小可行", "快速原型", "简单"],
            "web_application": ["web应用", "网站", "管理系统", "平台"],
            "mobile_app": ["app", "移动应用", "手机应用"],
            "mini_program": ["小程序", "微信", "支付宝", "百度"],
            "ai_system": ["ai", "人工智能", "识别", "预测", "推荐"],
            "ecommerce": ["电商", "购物", "商品", "订单", "支付"],
            "social": ["社交", "社区", "论坛", "聊天"],
            "content": ["内容", "博客", "文章", "cms"]
        }
        
        # 功能关键词
        self.feature_keywords = {
            "auth": ["登录", "注册", "用户", "权限", "认证"],
            "crud": ["增删改查", "crud", "管理", "列表"],
            "payment": ["支付", "微信", "支付宝", "stripe"],
            "upload": ["上传", "图片", "文件", "媒体"],
            "search": ["搜索", "查询", "筛选", "过滤"],
            "notification": ["通知", "消息", "推送", "提醒"],
            "analytics": ["统计", "分析", "报表", "图表"]
        }
    
    def parse_requirement(self, requirement: str) -> Dict[str, Any]:
        """解析需求并生成项目规格"""
        
        # 基础信息提取
        project_info = {
            "original_requirement": requirement,
            "parsed_at": datetime.datetime.now().isoformat(),
            "project_type": self._detect_project_type(requirement),
            "tech_stack": self._detect_tech_stack(requirement),
            "features": self._detect_features(requirement),
            "timeline": self._estimate_timeline(requirement),
            "complexity": self._assess_complexity(requirement),
            "risks": self._assess_risks(requirement),
            "recommendations": self._generate_recommendations(requirement)
        }
        
        # 生成项目配置
        project_config = self._generate_project_config(project_info)
        
        return {
            "analysis": project_info,
            "config": project_config,
            "next_steps": self._generate_next_steps(project_info)
        }
    
    def _detect_project_type(self, requirement: str) -> str:
        """检测项目类型"""
        req_lower = requirement.lower()
        
        for project_type, keywords in self.project_types.items():
            for keyword in keywords:
                if keyword in req_lower:
                    return project_type
        
        # 默认类型
        return "web_application"
    
    def _detect_tech_stack(self, requirement: str) -> Dict[str, str]:
        """检测技术栈"""
        req_lower = requirement.lower()
        detected = {}
        
        # 检测前端技术
        for tech, keywords in self.tech_keywords["前端"].items():
            for keyword in keywords:
                if keyword in req_lower:
                    detected["frontend"] = tech
                    break
        
        # 检测后端技术
        for tech, keywords in self.tech_keywords["后端"].items():
            for keyword in keywords:
                if keyword in req_lower:
                    detected["backend"] = tech
                    break
        
        # 检测数据库
        for tech, keywords in self.tech_keywords["数据库"].items():
            for keyword in keywords:
                if keyword in req_lower:
                    detected["database"] = tech
                    break
        
        # 检测AI相关
        for tech, keywords in self.tech_keywords["ai"].items():
            for keyword in keywords:
                if keyword in req_lower:
                    detected["ai"] = tech
                    break
        
        # 默认值
        if "frontend" not in detected:
            detected["frontend"] = "vue"
        if "backend" not in detected:
            detected["backend"] = "fastapi"
        if "database" not in detected:
            detected["database"] = "sqlite"
        
        return detected
    
    def _detect_features(self, requirement: str) -> List[str]:
        """检测功能需求"""
        req_lower = requirement.lower()
        detected = []
        
        for feature, keywords in self.feature_keywords.items():
            for keyword in keywords:
                if keyword in req_lower:
                    detected.append(feature)
                    break
        
        return detected
    
    def _estimate_timeline(self, requirement: str) -> Dict[str, str]:
        """估算项目时间线"""
        complexity = self._assess_complexity(requirement)
        
        timelines = {
            "simple": {
                "total": "1-2周",
                "phases": {
                    "需求分析": "1天",
                    "设计": "1-2天",
                    "开发": "3-5天",
                    "测试": "1-2天",
                    "部署": "1天"
                }
            },
            "medium": {
                "total": "3-4周",
                "phases": {
                    "需求分析": "2-3天",
                    "设计": "3-5天",
                    "开发": "1-2周",
                    "测试": "3-5天",
                    "部署": "2-3天"
                }
            },
            "complex": {
                "total": "6-8周",
                "phases": {
                    "需求分析": "1周",
                    "设计": "1-2周",
                    "开发": "3-4周",
                    "测试": "1-2周",
                    "部署": "1周"
                }
            }
        }
        
        return timelines.get(complexity, timelines["medium"])
    
    def _assess_complexity(self, requirement: str) -> str:
        """评估项目复杂度"""
        complexity_indicators = {
            "simple": ["简单", "基础", "mvp", "快速", "原型"],
            "complex": ["复杂", "企业级", "分布式", "微服务", "高并发", "ai", "机器学习"],
            "medium": []  # 默认中等
        }
        
        req_lower = requirement.lower()
        
        for level, indicators in complexity_indicators.items():
            for indicator in indicators:
                if indicator in req_lower:
                    return level
        
        return "medium"
    
    def _assess_risks(self, requirement: str) -> List[Dict[str, str]]:
        """评估项目风险"""
        risks = []
        req_lower = requirement.lower()
        
        # 技术风险
        if "ai" in req_lower or "机器学习" in req_lower:
            risks.append({
                "type": "技术",
                "level": "高",
                "description": "AI模型训练可能需要大量数据和计算资源",
                "mitigation": "建议使用预训练模型或云服务"
            })
        
        if "高并发" in req_lower or "分布式" in req_lower:
            risks.append({
                "type": "架构",
                "level": "中",
                "description": "分布式系统复杂度较高",
                "mitigation": "建议先实现单机版，再考虑扩展"
            })
        
        if "支付" in req_lower:
            risks.append({
                "type": "合规",
                "level": "高",
                "description": "涉及支付需要合规审查",
                "mitigation": "集成成熟的支付SDK，确保PCI合规"
            })
        
        # 时间风险
        if "1周" in req_lower or "快速" in req_lower:
            risks.append({
                "type": "时间",
                "level": "中",
                "description": "时间紧迫可能影响质量",
                "mitigation": "优先实现核心功能，采用MVP策略"
            })
        
        return risks
    
    def _generate_recommendations(self, requirement: str) -> List[str]:
        """生成建议"""
        recommendations = []
        req_lower = requirement.lower()
        
        # 技术建议
        if "小程序" in req_lower and "uni-app" not in req_lower:
            recommendations.append("建议使用uni-app实现一次开发，多端发布")
        
        if "web" in req_lower and "响应式" not in req_lower:
            recommendations.append("建议采用响应式设计，适配多端设备")
        
        if "数据库" not in req_lower:
            recommendations.append("建议使用SQLite快速启动，后续可迁移到PostgreSQL")
        
        # 开发建议
        recommendations.extend([
            "采用敏捷开发，每2-3天一个迭代",
            "使用Git进行版本控制",
            "优先实现MVP核心功能"
        ])
        
        return recommendations
    
    def _generate_project_config(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """生成项目配置"""
        return {
            "project_name": self._generate_project_name(analysis["original_requirement"]),
            "project_type": analysis["project_type"],
            "tech_stack": analysis["tech_stack"],
            "features": analysis["features"],
            "timeline": analysis["timeline"],
            "team_config": self._generate_team_config(analysis),
            "milestones": self._generate_milestones(analysis),
            "quality_gates": self._generate_quality_gates(analysis)
        }
    
    def _generate_project_name(self, requirement: str) -> str:
        """生成项目名称"""
        # 提取关键词
        keywords = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', requirement)
        
        if len(keywords) >= 2:
            name = "".join(keywords[:2])
        else:
            name = "新项目"
        
        # 添加时间戳
        timestamp = datetime.datetime.now().strftime("%m%d")
        return f"{name}_{timestamp}"
    
    def _generate_team_config(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """生成团队配置"""
        tech_stack = analysis["tech_stack"]
        project_type = analysis["project_type"]
        
        team = {
            "项目经理": {
                "role": "project-manager",
                "responsibility": "统一协调和管理项目进度"
            }
        }
        
        # 根据技术栈分配角色
        if "frontend" in tech_stack:
            frontend_map = {
                "vue": "vue-engineer",
                "react": "react-engineer", 
                "angular": "angular-engineer",
                "flutter": "flutter-engineer",
                "uniapp": "uniapp-engineer"
            }
            frontend_role = frontend_map.get(tech_stack["frontend"])
            if frontend_role:
                team["前端工程师"] = {
                    "role": frontend_role,
                    "responsibility": f"使用{tech_stack['frontend']}开发前端"
                }
        
        if "backend" in tech_stack:
            backend_map = {
                "fastapi": "fastapi-engineer",
                "nodejs": "nodejs-engineer",
                "go": "go-engineer",
                "rust": "rust-engineer"
            }
            backend_role = backend_map.get(tech_stack["backend"])
            if backend_role:
                team["后端工程师"] = {
                    "role": backend_role,
                    "responsibility": f"使用{tech_stack['backend']}开发后端API"
                }
        
        if "ai" in tech_stack:
            team["AI工程师"] = {
                "role": "python-ai-engineer",
                "responsibility": "开发AI模型和算法"
            }
            team["部署工程师"] = {
                "role": "cpp-ai-deployment-engineer",
                "responsibility": "优化和部署AI模型"
            }
        
        # 通用角色
        team["系统架构师"] = {
            "role": "system-architect",
            "responsibility": "设计系统架构和技术选型"
        }
        
        team["测试工程师"] = {
            "role": "test-engineer",
            "responsibility": "制定测试策略和质量保障"
        }
        
        return team
    
    def _generate_milestones(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成里程碑"""
        timeline = analysis["timeline"]
        phases = timeline["phases"]
        
        milestones = []
        current_date = datetime.datetime.now()
        
        for phase, duration in phases.items():
            # 解析持续时间
            if "天" in duration:
                days = int(duration.replace("天", ""))
            elif "周" in duration:
                days = int(duration.replace("周", "")) * 7
            else:
                days = 1
            
            milestone = {
                "phase": phase,
                "duration": duration,
                "target_date": (current_date + datetime.timedelta(days=days)).strftime("%Y-%m-%d"),
                "deliverables": self._get_phase_deliverables(phase, analysis)
            }
            
            milestones.append(milestone)
            current_date += datetime.timedelta(days=days)
        
        return milestones
    
    def _get_phase_deliverables(self, phase: str, analysis: Dict[str, Any]) -> List[str]:
        """获取阶段交付物"""
        deliverables_map = {
            "需求分析": ["需求文档", "用户故事", "技术方案"],
            "设计": ["架构设计", "UI设计", "API规范"],
            "开发": ["核心功能代码", "单元测试", "API文档"],
            "测试": ["测试报告", "Bug修复", "性能测试"],
            "部署": ["部署文档", "运行环境", "监控配置"]
        }
        
        return deliverables_map.get(phase, ["阶段性交付物"])
    
    def _generate_quality_gates(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成质量门控"""
        return [
            {
                "stage": "需求确认",
                "criteria": ["需求文档完整", "技术方案可行", "时间计划合理"],
                "reviewer": "项目经理"
            },
            {
                "stage": "设计评审",
                "criteria": ["架构设计合理", "UI设计符合要求", "技术选型合适"],
                "reviewer": "系统架构师"
            },
            {
                "stage": "代码Review",
                "criteria": ["代码规范", "功能完整", "测试覆盖"],
                "reviewer": "技术负责人"
            },
            {
                "stage": "测试通过",
                "criteria": ["功能测试通过", "性能达标", "安全扫描通过"],
                "reviewer": "测试工程师"
            }
        ]
    
    def _generate_next_steps(self, analysis: Dict[str, Any]) -> List[str]:
        """生成下一步操作"""
        return [
            "1. 确认项目配置是否符合预期",
            "2. 启动项目经理统一协调",
            f"3. 创建项目目录：{analysis['config']['project_name']}",
            "4. 初始化Git仓库",
            "5. 开始第一阶段：需求分析"
        ]

def main():
    """测试智能解析器"""
    parser = IntelligentProjectParser()
    
    test_requirements = [
        "创建一个简单的Todo应用，用Vue3和FastAPI，1周完成",
        "开发一个企业级电商系统，支持微信小程序和支付宝支付",
        "做一个AI图像识别系统，能识别猫狗，用Python开发"
    ]
    
    for req in test_requirements:
        print(f"\n{'='*60}")
        print(f"需求: {req}")
        print('='*60)
        
        result = parser.parse_requirement(req)
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()