---
scene: git_message
alwaysApply: true
description: Git 提交信息规范 - 生成符合项目标准的提交信息
---

# Git 提交信息规范

## 提交信息格式

使用 Conventional Commits 规范：

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

## type 类型

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档变更 |
| `style` | 代码格式（不影响功能） |
| `refactor` | 重构（不是新功能或修复） |
| `perf` | 性能优化 |
| `test` | 测试相关 |
| `chore` | 构建或辅助工具变动 |

## scope 范围

可选，标识影响范围：
- `core` - 核心模块
- `skills` - 技能系统
- `rules` - 规则系统
- `workflows` - 工作流
- `agent` - 智能体
- `docs` - 文档

## subject 主题

- 使用中文，简洁明了
- 不超过 50 个字符
- 不使用句号结尾
- 描述做了什么，而不是怎么做的

## 示例

```
feat(skills): 新增项目脚手架生成技能

支持 Vue、React、FastAPI 等多种技术栈

Closes #123
```

```
fix(core): 修复控制台输出编码问题

解决了 Windows 环境下中文乱码的问题
```

```
docs: 更新 README 文档

- 添加快速开始指南
- 完善使用示例
```

## 注意事项

- 每条提交信息应只包含一个逻辑变更
- 保持提交粒度适中，避免超长提交
- 重要变更在 body 中详细说明
- 使用 `Closes #issue` 关联 GitHub Issue
