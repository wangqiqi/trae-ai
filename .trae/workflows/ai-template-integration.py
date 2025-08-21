#!/usr/bin/env python3
"""
Trae AI 超级团队 - AI智能体模板集成模块

功能：
1. 智能体根据模板自动执行任务
2. 模板内容智能分析和优化
3. AI专家协作生成项目文档
4. 实时模板内容生成和更新

作者：Trae AI团队
版本：v3.0
"""

import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime

class AITemplateIntegration:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.templates_path = self.base_path / "templates"
        self.project_root = Path.cwd()
        
    def analyze_template_with_ai(self, template_name, project_context):
        """使用AI智能体分析模板内容"""
        template_file = self.templates_path / f"{template_name}.md"
        
        if not template_file.exists():
            return {"error": f"模板文件不存在: {template_name}"}
            
        # 读取模板内容
        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()
            
        # 根据模板类型选择AI智能体
        ai_agent = self.select_ai_agent(template_name)
        
        # 构建AI提示
        prompt = self.build_ai_prompt(template_name, template_content, project_context)
        
        # 调用AI智能体
        return self.call_ai_agent(ai_agent, prompt)
    
    def select_ai_agent(self, template_name):
        """根据模板类型选择最合适的AI智能体"""
        agent_mapping = {
            "requirements-template": "产品经理",
            "api-spec-template": "FastAPI工程师",
            "database-design-template": "系统架构师",
            "test-plan-template": "测试工程师",
            "deployment-template": "DevOps工程师",
            "code-review-template": "技术文档工程师",
            "project-init-template": "项目经理"
        }
        
        return agent_mapping.get(template_name, "产品经理")
    
    def build_ai_prompt(self, template_name, template_content, project_context):
        """构建AI提示"""
        prompts = {
            "requirements-template": f"""
            作为产品经理，请基于以下项目上下文，完善需求文档：
            
            项目信息：{json.dumps(project_context, ensure_ascii=False, indent=2)}
            
            模板内容：
            {template_content[:1000]}...
            
            请提供：
            1. 详细的功能需求描述
            2. 用户故事和用例
            3. 技术需求细化
            4. 验收标准具体化
            5. 风险评估
            """,
            
            "api-spec-template": f"""
            作为FastAPI工程师，请基于项目需求设计完整的API规范：
            
            项目信息：{json.dumps(project_context, ensure_ascii=False, indent=2)}
            
            请设计：
            1. RESTful API端点
            2. 请求/响应格式
            3. 认证授权方案
            4. 错误处理
            5. API版本管理
            """,
            
            "database-design-template": f"""
            作为系统架构师，请设计数据库架构：
            
            项目信息：{json.dumps(project_context, ensure_ascii=False, indent=2)}
            
            请设计：
            1. 数据模型和关系
            2. 数据库选型理由
            3. 表结构设计
            4. 索引策略
            5. 数据安全方案
            """,
            
            "test-plan-template": f"""
            作为测试工程师，请制定测试策略：
            
            项目信息：{json.dumps(project_context, ensure_ascii=False, indent=2)}
            
            请制定：
            1. 测试范围和策略
            2. 测试用例设计
            3. 自动化测试方案
            4. 性能测试计划
            5. 测试工具选择
            """,
            
            "deployment-template": f"""
            作为DevOps工程师，请设计部署方案：
            
            项目信息：{json.dumps(project_context, ensure_ascii=False, indent=2)}
            
            请设计：
            1. 部署架构
            2. CI/CD流程
            3. 容器化方案
            4. 监控告警
            5. 回滚策略
            """
        }
        
        return prompts.get(template_name, prompts["requirements-template"])
    
    def call_ai_agent(self, agent_name, prompt):
        """调用AI智能体"""
        try:
            # 构建调用命令
            cmd = [
                sys.executable,
                str(self.base_path / "trae-console.py"),
                "--agent",
                agent_name,
                "--prompt",
                prompt
            ]
            
            # 执行命令
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "content": result.stdout,
                    "agent": agent_name
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr,
                    "agent": agent_name
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": agent_name
            }
    
    def generate_smart_content(self, template_name, project_info):
        """生成智能内容"""
        # 分析项目上下文
        context = {
            "project_name": project_info.get("name", "MyProject"),
            "project_type": project_info.get("type", "web"),
            "tech_stack": project_info.get("tech_stack", []),
            "features": project_info.get("features", []),
            "target_users": project_info.get("target_users", "general"),
            "timeline": project_info.get("timeline", "2 weeks")
        }
        
        # 调用AI分析
        ai_result = self.analyze_template_with_ai(template_name, context)
        
        if ai_result.get("success"):
            # 生成增强内容
            enhanced_content = self.enhance_template_content(
                template_name, 
                ai_result["content"], 
                context
            )
            return enhanced_content
        else:
            # 使用默认模板
            return self.get_default_template_content(template_name, context)
    
    def enhance_template_content(self, template_name, ai_content, context):
        """增强模板内容"""
        enhanced_header = f"""# {template_name.replace('-', ' ').title()}

> **AI增强版本** - 由 {self.select_ai_agent(template_name)} 智能生成  
> **生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
> **项目**: {context['project_name']}  
> **技术栈**: {', '.join(context['tech_stack'])}

---

"""
        
        return enhanced_header + ai_content
    
    def get_default_template_content(self, template_name, context):
        """获取默认模板内容"""
        template_file = self.templates_path / f"{template_name}.md"
        
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 替换基础变量
            content = content.replace("{{PROJECT_NAME}}", context["project_name"])
            content = content.replace("{{TECH_STACK}}", ", ".join(context["tech_stack"]))
            content = content.replace("{{CURRENT_DATE}}", datetime.now().strftime("%Y-%m-%d"))
            
            return content
        
        return f"# {template_name}\n\n默认模板内容"
    
    def create_full_project_kit(self, project_name, project_type, features):
        """创建完整项目套件"""
        project_info = {
            "name": project_name,
            "type": project_type,
            "tech_stack": self.get_tech_stack(project_type),
            "features": features,
            "target_users": "end_users",
            "timeline": "4 weeks"
        }
        
        # 定义项目套件模板
        kit_templates = {
            "vue3": ["project-init-template", "requirements-template", "api-spec-template", "test-plan-template"],
            "react": ["project-init-template", "requirements-template", "api-spec-template", "test-plan-template"],
            "fastapi": ["project-init-template", "requirements-template", "api-spec-template", "database-design-template", "test-plan-template", "deployment-template"],
            "flutter": ["project-init-template", "requirements-template", "test-plan-template"],
            "node": ["project-init-template", "requirements-template", "api-spec-template", "test-plan-template", "deployment-template"]
        }
        
        templates = kit_templates.get(project_type, ["project-init-template", "requirements-template"])
        
        print(f"🚀 创建 {project_name} 完整项目套件...")
        
        # 创建项目目录
        project_path = Path.cwd() / project_name
        project_path.mkdir(exist_ok=True)
        
        # 生成所有模板
        for template in templates:
            content = self.generate_smart_content(template, project_info)
            
            # 保存文件
            filename = self.get_output_filename(template)
            output_path = project_path / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"✅ 生成: {filename}")
        
        # 创建项目配置文件
        self.create_project_config(project_path, project_info)
        
        print(f"🎉 项目套件创建完成！")
        print(f"📁 项目路径: {project_path}")
        
        return project_path
    
    def get_tech_stack(self, project_type):
        """获取技术栈"""
        stacks = {
            "vue3": ["Vue3", "TypeScript", "Vite", "Pinia", "Vue Router", "Axios"],
            "react": ["React18", "TypeScript", "Next.js", "Redux", "React Router", "Axios"],
            "fastapi": ["Python", "FastAPI", "SQLAlchemy", "PostgreSQL", "Docker", "Redis"],
            "flutter": ["Flutter", "Dart", "Firebase", "Provider", "GetX", "Dio"],
            "node": ["Node.js", "Express", "TypeScript", "MongoDB", "Docker", "Redis"]
        }
        return stacks.get(project_type, ["通用技术栈"])
    
    def get_output_filename(self, template_name):
        """获取输出文件名"""
        filename_map = {
            "project-init-template": "docs/01-项目初始化.md",
            "requirements-template": "docs/02-需求文档.md",
            "api-spec-template": "docs/03-API规范.md",
            "database-design-template": "docs/04-数据库设计.md",
            "test-plan-template": "docs/05-测试计划.md",
            "deployment-template": "docs/06-部署方案.md",
            "code-review-template": "docs/07-代码审查.md"
        }
        return filename_map.get(template_name, f"docs/{template_name}.md")
    
    def create_project_config(self, project_path, project_info):
        """创建项目配置文件"""
        config = {
            "project_name": project_info["name"],
            "project_type": project_info["type"],
            "tech_stack": project_info["tech_stack"],
            "features": project_info["features"],
            "created_at": datetime.now().isoformat(),
            "template_version": "3.0",
            "ai_enhanced": True
        }
        
        config_path = project_path / ".trae-project.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
            
        print("⚙️ 项目配置文件已创建")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="AI模板集成模块")
    parser.add_argument("action", choices=["enhance", "kit", "analyze"], 
                       help="操作类型")
    parser.add_argument("--template", help="模板名称")
    parser.add_argument("--project", help="项目名称")
    parser.add_argument("--type", choices=["vue3", "react", "fastapi", "flutter", "node"], 
                       help="项目类型")
    parser.add_argument("--features", nargs="+", default=[], 
                       help="项目功能列表")
    
    args = parser.parse_args()
    
    integration = AITemplateIntegration()
    
    if args.action == "enhance" and args.template:
        # 增强模板内容
        project_info = {"name": "MyProject", "type": "web"}
        content = integration.generate_smart_content(args.template, project_info)
        print(content)
        
    elif args.action == "kit" and args.project and args.type:
        # 创建完整项目套件
        integration.create_full_project_kit(
            args.project, 
            args.type, 
            args.features
        )
        
    elif args.action == "analyze" and args.template:
        # 分析模板
        project_info = {"name": "Analysis", "type": "analysis"}
        result = integration.analyze_template_with_ai(args.template, project_info)
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()