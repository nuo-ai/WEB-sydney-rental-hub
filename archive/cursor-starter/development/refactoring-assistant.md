# 代码重构助手

**使用场景：** 当您有可工作的代码需要改进、清理或重构时。

**技能水平：** 中级到高级

---

## 复制此提示：

```
我有一些可工作的代码需要重构，以提高其质量、可维护性和/或性能。请帮助我系统地重构这些代码。

## 当前代码：
[在此处粘贴您的代码]

## 重构目标：
请勾选适用于您情况的目标：
- [ ] 提高代码可读性和清晰度
- [ ] 减少代码重复
- [ ] 提高性能
- [ ] 更好的错误处理
- [ ] 增强可测试性
- [ ] 遵循更好的设计模式
- [ ] 降低复杂性
- [ ] 提高可维护性
- [ ] 更好地分离关注点
- [ ] [其他具体目标]

## 上下文：
- **代码功能**：[功能的简要描述]
- **当前痛点**：[当前代码存在哪些问题？]
- **限制**：[任何限制——不能更改接口、需要向后兼容等]
- **性能要求**：[任何特定的性能需求]

## 重构分析：

请提供：

### 1. 代码评估
- 识别具体的代码异味和问题
- 突出显示最需要关注的区域
- 解释为什么这些区域存在问题

### 2. 重构策略
- 建议分步重构计划
- 按影响和风险优先排序更改
- 推荐首先进行哪些重构

### 3. 具体改进
对于每个问题区域，请提供：
- **当前代码片段**
- **重构后的版本**
- **解释**改进了什么以及为什么
- 更改的**好处**

### 4. 设计模式机会
- 识别设计模式可以改进代码的地方
- 建议具体的模式以及如何实现它们
- 解释每种模式的好处

### 5. 测试策略
- 建议如何测试重构后的代码
- 建议确保行为未改变的方法
- 识别需要额外测试覆盖的区域

### 6. 迁移计划
- 如果这是一项大型重构，建议如何增量进行
- 识别潜在的破坏性更改
- 推荐回滚策略

### 7. 性能影响
- 突出显示任何性能影响（正面或负面）
- 建议性能改进
- 推荐基准测试方法

请专注于提供明确好处的实用、可操作的改进。解释每个建议更改背后的原因。
```

---

## 获得更好结果的提示：

- **包含代码功能的完整上下文**
- **指定您的限制**——可以更改什么，不能更改什么
- **提及您的代码库模式**——要遵循的现有约定
- **明确优先级**——可读性与性能与可维护性
- **包含可能受更改影响的相关代码**

# Code Refactoring Assistant

**Use this when:** You have working code that needs to be improved, cleaned up, or restructured.

**Skill Level:** Intermediate to Advanced

---

## Copy This Prompt:

```
I have working code that needs refactoring to improve its quality, maintainability, and/or performance. Please help me systematically refactor this code.

## Current Code:
[PASTE YOUR CODE HERE]

## Refactoring Goals:
Please check the goals that apply to your situation:
- [ ] Improve code readability and clarity
- [ ] Reduce code duplication
- [ ] Improve performance
- [ ] Better error handling
- [ ] Enhance testability
- [ ] Follow better design patterns
- [ ] Reduce complexity
- [ ] Improve maintainability
- [ ] Better separation of concerns
- [ ] [Other specific goals]

## Context:
- **What the code does**: [Brief description of functionality]
- **Current pain points**: [What's problematic about the current code?]
- **Constraints**: [Any limitations - can't change interfaces, need backward compatibility, etc.]
- **Performance requirements**: [Any specific performance needs]

## Refactoring Analysis:

Please provide:

### 1. Code Assessment
- Identify specific code smells and issues
- Highlight areas that need the most attention
- Explain why these areas are problematic

### 2. Refactoring Strategy
- Suggest a step-by-step refactoring plan
- Prioritise changes by impact and risk
- Recommend which refactorings to do first

### 3. Specific Improvements
For each problematic area, provide:
- **Current code snippet**
- **Refactored version**
- **Explanation** of what was improved and why
- **Benefits** of the change

### 4. Design Pattern Opportunities
- Identify where design patterns could improve the code
- Suggest specific patterns and how to implement them
- Explain the benefits of each pattern

### 5. Testing Strategy
- Recommend how to test the refactored code
- Suggest ways to ensure behavior hasn't changed
- Identify areas that need additional test coverage

### 6. Migration Plan
- If this is a large refactoring, suggest how to do it incrementally
- Identify potential breaking changes
- Recommend rollback strategies

### 7. Performance Implications
- Highlight any performance impacts (positive or negative)
- Suggest performance improvements
- Recommend benchmarking approaches

Please focus on practical, actionable improvements that provide clear benefits. Explain the reasoning behind each suggested change.
```

---

## Tips for Better Results:

- **Include the full context** of what the code does
- **Specify your constraints** - what can and cannot be changed
- **Mention your codebase patterns** - existing conventions to follow
- **Be clear about priorities** - readability vs performance vs maintainability
- **Include related code** that might be affected by changes
