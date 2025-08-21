# 🎯 Trae AI 超级团队 - 中文用户规则手册

> 零学习成本，复制即用，20个AI专家为你服务
> 最新版本：v2.0 - 2025年8月全面升级

---

## 📋 目录导航

- [🚀 30秒快速上手](#-30秒快速上手)
- [🎭 20个AI智能体指南](#-20个ai智能体指南)
- [🔧 核心工具系统](#-核心工具系统)
- [📊 工作流自动化](#-工作流自动化)
- [🎯 优雅开发原则](#-优雅开发原则)
- [🆘 故障排除指南](#-故障排除指南)
- [💡 高级使用技巧](#-高级使用技巧)

---

## 🚀 30秒快速上手

### 🟢 零配置方案（新手推荐）

**第1步：复制目录**
```bash
# 复制整个 .trae 目录到你的项目根目录
cp -r learn_trae/.trae my-project/
cd my-project
```

**第2步：完成！**
- ✅ Trae IDE会自动检测并配置
- ✅ 无需任何手动操作
- ✅ 20个AI专家立即待命

### 🟡 快速启动方案

```bash
# 启动团队向导
python .trae/trae.py start

# 或直接进入控制台
python .trae/workflows/trae-console.py
```

### 🔵 项目初始化

```bash
# 一键初始化
python .trae/workflows/project-init.py quick

# 自定义初始化
python .trae/workflows/project-init.py custom
```

---

## 🎭 20个AI智能体指南

### 👥 管理类智能体（4个）

#### @产品经理
**专长**：需求分析、产品设计、用户故事
```
使用示例：
@产品经理 帮我设计一个Vue3任务管理系统
@产品经理 分析这个电商网站的用户需求
```

#### @系统架构师
**专长**：技术架构设计、系统规划
```
使用示例：
@系统架构师 设计Vue3+FastAPI的架构方案
@系统架构师 评估微服务架构的优缺点
```

#### @项目经理
**专长**：项目统筹、进度管理、风险控制
```
使用示例：
@项目经理 制定一个2周的项目开发计划
@项目经理 评估项目风险和时间节点
```

#### @项目协调员
**专长**：团队协作、任务分配、进度跟踪
```
使用示例：
@项目协调员 分配今天的开发任务
@项目协调员 跟踪项目进度和完成情况
```

### 💻 前端开发智能体（5个）

#### @Vue工程师
**技术栈**：Vue3 + TypeScript + Vite + Pinia
```
使用示例：
@Vue工程师 创建一个响应式待办事项组件
@Vue工程师 配置Vue Router和状态管理
```

#### @React工程师
**技术栈**：React18 + Hooks + Next.js + Redux
```
使用示例：
@React工程师 创建React电商商品列表
@React工程师 配置Next.js服务端渲染
```

#### @Angular工程师
**技术栈**：Angular15+ + RxJS + NgRx
```
使用示例：
@Angular工程师 创建Angular企业级仪表板
@Angular工程师 配置Angular表单验证
```

#### @Uniapp工程师
**技术栈**：Uniapp + 小程序 + App跨平台
```
使用示例：
@Uniapp工程师 创建跨平台商城应用
@Uniapp工程师 配置微信小程序支付功能
```

#### @Flutter工程师
**技术栈**：Flutter + Dart + 跨平台移动开发
```
使用示例：
@Flutter工程师 创建Flutter社交应用
@Flutter工程师 实现Flutter状态管理
```

### ⚙️ 后端开发智能体（5个）

#### @Python工程师
**技术栈**：FastAPI/Django/Flask + SQLAlchemy
```
使用示例：
@Python工程师 创建FastAPI用户认证系统
@Python工程师 设计RESTful API接口
```

#### @FastAPI工程师
**专长**：FastAPI专业API开发、异步编程
```
使用示例：
@FastAPI工程师 创建高性能API服务
@FastAPI工程师 配置FastAPI中间件和验证
```

#### @Node工程师
**技术栈**：Express/Nest.js + TypeScript
```
使用示例：
@Node工程师 创建Node.js后端服务
@Node工程师 配置Express中间件和路由
```

#### @Go工程师
**技术栈**：Go + Gin + GORM高性能后端
```
使用示例：
@Go工程师 创建Go微服务架构
@Go工程师 实现Go并发处理
```

#### @Rust工程师
**技术栈**：Rust + Actix + 系统级开发
```
使用示例：
@Rust工程师 创建Rust高性能服务
@Rust工程师 实现Rust内存安全编程
```

### 🔧 专项技术智能体（6个）

#### @测试工程师
**专长**：自动化测试、质量保证、测试策略
```
使用示例：
@测试工程师 为Vue3组件编写单元测试
@测试工程师 设计API接口测试方案
```

#### @DevOps工程师
**专长**：CI/CD、容器化、云部署
```
使用示例：
@DevOps工程师 配置Docker容器化部署
@DevOps工程师 设置GitHub Actions自动化部署
```

#### @UI/UX设计师
**专长**：界面设计、用户体验、交互原型
```
使用示例：
@UI/UX设计师 设计现代化管理后台界面
@UI/UX设计师 优化移动端用户体验
```

#### @技术文档工程师
**专长**：技术文档、API文档、用户手册
```
使用示例：
@技术文档工程师 生成API接口文档
@技术文档工程师 编写项目使用手册
```

#### @C++部署工程师
**专长**：C++系统部署和优化
```
使用示例：
@C++部署工程师 优化C++服务性能
@C++部署工程师 配置C++生产环境部署
```

---

## 🔧 核心工具系统

### 🎯 统一入口 - trae.py

**自动执行最合适的操作**
```bash
# 自动检测并执行
python .trae/trae.py

# 指定操作
python .trae/trae.py start    # 启动团队
python .trae/trae.py console # 启动控制台
python .trae/trae.py dev     # 开发助手
```

### 🛠️ 5大核心工具

#### 1. 系统增强器 - system-enhancer.py
**职责**：系统级优化、环境配置
```bash
python .trae/core/system-enhancer.py --full     # 全面优化
python .trae/core/system-enhancer.py --check    # 环境检查
python .trae/core/system-enhancer.py --python   # Python环境优化
```

#### 2. 项目助手 - project-assistant.py
**职责**：项目生命周期管理
```bash
python .trae/core/project-assistant.py --report     # 项目报告
python .trae/core/project-assistant.py --status     # 状态检查
python .trae/core/project-assistant.py --suggest    # 优化建议
```

#### 3. 智能清理 - smart-cleanup.py
**职责**：安全清理、空间优化
```bash
python .trae/core/smart-cleanup.py --analyze    # 分析可清理内容
python .trae/core/smart-cleanup.py --clean      # 执行清理
python .trae/core/smart-cleanup.py --backup    # 备份重要文件
```

#### 4. 智能提醒 - smart-reminder.py
**职责**：开发提醒、关键节点通知
```bash
python .trae/core/smart-reminder.py start       # 开始项目提醒
python .trae/core/smart-reminder.py developing   # 开发中提醒
python .trae/core/smart-reminder.py deploy       # 部署前提醒
```

#### 5. 跨平台适配器 - cross-platform-adapter.py
**职责**：命令统一、平台兼容（内部调用）

---

## 📊 工作流自动化

### 🔄 标准开发工作流

#### 阶段1：项目启动
```bash
# 1. 初始化项目
python .trae/workflows/project-init.py

# 2. 启动团队
python .trae/workflows/team-launcher.py start

# 3. 环境检查
python .trae/workflows/universal-env-manager.py check
```

#### 阶段2：开发进行
```bash
# 1. 进入控制台
python .trae/workflows/trae-console.py

# 2. 对话式开发
"我想创建一个Vue3电商网站"
"@Vue工程师 创建商品列表组件"
"@Python工程师 设计商品API"
```

#### 阶段3：部署上线
```bash
# 1. 部署准备
python .trae/workflows/universal-env-manager.py setup

# 2. 创建部署配置
@DevOps工程师 配置Docker部署

# 3. 执行部署
python .trae/workflows/deployment.py
```

### 🎯 智能体协作模式

#### 单人模式
```
用户 → @特定智能体 → 完成任务
```

#### 团队协作模式
```
用户 → @项目经理 → 任务分解 → 分配给其他智能体 → 整合结果
```

#### 项目模式
```
#项目类型 需求描述
#web 创建一个Vue3管理后台
#mobile 创建一个Flutter电商App
#api 创建FastAPI用户认证系统
```

---

## 🎯 优雅开发原则

### 📋 6大核心原则

#### PRINCIPLE-001：需求澄清原则
**实施步骤**：
1. 使用需求文档模板
2. 明确功能边界
3. 定义验收标准

**模板位置**：`.trae/templates/requirements-template.md`

#### PRINCIPLE-002：技术选型对比原则
**对比维度**：
- 学习成本
- 开发效率
- 性能表现
- 社区生态
- 维护成本
- 扩展性

**模板位置**：`.trae/templates/tech-choice-template.md`

#### PRINCIPLE-003：文档驱动开发原则
**文档清单**：
```
docs/
├── requirements.md      # 需求文档
├── architecture.md      # 系统设计
├── api-spec.md          # API文档
├── deployment.md        # 部署指南
└── checklist.md         # 验收清单
```

#### PRINCIPLE-004：渐进式实施原则
**四阶段迭代**：
| 阶段 | 目标 | 时间 | 交付物 |
|------|------|------|--------|
| 阶段1 | MVP验证 | 1-2天 | 核心功能 |
| 阶段2 | 功能完善 | 2-3天 | 增强功能 |
| 阶段3 | 性能优化 | 1天 | 质量提升 |
| 阶段4 | 扩展支持 | 1-2天 | 多端适配 |

#### PRINCIPLE-005：自动化文档生成原则
- 开发过程中自动生成API文档
- 保持文档与代码同步更新
- 确保docs目录完整性

#### PRINCIPLE-006：高效沟通协作原则
- 使用结构化反馈
- 关键节点自动通知
- 减少沟通次数，提高效率

---

## 🆘 故障排除指南

### 🔍 常见问题速查

#### Q1: 复制后无法运行？
**解决方案**：
```bash
# 1. 检查Python版本
python --version  # 需要3.7+

# 2. Windows系统权限
右键→属性→解除锁定

# 3. Linux/Mac权限
chmod +x .trae/trae.py
```

#### Q2: 智能体无法识别？
```bash
# 重新扫描智能体
python .trae/workflows/team-launcher.py list

# 检查路径
python .trae/workflows/team-launcher.py doctor
```

#### Q3: 环境配置问题？
```bash
# 诊断环境
python .trae/workflows/universal-env-manager.py doctor

# 重新配置
python .trae/workflows/universal-env-manager.py reset
```

#### Q4: 如何添加自定义智能体？
```bash
# 使用模板创建
python .trae/workflows/agent-suite.py create-custom

# 或手动创建
# 复制agent-template.json并修改
```

### 🚨 错误代码对照表

| 错误代码 | 问题描述 | 解决方案 |
|----------|----------|----------|
| TRAE-001 | Python版本过低 | 升级Python到3.7+ |
| TRAE-002 | 权限不足 | 以管理员身份运行 |
| TRAE-003 | 路径错误 | 检查项目根目录 |
| TRAE-004 | 智能体缺失 | 重新运行初始化 |

---

## 💡 高级使用技巧

### 🎯 控制台高级用法

#### 多智能体协作
```
# 在控制台中：
"@产品经理 帮我设计需求，然后@Vue工程师实现前端，@Python工程师实现后端"
```

#### 项目模板快速生成
```bash
# 生成完整项目模板
python .trae/workflows/agent-suite.py generate vue
python .trae/workflows/agent-suite.py generate react
python .trae/workflows/agent-suite.py generate fastapi
```

#### 批量任务处理
```bash
# 批量创建智能体
python .trae/workflows/agent-suite.py batch-create

# 批量更新配置
python .trae/workflows/agent-suite.py update-all
```

### 🔄 团队协作最佳实践

#### 1. 版本控制
```bash
# 将配置文件加入Git
git add .trae/
git add .trae-project.json
git commit -m "添加Trae AI团队配置"
```

#### 2. 环境同步
```bash
# 团队成员快速同步
python .trae/workflows/universal-env-manager.py sync
```

#### 3. 定期维护
```bash
# 每周运行一次
python .trae/core/smart-cleanup.py --analyze
python .trae/core/system-enhancer.py --check
```

### 📊 性能监控

#### 开发效率统计
```bash
# 查看项目统计
python .trae/core/project-assistant.py --stats

# 智能体使用统计
python .trae/workflows/team-launcher.py --usage
```

---

## 📱 跨平台使用指南

### 🪟 Windows
```bash
# 使用启动脚本
.trae\start.bat

# 或直接运行
python .trae\trae.py start
```

### 🍎 macOS
```bash
# 使用启动脚本
./.trae/start.sh

# 或直接运行
python3 .trae/trae.py start
```

### 🐧 Linux
```bash
# 使用启动脚本
./.trae/start.sh

# 或直接运行
python3 .trae/trae.py start
```

---

## 🎉 更新与维护

### 🔄 智能更新系统
```bash
# 检查更新
python .trae/workflows/team-launcher.py check-update

# 更新智能体
python .trae/workflows/agent-suite.py update-all

# 同步最新模板
python .trae/workflows/project-init.py sync-templates
```

### 💾 备份与恢复
```bash
# 备份当前配置
python .trae/core/smart-cleanup.py backup

# 恢复配置
python .trae/core/smart-cleanup.py restore
```

---

## 📞 获取帮助

### 🤝 支持渠道
1. **智能体帮助**：直接问@技术文档工程师
2. **系统诊断**：运行`python .trae/trae.py doctor`
3. **社区支持**：查看`.trae/README.md`

### 📚 学习资源
- [完整README](README.md) - 系统全面介绍
- [开发原则](principles.md) - 优雅开发最佳实践
- [模板库](templates/) - 各种项目模板

---

## 🎯 一句话总结

> **描述你的需求，20个AI专家会给你完整的解决方案！**

**复制即用，零配置，零学习成本！**

---

*最后更新：2025年8月 - v2.0 全面升级版本*