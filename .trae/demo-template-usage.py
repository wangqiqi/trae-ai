#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trae AI 模板应用演示脚本

演示如何在实际项目中使用模板自动化系统
"""

import os
import json
from pathlib import Path
from datetime import datetime

class TemplateDemo:
    """模板应用演示类"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.templates_dir = self.base_dir / "templates"
        self.demo_projects_dir = self.base_dir / "demo-projects"
        
        self.demo_projects_dir.mkdir(exist_ok=True)
    
    def demo_vue3_ecommerce(self):
        """演示Vue3电商项目模板应用"""
        print("🎯 演示：Vue3电商网站项目创建")
        
        project_name = f"vue3-ecommerce-demo-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        project_dir = self.demo_projects_dir / project_name
        
        # 创建项目结构
        project_dir.mkdir(exist_ok=True)
        
        # 应用模板
        templates_to_apply = [
            "project-init-template.md",
            "requirements-template.md", 
            "api-spec-template.md",
            "database-design-template.md",
            "test-plan-template.md"
        ]
        
        print(f"📁 创建项目：{project_name}")
        print(f"📍 位置：{project_dir}")
        
        for template_name in templates_to_apply:
            template_path = self.templates_dir / template_name
            if template_path.exists():
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 智能填充内容
                filled_content = self.fill_template_content(content, {
                    'project_name': project_name,
                    'project_type': 'Vue3电商网站',
                    'tech_stack': 'Vue3 + TypeScript + Vite + Pinia',
                    'features': ['用户认证', '商品管理', '购物车', '支付功能', '订单管理'],
                    'team_size': '3-5人',
                    'timeline': '4周'
                })
                
                # 保存到项目目录
                output_file = project_dir / template_name.replace('-template.md', '.md')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(filled_content)
                
                print(f"✅ 已应用：{template_name}")
        
        # 创建项目结构
        self.create_project_structure(project_dir, 'vue3')
        
        return project_dir
    
    def demo_fastapi_user_system(self):
        """演示FastAPI用户系统模板应用"""
        print("🎯 演示：FastAPI用户系统项目创建")
        
        project_name = f"fastapi-user-system-demo-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        project_dir = self.demo_projects_dir / project_name
        
        project_dir.mkdir(exist_ok=True)
        
        templates_to_apply = [
            "project-init-template.md",
            "requirements-template.md",
            "api-spec-template.md", 
            "database-design-template.md",
            "deployment-template.md",
            "test-plan-template.md"
        ]
        
        print(f"📁 创建项目：{project_name}")
        print(f"📍 位置：{project_dir}")
        
        for template_name in templates_to_apply:
            template_path = self.templates_dir / template_name
            if template_path.exists():
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                filled_content = self.fill_template_content(content, {
                    'project_name': project_name,
                    'project_type': 'FastAPI用户认证系统',
                    'tech_stack': 'FastAPI + SQLAlchemy + PostgreSQL + Docker',
                    'features': ['用户注册', '登录认证', '权限管理', 'JWT令牌', '密码重置'],
                    'team_size': '2-3人',
                    'timeline': '2周'
                })
                
                output_file = project_dir / template_name.replace('-template.md', '.md')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(filled_content)
                
                print(f"✅ 已应用：{template_name}")
        
        self.create_project_structure(project_dir, 'fastapi')
        
        return project_dir
    
    def fill_template_content(self, template_content: str, context: dict) -> str:
        """智能填充模板内容"""
        content = template_content
        
        # 基础替换
        for key, value in context.items():
            if isinstance(value, list):
                value = '\n'.join(f"- {item}" for item in value)
            content = content.replace(f"{{{key}}}", str(value))
            content = content.replace(f"{{ {key} }}", str(value))
        
        # 智能填充示例内容
        if '需求文档' in content:
            content = self.add_requirements_examples(content, context)
        
        if 'API规范' in content:
            content = self.add_api_examples(content, context)
        
        if '数据库设计' in content:
            content = self.add_database_examples(content, context)
        
        return content
    
    def add_requirements_examples(self, content: str, context: dict) -> str:
        """添加需求文档示例"""
        examples = f"""

## 具体需求示例

### 用户故事
- 作为{context['project_type']}的用户，我需要{context['features'][0]}功能，以便能够...
- 作为管理员，我需要管理{context['features'][1]}，以便...

### 功能清单
{context['features']}

### 非功能需求
- 性能：页面加载时间 < 2秒
- 安全：用户数据加密存储
- 可用性：99.9%在线时间

### 验收标准
- [ ] 用户能够成功注册和登录
- [ ] {context['features'][0]}功能正常工作
- [ ] 系统响应时间在可接受范围内

### 时间规划
- 第1周：项目初始化和基础架构
- 第2周：{context['features'][0]}功能开发
- 第3周：{context['features'][1]}功能开发
- 第4周：测试和部署

"""
        return content + examples
    
    def add_api_examples(self, content: str, context: dict) -> str:
        """添加API示例"""
        examples = f"""

## 具体API接口示例

### 用户认证接口
```
POST /api/auth/register
{
  "username": "string",
  "email": "string",
  "password": "string"
}

POST /api/auth/login
{
  "email": "string",
  "password": "string"
}
```

### {context['features'][0]}接口
```
GET /api/{context['features'][0].lower()}
POST /api/{context['features'][0].lower()}
PUT /api/{context['features'][0].lower()}/:id
DELETE /api/{context['features'][0].lower()}/:id
```

"""
        return content + examples
    
    def add_database_examples(self, content: str, context: dict) -> str:
        """添加数据库示例"""
        examples = f"""

## 具体数据表设计

### 用户表 (users)
| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | BIGINT | 主键 |
| username | VARCHAR(50) | 用户名 |
| email | VARCHAR(100) | 邮箱 |
| password_hash | VARCHAR(255) | 密码哈希 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### {context['features'][0]}表
| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | BIGINT | 主键 |
| user_id | BIGINT | 用户ID |
| title | VARCHAR(255) | 标题 |
| description | TEXT | 描述 |
| status | VARCHAR(20) | 状态 |
| created_at | TIMESTAMP | 创建时间 |

"""
        return content + examples
    
    def create_project_structure(self, project_dir: Path, project_type: str):
        """创建项目基础结构"""
        structure = {
            'vue3': {
                'src': ['components', 'views', 'store', 'router', 'utils'],
                'public': [],
                'docs': [],
                'tests': []
            },
            'fastapi': {
                'app': ['api', 'models', 'schemas', 'utils'],
                'tests': [],
                'migrations': [],
                'docs': []
            }
        }
        
        if project_type in structure:
            for folder, subfolders in structure[project_type].items():
                folder_path = project_dir / folder
                folder_path.mkdir(exist_ok=True)
                
                for subfolder in subfolders:
                    (folder_path / subfolder).mkdir(exist_ok=True)
        
        # 创建README
        readme_content = f"""# {project_dir.name}

这是一个使用Trae AI模板自动生成的项目。

## 项目特点
- ✅ 使用Trae AI模板系统
- ✅ 包含完整的需求文档
- ✅ 包含API规范
- ✅ 包含数据库设计
- ✅ 包含测试计划

## 快速开始

```bash
# 安装依赖
npm install  # 或 pip install -r requirements.txt

# 启动开发服务器
npm run dev  # 或 python app.py
```

## 项目结构

- `docs/` - 项目文档
- `src/` - 源代码
- `tests/` - 测试文件
- `requirements.md` - 需求文档
- `api-spec.md` - API规范
- `database-design.md` - 数据库设计
- `test-plan.md` - 测试计划

## 使用Trae AI

```bash
# 启动控制台
python .trae/quick-start.py

# 继续开发
"@产品经理 帮我设计商品详情页"
"@Vue工程师 创建购物车组件"
```
"""
        
        with open(project_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def run_demo(self):
        """运行完整演示"""
        print("🎬 Trae AI 模板自动化演示开始")
        print("=" * 50)
        
        # 演示1：Vue3电商项目
        vue_project = self.demo_vue3_ecommerce()
        
        print("\n" + "=" * 50)
        
        # 演示2：FastAPI用户系统
        fastapi_project = self.demo_fastapi_user_system()
        
        print("\n" + "=" * 50)
        print("✅ 演示完成！")
        print(f"📁 演示项目已创建在: {self.demo_projects_dir}")
        print(f"🎯 Vue3项目: {vue_project.name}")
        print(f"🎯 FastAPI项目: {fastapi_project.name}")
        
        print("\n💡 下一步操作：")
        print("1. 查看项目文档")
        print("2. 启动Trae AI控制台: python .trae/quick-start.py")
        print("3. 继续开发: @产品经理 @Vue工程师 @Python工程师")

if __name__ == "__main__":
    demo = TemplateDemo()
    demo.run_demo()