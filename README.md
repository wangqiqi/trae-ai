# 🚀 SOLO AI 开发助手

一个基于Trae IDE的AI驱动开发助手，通过自然语言对话就能完成项目开发。

## ✨ 核心特性

- **🎯 自然语言开发**：直接对话就能创建项目
- **🤖 多智能体协作**：产品经理、架构师、工程师等角色分工合作
- **📦 一键迁移**：复制`.trae`目录即可在新项目使用
- **🔄 零配置**：开箱即用，无需复杂设置
- **🌐 全栈支持**：Vue、React、Python、Node.js等技术栈

## 📁 项目结构

```
SOLO-AI-Assistant/
├── .trae/                           # AI系统核心目录
│   ├── agents/                     # 智能体配置（19个标准化角色）
│   │   ├── *-standardized.json   # 标准化智能体文件
│   ├── scripts/                    # 工具脚本
│   │   ├── agent-standardization-suite.py  # 🔧 统一智能体管理工具
│   │   └── templates/             # 标准模板
│   ├── trae-console.py            # 🚀 统一控制台（项目管理+基础智能体管理）
│   ├── .trae-config.json          # 智能体配置
│   └── PROJECT-CHOICE-GUIDE.md    # 智能体选择指南
├── .trae-dev.py                    # 极简入口（兼容旧版）
├── user-data/                     # 📊 用户项目数据（独立管理）
├── .gitignore                     # Git配置
└── README.md                      # 本文档
```

## 🚀 快速开始

### 🆕 方法1：统一控制台（推荐）

**交互模式**（最直观）：
```bash
python .trae/trae-console.py
# 然后输入：我想创建一个Vue3任务管理系统
```

**命令行模式**：
```bash
# 创建项目
python .trae/trae-console.py create-project "Vue3任务管理系统"

# 查看项目列表  
python .trae/trae-console.py list-projects

# 管理智能体
python .trae/trae-console.py list-agents
```

### 🔄 方法2：极简入口（兼容旧版）

```bash
# 快速创建
python .trae-dev.py "创建React电商网站"

# 项目模板
#todo 任务管理应用
#ecommerce 电商网站
#blog 博客系统
#ai AI识别系统
```

### 🌐 方法3：对话开发（自然语言）

在Trae对话框直接输入：
```
@产品经理 我想创建一个Vue3任务管理应用
```

## 🤖 可用智能体

| 智能体 | 角色描述 | 使用示例 |
|---|---|---|
| `@产品经理` | 需求分析、功能规划 | `@产品经理 分析这个需求` |
| `@系统架构师` | 技术选型、架构设计 | `@系统架构师 设计Vue3+FastAPI架构` |
| `@Vue工程师` | Vue.js前端开发 | `@Vue工程师 创建任务列表页面` |
| `@React工程师` | React前端开发 | `@React工程师 设计组件结构` |
| `@Python工程师` | FastAPI后端开发 | `@Python工程师 创建CRUD API` |
| `@Node工程师` | Express.js后端开发 | `@Node工程师 创建用户认证API` |
| `@AI工程师` | AI模型集成 | `@AI工程师 添加图像识别功能` |
| `@测试工程师` | 测试方案设计 | `@测试工程师 为登录功能写测试` |
| `@DevOps工程师` | 部署和运维 | `@DevOps工程师 部署到Docker` |
| `@项目经理` | 项目管理和规划 | `@项目经理 制定项目计划` |

## 🎯 使用场景示例

### 场景1：创建新项目
```
@产品经理 我想做一个类似Trello的任务管理应用，需要支持拖拽功能
```

### 场景2：设计技术架构
```
@系统架构师 为这个任务管理应用设计技术栈和架构
```

### 场景3：开发具体功能
```
@Vue工程师 创建一个支持拖拽的任务看板组件
```

### 场景4：后端API开发
```
@Python工程师 创建任务的CRUD API，包含状态管理
```

## 🔄 迁移到新项目

### 方法1：复制目录
```bash
# 复制到新项目
cp -r .trae .trae-dev.py /path/to/new-project/
cd /path/to/new-project

# 开始开发
python .trae-dev.py "创建新项目"
```

### 方法2：Git子模块（推荐）
```bash
git submodule add https://github.com/your-repo/SOLO-AI-Assistant.git .ai-assistant
cd .ai-assistant
python .trae-dev.py "开始项目"
```

## 🛠️ 技术栈支持

### 前端技术栈
- **Vue.js**: Vue3 + TypeScript + Vite
- **React.js**: React18 + TypeScript + Vite
- **Uniapp**: 跨平台小程序开发

### 后端技术栈  
- **Python**: FastAPI + SQLAlchemy + Pydantic
- **Node.js**: Express.js + MongoDB + TypeScript
- **Go**: Gin框架 + GORM
- **Rust**: Actix-web + Diesel

### 全栈模板
- **Vue + FastAPI**: 前后端分离
- **React + Node.js**: MERN技术栈
- **Flutter**: 跨平台移动应用

## 📊 项目数据

项目信息存储在：
- `user-data/projects.json` - 项目列表（用户数据独立管理）
- `user-data/risks.json` - 风险评估
- `user-data/demo-projects.json` - 示例项目

> 💡 **数据分离设计**：系统配置与用户数据完全分离，便于版本管理和迁移

## 🔧 API接口

启动API服务器后：
- `GET /api/projects` - 获取项目列表
- `POST /api/projects` - 创建新项目
- `POST /api/analyze-requirement` - 需求分析
- `GET /api/templates` - 获取模板列表
- `GET /api/health` - 健康检查

## 🎮 开发调试

### 启动开发模式
```bash
# 启动API服务器
python .trae/scripts/solo-api-server.py

# 访问Web界面
open http://localhost:8000
```

### 测试智能体
```bash
# 测试统一控制台
python .trae/trae-console.py create-project "测试项目"

# 测试极简入口（兼容）
python .trae-dev.py "@产品经理 分析需求"

# 测试项目模板
python .trae-dev.py "#todo 创建任务管理应用"
```

## 📝 贡献指南

欢迎贡献新的智能体或改进现有功能：

1. **添加新智能体**: 在`.trae/agents/`目录添加配置文件
2. **创建新模板**: 在`.trae/templates/`目录添加模板文件
3. **优化逻辑**: 修改`.trae/trae-console.py`中的处理逻辑
4. **查看智能体选择**: 参考`.trae/PROJECT-CHOICE-GUIDE.md`了解智能体设计思路

## 🐛 常见问题

**Q: 智能体没有响应？**
A: 确保API服务器已启动：`python .trae/scripts/solo-api-server.py`

**Q: 如何自定义智能体？**
A: 编辑`.trae/.trae-config.json`中的智能体配置

**Q: 支持哪些项目类型？**
A: 支持todo、ecommerce、blog、ai等模板，可扩展

## 📄 许可证

MIT License - 可自由使用和修改

## 🌟 Star

如果这个项目对你有帮助，请给个Star！ ⭐