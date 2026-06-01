---
command: skill
description: "技能调用系统 - 使用 @skill 技能名 来激活各种实用技能"
alwaysApply: false
---

# 🎯 技能调用系统

## 使用方式

```
@skill 技能名 [参数]
```

## 可用技能

### 项目脚手架
- `@skill project_scaffold` - 快速生成 Vue/React/FastAPI/Node 项目

### 项目分析
- `@skill code_analyzer` - 分析项目结构和代码质量
- `@skill env_detector` - 检测项目技术栈和环境
- `@skill project_intelligence` - 智能项目分析与推荐

### 文档生成
- `@skill readme_generator` - 自动生成专业 README

### Git 初始化
- `@skill git_initializer` - 快速初始化 Git 仓库

### 配置生成
- `@skill docker_generator` - 生成 Dockerfile 和 docker-compose
- `@skill file_searcher` - 搜索项目文件

### 依赖安装
- `@skill dependency_installer` - 智能安装项目依赖

### Trae 集成
- `@skill trae_integrator` - 配置 Trae AI 环境

## 使用示例

```
@skill code_analyzer 分析当前项目

@skill readme_generator 生成 README

@skill git_initializer 初始化 Git
```

## 技能文件位置

所有技能文件位于：
```
.trae/skills/
```

每个技能是一个独立的 Python 模块，包含 `execute(**kwargs)` 函数。
