# 🤖 智能体文件统一工具包使用指南

## 🎯 工具简介

`agent_toolkit.py` 是一个统一的智能体文件管理工具，整合了之前三个独立脚本的功能：
- ✅ **check** - 检查文件状态
- 🔧 **fix** - 修复JSON格式
- ✨ **optimize** - 优化文件结构

## 📋 基本用法

### 1. 检查文件状态
```bash
# 检查单个文件
python agent_toolkit.py check 文件名.json

# 检查所有文件
python agent_toolkit.py --all-files check
```

### 2. 修复JSON格式
```bash
# 修复单个文件
python agent_toolkit.py fix 文件名.json

# 修复所有文件
python agent_toolkit.py --all-files fix
```

### 3. 优化文件结构
```bash
# 优化单个文件
python agent_toolkit.py optimize 文件名.json

# 优化所有文件
python agent_toolkit.py --all-files optimize
```

## 🚀 高级用法 - 组合命令

### 一键完成所有操作
```bash
# 对单个文件执行所有操作
python agent_toolkit.py all 文件名.json

# 对所有文件执行所有操作
python agent_toolkit.py --all-files all
```

### 自定义组合操作
```bash
# 检查+修复
python agent_toolkit.py check+fix 文件名.json

# 检查+优化
python agent_toolkit.py check+optimize 文件名.json

# 修复+优化
python agent_toolkit.py fix+optimize 文件名.json

# 检查+修复+优化
python agent_toolkit.py check+fix+optimize 文件名.json
```

## 📊 状态说明

| 状态 | 含义 | 自动修复 |
|------|------|----------|
| ✅ | 优秀 - 无需任何操作 | - |
| ⚠️ | 需优化 - 缺少字段或格式问题 | 可以 |
| 🔴 | 需修复 - 命名或结构问题 | 可以 |
| ❌ | 错误 - JSON格式错误 | 可以 |

## 🔍 检查内容

工具会自动检查以下内容：

### 1. 必需字段
- `name` - 智能体名称
- `role` - 角色描述
- `description` - 详细描述
- `capabilities` - 能力列表
- `prompts` - 提示词
- `output_format` - 输出格式
- `examples` - 示例
- `templates` - 模板
- `review_checkpoints` - 检查点

### 2. Examples格式
- 自动转换：`scenario` → `input`
- 自动转换：`description` → `output`

### 3. 字段命名
- 自动修复：`core_responsibilities` → `capabilities`

### 4. JSON格式
- 美化JSON格式，统一缩进

## 💡 使用建议

### 日常维护
```bash
# 每天开始工作前检查
python agent_toolkit.py --all-files check

# 发现问题后一键修复
python agent_toolkit.py --all-files all
```

### 新增文件
```bash
# 添加新文件后立即检查
python agent_toolkit.py check 新文件.json

# 一键优化
python agent_toolkit.py all 新文件.json
```

### 批量处理
```bash
# 批量检查
python agent_toolkit.py --all-files check

# 批量修复
python agent_toolkit.py --all-files fix

# 批量优化
python agent_toolkit.py --all-files optimize

# 批量全部处理
python agent_toolkit.py --all-files all
```

## 🎯 实际案例

### 案例1：发现问题的文件
```bash
# 检查发现问题
python agent_toolkit.py check test_agent.json
# 输出：
# 🔴 检查结果:
#    - examples格式需转换: scenario→input
#    - 字段命名需修复: core_responsibilities→capabilities
#    缺失字段: description, capabilities, prompts...

# 一键修复
python agent_toolkit.py all test_agent.json
# 输出：
# ✅ JSON格式已修复
# ✅ 优化完成: scenario→input, description→output...
```

### 案例2：批量处理
```bash
# 检查所有文件
python agent_toolkit.py --all-files check

# 一键优化所有文件
python agent_toolkit.py --all-files all
```

## 📝 注意事项

1. **备份建议**：在批量操作前建议备份重要文件
2. **逐步操作**：可以先检查再修复，避免意外修改
3. **查看结果**：每次操作后都有详细的状态报告
4. **组合使用**：灵活使用组合命令提高效率

## 🔄 迁移说明

### 从旧脚本迁移

| 旧脚本 | 新命令 |
|--------|--------|
| `check_agents.py` | `agent_toolkit.py check` |
| `fix_json.py 文件.json` | `agent_toolkit.py fix 文件.json` |
| `batch_optimize.py 文件.json` | `agent_toolkit.py optimize 文件.json` |
| `batch_optimize.py --all` | `agent_toolkit.py --all-files all` |

## 🎉 总结

新工具 `agent_toolkit.py` 提供了：
- ✅ 更统一的操作体验
- 🚀 支持组合命令
- 📊 详细的状态报告
- 🔄 向后兼容旧功能
- 💡 更智能的自动修复

使用这个新工具，你可以更高效地管理智能体文件，确保所有文件都符合统一标准！