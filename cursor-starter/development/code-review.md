# 全面代码审查

**使用场景：** 当您希望在提交或部署代码之前获得对其进行彻底分析和反馈时。

**技能水平：** 初级到高级

---

## 复制此提示：

```
请对以下代码进行全面代码审查。我希望获得关于代码质量、最佳实践、潜在问题和改进建议的详细反馈。

[在此处粘贴您的代码或引用要审查的文件]

## 代码审查重点领域：

### 1. 代码质量与结构
- 代码是否组织良好且易于理解？
- 函数和类的大小和焦点是否适当？
- 命名是否清晰且具有描述性？
- 是否存在任何代码异味或反模式？

### 2. 最佳实践与标准
- 代码是否遵循语言/框架的最佳实践？
- 是否存在任何编码标准违规？
- 错误处理是否正确实现？
- 是否存在任何安全漏洞？

### 3. 性能与效率
- 是否存在任何性能瓶颈？
- 任何算法或数据结构是否可以优化？
- 资源是否得到有效利用？
- 是否存在任何不必要的计算或内存使用？

### 4. 可维护性与可读性
- 这段代码维护起来有多容易？
- 注释是否有帮助且不冗余？
- 代码是否具有自文档性？
- 新开发人员是否能轻松理解？

### 5. 测试与可靠性
- 边缘情况是否得到妥善处理？
- 您看到了哪些潜在的错误或问题？
- 是否有机会更好地处理错误？
- 您会推荐测试什么？

### 6. 架构与设计
- 代码是否遵循良好的架构原则？
- 是否有适当的关注点分离？
- 依赖项是否管理良好？
- 设计是否可以简化或改进？

## 反馈格式：
请提供：
- **关键问题**：必须修复的问题（安全、错误等）
- **主要改进**：重要的代码质量问题
- **次要建议**：锦上添花的改进
- **积极方面**：代码中做得好的地方
- **重构建议**：具体的代码改进示例

对于每个问题，请解释问题并提供建议的解决方案或改进。
```

---

## 获得更好结果的提示：

- **包含项目上下文**以及代码的功能
- **提及您对某些部分的具体担忧**
- **指定您的经验水平**，以便可以相应地调整反馈
- **包含任何限制**（性能要求、遗留系统兼容性）
- **要求对建议的改进进行优先级排序**

# Comprehensive Code Review

**Use this when:** You want thorough analysis and feedback on your code before committing or deploying.

**Skill Level:** Beginner to Advanced

---

## Copy This Prompt:

```
Please perform a comprehensive code review of the following code. I want detailed feedback on code quality, best practices, potential issues, and suggestions for improvement.

[PASTE YOUR CODE HERE OR REFERENCE THE FILES TO REVIEW]

## Code Review Focus Areas:

### 1. Code Quality & Structure
- Is the code well-organised and easy to understand?
- Are functions and classes appropriately sized and focused?
- Is the naming clear and descriptive?
- Are there any code smells or anti-patterns?

### 2. Best Practices & Standards
- Does the code follow language/framework best practices?
- Are there any violations of coding standards?
- Is error handling implemented properly?
- Are there any security vulnerabilities?

### 3. Performance & Efficiency
- Are there any performance bottlenecks?
- Can any algorithms or data structures be optimised?
- Are resources being used efficiently?
- Any unnecessary computations or memory usage?

### 4. Maintainability & Readability
- How easy would this code be to maintain?
- Are comments helpful and not redundant?
- Is the code self-documenting?
- Would a new developer understand this easily?

### 5. Testing & Reliability
- Are edge cases handled properly?
- What potential bugs or issues do you see?
- Are there opportunities for better error handling?
- What would you recommend testing?

### 6. Architecture & Design
- Does the code follow good architectural principles?
- Is there proper separation of concerns?
- Are dependencies managed well?
- Could the design be simplified or improved?

## Feedback Format:
Please provide:
- **Critical Issues**: Must-fix problems (security, bugs, etc.)
- **Major Improvements**: Important code quality issues
- **Minor Suggestions**: Nice-to-have improvements
- **Positive Aspects**: What's done well in the code
- **Refactoring Suggestions**: Specific code improvements with examples

For each issue, please explain the problem and provide a suggested solution or improvement.
```

---

## Tips for Better Results:

- **Include context** about the project and what the code does
- **Mention specific concerns** you have about certain parts
- **Specify your experience level** so feedback can be tailored appropriately
- **Include any constraints** (performance requirements, legacy system compatibility)
- **Ask for priority ranking** of suggested improvements
