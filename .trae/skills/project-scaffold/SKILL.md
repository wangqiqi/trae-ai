---
name: project-scaffold
description: 快速生成项目脚手架，支持 Vue、React、FastAPI、Node.js 等多种技术栈
---

# 项目脚手架生成器

## 描述
快速为不同技术栈的项目生成标准的项目结构和基础文件。

## 使用场景
- 从零开始创建新项目时
- 需要快速初始化项目结构时
- 学习新技术栈，需要参考标准项目结构时

## 指令

### 支持的技术栈
- Vue 3 + Vite + TypeScript
- React + Vite
- FastAPI
- Node.js + Express
- 其他常见技术栈

### 生成的标准结构
根据不同技术栈，生成相应的项目结构和初始文件：

#### Vue 3 项目
```
my-project/
├── src/
│   ├── components/
│   ├── views/
│   ├── stores/
│   └── router/
├── public/
├── package.json
├── vite.config.ts
└── README.md
```

#### FastAPI 项目
```
my-project/
├── app/
│   ├── api/
│   ├── models/
│   └── core/
├── tests/
├── requirements.txt
├── main.py
└── README.md
```

## 示例

### 输入
"帮我创建一个 Vue 3 项目脚手架"

### 输出
```
已创建 Vue 3 项目脚手架：

📦 my-vue-project/
├── src/
│   ├── components/
│   ├── views/
│   ├── stores/
│   └── router/
├── package.json
├── vite.config.ts
└── README.md

项目已准备就绪！请运行：
cd my-vue-project
npm install
npm run dev
```
