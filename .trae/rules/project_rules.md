# 🎯 Trae AI 超级团队 - 项目级规则手册

> 项目专用配置，复制到新项目时自动生效
> 版本：v4.0 - 项目级专用规则

## 📋 项目规则总览

> **📖 开发原则**：开始前请先阅读 [principles.md](../principles.md) - 3分钟掌握核心开发原则
> 
> **🎯 推荐流程**：principles.md → project_rules.md → 实际开发

### 🚀 快速开始（项目级）
```bash
# 复制本项目配置到新项目
cp -r .trae/rules/project_rules.md ../my-new-project/.trae/rules/
```

### 🎯 核心规则内容

本文件包含项目级专用规则，从原 `user_rules.md` 整合而来，专注项目开发场景。

## 🎭 20个AI智能体快速指南

### 👥 管理类智能体
- @产品经理 - 需求分析、产品设计
- @系统架构师 - 技术架构设计
- @项目经理 - 项目统筹管理
- @项目协调员 - 团队协作

### 💻 前端开发智能体
- @Vue工程师 - Vue3 + TypeScript
- @React工程师 - React18 + Next.js
- @Angular工程师 - Angular15+
- @Uniapp工程师 - 跨平台小程序
- @Flutter工程师 - 跨平台移动App

### ⚙️ 后端开发智能体
- @Python工程师 - FastAPI/Django/Flask
- @FastAPI工程师 - FastAPI专业开发
- @Node工程师 - Express/Nest.js
- @Go工程师 - Go语言高性能后端
- @Rust工程师 - Rust系统级开发

### 🔧 专项技术智能体
- @测试工程师 - 自动化测试
- @DevOps工程师 - CI/CD部署
- @UI/UX设计师 - 界面设计
- @技术文档工程师 - 技术文档
- @C++部署工程师 - C++系统优化
- @环境管理工程师 - 统一环境配置

## 🎯 项目开发工作流

### 标准开发流程
1. **需求阶段** - @产品经理分析需求
2. **设计阶段** - @系统架构师设计架构
3. **开发阶段** - 前后端工程师协作编码
4. **测试阶段** - @测试工程师验证
5. **部署阶段** - @DevOps工程师上线

### 🛠️ 项目工具使用
```bash
# 项目启动
python .trae/workflows/project-init.py quick

# 团队启动
python .trae/workflows/team-launcher.py start

# 控制台交互
python .trae/workflows/trae-console.py
```

## 📊 项目模板

### 可用模板
- vue3-fastapi-template - Vue3 + FastAPI
- react-ecommerce-template - React + Node.js
- flutter-mobile-template - Flutter移动应用
- uniapp-miniprogram-template - 小程序开发
- fastapi-api-template - 纯API服务

## 🔧 项目级工具

### 核心工具
- system-enhancer.py - 系统优化
- project-assistant.py - 项目管理
- smart-cleanup.py - 智能清理
- smart-reminder.py - 开发提醒

### 工作流工具
- project-init.py - 项目初始化
- team-launcher.py - 团队启动
- trae-console.py - AI控制台
- universal-env-manager.py - 环境管理

## 🚀 详细快速上手

### 零配置启动
```bash
# 1. 复制到项目根目录
cp -r .trae ../my-project/
cd ../my-project

# 2. 启动项目向导
python .trae/trae.py start

# 3. 进入AI控制台
python .trae/workflows/trae-console.py
```

### 项目初始化模板
```bash
# 快速初始化Vue3项目
python .trae/workflows/project-init.py vue3

# 快速初始化React项目
python .trae/workflows/project-init.py react

# 自定义初始化
python .trae/workflows/project-init.py custom
```

## 🔧 实际使用示例

### Vue3项目开发流程
```bash
# 启动项目
@产品经理 设计一个Vue3电商管理系统

# 前端开发
@Vue工程师 创建商品管理页面，包含增删改查功能

# 后端API
@FastAPI工程师 创建商品管理的RESTful API

# 数据库设计
@系统架构师 设计商品表结构

# 测试验证
@测试工程师 为商品API编写单元测试
```

### React项目开发流程
```bash
# 需求分析
@产品经理 分析React社交App需求

# 前端实现
@React工程师 创建用户登录注册组件

# 后端服务
@Node工程师 实现用户认证API

# 部署配置
@DevOps工程师 配置Docker容器化部署
```

## 🛠️ 故障排除

### 常见问题
1. **智能体无法识别**：运行 `python .trae/workflows/team-launcher.py doctor`
2. **环境配置错误**：运行 `python .trae/workflows/universal-env-manager.py check`
3. **权限问题**：Windows右键解除锁定，Linux/Mac运行 `chmod +x`

### 调试命令
```bash
# 检查系统状态
python .trae/core/project-assistant.py --status

# 查看智能体列表
python .trae/workflows/team-launcher.py list

# 环境诊断
python .trae/workflows/universal-env-manager.py doctor
```

## 📊 项目统计与监控

### 查看项目统计
```bash
python .trae/core/project-assistant.py --report
python .trae/core/project-assistant.py --stats
```

### 智能体使用统计
```bash
python .trae/workflows/team-launcher.py --usage
```

## 🔄 跨平台使用

### Windows
```cmd
.trae\start.bat
python .trae\trae.py start
```

### macOS/Linux
```bash
./.trae/start.sh
python3 .trae/trae.py start
```

## 🎯 项目模板使用

### 使用内置模板
```bash
# 列出可用模板
python .trae/workflows/agent-suite.py list-templates

# 生成Vue3项目
python .trae/workflows/agent-suite.py generate vue3

# 生成React项目
python .trae/workflows/agent-suite.py generate react

# 生成Flutter项目
python .trae/workflows/agent-suite.py generate flutter
```

### 自定义模板
```bash
# 基于现有项目创建模板
python .trae/workflows/agent-suite.py create-template my-template
```

## 🆘 获取帮助

### 智能帮助系统
```bash
# 获取帮助
python .trae/trae.py help

# 查看具体智能体帮助
@技术文档工程师 显示所有可用命令

# 系统诊断
python .trae/trae.py doctor
```

---

*项目级规则手册 - 专注于实际项目开发场景，复制即用！*