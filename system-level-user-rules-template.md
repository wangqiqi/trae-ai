# 🎯 Trae AI 系统级用户规则 - 融合版

> 将项目级最佳实践融合到系统级配置
> 适用于所有项目的全局AI行为配置

---\n
## 🚀 系统级核心原则

### 📋 全局开发规范

#### 1. 时间信息原则 (SYSTEM-001)
**强制要求**：
- ✅ 每次对话开始时自动获取当前日期时间
- ✅ 获取当前用户名和Git配置信息
- ✅ 所有文档和代码必须包含准确的时间戳
- ✅ 版权信息自动更新为当前年份

#### 2. 项目结构标准化 (SYSTEM-002)
**强制目录结构**：
```
项目根目录/
├── .trae/                 # AI团队配置
│   ├── principles.md      # 开发原则
│   ├── user_rules.md      # 项目规则
│   └── workflows/         # 工作流脚本
├── docs/                  # 文档目录
├── src/                   # 源代码
└── README.md             # 项目说明
```

#### 3. 智能体调用规范 (SYSTEM-003)
**标准格式**：
```
@智能体名称 具体任务描述 + 技术栈要求 + 截止时间

示例：
@Vue工程师 创建一个响应式用户登录组件，使用Vue3+TypeScript，今天完成
@Python工程师 设计RESTful API接口，使用FastAPI，包含用户认证功能
```

#### 4. 代码质量门槛 (SYSTEM-004)
**强制检查项**：
- 🎯 代码必须经过@测试工程师的测试用例
- 🎯 文档必须同步更新
- 🎯 每次提交前运行@DevOps工程师的环境检查
- 🎯 关键功能需要@系统架构师评审

#### 5. 渐进式开发流程 (SYSTEM-005)
**四阶段标准**：
| 阶段 | 时间 | 强制要求 | 交付标准 |
|------|------|----------|----------|
| 需求澄清 | 30分钟 | @产品经理参与 | 需求文档+验收标准 |
| 技术选型 | 20分钟 | @系统架构师评估 | 技术对比表+决策依据 |
| MVP开发 | 1-2天 | 单元测试覆盖 | 可运行Demo+文档 |
| 完善优化 | 1天 | 全测试覆盖 | 生产就绪+部署指南 |

---

## 🎯 智能体全局配置

### 👥 默认智能体优先级
1. **@产品经理** - 需求澄清阶段必须参与
2. **@系统架构师** - 技术方案必须评审
3. **@测试工程师** - 质量保证必须检查
4. **@DevOps工程师** - 部署前必须验证

### 🔧 技术栈默认配置

#### Web开发默认
- 前端：Vue3 + TypeScript + Vite + Pinia
- 后端：FastAPI + Python3.9+ + PostgreSQL
- 部署：Docker + Nginx + HTTPS

#### 移动开发默认
- 跨平台：Flutter + Dart
- 小程序：Uniapp + Vue3
- 原生：Swift/Kotlin

#### 数据科学默认
- Python：Pandas + NumPy + Scikit-learn
- 可视化：Plotly + Streamlit
- 部署：FastAPI + Docker

---

## 📊 工作流自动化模板

### 🔄 通用开发流程

```bash
# 1. 项目初始化（自动触发）
python .trae/workflows/project-init.py auto

# 2. 需求分析阶段
@产品经理 分析需求并生成PRD文档

# 3. 技术方案阶段  
@系统架构师 设计技术架构并评估方案

# 4. 开发阶段
@对应技术工程师 按阶段开发并测试

# 5. 部署阶段
@DevOps工程师 配置CI/CD并部署
```

### 🎯 质量检查点

#### 代码提交前检查
```bash
# 自动运行质量检查
python .trae/core/smart-cleanup.py pre-commit

# 运行测试套件
@测试工程师 执行全量测试用例

# 环境验证
python .trae/workflows/universal-env-manager.py validate
```

---

## 🚨 系统级故障排除

### 🔍 常见问题快速解决

#### Q1: 智能体无法识别
```bash
# 系统级重置
python .trae/workflows/team-launcher.py system-reset

# 重新扫描所有智能体
python .trae/workflows/team-launcher.py global-scan
```

#### Q2: 项目初始化失败
```bash
# 系统环境诊断
python .trae/core/system-enhancer.py --system-check

# 修复权限和路径
python .trae/core/system-enhancer.py --fix-permissions
```

#### Q3: 跨项目配置同步
```bash
# 将当前项目配置同步到系统级
python .trae/workflows/universal-env-manager.py sync-to-global

# 从系统级同步到新项目
python .trae/workflows/universal-env-manager.py sync-from-global
```

---

## 💡 高级系统功能

### 🎯 项目模板系统

#### 快速创建标准项目
```bash
# Web项目模板
python .trae/workflows/agent-suite.py generate system-web

# API服务模板  
python .trae/workflows/agent-suite.py generate system-api

# 移动应用模板
python .trae/workflows/agent-suite.py generate system-mobile
```

### 📊 全局统计分析

```bash
# 查看系统级使用统计
python .trae/core/project-assistant.py --system-stats

# 智能体使用效率分析
python .trae/workflows/team-launcher.py --global-usage

# 项目质量趋势报告
python .trae/core/project-assistant.py --quality-trend
```

---

## 🎉 一键系统配置

### 🔧 快速系统设置

#### 步骤1：备份现有配置
```bash
# 备份当前系统配置
copy "$env:USERPROFILE\.trae-cn\user_rules.md" "$env:USERPROFILE\.trae-cn\user_rules.md.backup"
```

#### 步骤2：应用系统级配置
将以下内容复制到：`C:\Users\%USERNAME%\.trae-cn\user_rules.md`

#### 步骤3：验证配置
```bash
# 测试系统级配置
python .trae/trae.py system-test
```

---

## 🎯 一句话总结

> **系统级配置 = 项目级最佳实践 × 全局标准化**

**一次配置，所有项目受益！**

---

*系统级配置更新时间：2025年8月*