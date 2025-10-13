# 全面测试生成

**使用场景：** 当您需要为代码创建全面的测试时，无论是单元测试、集成测试还是端到端测试。

**技能水平：** 初级到高级

---

## 复制此提示：

```
我需要帮助为我的代码生成全面的测试。请创建一个全面的测试套件，涵盖各种场景和边缘情况。

## 要测试的代码：
[在此处粘贴您的代码或描述功能]

## 测试要求：
- **所需测试类型**：[单元测试 / 集成测试 / E2E 测试 / 以上全部]
- **测试框架**：[Jest、Vitest、Pytest、JUnit 等 - 或请求推荐]
- **覆盖率目标**：[您期望的代码覆盖率百分比是多少？]
- **具体关注点**：[您担心的任何特定边缘情况或场景？]

## 测试生成请求：

请创建：

### 1. 测试策略概述
- 解释整体测试方法
- 确定每个级别需要测试的内容
- 推荐测试结构和组织

### 2. 单元测试
生成涵盖以下内容的单元测试：
- **正常路径场景** - 正常、预期的使用
- **边缘情况** - 边界条件、空输入、空值
- **错误条件** - 无效输入、网络故障等
- **状态更改** - 有状态代码的前后条件
- **集成点** - 模拟的依赖项及其交互

### 3. 测试数据和固定数据
创建：
- **各种场景的测试数据集**
- **外部依赖项的模拟对象**
- **用于设置和拆卸的测试固定数据**
- **用于生成测试数据的工厂函数**

### 4. 断言和期望
对于每个测试，包括：
- **清晰的测试描述**，解释正在测试的内容
- **验证预期行为的正确断言**
- **错误情况的错误消息验证**
- **如果相关，则进行性能断言**

### 5. 高级测试场景
考虑：
- **并发测试** - 竞态条件、异步行为
- **安全测试** - 输入验证、注入攻击
- **性能测试** - 负载、压力、内存使用
- **兼容性测试** - 不同的环境、浏览器、设备

### 6. 测试维护
提供：
- **测试组织** - 如何组织测试文件
- **测试和测试数据的命名约定**
- **复杂测试场景的文档**
- **CI/CD 集成**建议

## 测试代码格式：
请提供：
- 完整、可运行的测试代码
- 解释复杂测试逻辑的清晰注释
- 需要时的设置和拆卸代码
- 运行测试的说明

## 额外考虑：
- 建议用于测试覆盖率报告的工具
- 推荐测试难以测试的代码的方法
- 提供随着代码演变维护测试的指南
- 如果适用，建议性能基准

重点是创建可靠、可维护且能提供代码正确性信心的测试。
```

---

## 获得更好结果的提示：

- **包含完整的代码上下文**——不仅仅是单个函数
- **指定您的测试环境**和任何限制
- **提及现有测试**，以便 AI 不会重复工作
- **明确测试理念**——严格的 TDD 与务实的测试
- **包含影响应测试内容领域知识**

# Comprehensive Test Generation

**Use this when:** You need to create thorough tests for your code, whether unit, integration, or end-to-end tests.

**Skill Level:** Beginner to Advanced

---

## Copy This Prompt:

```
I need help generating comprehensive tests for my code. Please create a thorough test suite that covers various scenarios and edge cases.

## Code to Test:
[PASTE YOUR CODE HERE OR DESCRIBE THE FUNCTIONALITY]

## Testing Requirements:
- **Test Types Needed**: [Unit tests / Integration tests / E2E tests / All of the above]
- **Testing Framework**: [Jest, Vitest, Pytest, JUnit, etc. - or ask for recommendation]
- **Coverage Goals**: [What percentage of code coverage are you aiming for?]
- **Specific Concerns**: [Any particular edge cases or scenarios you're worried about?]

## Test Generation Request:

Please create:

### 1. Test Strategy Overview
- Explain the overall testing approach
- Identify what needs to be tested at each level
- Recommend test structure and organisation

### 2. Unit Tests
Generate unit tests that cover:
- **Happy path scenarios** - normal, expected usage
- **Edge cases** - boundary conditions, empty inputs, null values
- **Error conditions** - invalid inputs, network failures, etc.
- **State changes** - before/after conditions for stateful code
- **Integration points** - mocked dependencies and their interactions

### 3. Test Data & Fixtures
Create:
- **Test data sets** for various scenarios
- **Mock objects** for external dependencies
- **Test fixtures** for setup and teardown
- **Factory functions** for generating test data

### 4. Assertions & Expectations
For each test, include:
- **Clear test descriptions** that explain what's being tested
- **Proper assertions** that validate expected behavior
- **Error message validation** for error cases
- **Performance assertions** if relevant

### 5. Advanced Testing Scenarios
Consider:
- **Concurrency testing** - race conditions, async behavior
- **Security testing** - input validation, injection attacks
- **Performance testing** - load, stress, memory usage
- **Compatibility testing** - different environments, browsers, devices

### 6. Test Maintenance
Provide:
- **Test organisation** - how to structure test files
- **Naming conventions** for tests and test data
- **Documentation** for complex test scenarios
- **CI/CD integration** recommendations

## Test Code Format:
Please provide:
- Complete, runnable test code
- Clear comments explaining complex test logic
- Setup and teardown code where needed
- Instructions for running the tests

## Additional Considerations:
- Suggest tools for test coverage reporting
- Recommend approaches for testing difficult-to-test code
- Provide guidelines for maintaining tests as code evolves
- Suggest performance benchmarks if applicable

Focus on creating tests that are reliable, maintainable, and provide confidence in the code's correctness.
```

---

## Tips for Better Results:

- **Include complete code context** - not just individual functions
- **Specify your testing environment** and any constraints
- **Mention existing tests** so AI doesn't duplicate efforts
- **Be clear about testing philosophy** - strict TDD vs pragmatic testing
- **Include domain knowledge** that affects what should be tested
