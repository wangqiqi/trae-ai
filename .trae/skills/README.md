# 🎯 Trae AI Skills 技能目录

这里存放可以被 Trae AI 系统调用的自定义技能。

## 什么是技能？

技能是可以让 Trae AI 执行特定任务的扩展能力。每个技能都是一个 Python 文件，遵循特定的接口规范。

## 技能文件结构

```python
# .trae/skills/your_skill_name.py

def execute(**kwargs):
    """
    技能执行入口函数
    
    Args:
        **kwargs: 技能参数
        
    Returns:
        执行结果
    """
    # 你的技能代码
    pass
```

## 使用技能

在与 Trae AI 对话时，可以直接调用技能：
```
使用技能 your_skill_name 参数1=值1 参数2=值2
```

## 技能示例

- **project_scaffold** - 项目脚手架生成
- **code_analyzer** - 代码分析工具
- **doc_generator** - 文档生成器
