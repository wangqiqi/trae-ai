---
name: git-initializer
description: 快速初始化 Git 仓库，配置 .gitignore，添加初始提交
---

# Git 初始化器

## 描述
为项目快速初始化 Git 仓库，创建标准的 .gitignore 文件，并完成初始提交。

## 使用场景
- 新建项目时，需要初始化 Git 版本控制
- 已有项目但还没有 Git 仓库
- 需要快速配置标准的 Git 忽略规则

## 指令

1. **初始化 Git 仓库**
   ```bash
   git init
   ```

2. **创建 .gitignore 文件**
   - 根据项目类型（Node.js、Python、Java 等）创建相应的忽略规则
   - 包含常用的忽略项（node_modules、__pycache__、.env 等）

3. **添加初始文件**
   ```bash
   git add .
   git commit -m "Initial commit"
   ```

## 示例

### 输出
```
✅ Git 仓库已初始化！

已创建 .gitignore 文件，包含以下规则：
- node_modules/
- .env
- dist/
- build/
- *.pyc

已完成初始提交："Initial commit"

下一步：
git remote add origin <your-repo-url>
git push -u origin main
```
