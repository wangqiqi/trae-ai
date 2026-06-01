# 🚀 Trae AI 超级团队

> **官方设计风格 · 零配置 · 开箱即用**

基于官方 Trae AI 设计模式重构的 AI 开发助手！

---

## 📋 快速开始

### 使用方式：一句话唤起

| 功能 | 唤起方式 | 示例 |
|------|---------|------|
| **Agents (智能体)** | `@智能体名` | `@Vue工程师` |
| **Rules (规则)** | 自动应用 | `constitution` 自动生效 |
| **Skills (技能)** | `@skill 技能名` | `@skill code_analyzer` |

---

## 🎭 可用的 Agents

### 前端开发
- `@Vue工程师` - Vue 3 专家
- `@React工程师` - React 专家
- `@Angular工程师` - Angular 专家
- `@UI/X设计师` - UI/UX 设计
- `@Uniapp工程师` - 跨平台小程序
- `@Flutter工程师` - 跨平台移动应用

### 后端开发
- `@Python工程师` - Python 全栈
- `@FastAPI工程师` - FastAPI 专家
- `@NodeJS工程师` - Node.js 专家
- `@Go工程师` - Go 语言专家
- `@Rust工程师` - Rust 专家

### 管理与支持
- `@产品经理` - 需求分析与产品设计
- `@系统架构师` - 技术架构设计
- `@项目经理` - 项目管理与协调
- `@测试工程师` - 测试与质量保证
- `@DevOps工程师` - 部署与运维
- `@技术文档工程师` - 文档编写
- `@C++AI部署工程师` - C++ 系统优化
- `@环境管理工程师` - 环境配置

---

## 🔧 可用的 Skills

### 项目脚手架
`@skill project_scaffold` - 快速生成 Vue/React/FastAPI/Node 项目

### 项目分析
`@skill code_analyzer` - 分析项目结构和代码质量  
`@skill env_detector` - 检测项目技术栈和环境  
`@skill project_intelligence` - 智能项目分析与推荐

### 文档生成
`@skill readme_generator` - 自动生成专业 README

### Git 初始化
`@skill git_initializer` - 快速初始化 Git 仓库

### 配置生成
`@skill docker_generator` - 生成 Dockerfile 和 docker-compose  
`@skill file_searcher` - 搜索项目文件

### 依赖安装
`@skill dependency_installer` - 智能安装项目依赖

### Trae 集成
`@skill trae_integrator` - 配置 Trae AI 环境

---

## 📜 内置 Rules（自动生效）

| 规则 | 作用 |
|------|------|
| **constitution** | AI 共生宪法 - 最高准则 |
| **philosophy** | 开发哲学指导 |
| **system_info** | 系统信息规则 |
| **templates** | 模板管理规则 |
| **evolution-automation** | 进化自动化 |
| **evolution-governance** | 进化治理 |
| **intelligent_evolution** | 智能进化系统 |

---

## 🎯 实际使用示例

### 1️⃣ 使用 Agent 开发
```
@Vue工程师 帮我创建一个用户管理页面，包含增删改查功能
```

### 2️⃣ 使用 Skill 分析
```
@skill code_analyzer 分析当前项目的代码结构
```

### 3️⃣ 使用 Skill 初始化
```
@skill git_initializer 初始化 Git 仓库
```

### 4️⃣ 使用 Skill 生成文档
```
@skill readme_generator 为当前项目生成 README
```

---

## 📂 项目结构

```
你的项目/
├── .trae/                          # Trae AI 配置（可复制到任意项目）
│   ├── agent/                      # Agents (智能体)
│   │   ├── vue-engineer.json
│   │   ├── react-engineer.json
│   │   └── ...
│   ├── rules/                      # Rules (规则)
│   │   └── cursor/
│   │       ├── constitution/
│   │       │   └── RULE.md
│   │       └── ...
│   ├── skills/                     # Skills (技能)
│   │   ├── __init__.py
│   │   ├── code_analyzer.py
│   │   └── ...
│   ├── templates/                  # Templates (模板)
│   ├── core/                       # 核心工具
│   ├── workflows/                  # 工作流工具
│   └── install.sh                  # 一键安装脚本
│
└── ... 你的项目文件
```

---

## 🚀 安装与配置

### 1. 复制到项目
将 `.trae/` 文件夹复制到你的项目根目录。

### 2. 一键安装
```bash
# Linux/Mac
chmod +x .trae/install.sh
./.trae/install.sh

# Windows
.trae/install.bat
```

### 3. 开始使用
直接在对话中使用 `@Agent名` 或 `@skill 技能名` 即可！

---

## 💡 核心设计理念（官方风格）

### 1. 宪法驱动 (Constitution Driven)
- **意图主权** - 人类永远拥有最终决策权
- **信号可信** - AI 输出可追溯、可验证
- **认知可审计** - 所有过程支持 3 秒回溯

### 2. 分层架构
- **L1 信号层** - Context + Index + Rules
- **L2 协议层** - MCP + Tools
- **L3 代理层** - Agents + Model
- **L4 主权层** - 人类决策界面

### 3. 自然语言唤起
- `@Agent名` - 调用智能体
- `@skill 技能名` - 调用技能
- 规则自动生效 - 无需手动触发

---

## 🎊 开始使用

现在你可以：

1. **找 Agent 帮忙**：`@Vue工程师 帮我写个组件`
2. **用 Skill 加速**：`@skill code_analyzer`
3. **让 Rules 护航**：自动确保最佳实践

**一句话就能开始！** 🚀

---

*基于官方 Trae AI 设计理念重构 · 零配置 · 开箱即用*
