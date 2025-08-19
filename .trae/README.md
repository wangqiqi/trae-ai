# Trae AI 统一控制台 v3.0

## 🎯 功能概览

**一个文件，全部搞定！** 新的统一控制台整合了：
- ✅ **项目管理**（原trae-ai-assistant.py功能）
- ✅ **智能体管理**（原agent-manager.py功能）
- ✅ **交互式操作**（命令行 + 对话模式）

## 📁 文件结构

```
.trae/
├── trae-console.py          # 🚀 统一控制台（新增）
├── .trae-dev.py            # 主程序（保持不变）
├── agents/                 # 智能体配置目录
│   ├── vue-engineer.json
│   ├── react-engineer.json
│   └── ...
└── data/                   # 项目数据
    └── projects.json       # 项目列表
```

## 🚀 快速开始

### 1. 交互模式（推荐）
```bash
python .trae/trae-console.py
```

### 2. 命令行模式
```bash
# 项目管理
python .trae/trae-console.py create-project "我想做一个Vue3任务管理系统"
python .trae/trae-console.py list-projects

# 智能体管理
python .trae/trae-console.py list-agents
python .trae/trae-console.py add-agent --name "新智能体" --role "new-role" --description "描述" --prompt "提示词"
python .trae/trae-console.py remove-agent --name "智能体名称"
```

## 🔄 从旧版本迁移

### ✅ 已完成的合并
- `trae-ai-assistant.py` → 整合到 `trae-console.py`
- `agent-manager.py` → 整合到 `trae-console.py`

### 📝 使用变化
**旧命令：**
```bash
python .trae/trae-ai-assistant.py "创建Vue3项目"
python .trae/agent-manager.py list
```

**新命令：**
```bash
python .trae/trae-console.py create-project "创建Vue3项目"
python .trae/trae-console.py list-agents
```

## 🎨 交互界面示例

```
🎯 Trae AI 统一控制台 v3.0
==================================================
💡 可用命令：
  项目相关：
    - '创建项目：我想做xxx'
    - '查看项目列表'
  智能体相关：
    - '查看智能体'
    - '添加智能体'
    - '删除智能体'
==================================================

🤖 请输入命令：我想做一个React博客系统
✅ 项目创建成功！
   名称：个人博客平台_0819
   技术栈：React + Node.js + MongoDB
   预计时间：2-4周
```

## 🛠️ 技术特点

- **🎭 统一入口**：一个文件，两种模式
- **🔄 向后兼容**：所有原功能保留
- **📊 数据分离**：项目数据与智能体配置独立存储
- **🎯 智能解析**：自动识别需求类型和技术栈

## 💡 使用建议

1. **日常使用**：启动交互模式，对话式操作
2. **脚本集成**：使用命令行模式，方便自动化
3. **团队协作**：智能体配置共享，项目数据独立

---

**版本升级完成！** 现在你只需要这一个文件，就能管理所有Trae AI功能！🎉