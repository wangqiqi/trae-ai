---
command: evolution-automation
description: "自动化演进系统 - 基于感知数据的智能规则自动优化"
globs: ["*.json", "*.yaml", "*.yml"]
alwaysApply: false
---

# 🤖 自动化演进系统 (Automated Evolution System)

*版本: v3.0.0 | 最后更新: {{GENERATION_TIME}} | 作者: {{AUTHOR_NAME}} <{{AUTHOR_EMAIL}}}*

## 🎯 核心机制 (Core Mechanisms)

自动化演进系统通过持续感知项目状态和用户行为，实现规则的智能优化和自动调整。新增规则演进建议系统，基于数据驱动提供具体的演进方向和实施建议。

## 📊 自动化感知接口 (Automated Perception Interface)

自动化演进系统基于直接的数据源感知，实现规则的自动优化。

### 数据源 (Data Sources)
- **项目状态**: 直接调用 `perception.sh` 脚本进行项目变化感知
- **用户行为**: 基于协作历史和使用模式分析
- **系统指标**: 集成 `@evolution-governance` 的监控数据

### 感知触发 (Perception Triggers)
系统通过以下方式获取感知数据：
- 定时调用 `perception.sh` 脚本进行项目状态扫描
- 分析用户协作模式和反馈数据
- 集成 `@evolution-governance` 的实时监控指标

## 🤖 自动化优化算法 (Automated Optimization Algorithms)

### 核心算法 (Core Algorithms)

#### 强化学习优化 (Reinforcement Learning)
```python
# 基于历史数据训练规则参数优化模型
class RuleOptimizer:
    def __init__(self, perception_data, governance_metrics):
        self.perception = perception_data
        self.metrics = governance_metrics

    def optimize_rules(self):
        # 分析感知数据变化趋势
        trends = self.analyze_trends()

        # 计算最优参数组合
        optimal_params = self.calculate_optimal(trends)

        # 生成优化建议
        suggestions = self.generate_suggestions(optimal_params)
        return suggestions
```

#### 规则演进建议引擎 (Rule Evolution Suggestion Engine) ⭐ 新增

基于感知数据和使用模式，智能生成具体的规则演进建议：

##### 演进分析维度 (Evolution Analysis Dimensions)
```typescript
interface EvolutionAnalyzer {
  // 项目成熟度分析
  analyzeProjectMaturity(perception: PerceptionData): MaturityLevel

  // 用户协作模式分析
  analyzeCollaborationPatterns(interactions: InteractionHistory[]): CollaborationPattern

  // 技术栈演进趋势
  analyzeTechStackEvolution(techData: TechStackData): EvolutionTrend

  // 规则使用效率分析
  analyzeRuleEfficiency(usage: RuleUsageData): EfficiencyMetrics

  // 生成演进建议
  generateEvolutionSuggestions(analysis: AnalysisResult): EvolutionSuggestion[]
}

// 演进建议生成示例
const analyzer = new EvolutionAnalyzer()

// 1. 综合分析
const maturity = analyzer.analyzeProjectMaturity(perceptionData)
// 返回: {level: 'growing', confidence: 0.85}

const patterns = analyzer.analyzeCollaborationPatterns(interactionHistory)
// 返回: {style: 'iterative', team_size: 'small', frequency: 'daily'}

const techTrends = analyzer.analyzeTechStackEvolution(techStackData)
// 返回: {direction: 'modernization', priority: 'high', timeline: '3_months'}

const efficiency = analyzer.analyzeRuleEfficiency(ruleUsageData)
// 返回: {optimal_rules: ['eslint', 'system_info'], underutilized: ['templates']}

// 2. 生成综合建议
const suggestions = analyzer.generateEvolutionSuggestions({
  maturity, patterns, techTrends, efficiency
})
```

##### 智能建议类型 (Intelligent Suggestion Types)

###### 项目成熟度建议 (Maturity-Based Suggestions)
- **早期项目**：建议启用基础规则，保持轻量级
- **成长项目**：建议增加质量控制和协作规则
- **成熟项目**：建议启用高级自动化和治理规则

###### 协作模式建议 (Collaboration-Based Suggestions)
- **个人开发**：优化为高效单人工作流
- **小团队**：启用同行评审和标准化规则
- **大团队**：强化流程控制和文档要求

