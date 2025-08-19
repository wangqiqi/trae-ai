#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目风险自动评估引擎
基于历史数据和项目特征进行风险预测和管理
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
import datetime
import hashlib

class RiskAssessmentEngine:
    """项目风险评估引擎"""
    
    def __init__(self):
        self.base_path = Path(os.getcwd())
        self.risk_db_path = self.base_path / ".trae" / "risk-history.json"
        self.risk_rules_path = self.base_path / ".trae" / "risk-rules.json"
        
        # 初始化风险数据库
        self._init_risk_database()
        
        # 风险评分权重
        self.risk_weights = {
            "技术复杂度": 0.25,
            "时间紧迫度": 0.20,
            "团队经验": 0.15,
            "需求变更": 0.15,
            "外部依赖": 0.10,
            "合规要求": 0.15
        }
    
    def _init_risk_database(self):
        """初始化风险数据库"""
        if not self.risk_db_path.exists():
            initial_data = {
                "version": "1.0.0",
                "created_at": datetime.datetime.now().isoformat(),
                "projects": [],
                "risk_patterns": {
                    "技术风险": {
                        "高并发": {"probability": 0.8, "impact": "高", "mitigation": "云服务扩展"},
                        "AI算法": {"probability": 0.7, "impact": "中", "mitigation": "预训练模型"},
                        "新技术": {"probability": 0.6, "impact": "中", "mitigation": "技术调研"}
                    },
                    "时间风险": {
                        "紧急交付": {"probability": 0.9, "impact": "高", "mitigation": "MVP策略"},
                        "需求变更": {"probability": 0.8, "impact": "中", "mitigation": "敏捷迭代"}
                    },
                    "合规风险": {
                        "支付功能": {"probability": 0.6, "impact": "高", "mitigation": "第三方SDK"},
                        "用户数据": {"probability": 0.7, "impact": "高", "mitigation": "加密存储"}
                    }
                }
            }
            self.risk_db_path.write_text(json.dumps(initial_data, ensure_ascii=False, indent=2))
    
    def assess_project_risk(self, project_spec: Dict[str, Any]) -> Dict[str, Any]:
        """评估项目风险"""
        
        # 计算项目指纹
        project_hash = self._calculate_project_hash(project_spec)
        
        # 基础风险评估
        base_risks = self._assess_base_risks(project_spec)
        
        # 历史模式匹配
        historical_risks = self._match_historical_patterns(project_spec)
        
        # 综合风险评分
        risk_score = self._calculate_risk_score(base_risks, historical_risks)
        
        # 生成风险报告
        risk_report = {
            "project_hash": project_hash,
            "assessment_date": datetime.datetime.now().isoformat(),
            "overall_risk_level": self._get_risk_level(risk_score),
            "risk_score": risk_score,
            "risk_categories": {
                "技术风险": base_risks["技术"],
                "时间风险": base_risks["时间"],
                "团队风险": base_risks["团队"],
                "外部风险": base_risks["外部"],
                "合规风险": base_risks["合规"]
            },
            "historical_patterns": historical_risks,
            "mitigation_strategies": self._generate_mitigation_strategies(base_risks, historical_risks),
            "monitoring_alerts": self._generate_monitoring_alerts(project_spec),
            "recommendations": self._generate_recommendations(project_spec, risk_score)
        }
        
        # 保存评估结果
        self._save_risk_assessment(project_hash, risk_report)
        
        return risk_report
    
    def _calculate_project_hash(self, project_spec: Dict[str, Any]) -> str:
        """计算项目指纹"""
        content = json.dumps(project_spec, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def _assess_base_risks(self, project_spec: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """评估基础风险"""
        
        risks = {
            "技术": [],
            "时间": [],
            "团队": [],
            "外部": [],
            "合规": []
        }
        
        # 技术风险评估
        tech_stack = project_spec.get("tech_stack", {})
        features = project_spec.get("features", [])
        
        # AI相关风险
        if "ai" in tech_stack or any("ai" in str(f).lower() for f in features):
            risks["技术"].append({
                "risk": "AI模型训练风险",
                "probability": 0.7,
                "impact": "中",
                "description": "模型效果可能不达预期",
                "mitigation": "使用预训练模型，准备测试数据集"
            })
        
        # 高并发风险
        if "高并发" in str(project_spec) or "分布式" in str(project_spec):
            risks["技术"].append({
                "risk": "性能优化风险",
                "probability": 0.8,
                "impact": "高",
                "description": "系统可能无法承受高并发",
                "mitigation": "使用云服务，设计可扩展架构"
            })
        
        # 新技术风险
        new_techs = ["rust", "flutter", "go"]
        for tech in new_techs:
            if tech in str(tech_stack).lower():
                risks["技术"].append({
                    "risk": f"{tech}技术栈风险",
                    "probability": 0.6,
                    "impact": "中",
                    "description": f"团队对{tech}经验不足",
                    "mitigation": "预留学习时间，寻找最佳实践"
                })
        
        # 时间风险评估
        timeline = project_spec.get("timeline", {})
        if "1周" in str(timeline) or "快速" in str(project_spec):
            risks["时间"].append({
                "risk": "时间紧迫风险",
                "probability": 0.9,
                "impact": "高",
                "description": "开发时间可能不足",
                "mitigation": "采用MVP策略，优先核心功能"
            })
        
        # 功能复杂度风险
        feature_count = len(features)
        if feature_count > 5:
            risks["时间"].append({
                "risk": "功能复杂度过高风险",
                "probability": 0.7,
                "impact": "中",
                "description": f"{feature_count}个功能可能超出预期时间",
                "mitigation": "分阶段实现，优先核心功能"
            })
        
        # 合规风险评估
        if "支付" in str(project_spec) or "微信" in str(project_spec):
            risks["合规"].append({
                "risk": "支付合规风险",
                "probability": 0.6,
                "impact": "高",
                "description": "需要符合支付行业规范",
                "mitigation": "使用官方支付SDK，确保合规"
            })
        
        if "用户" in str(project_spec) or "登录" in str(project_spec):
            risks["合规"].append({
                "risk": "数据隐私风险",
                "probability": 0.7,
                "impact": "中",
                "description": "需要保护用户隐私数据",
                "mitigation": "数据加密存储，遵循隐私法规"
            })
        
        return risks
    
    def _match_historical_patterns(self, project_spec: Dict[str, Any]) -> List[Dict[str, Any]]:
        """匹配历史风险模式"""
        
        # 加载历史数据
        try:
            with open(self.risk_db_path, 'r', encoding='utf-8') as f:
                risk_db = json.load(f)
        except:
            risk_db = {"projects": []}
        
        patterns = []
        
        # 基于项目类型匹配
        project_type = project_spec.get("project_type", "")
        similar_projects = [
            p for p in risk_db["projects"]
            if p.get("project_type") == project_type
        ]
        
        if similar_projects:
            # 分析相似项目的风险模式
            risk_counts = {}
            for project in similar_projects:
                for risk in project.get("risks", []):
                    risk_type = risk.get("type")
                    if risk_type:
                        risk_counts[risk_type] = risk_counts.get(risk_type, 0) + 1
            
            # 找出高频风险
            for risk_type, count in risk_counts.items():
                if count >= 2:
                    patterns.append({
                        "type": "历史模式",
                        "risk": f"{project_type}项目常见{risk_type}",
                        "frequency": f"{count}次",
                        "recommendation": f"参考历史项目的{count}个类似案例"
                    })
        
        return patterns
    
    def _calculate_risk_score(self, base_risks: Dict, historical_risks: List) -> float:
        """计算综合风险评分"""
        
        total_score = 0
        max_score = 0
        
        # 基础风险评分
        risk_weights = {"低": 1, "中": 3, "高": 5}
        
        for category, risks in base_risks.items():
            for risk in risks:
                probability = risk.get("probability", 0.5)
                impact = risk_weights.get(risk.get("impact", "中"), 3)
                total_score += probability * impact
                max_score += 5
        
        # 历史风险加权
        historical_weight = min(len(historical_risks) * 0.1, 0.3)
        total_score *= (1 + historical_weight)
        
        # 归一化到0-100
        risk_score = min((total_score / max_score) * 100, 100)
        return round(risk_score, 2)
    
    def _get_risk_level(self, score: float) -> str:
        """根据分数获取风险等级"""
        if score <= 30:
            return "低风险"
        elif score <= 60:
            return "中风险"
        elif score <= 80:
            return "高风险"
        else:
            return "极高风险"
    
    def _generate_mitigation_strategies(self, base_risks: Dict, historical_risks: List) -> List[Dict[str, Any]]:
        """生成风险缓解策略"""
        
        strategies = []
        
        # 按优先级排序风险
        all_risks = []
        for category, risks in base_risks.items():
            for risk in risks:
                risk["category"] = category
                all_risks.append(risk)
        
        # 按影响程度排序
        impact_order = {"高": 3, "中": 2, "低": 1}
        all_risks.sort(key=lambda x: impact_order.get(x.get("impact", "中"), 2), reverse=True)
        
        for risk in all_risks[:5]:  # 只处理前5个高风险
            strategies.append({
                "risk": risk["risk"],
                "priority": "高" if risk["impact"] == "高" else "中",
                "strategy": risk.get("mitigation", "制定详细计划"),
                "timeline": "立即执行",
                "owner": self._assign_risk_owner(risk["category"])
            })
        
        return strategies
    
    def _assign_risk_owner(self, category: str) -> str:
        """分配风险负责人"""
        owners = {
            "技术": "系统架构师",
            "时间": "项目经理",
            "团队": "项目经理",
            "外部": "项目经理",
            "合规": "产品经理"
        }
        return owners.get(category, "项目经理")
    
    def _generate_monitoring_alerts(self, project_spec: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成监控告警"""
        
        alerts = []
        
        # 时间监控
        timeline = project_spec.get("timeline", {})
        if "1周" in str(timeline):
            alerts.append({
                "type": "时间预警",
                "condition": "开发进度延迟超过1天",
                "action": "立即调整计划或缩减功能",
                "notify": ["项目经理", "相关工程师"]
            })
        
        # 技术监控
        tech_stack = project_spec.get("tech_stack", {})
        if "ai" in str(tech_stack):
            alerts.append({
                "type": "技术预警",
                "condition": "AI模型准确率低于80%",
                "action": "调整模型参数或更换算法",
                "notify": ["AI工程师", "系统架构师"]
            })
        
        # 质量监控
        alerts.extend([
            {
                "type": "质量预警",
                "condition": "测试覆盖率低于80%",
                "action": "增加测试用例",
                "notify": ["测试工程师"]
            },
            {
                "type": "部署预警",
                "condition": "部署失败超过2次",
                "action": "回滚版本并检查配置",
                "notify": ["运维工程师"]
            }
        ])
        
        return alerts
    
    def _generate_recommendations(self, project_spec: Dict[str, Any], risk_score: float) -> List[str]:
        """生成项目建议"""
        
        recommendations = []
        
        # 基于风险评分的建议
        if risk_score > 80:
            recommendations.extend([
                "建议采用分阶段交付策略",
                "增加技术调研和原型验证阶段",
                "考虑使用更成熟的技术栈",
                "建立每日进度同步机制"
            ])
        elif risk_score > 60:
            recommendations.extend([
                "采用敏捷开发方法，每3天一个迭代",
                "建立风险监控仪表板",
                "准备备选技术方案"
            ])
        else:
            recommendations.extend([
                "按标准流程执行即可",
                "重点关注代码质量",
                "保持现有开发节奏"
            ])
        
        # 基于项目特征的建议
        project_type = project_spec.get("project_type", "")
        if project_type == "mvp_web":
            recommendations.append("优先实现核心功能，界面简洁为主")
        elif project_type == "ai_system":
            recommendations.append("准备测试数据集，建立模型评估标准")
        elif project_type == "mini_program":
            recommendations.append("提前了解各平台审核要求")
        
        return recommendations
    
    def _save_risk_assessment(self, project_hash: str, assessment: Dict[str, Any]):
        """保存风险评估结果"""
        try:
            with open(self.risk_db_path, 'r', encoding='utf-8') as f:
                risk_db = json.load(f)
        except:
            risk_db = {"projects": []}
        
        # 添加新项目记录
        project_record = {
            "project_hash": project_hash,
            "assessment_date": datetime.datetime.now().isoformat(),
            "risk_score": assessment["risk_score"],
            "risk_level": assessment["overall_risk_level"],
            "risks": assessment["risk_categories"],
            "status": "assessed"
        }
        
        risk_db["projects"].append(project_record)
        
        # 保存更新
        with open(self.risk_db_path, 'w', encoding='utf-8') as f:
            json.dump(risk_db, f, ensure_ascii=False, indent=2)
    
    def get_risk_dashboard(self) -> Dict[str, Any]:
        """获取风险仪表板"""
        try:
            with open(self.risk_db_path, 'r', encoding='utf-8') as f:
                risk_db = json.load(f)
        except:
            return {"error": "风险数据库不存在"}
        
        projects = risk_db.get("projects", [])
        
        # 统计信息
        total_projects = len(projects)
        risk_levels = {"低风险": 0, "中风险": 0, "高风险": 0, "极高风险": 0}
        
        for project in projects:
            level = project.get("risk_level", "中风险")
            risk_levels[level] = risk_levels.get(level, 0) + 1
        
        return {
            "total_projects": total_projects,
            "risk_distribution": risk_levels,
            "recent_projects": projects[-5:] if projects else [],
            "risk_trends": self._calculate_risk_trends(projects)
        }
    
    def _calculate_risk_trends(self, projects: List[Dict]) -> List[Dict[str, Any]]:
        """计算风险趋势"""
        if not projects:
            return []
        
        # 按月份分组
        monthly_trends = {}
        for project in projects:
            date = project.get("assessment_date", "")
            if date:
                month = date[:7]  # YYYY-MM
                score = project.get("risk_score", 50)
                
                if month not in monthly_trends:
                    monthly_trends[month] = []
                monthly_trends[month].append(score)
        
        # 计算每月平均风险
        trends = []
        for month, scores in sorted(monthly_trends.items()):
            avg_score = sum(scores) / len(scores)
            trends.append({
                "month": month,
                "avg_risk_score": round(avg_score, 2),
                "project_count": len(scores)
            })
        
        return trends

def main():
    """测试风险评估引擎"""
    engine = RiskAssessmentEngine()
    
    # 测试项目规格
    test_project = {
        "project_type": "ai_system",
        "tech_stack": {
            "frontend": "vue",
            "backend": "fastapi",
            "ai": "python_ai"
        },
        "features": ["图像识别", "用户管理", "数据上传"],
        "timeline": {
            "total": "4-6周",
            "phases": {
                "需求分析": "1周",
                "开发": "3-4周",
                "测试": "1周"
            }
        }
    }
    
    print("项目风险评估结果：")
    result = engine.assess_project_risk(test_project)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    print("\n风险仪表板：")
    dashboard = engine.get_risk_dashboard()
    print(json.dumps(dashboard, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()