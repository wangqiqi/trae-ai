# 🏗️ Trae AI 三目录架构

> **配置 + 用户数据 + 运行时数据 = 安全 + 可复制 + 可共享 + 可用户级**

---

## 📁 三目录设计理念

### `.trae/` 📦 项目配置（可复制）

- 规则定义、核心脚本、文档
- 可安全复制到任何项目
- **完全独立于用户和项目数据**
- 支持版本控制和团队共享

### `.trae-user/` 👤 用户数据（项目级/用户级）

- 用户偏好、项目列表、学习记录
- **可放在项目根目录（项目级）**
- **也可放在 HOME 目录（用户级，跨项目共享）**
- 自动添加到 `.gitignore` 保护隐私

### `.trae-data/` 🌱 项目运行时数据（可选）

- AI学习记录、缓存数据、性能监控
- 每个项目独立生长
- 不复制到其他项目

---

## 📂 完整目录结构

```
my-project/
├── .trae/                      # 📦 项目配置（可复制）
│   ├── CONSTITUTION.md          # 🏛️ 宪法
│   ├── principles.md            # 📜 开发原则
│   ├── project_rules.md         # 📋 项目规则
│   ├── AGENTS.md               # 🤖 AI智能体定义
│   ├── agent/                   # 🤖 AI专家配置
│   │   ├── vue-engineer.json
│   │   ├── react-engineer.json
│   │   └── ...
│   ├── core/                   # 🔧 核心脚本
│   │   ├── console_utils.py
│   │   ├── data_manager.py
│   │   └── ...
│   ├── docs/                   # 📖 文档
│   │   ├── VIBE_METHODOLOGY.md # VIBE方法论
│   │   ├── PERSONA_SYSTEM.md  # 人格角色系统
│   │   └── DUAL_DIRECTORY_DESIGN.md
│   ├── skills/                 # 🎯 技能系统
│   │   ├── code-analyzer/
│   │   ├── project-scaffold/
│   │   └── ...
│   ├── templates/              # 📝 项目模板
│   ├── workflows/              # ⚡ 工作流
│   ├── rules/                  # 📋 Cursor规则
│   ├── install.sh              # 🚀 安装脚本
│   └── setup-trae.sh           # 🔧 配置脚本
│
├── .trae-user/                 # 👤 用户数据（项目级或用户级）
│   ├── preferences.json        # 用户偏好设置
│   ├── projects.json          # 项目列表
│   ├── .example/              # 📝 示例文件
│   │   ├── preferences.json.example
│   │   └── projects.json.example
│   └── .gitignore             # 🔒 自动保护
│
├── .trae-data/                 # 🌱 项目运行时数据（可选）
│   ├── logs/                   # 📊 操作日志
│   ├── cache/                  # 💾 缓存数据
│   ├── learning/              # 🧠 学习记录
│   ├── stats/                 # 📈 统计数据
│   └── .gitignore
│
├── .trae-project.json          # 📋 项目配置
├── .gitignore                  # 🔒 包含 .trae-user/ 和 .trae-data/
└── ...
```

---

## 🎯 核心设计原则

### 1️⃣ 项目独立 (Project Agnostic)

- ✅ **即插即用** - 复制 `.trae/` 到任何Git项目，立即获得完整AI能力
- ✅ **完全干净** - `.trae/` 不包含任何用户数据或项目数据
- ✅ **自动适应** - 智能检测项目类型、技术栈、环境配置
- ✅ **多项目支持** - 同一AI系统可在多个项目同时使用

### 2️⃣ 用户数据独立 (User Data Agnostic)

- ✅ **灵活位置** - `.trae-user/` 可在项目级或用户级
- ✅ **跨项目共享** - 放在 HOME 目录，跨项目共享用户偏好
- ✅ **数据隔离** - 用户数据完全与项目配置分离
- ✅ **隐私保护** - 自动添加到 `.gitignore`

### 3️⃣ 系统独立 (System Agnostic)

- ✅ **跨平台兼容** - 完整支持 Linux/macOS/Windows
- ✅ **自动检测** - 智能识别OS类型和环境变量
- ✅ **统一接口** - 屏蔽底层系统差异，提供一致体验

---

## 🔒 隐私保护机制

### 自动添加到 .gitignore

```gitignore
# Trae AI 用户数据（项目级）
.trae-user/

# Trae AI 运行时数据
.trae-data/

# Trae AI 配置缓存
.trae/cache/
.trae/logs/
```

### .trae-user/.gitignore

```gitignore
# 用户配置文件
*.json
!*.example
!.example/*.json

# 日志文件
*.log
logs/

# 缓存
cache/

# 临时文件
*.tmp
*.temp
```

### 数据隔离策略

| 数据类型 | 存储位置 | 复制策略 |
|---------|---------|---------|
| 配置文件 | `.trae/` | ✅ 复制 |
| 规则定义 | `.trae/rules/` | ✅ 复制 |
| 核心脚本 | `.trae/core/` | ✅ 复制 |
| 用户偏好 | `.trae-user/` | ⚙️ 可选 |
| 项目列表 | `.trae-user/` | ⚙️ 可选 |
| 操作日志 | `.trae-data/logs/` | ❌ 不复制 |
| 学习记录 | `.trae-data/learning/` | ❌ 不复制 |
| 缓存数据 | `.trae-data/cache/` | ❌ 不复制 |

---

## 🚀 快速开始

### 方式一：复制到现有项目

```bash
# 1️⃣ 复制 .trae 配置到项目
cp -r .trae /path/to/your/project/

# 2️⃣ 进入项目目录
cd your-project

# 3️⃣ 运行安装脚本
./.trae/install.sh

# 4️⃣ 完成！在 Trae IDE 中使用
```

### 方式二：克隆新项目

```bash
# 1️⃣ 创建项目目录
mkdir my-project && cd my-project

# 2️⃣ 克隆 Trae 配置
git clone https://github.com/wangqiqi/trae-ai.git .trae-template
mv .trae-template/.trae .
rm -rf .trae-template

# 3️⃣ 初始化
./.trae/install.sh

# 4️⃣ 开始使用
python .trae/workflows/trae-console.py
```

---

## 📊 .trae-user/ 数据说明

### 用户偏好 (preferences.json)

```json
{
  "theme": "auto",
  "skill_level": "intermediate",
  "favorite_tools": [],
  "preferred_persona": "professional",
  "language": "zh-CN",
  "auto_suggestions": true
}
```

### 项目列表 (projects.json)

```json
{
  "version": "2.0.0",
  "projects": [
    {
      "id": "example-001",
      "name": "示例项目",
      "path": "/path/to/project",
      "tech_stack": ["Vue", "FastAPI"],
      "status": "active"
    }
  ],
  "stats": {
    "total_projects": 1,
    "completed_projects": 0
  }
}
```

---

## 🔧 管理命令

```bash
# 初始化 Trae 环境
python .trae/workflows/trae-console.py --init

# 查看数据统计
python .trae/workflows/trae-console.py --stats

# 清理缓存
python .trae/workflows/trae-console.py --clean

# 导出配置
python .trae/workflows/trae-console.py --export

# 导入配置
python .trae/workflows/trae-console.py --import <config-path>
```

---

## 📊 .trae-data/ 自动记录

`.trae-data/` 目录会自动记录：

- 📈 **使用统计** - 技能使用次数、成功率
- 🧠 **学习记录** - 项目特点、技术栈偏好
- 📊 **性能指标** - 响应时间、Token消耗
- 🔍 **分析数据** - 代码质量、依赖关系

---

*三目录设计 = 配置可共享 + 用户数据可迁移 + 运行时数据可保护*
