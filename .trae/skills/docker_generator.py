#!/usr/bin/env python3
"""
Dockerfile 生成器技能 - 自动生成 Dockerfile 和 docker-compose
"""
from pathlib import Path
from typing import Dict, Any

def execute(**kwargs) -> Dict[str, Any]:
    """
    生成 Dockerfile
    
    Args:
        project_type: 项目类型 (python/node/vue/react/fastapi等)
        port: 端口号
        output_dir: 输出目录
    
    Returns:
        生成结果
    """
    project_type = kwargs.get('project_type', 'python')
    port = kwargs.get('port', '8000')
    output_dir = kwargs.get('output_dir', '.')
    
    results = {
        'success': True,
        'files': [],
        'message': ''
    }
    
    try:
        # 生成 Dockerfile
        dockerfile_content = generate_dockerfile(project_type, port)
        dockerfile_path = Path(output_dir) / 'Dockerfile'
        
        with open(dockerfile_path, 'w', encoding='utf-8') as f:
            f.write(dockerfile_content)
        
        results['files'].append(str(dockerfile_path))
        
        # 如果是 web 应用，生成 docker-compose.yml
        if project_type in ['vue', 'react', 'node']:
            compose_content = generate_docker_compose(project_type, port)
            compose_path = Path(output_dir) / 'docker-compose.yml'
            
            with open(compose_path, 'w', encoding='utf-8') as f:
                f.write(compose_content)
            
            results['files'].append(str(compose_path))
        
        results['message'] = f'✅ Docker 配置已生成！创建了 {len(results["files"])} 个文件'
        
    except Exception as e:
        results['success'] = False
        results['message'] = f'❌ 生成失败: {e}'
    
    return results

def generate_dockerfile(project_type: str, port: str) -> str:
    """生成 Dockerfile"""
    
    templates = {
        'python': '''# Python Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE {port}

# 启动命令
CMD ["python", "main.py"]
'''.format(port=port),

        'fastapi': '''# FastAPI Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 安装 uvicorn
RUN pip install uvicorn

# 暴露端口
EXPOSE {port}

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "{port}"]
'''.format(port=port),

        'vue': '''# Vue Dockerfile (多阶段构建)
FROM node:18-alpine AS builder

WORKDIR /app

# 复制 package.json
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制源代码
COPY . .

# 构建项目
RUN npm run build

# 生产镜像
FROM nginx:alpine

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE {port}

CMD ["nginx", "-g", "daemon off;"]
'''.format(port=port),

        'react': '''# React Dockerfile (多阶段构建)
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE {port}

CMD ["nginx", "-g", "daemon off;"]
'''.format(port=port),

        'node': '''# Node.js Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE {port}

CMD ["node", "index.js"]
'''.format(port=port)
    }
    
    return templates.get(project_type, templates['python'])

def generate_docker_compose(project_type: str, port: str) -> str:
    """生成 docker-compose.yml"""
    
    return f'''version: '3.8'

services:
  app:
    build: .
    ports:
      - "{port}:{port}"
    environment:
      - NODE_ENV=production
    restart: unless-stopped
'''
