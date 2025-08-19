#!/usr/bin/env python3
"""
SOLO智能开发控制台API服务器
提供Web界面的后端服务，支持项目管理、风险监控、智能分析等功能
"""

import os
import sys
import json
import asyncio
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import uvicorn

try:
    from intelligent_project_parser import IntelligentProjectParser
    from risk_assessment_engine import RiskAssessmentEngine
except ImportError as e:
    print(f"警告: 无法导入模块 - {e}")
    # 创建模拟类用于测试
    class IntelligentProjectParser:
        def parse_requirement(self, requirement: str) -> Dict:
            return {
                "project_name": "示例项目",
                "project_type": "web_application",
                "tech_stack": {"frontend": "vue", "backend": "fastapi", "database": "sqlite"},
                "timeline": "2-3周",
                "features": ["用户管理", "数据展示", "API接口"]
            }
    
    class RiskAssessmentEngine:
        def assess_project(self, project_data: Dict) -> Dict:
            return {
                "risk_score": 35,
                "risk_level": "低风险",
                "risks": [],
                "recommendations": ["建议增加测试", "注意代码质量"]
            }

# 创建全局app实例
app = FastAPI(title="SOLO智能开发控制台", version="2.0.0")

# 初始化核心组件
project_parser = IntelligentProjectParser()
risk_engine = RiskAssessmentEngine()

# 项目数据存储
projects_file = Path("../data/projects.json")
risks_file = Path("../data/risks.json")

# 确保数据文件存在
for file_path in [projects_file, risks_file]:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if not file_path.exists():
        file_path.write_text('[]')

def load_data(file_path: Path) -> List[Dict]:
    """加载JSON数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(file_path: Path, data: List[Dict]):
    """保存JSON数据"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 配置中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 设置路由

@app.get("/")
async def root():
    """根路径返回Web界面"""
    return FileResponse("../templates/solo-dashboard.html")

@app.get("/api/stats")
async def get_stats():
    """获取项目统计信息"""
    projects = load_data(projects_file)
    
    total = len(projects)
    active = len([p for p in projects if p.get('status') == 'active'])
    completed = len([p for p in projects if p.get('status') == 'completed'])
    
    risks = load_data(risks_file)
    risk_alerts = len([r for r in risks if r.get('level') in ['high', 'critical']])
    
    return {
        "total_projects": total,
        "active_projects": active,
        "completed_projects": completed,
        "risk_alerts": risk_alerts,
        "last_updated": datetime.now().isoformat()
    }

@app.get("/api/projects")
async def get_projects():
    """获取项目列表"""
    return load_data(projects_file)

@app.post("/api/projects")
async def create_project(project_data: Dict[str, Any]):
    """创建新项目"""
    projects = load_data(projects_file)
    
    # 生成项目ID
    project_id = f"proj_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    project_data['id'] = project_id
    project_data['created_at'] = datetime.now().isoformat()
    project_data['status'] = 'planning'
    
    # 智能分析需求
    if 'requirement' in project_data:
        analysis = project_parser.parse_requirement(project_data['requirement'])
        project_data.update(analysis)
    
    # 风险评估
    risk_assessment = risk_engine.assess_project(project_data)
    project_data['risk'] = risk_assessment
    
    projects.append(project_data)
    save_data(projects_file, projects)
    
    return {"project_id": project_id, "status": "created"}

@app.post("/api/analyze-requirement")
async def analyze_requirement(requirement: Dict[str, str]):
    """智能分析项目需求"""
    if 'text' not in requirement:
        raise HTTPException(status_code=400, detail="需求文本不能为空")
    
    analysis = project_parser.parse_requirement(requirement['text'])
    risk = risk_engine.assess_project(analysis)
    
    return {
        "analysis": analysis,
        "risk": risk,
        "recommendations": ["Vue3 + FastAPI是推荐组合", "MVP开发建议优先核心功能"]
    }

@app.get("/api/templates")
async def get_templates():
    """获取项目模板"""
    templates = [
        {
            "id": "todo",
            "name": "Todo应用",
            "description": "简单的任务管理应用",
            "tech_stack": {"frontend": "vue", "backend": "fastapi"},
            "timeline": "1-2周"
        },
        {
            "id": "ecommerce",
            "name": "电商网站",
            "description": "完整的电商解决方案",
            "tech_stack": {"frontend": "vue", "backend": "fastapi"},
            "timeline": "4-6周"
        },
        {
            "id": "blog",
            "name": "博客系统",
            "description": "个人博客平台",
            "tech_stack": {"frontend": "react", "backend": "node"},
            "timeline": "3-4周"
        },
        {
            "id": "ai",
            "name": "AI识别系统",
            "description": "AI图像识别应用",
            "tech_stack": {"frontend": "vue", "backend": "fastapi", "ai": "tensorflow"},
            "timeline": "6-8周"
        }
    ]
    return templates

@app.get("/api/health")
async def health_check():
    """系统健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

# 启动服务器
if __name__ == "__main__":
    uvicorn.run(
        "solo-api-server:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )