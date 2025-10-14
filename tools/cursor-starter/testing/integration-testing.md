# 集成测试助手

**使用场景：** 当您需要测试系统的不同部分如何协同工作时，包括 API、数据库和外部服务。

**技能水平：** 中级到高级

---

## 复制此提示：

```
我需要帮助为我的应用程序创建全面的集成测试。请帮助我设计和实施测试，以验证不同组件如何协同工作。

## 系统上下文：
- **应用程序架构**：[微服务、单体、无服务器等]
- **技术栈**：[语言、框架、数据库等]
- **外部依赖项**：[API、数据库、消息队列等]
- **测试框架**：[Jest、Pytest、JUnit 等 - 或请求推荐]

## 要测试的集成点：
[描述关键集成点 - API 端点、数据库操作、外部服务调用等]

## 当前测试设置：
[描述任何现有的测试基础设施以及您已测试的内容]

## 集成测试策略：

请创建一个全面的集成测试方法，涵盖：

### 1. 测试策略概述
- 集成测试级别和范围
- 测试环境设置和要求
- 测试的数据管理策略
- CI/CD 集成方法

### 2. API 集成测试
- **端点测试**：完整的请求/响应周期测试
- **身份验证测试**：令牌验证、会话管理
- **数据验证**：请求/响应模式验证
- **错误处理**：错误响应、超时处理
- **速率限制**：API 节流和配额测试

### 3. 数据库集成测试
- **CRUD 操作**：创建、读取、更新、删除测试
- **事务测试**：数据库事务完整性
- **迁移测试**：模式更改和数据迁移
- **性能测试**：查询性能和优化
- **约束测试**：外键、唯一约束、验证

### 4. 外部服务集成
- **API 客户端测试**：第三方 API 集成
- **模拟与真实服务**：何时使用模拟与真实服务
- **失败场景**：网络故障、服务停机
- **身份验证流**：OAuth、API 密钥验证
- **数据同步**：跨服务的数据一致性

### 5. 消息队列/事件测试
- **消息发布**：事件发布和路由
- **消息消费**：事件处理和处理
- **死信队列**：失败消息处理
- **排序和交付**：消息排序保证
- **事件溯源**：事件存储集成（如果适用）

### 6. 文件系统集成
- **文件上传/下载**：文件处理操作
- **存储集成**：云存储（S3、GCS 等）
- **文件处理**：图像处理、文档处理
- **备份和恢复**：数据备份程序

### 7. 测试数据管理
- **测试数据设置**：创建逼真的测试数据集
- **数据清理**：拆卸和清理程序
- **数据隔离**：防止测试干扰
- **种子数据**：跨环境的一致测试数据
- **数据工厂**：以编程方式生成测试数据

### 8. 环境配置
- **测试环境设置**：隔离的测试环境
- **配置管理**：环境特定设置
- **秘密管理**：测试中的 API 密钥、凭据
- **容器测试**：Docker/Kubernetes 集成
- **本地开发**：在本地运行集成测试

### 9. 测试实施示例
对于每个集成点，请提供：
- **完整的测试代码**，包括设置和拆卸
- **成功和失败案例的断言示例**
- **外部依赖项的模拟配置**
- **网络故障的错误处理测试**
- **相关情况下的性能断言**

### 10. 高级测试场景
- **契约测试**：API 契约验证
- **端到端工作流**：多步骤业务流程
- **并发测试**：竞态条件、并行执行
- **安全测试**：授权、输入验证
- **混沌测试**：弹性和容错性

## 测试组织结构：
- 推荐测试文件组织
- 集成测试的命名约定
- 有效地对相关测试进行分组
- 并行测试执行策略

## CI/CD 集成：
- 集成测试流水线设置
- 何时运行集成测试
- 处理测试失败和重试
- 测试报告和通知

## 监控和维护：
- 测试结果分析和报告
- 识别不稳定的测试
- 测试性能监控
- 随系统更改更新测试

请提供具体的、可立即实施的可运行测试代码示例。
```

---

## 获得更好结果的提示：

- **规划所有集成点**——API、数据库、外部服务
- **包含您当前的测试设置**——您正在使用的框架和工具
- **指定环境限制**——本地与云、CI/CD 要求
- **提及数据敏感性**——PII、测试数据隔离需求
- **包含性能要求**——测试执行时间、并行执行

# Integration Testing Assistant

