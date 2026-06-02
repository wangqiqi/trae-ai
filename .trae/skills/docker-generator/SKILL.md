---
name: docker-generator
description: 自动生成 Dockerfile 和 docker-compose.yml 文件，支持多种技术栈的容器化部署
---

# Docker 配置生成器

## 描述
根据项目类型，自动生成标准的 Dockerfile 和 docker-compose.yml 配置文件。

## 使用场景
- 项目需要容器化部署时
- 本地开发环境需要 Docker 化时
- 需要快速配置 CI/CD 的容器化流程时

## 指令

### 支持的技术栈
- Node.js (前端、后端)
- Python (FastAPI, Django, Flask)
- Go
- Vue/React (静态文件服务)

### 生成的文件
1. **Dockerfile** - 镜像构建配置
2. **docker-compose.yml** (可选) - 多容器编排配置

### 示例结构

#### Node.js 项目
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

#### Python (FastAPI)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

## 示例

### 输出
```
✅ Docker 配置已生成！

已创建：
- Dockerfile
- docker-compose.yml

使用方法：
docker-compose up -d --build

或单独运行：
docker build -t my-app .
docker run -p 3000:3000 my-app
```