###### 技术栈演进建议 (Technology Evolution Suggestions)
- **现代化改造**：建议升级到新版本框架
- **最佳实践 adoption**：引入行业标准工具
- **性能优化**：基于使用数据优化技术选择

###### 使用效率建议 (Efficiency-Based Suggestions)
- **规则优化**：停用低效规则，启用高效替代
- **流程简化**：基于使用模式优化工作流程
- **自动化增强**：增加重复任务的自动化程度

##### 建议优先级算法 (Suggestion Priority Algorithm)
```typescript
interface SuggestionPrioritizer {
  // 计算建议优先级
  calculatePriority(suggestion: EvolutionSuggestion): PriorityScore

  // 考虑实施难度
  assessImplementationDifficulty(suggestion: EvolutionSuggestion): DifficultyLevel

  // 评估潜在收益
  estimatePotentialBenefit(suggestion: EvolutionSuggestion): BenefitScore

  // 生成实施路线图
  createImplementationRoadmap(suggestions: EvolutionSuggestion[]): Roadmap
}

// 优先级计算示例
const prioritizer = new SuggestionPrioritizer()

const priority = prioritizer.calculatePriority(suggestion)
// 基于: 收益大小 × 实施难度倒数 × 紧急程度

const roadmap = prioritizer.createImplementationRoadmap(suggestions)
// 返回结构化的实施计划，按阶段和依赖关系排序
        suggestions = self.generate_suggestions(optimal_params)

        return suggestions
```

#### 模式识别引擎 (Pattern Recognition Engine)
- **聚类分析**: 识别用户群体和行为模式
- **趋势预测**: 基于历史数据预测未来需求
- **异常检测**: 识别异常行为和潜在问题

#### 决策树优化 (Decision Tree Optimization)
```yaml
optimization_decision_tree:
  root: "perception_data_changed"
  branches:
    - condition: "project_scale > 25%"
      action: "relax_code_quality_rules"
      reason: "大项目需要平衡效率与质量"
    - condition: "team_size > 10"
      action: "enable_collaboration_gates"
      reason: "大团队需要更严格的协作控制"
    - condition: "user_satisfaction < 70%"
      action: "adjust_interaction_mode"
      reason: "提升用户体验优先级"
```

### 执行机制 (Execution Mechanisms)

#### 渐进式应用 (Gradual Application)
1. **评估阶段**: 计算优化影响和风险
2. **试点阶段**: 小范围测试优化效果
3. **扩展阶段**: 逐步扩大应用范围
4. **验证阶段**: 确认优化效果并固化改进

## 📈 学习算法 (Learning Algorithms)

### 数据收集 (Data Collection)
```json
{
  "usage_metrics": {
    "rule_activation_count": 150,
    "average_response_time": 2.3,
    "user_satisfaction_score": 4.2
  },
  "feedback_analysis": {
    "positive_signals": 45,
    "negative_signals": 12,
    "improvement_suggestions": 8
  }
}
```

### 模型训练 (Model Training)
- 基于历史数据训练优化模型
- 使用强化学习优化规则参数
- 应用聚类分析识别用户群体

### 效果评估 (Effectiveness Evaluation)
- A/B测试不同规则配置
- 用户满意度调查和分析
- 性能指标监控和趋势分析

## 🛡️ 安全集成 (Safety Integration)

自动化演进系统与 `@evolution-governance` 深度集成，确保所有自动化操作符合安全标准：

### 治理集成 (Governance Integration)
- **风险评估**: 调用 governance 的风险控制机制
- **质量验证**: 使用 governance 的质量控制流程
- **合规检查**: 遵循 governance 的合规性要求

### 安全执行 (Safe Execution)
- **渐进部署**: 遵循 governance 的灰度发布策略
- **监控告警**: 集成 governance 的监控体系
- **应急响应**: 使用 governance 的应急响应流程

## 📊 效果追踪 (Effectiveness Tracking)

自动化系统通过 `@evolution-governance` 的监控体系追踪优化效果：

### 关键指标 (Key Metrics)
- **自动化效率**: 规则优化响应时间和成功率
- **用户影响**: 自动化调整对用户体验的影响
- **系统稳定性**: 自动化操作的可靠性和异常率

### 数据集成 (Data Integration)
所有性能数据通过 governance 的监控系统统一收集和分析，确保数据一致性和可追溯性。

---

*自动化演进系统通过智能感知和数据驱动的方式，实现规则的自动优化和持续改进。*

