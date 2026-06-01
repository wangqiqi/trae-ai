# 🚀 Trae AI 超级团队项目配置

> 官方 Trae AI 规范 · 100% 标准 · 开箱即用

本项目包含完整的 Trae AI 配置，按照官方文档标准设计，可直接复制到任意项目使用。

---

## 📋 目录结构（100% 官方规范）

```
.trae/
├── AGENTS.md                  # 智能体定义（官方标准 AGENTS.md）
├── skills/                   # 技能（官方 SKILL.md 格式）
│   ├── code-analyzer/
│   │   └── SKILL.md
│   ├── readme-generator/
│   │   └── SKILL.md
│   ├── project-scaffold/
│   │   └── SKILL.md
│   ├── git-initializer/
│   │   └── SKILL.md
│   └── docker-generator/
│       └── SKILL.md
├── rules/                    # 规则（官方 Front Matter 格式）
│   ├── principles.md
│   ├── agents.md
│   └── roles.md
├── docs/                     # 完整文档
│   ├── ROLES.md             # 🎭 AI 人格角色系统
│   ├── CONSTITUTION.md      # 🏛️ 宪法驱动系统
│   └── VIBE_METHODOLOGY.md  # 🚀 VIBE 开发方法论
└── principles.md             # 开发原则
```

---

## 🎮 使用方式（100% 官方标准）

### 1️⃣ 智能体 (Agent) - 官方 AGENTS.md

使用官方标准方式：
```
帮我用 Vue 3 开发一个用户管理组件 → 自动识别为 Vue工程师角色
帮我设计一个 RESTful API → 自动识别为 FastAPI工程师角色
帮我写单元测试 → 自动识别为 测试工程师角色
```

### 2️⃣ 技能 (Skill)

在对话中直接使用技能，AI 会自动识别或手动调用：
```
使用 code-analyzer 技能分析一下项目结构
帮我用 readme-generator 生成一个专业的 README
```

### 3️⃣ 规则 (Rule)

规则自动生效，无需手动调用。包含：
- **始终生效规则** - 所有对话都适用（如 `principles.md`）
- **智能生效规则** - 根据场景自动应用
- **手动触发规则** - 使用 `#Rule` 引用

### 4️⃣ 人格角色 (Role) 🎭 **新功能**

通过不同的沟通风格满足心理需求，21种角色可选：

**👔 专业角色 (8种)：**
专业助手、谦逊助手、友好伙伴、专家导师、创意艺术家、严格教师、搞笑演员、极简禅者

**🌟 动漫风格角色 (13种)：**
可爱萝莉、御姐女王、完美女仆、赛博朋克黑客、魔法少女程序员、高冷学霸、暖男助手、精灵工程师、机械管家、古风书生、元气少女、神秘侦探、太空漫游者

**使用方式：**
```
小妮，帮我写个组件          # 直接称呼昵称
切换到可爱萝莉模式          # 明确切换指令
大师，帮我分析架构          # 专业导师模式
女王，这个设计怎么样        # 御姐女王模式
```

角色系统自动生效，根据你的语气和内容自动适配！

---

## 🧰 已配置的技能

| 技能 | 功能 | 使用场景 |
|------|------|----------|
| `code-analyzer` | 分析项目结构和技术栈 | 了解新项目、代码审计 |
| `readme-generator` | 自动生成专业 README | 项目初始化、文档完善 |
| `project-scaffold` | 生成项目脚手架 | 从零创建新项目 |
| `git-initializer` | Git 仓库初始化 | 项目版本控制 |
| `docker-generator` | 生成 Docker 配置 | 容器化部署 |

---

## 📜 设计原则（来自官方规范）

### 技能 (Skills) 规范
- 位置：`.trae/skills/{skill-name}/`
- 主文件：`SKILL.md`（Front Matter 格式）
- 结构：
  ```markdown
  ---
  name: 技能名
  description: 技能描述
  ---
  # 技能名称
  ## 描述
  ## 使用场景
  ## 指令
  ## 示例
  ```

### 规则 (Rules) 规范
- 位置：`.trae/rules/`
- 格式：Front Matter + Markdown
- 结构：
  ```markdown
  ---
  alwaysApply: true/false
  description: 适用场景
  globs: ["*.js"]
  ---
  规则内容...
  ```

---

## 🚀 快速开始

### 方式一：复制到现有项目
```bash
# 1. 复制 .trae 文件夹到你的项目
cp -r .trae /path/to/your/project/

# 2. 在 Trae IDE 中打开项目，配置自动生效
```

### 方式二：在新项目中初始化
```bash
# 1. 创建新目录
mkdir my-project && cd my-project

# 2. 复制 .trae 文件夹
cp -r /path/to/.trae .

# 3. 开始使用 Trae AI！
```

---

## 📚 官方文档参考

- [技能 (Skills) 官方文档](https://docs.trae.cn/ide/skills)
- [规则 (Rules) 官方文档](https://docs.trae.cn/ide/rules)
- [智能体 (Agent) 官方文档](https://docs.trae.cn/ide/agent-overview)
- [TRAE SOLO 介绍](https://docs.trae.cn/ide/trae-solo-is-now-available)

---

## 📄 许可证

MIT License

---

✨ 现在开始享受 Trae AI 的强大功能吧！
