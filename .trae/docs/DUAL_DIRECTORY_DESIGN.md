# 🏗️ Trae AI 双目录架构

> **配置与数据分离 = 安全 + 可复制 + 可共享**

---

## 📁 双目录设计理念

### `.trae/` 📦 项目配置（可复制）
- 规则定义、核心脚本、文档
- 可安全复制到任何项目
- 支持版本控制和团队共享

### `.trae-data/` 🌱 项目私有数据（不复制）
- AI学习记录、缓存数据、性能监控
- 每个项目独立生长
- 自动添加到 `.gitignore` 保护隐私

---

## 📂 完整目录结构

```
my-project/
├── .trae/                      # 📦 项目配置（可复制）
│   ├── CONSTITUTION.md          # 🏛️ 宪法
│   ├── principles.md            # 📜 开发原则
│   ├── project_rules.md         # 📋 项目规则
│   ├── agents/                 # 🤖 AI智能体配置
│   │   ├── pm.json             # 产品经理
│   │   ├── architect.json      # 架构师
│   │   └── ...
│   ├── core/                   # 🔧 核心脚本
│   │   ├── console_utils.py
│   │   └── ...
│   ├── docs/                   # 📖 文档
│   │   └── VIBE_METHODOLOGY.md # VIBE方法论
│   ├── skills/                 # 🎯 技能系统
│   │   ├── __init__.py
│   │   └── ...
│   ├── templates/              # 📝 项目模板
│   ├── workflows/              # ⚡ 工作流
│   ├── rules/                  # 📋 Cursor规则
│   ├── install.sh              # 🚀 一键安装脚本
│   └── setup-trae.sh           # 🔧 Trae配置脚本
│
├── .trae-data/                 # 🌱 项目私有数据（不复制）
│   ├── logs/                   # 📊 操作日志
│   │   └── console.log
│   ├── cache/                  # 💾 缓存数据
│   │   └── project_cache.json
│   ├── learning/              # 🧠 学习记录
│   │   └── user_preferences.json
│   ├── stats/                 # 📈 统计数据
│   │   └── usage_stats.json
│   └── .gitignore             # 🔒 自动保护
│
├── .trae-project.json          # 📋 项目配置
├── .gitignore                  # 🔒 包含 .trae-data/
└── ...
```

---

## 🎯 三大独立设计原则

### 1️⃣ 项目独立 (Project Agnostic)

- ✅ **即插即用** - 复制 `.trae/` 到任何Git项目，立即获得完整AI能力
- ✅ **自动适应** - 智能检测项目类型、技术栈、环境配置
- ✅ **多项目支持** - 同一AI系统可在多个项目同时使用

### 2️⃣ 系统独立 (System Agnostic)

- ✅ **跨平台兼容** - 完整支持 Linux/macOS/Windows
- ✅ **自动检测** - 智能识别OS类型和环境变量
- ✅ **统一接口** - 屏蔽底层系统差异，提供一致体验

### 3️⃣ 用户独立 (User Agnostic)

- ✅ **AI核心独立** - 核心AI能力不依赖特定用户身份
- ✅ **数据隔离** - `.trae-data/` 目录存储所有用户特定数据
- ✅ **隐私保护** - 用户偏好和学习数据完全本地化

---

## 🔒 隐私保护机制

### 自动添加到 .gitignore

```
# .trae-data/.gitignore
# Trae AI 私有数据 - 请勿提交到版本控制

# 日志文件
*.log
logs/

# 缓存
*.cache
*.tmp

# 学习数据
learning/
stats/

# 个人配置
personal/
```

### 数据隔离策略

| 数据类型 | 存储位置 | 复制策略 |
|---------|---------|---------|
| 配置文件 | `.trae/` | ✅ 复制 |
| 规则定义 | `.trae/rules/` | ✅ 复制 |
| 核心脚本 | `.trae/core/` | ✅ 复制 |
| 操作日志 | `.trae-data/logs/` | ❌ 不复制 |
| 学习记录 | `.trae-data/learning/` | ❌ 不复制 |
| 缓存数据 | `.trae-data/cache/` | ❌ 不复制 |

---

## 🚀 快速开始

### 1. 在新项目中使用

```bash
# 复制配置
cp -r /path/to/.trae /your-new-project/

# 安装
cd /your-new-project
./.trae/install.sh

# 启动
python .trae/workflows/trae-console.py
```

### 2. 在团队中共享

```bash
# 团队成员克隆项目后
git clone <repo>
cd <project>

# 复制团队配置（不包括私有数据）
cp -r .trae-example .trae  # 或手动复制 .trae/ 目录

# 初始化（不复制私有数据）
./.trae/install.sh
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

# 导出配置（不包括私有数据）
python .trae/workflows/trae-console.py --export

# 导入配置
python .trae/workflows/trae-console.py --import <config-path>
```

---

## 📊 数据统计

`.trae-data/` 目录会自动记录：

- 📈 **使用统计** - 技能使用次数、成功率
- 🧠 **学习记录** - 用户偏好、项目特点
- 📊 **性能指标** - 响应时间、Token消耗
- 🔍 **分析数据** - 代码质量、依赖关系

---

*双目录设计 = 配置可共享 + 数据可保护 + 项目可移植*
