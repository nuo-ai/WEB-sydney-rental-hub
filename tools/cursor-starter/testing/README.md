# 测试阶段提示

此文件夹包含用于全面测试策略的提示——从单元测试到端到端测试和性能验证。这些提示可帮助您创建强大的测试套件，确保您的应用程序在所有条件下都能正常工作。

## 可用提示

### 核心测试
- **[测试生成](./test-generation.md)** - 创建全面的单元、集成和端到端测试
- **[集成测试](./integration-testing.md)** - 测试不同系统组件如何协同工作
- **[E2E 测试策略](./e2e-testing.md)** - 针对完整用户工作流的端到端测试

### 性能测试
- **[性能测试](./performance-testing.md)** - 负载测试、压力测试和基准测试

## 何时使用测试提示

### 开始测试开发
- 当您需要为新代码或现有代码创建测试时，使用**测试生成**
- 当您需要测试 API 端点、数据库操作或外部服务时，使用**集成测试**
- 当您想测试完整的用户旅程时，使用**E2E 测试策略**

### 性能验证
- 当您需要在负载下验证应用程序时，使用**性能测试**
- 将此用于容量规划、查找瓶颈和确保 SLA 合规性

## 测试工作流

使用这些提示的全面测试方法：

1. **单元测试** → 使用测试生成对单个函数和组件进行测试
2. **集成测试** → 使用集成测试对系统组件交互进行测试
3. **E2E 测试** → 使用 E2E 测试策略对完整的用户工作流进行测试
4. **性能测试** → 使用性能测试进行负载和压力验证

## 测试专业提示

### 测试生成
- 从关键业务逻辑和面向用户的功能开始
- 包括正常路径和错误场景
- 考虑边缘情况和边界条件

### 集成测试
- 尽可能测试实际集成，谨慎使用模拟
- 关注组件之间的数据流
- 包括故障场景和恢复测试

### E2E 测试
- 关注产生业务价值的关键用户旅程
- 保持测试的可维护性，不要太脆弱
- 包括跨浏览器和设备测试

### 性能测试
- 在测试前建立基线性能指标
- 使用真实的数据量和用户模式进行测试
- 包括正常负载和压力场景

## 与其他阶段的集成

- **从开发**：使用测试验证使用[开发阶段](../development/)提示创建的代码
- **从规划**：使用[规划阶段](../planning/)的要求指导测试场景
- **到部署**：使用[部署阶段](../deployment/)提示将测试集成到 CI/CD 中

## 测试策略快速参考

| 我想... | 使用此提示 |
|---|---|
| 为我的函数创建单元测试 | 测试生成 |
| 测试 API 端点和数据库操作 | 集成测试 |
| 测试完整的用户工作流 | E2E 测试策略 |
| 在负载下验证性能 | 性能测试 |

## 后续步骤

创建测试后：
- 使用[文档阶段](../documentation/)提示记录您的测试方法
- 使用[部署阶段](../deployment/)提示将测试集成到您的 CI/CD 流水线中
- 使用[维护阶段](../maintenance/)提示进行持续的测试维护

# Testing Phase Prompts

This folder contains prompts for comprehensive testing strategies - from unit tests to end-to-end testing and performance validation. These prompts help you create robust testing suites that ensure your application works correctly under all conditions.

## Available Prompts

### Core Testing
- **[Test Generation](./test-generation.md)** - Create comprehensive unit, integration, and e2e tests
- **[Integration Testing](./integration-testing.md)** - Test how different system components work together  
- **[E2E Testing Strategy](./e2e-testing.md)** - End-to-end testing for complete user workflows

### Performance Testing
- **[Performance Testing](./performance-testing.md)** - Load testing, stress testing, and benchmarking

## When to Use Testing Prompts

### Starting Test Development
- **Test Generation** when you need to create tests for new or existing code
- **Integration Testing** when you need to test API endpoints, database operations, or external services
- **E2E Testing Strategy** when you want to test complete user journeys

### Performance Validation
- **Performance Testing** when you need to validate your application under load
- Use this for capacity planning, finding bottlenecks, and ensuring SLA compliance

## Testing Workflow

A comprehensive testing approach using these prompts:

1. **Unit Tests** → Use Test Generation for individual functions and components
2. **Integration Tests** → Use Integration Testing for system component interactions
3. **E2E Tests** → Use E2E Testing Strategy for complete user workflows
4. **Performance Tests** → Use Performance Testing for load and stress validation

## Pro Tips for Testing

### Test Generation
- Start with critical business logic and user-facing features
- Include both happy path and error scenarios
- Consider edge cases and boundary conditions

### Integration Testing
- Test real integrations where possible, use mocks sparingly
- Focus on data flow between components
- Include failure scenarios and recovery testing

### E2E Testing
- Focus on critical user journeys that generate business value
- Keep tests maintainable and not too brittle
- Include cross-browser and device testing

### Performance Testing
- Establish baseline performance metrics before testing
- Test with realistic data volumes and user patterns
- Include both normal load and stress scenarios

## Integration with Other Phases

- **From Development**: Use tests to validate code created with [Development Phase](../development/) prompts
- **From Planning**: Use requirements from [Planning Phase](../planning/) to guide test scenarios
- **To Deployment**: Integrate tests into CI/CD using [Deployment Phase](../deployment/) prompts

## Testing Strategy Quick Reference

| I want to... | Use this prompt |
|--------------|----------------|
| Create unit tests for my functions | Test Generation |
| Test API endpoints and database operations | Integration Testing |
| Test complete user workflows | E2E Testing Strategy |
| Validate performance under load | Performance Testing |

## Next Steps

After creating your tests:
- Use [Documentation Phase](../documentation/) prompts to document your testing approach
- Use [Deployment Phase](../deployment/) prompts to integrate tests into your CI/CD pipeline
- Use [Maintenance Phase](../maintenance/) prompts for ongoing test maintenance
