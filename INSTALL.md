# 🚀 Trae AI 超级团队 - 安装指南

> **3 步快速上手 · 复制即用 · 开箱即用**

---

## ⚡ 快速开始（3 步）

### 方式一：复制到现有项目（推荐）

```bash
# 1️⃣ 复制 .trae 文件夹到你的项目
cp -r .trae /path/to/your/project/

# 2️⃣ 进入项目目录
cd your-project

# 3️⃣ 完成！直接在 Trae IDE 中使用 AI 专家团队
```

### 方式二：克隆到新项目

```bash
# 1️⃣ 创建新目录
mkdir my-project && cd my-project

# 2️⃣ 克隆配置
git clone https://github.com/wangqiqi/trae-ai.git .trae-template
mv .trae-template/.trae .
rm -rf .trae-template

# 3️⃣ 开始使用
```

### 方式三：手动下载

1. 下载项目 ZIP 包
2. 解压后复制 `.trae/` 文件夹到你的项目根目录
3. 在 Trae IDE 中打开项目

---

## 🎯 立即使用

### 智能体调用

在 Trae IDE 对话中直接使用：

```
帮我用 Vue 3 开发一个用户管理组件    → 自动调用 Vue 工程师
帮我设计一个 RESTful API             → 自动调用 FastAPI 工程师
帮我分析一下项目架构                 → 自动调用系统架构师
帮我写单元测试                        → 自动调用测试工程师
```

### 技能系统

```
使用 code-analyzer 分析项目结构
使用 project-scaffold 创建一个 Vue 3 项目
使用 docker-generator 生成 Docker 配置
```

---

## 🔧 可选配置

### 安装依赖（可选）

```bash
# Linux / macOS
./.trae/install.sh

# Windows
./.trae/install.bat
```

### 启动 AI 控制台（可选）

```bash
python .trae/workflows/trae-console.py
```

---

## 📦 包含内容

`.trae/` 目录包含完整的 AI 专家团队配置：

- **20 个 AI 专家**：Vue、React、FastAPI、测试等各领域专家
- **5 个技能**：代码分析、项目脚手架、README 生成等
- **7 个项目模板**：API 规范、代码审查、需求文档等
- **VIBE 开发方法论**：文档驱动的迭代开发流程
- **宪法系统**：三大公理 + 六大协作原则

---

## ❓ 常见问题

### Q: 需要配置 API 密钥吗？

**A**: 不需要！`复制即用`，无需任何配置。

### Q: 支持哪些技术栈？

**A**: Vue 3、React、FastAPI、Node.js、Python、Flutter、Go、Rust 等主流技术栈。

### Q: 如何查看所有可用功能？

**A**: 阅读项目根目录的 `README.md`，或直接在 Trae IDE 中体验。

### Q: 可以自定义 AI 专家吗？

**A**: 可以！在 `.trae/agent/` 目录下修改或添加新的智能体配置文件。

---

## 🎉 完成！

现在你的项目已经拥有了 20 个 AI 专家的支持。立即在 Trae IDE 中开始你的开发之旅吧！

**文档版本**: v1.0  
**最后更新**: 2026-06-02
