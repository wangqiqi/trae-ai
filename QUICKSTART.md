# 🚀 Trae AI 超级团队 - 快速入门

## 快速开始

### 1. 启动控制台

```bash
python .trae/workflows/trae-console.py
```

### 2. 使用技能系统

在控制台中选择 **9. 技能系统**，你可以使用以下技能：

| 技能 | 功能 | 常用场景 |
|------|------|----------|
| project_scaffold | 项目脚手架 | 快速创建 Vue/React/FastAPI 项目 |
| code_analyzer | 代码分析 | 分析现有项目结构和语言分布 |
| readme_generator | README 生成 | 自动生成项目文档 |
| git_initializer | Git 初始化 | 快速配置 Git 仓库和 .gitignore |
| file_searcher | 文件搜索 | 快速搜索项目文件 |

### 3. 技能使用示例

#### 示例 1: 创建一个 Vue 项目

```
选择技能: 1 (project_scaffold)

输入参数:
  project_name: my-vue-app
  project_type: vue
```

#### 示例 2: 初始化 Git 仓库

```
选择技能: 4 (git_initializer)

输入参数:
  gitignore_template: python
  init: yes
  first_commit: yes
```

#### 示例 3: 生成 README

```
选择技能: 3 (readme_generator)

输入参数:
  project_name: my-awesome-project
  description: 一个很棒的项目
  author: 你的名字
  tech_stack: Python,FastAPI,Vue
```

### 4. 直接调用技能（编程方式）

你也可以在自己的代码中调用技能：

```python
import sys
from pathlib import Path

# 添加技能路径
skills_path = Path('.trae/skills')
sys.path.insert(0, str(skills_path))

# 使用技能管理器
from .trae.skills import use_skill, list_available_skills

# 查看所有技能
print("可用技能:", list_available_skills())

# 使用项目脚手架
result = use_skill('project_scaffold', 
                  project_type='vue', 
                  project_name='my-app')
print(result)
```

## 项目结构

```
learn_trae/
├── .trae/
│   ├── agent/           # AI 智能体配置
│   ├── core/            # 核心模块
│   ├── skills/          # 技能系统 🆕
│   ├── templates/       # 项目模板
│   ├── workflows/       # 工作流工具
│   └── ...
├── QUICKSTART.md        # 本文档
├── PROJECT_EVALUATION.md # 项目评估
└── requirements.txt
```

## 下一步

- 阅读 `PROJECT_EVALUATION.md` 了解项目评估和未来规划
- 尝试创建自定义技能，在 `.trae/skills/` 目录下添加新文件
- 探索 `templates` 目录下的项目模板

## 创建自定义技能

在 `.trae/skills/` 目录下创建新文件 `my_skill.py`：

```python
def execute(**kwargs):
    """你的技能描述"""
    name = kwargs.get('name', 'world')
    
    # 你的技能逻辑
    
    return {
        'success': True,
        'message': f'Hello, {name}!',
        'other_data': ...
    }
```

技能会自动被发现和加载！