**Use this when:** You need to test how different parts of your system work together, including APIs, databases, and external services.

**Skill Level:** Intermediate to Advanced

---

## Copy This Prompt:

```
I need help creating comprehensive integration tests for my application. Please help me design and implement tests that verify how different components work together.

## System Context:
- **Application Architecture**: [Microservices, monolith, serverless, etc.]
- **Technology Stack**: [Languages, frameworks, databases, etc.]
- **External Dependencies**: [APIs, databases, message queues, etc.]
- **Testing Framework**: [Jest, Pytest, JUnit, etc. - or ask for recommendation]

## Integration Points to Test:
[Describe the key integration points - API endpoints, database operations, external service calls, etc.]

## Current Testing Setup:
[Describe any existing testing infrastructure and what you've already tested]

## Integration Testing Strategy:

Please create a comprehensive integration testing approach that covers:

### 1. Testing Strategy Overview
- Integration testing levels and scope
- Test environment setup and requirements
- Data management strategy for tests
- CI/CD integration approach

### 2. API Integration Testing
- **Endpoint Testing**: Full request/response cycle testing
- **Authentication Testing**: Token validation, session management
- **Data Validation**: Request/response schema validation
- **Error Handling**: Error responses, timeout handling
- **Rate Limiting**: API throttling and quota testing

### 3. Database Integration Testing
- **CRUD Operations**: Create, read, update, delete testing
- **Transaction Testing**: Database transaction integrity
- **Migration Testing**: Schema changes and data migration
- **Performance Testing**: Query performance and optimization
- **Constraint Testing**: Foreign keys, unique constraints, validations

### 4. External Service Integration
- **API Client Testing**: Third-party API integration
- **Mock vs Real Services**: When to use mocks vs real services
- **Failure Scenarios**: Network failures, service downtime
- **Authentication Flow**: OAuth, API key validation
- **Data Synchronization**: Data consistency across services

### 5. Message Queue/Event Testing
- **Message Publishing**: Event publishing and routing
- **Message Consumption**: Event processing and handling
- **Dead Letter Queues**: Failed message handling
- **Ordering and Delivery**: Message ordering guarantees
- **Event Sourcing**: Event store integration (if applicable)

### 6. File System Integration
- **File Upload/Download**: File handling operations
- **Storage Integration**: Cloud storage (S3, GCS, etc.)
- **File Processing**: Image processing, document handling
- **Backup and Recovery**: Data backup procedures

### 7. Test Data Management
- **Test Data Setup**: Creating realistic test datasets
- **Data Cleanup**: Teardown and cleanup procedures
- **Data Isolation**: Preventing test interference
- **Seed Data**: Consistent test data across environments
- **Data Factories**: Generating test data programmatically

### 8. Environment Configuration
- **Test Environment Setup**: Isolated testing environments
- **Configuration Management**: Environment-specific settings
- **Secret Management**: API keys, credentials in tests
- **Container Testing**: Docker/Kubernetes integration
- **Local Development**: Running integration tests locally

### 9. Test Implementation Examples
For each integration point, provide:
- **Complete test code** with setup and teardown
- **Assertion examples** for success and failure cases
- **Mock configurations** for external dependencies
- **Error handling tests** for network failures
- **Performance assertions** where relevant

### 10. Advanced Testing Scenarios
- **Contract Testing**: API contract validation
- **End-to-End Workflows**: Multi-step business processes
- **Concurrency Testing**: Race conditions, parallel execution
- **Security Testing**: Authorization, input validation
- **Chaos Testing**: Resilience and fault tolerance

## Test Organization Structure:
- Recommend test file organization
- Naming conventions for integration tests
- Grouping related tests effectively
- Parallel test execution strategies

## CI/CD Integration:
- Integration test pipeline setup
- When to run integration tests
- Handling test failures and retries
- Test reporting and notifications

## Monitoring and Maintenance:
- Test result analysis and reporting
- Identifying flaky tests
- Test performance monitoring
- Updating tests with system changes

Please provide specific, runnable test code examples that I can implement immediately.
```

---

## Tips for Better Results:

- **Map out all integration points** - APIs, databases, external services
- **Include your current test setup** - what framework and tools you're using
- **Specify environment constraints** - local vs cloud, CI/CD requirements
- **Mention data sensitivity** - PII, test data isolation needs
- **Include performance requirements** - test execution time, parallel execution
