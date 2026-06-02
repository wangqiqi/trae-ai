#!/usr/bin/env python3
# 🎯 云端部署工程师
# 一键部署到主流云平台

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class CloudDeployEngineer:
    """
    云端部署工程师
    职责：一键部署应用到主流云平台
    功能：Docker镜像构建、云平台配置、CI/CD流水线配置、部署验证
    """
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.trae_path = self.project_root / ".trae"
        self.deploy_config = self.trae_path / "deploy-config.json"
        self.load_config()
    
    def load_config(self):
        """加载部署配置"""
        if self.deploy_config.exists():
            with open(self.deploy_config, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "cloud_provider": "docker",
                "registry": "docker.io",
                "image_name": "my-app",
                "image_tag": "latest",
                "deploy_targets": [],
                "env_vars": {}
            }
    
    def save_config(self):
        """保存部署配置"""
        with open(self.deploy_config, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def check_docker_installed(self) -> bool:
        """检查Docker是否安装"""
        try:
            result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def check_cloud_cli(self, provider: str) -> bool:
        """检查云平台CLI是否安装"""
        cli_commands = {
            "aws": ["aws", "--version"],
            "azure": ["az", "--version"],
            "gcp": ["gcloud", "--version"],
            "aliyun": ["aliyun", "--version"],
            "tencent": ["tcli", "--version"]
        }
        
        if provider in cli_commands:
            try:
                result = subprocess.run(cli_commands[provider], capture_output=True, text=True)
                return result.returncode == 0
            except:
                return False
        return False
    
    def build_docker_image(self, dockerfile_path: str = "Dockerfile") -> str:
        """构建Docker镜像"""
        if not self.check_docker_installed():
            return "❌ Docker未安装，请先安装Docker"
        
        image_name = f"{self.config['image_name']}:{self.config['image_tag']}"
        
        try:
            result = subprocess.run(
                ["docker", "build", "-t", image_name, "-f", dockerfile_path, "."],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                self.config["last_build"] = datetime.now().isoformat()
                self.save_config()
                return f"✅ Docker镜像构建成功: {image_name}"
            else:
                return f"❌ Docker镜像构建失败:\n{result.stderr}"
        except Exception as e:
            return f"❌ 构建失败: {str(e)}"
    
    def push_docker_image(self) -> str:
        """推送Docker镜像到仓库"""
        if not self.check_docker_installed():
            return "❌ Docker未安装，请先安装Docker"
        
        full_image_name = f"{self.config['registry']}/{self.config['image_name']}:{self.config['image_tag']}"
        
        try:
            subprocess.run(["docker", "tag", f"{self.config['image_name']}:{self.config['image_tag']}", full_image_name])
            
            result = subprocess.run(
                ["docker", "push", full_image_name],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return f"✅ 镜像推送成功: {full_image_name}"
            else:
                return f"❌ 镜像推送失败:\n{result.stderr}"
        except Exception as e:
            return f"❌ 推送失败: {str(e)}"
    
    def generate_dockerfile(self, project_type: str = "python") -> str:
        """生成Dockerfile"""
        dockerfiles = {
            "python": """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
""",
            "node": """FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
""",
            "vue": """FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
""",
            "fastapi": """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        }
        
        content = dockerfiles.get(project_type, dockerfiles["python"])
        dockerfile_path = self.project_root / "Dockerfile"
        
        with open(dockerfile_path, 'w') as f:
            f.write(content)
        
        return f"✅ Dockerfile已生成: {dockerfile_path}"
    
    def generate_kubernetes_config(self, app_name: str = "my-app") -> str:
        """生成Kubernetes部署配置"""
        k8s_config = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}
  labels:
    app: {app_name}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {app_name}
  template:
    metadata:
      labels:
        app: {app_name}
    spec:
      containers:
      - name: {app_name}
        image: {self.config['registry']}/{self.config['image_name']}:{self.config['image_tag']}
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: {app_name}-service
spec:
  selector:
    app: {app_name}
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
"""
        
        k8s_path = self.project_root / "deployment.yaml"
        
        with open(k8s_path, 'w') as f:
            f.write(k8s_config)
        
        return f"✅ Kubernetes配置已生成: {k8s_path}"
    
    def deploy_to_kubernetes(self) -> str:
        """部署到Kubernetes"""
        try:
            result = subprocess.run(
                ["kubectl", "apply", "-f", "deployment.yaml"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                return "✅ 部署到Kubernetes成功"
            else:
                return f"❌ 部署失败:\n{result.stderr}"
        except Exception as e:
            return f"❌ 部署失败: {str(e)}"
    
    def generate_deploy_report(self) -> str:
        """生成部署报告"""
        report = f"""
🎯 云端部署报告
{'='*60}
📊 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
📁 项目路径: {self.project_root}

🔧 部署配置
-----------
- 云平台: {self.config.get('cloud_provider', 'Docker')}
- 镜像仓库: {self.config.get('registry', 'docker.io')}
- 镜像名称: {self.config.get('image_name', 'my-app')}
- 镜像标签: {self.config.get('image_tag', 'latest')}

✅ 环境检查
-----------
- Docker安装: {'✅' if self.check_docker_installed() else '❌'}
- AWS CLI: {'✅' if self.check_cloud_cli('aws') else '❌'}
- Azure CLI: {'✅' if self.check_cloud_cli('azure') else '❌'}
- GCP CLI: {'✅' if self.check_cloud_cli('gcp') else '❌'}

📋 部署文件状态
---------------
"""
        
        deploy_files = ["Dockerfile", "deployment.yaml", "docker-compose.yml", "requirements.txt"]
        
        for file in deploy_files:
            path = self.project_root / file
            exists = path.exists()
            report += f"- {file}: {'✅' if exists else '❌'}\n"
        
        report += "\n🎯 部署建议:\n"
        report += "  1. 确保Docker已安装并运行\n"
        report += "  2. 配置镜像仓库认证\n"
        report += "  3. 生成Dockerfile和部署配置\n"
        report += "  4. 构建并推送镜像\n"
        report += "  5. 部署到目标平台\n"
        
        return report
    
    def run_interactive(self):
        """运行交互模式"""
        while True:
            menu = """
🎯 云端部署控制台
==================
1. 🔧 查看部署配置
2. ⚙️ 修改部署配置
3. 📦 生成Dockerfile
4. 🏗️ 构建Docker镜像
5. 🚀 推送Docker镜像
6. 📊 生成Kubernetes配置
7. ☸️ 部署到Kubernetes
8. 📋 生成部署报告
9. ❓ 帮助
10. 🚪 退出

请选择 (1-10): """
            
            choice = input(menu).strip()
            
            if choice == "1":
                print("\n🔧 部署配置:")
                print(json.dumps(self.config, indent=2, ensure_ascii=False))
            elif choice == "2":
                self.config["image_name"] = input("📝 镜像名称: ").strip() or self.config["image_name"]
                self.config["image_tag"] = input("🏷️ 镜像标签: ").strip() or self.config["image_tag"]
                self.config["registry"] = input("📦 镜像仓库: ").strip() or self.config["registry"]
                self.save_config()
                print("✅ 配置保存成功!")
            elif choice == "3":
                project_type = input("📱 项目类型(python/node/vue/fastapi): ").strip() or "python"
                print(self.generate_dockerfile(project_type))
            elif choice == "4":
                dockerfile = input("📄 Dockerfile路径(默认Dockerfile): ").strip() or "Dockerfile"
                print(self.build_docker_image(dockerfile))
            elif choice == "5":
                print(self.push_docker_image())
            elif choice == "6":
                app_name = input("📝 应用名称: ").strip() or "my-app"
                print(self.generate_kubernetes_config(app_name))
            elif choice == "7":
                print(self.deploy_to_kubernetes())
            elif choice == "8":
                print(self.generate_deploy_report())
            elif choice == "9":
                print("\n❓ 帮助信息:")
                print("   云端部署工程师帮助您将应用部署到云平台")
                print("   支持: Docker构建、Kubernetes部署")
            elif choice == "10":
                print("👋 再见!")
                break
            else:
                print("❌ 无效选择，请重新输入")
    
    def run(self):
        """运行云端部署工程师"""
        if len(sys.argv) > 1 and sys.argv[1] == "--report":
            print(self.generate_deploy_report())
        else:
            self.run_interactive()

if __name__ == "__main__":
    engineer = CloudDeployEngineer()
    engineer.run()