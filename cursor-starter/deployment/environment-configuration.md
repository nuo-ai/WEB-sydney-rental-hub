# 环境配置助手

**使用场景：** 当您需要设置和管理跨不同环境（开发、预发布、生产）的配置时。

**技能水平：** 中级到高级

---

## 复制此提示：

```
我需要帮助为我的应用程序设置全面的环境配置管理。请帮助我设计一个健壮的系统来管理跨不同环境的设置。

## 项目背景：
- **应用程序类型**：[Web 应用、API、微服务、移动后端等]
- **技术栈**：[语言、框架、部署平台]
- **所需环境**：[开发、预发布、生产、测试等]
- **部署平台**：[AWS、Azure、Google Cloud、Vercel、Heroku、自托管]
- **团队规模**：[独立开发者、小型团队、大型团队]

## 当前配置：
[描述您当前的配置设置，如果有的话]

## 配置要求：
- **数据库设置**：[连接字符串、凭据等]
- **API 密钥**：[第三方服务、支付处理器等]
- **功能标志**：[A/B 测试、渐进式发布等]
- **安全设置**：[CORS、速率限制、加密密钥]
- **性能设置**：[缓存、连接池、超时]

## 环境配置策略：

请创建一个全面的配置管理系统，包括：

### 1. 配置架构
- 整体配置策略和原则
- 环境层次结构和继承
- 配置文件结构和组织
- 秘密管理方法

### 2. 环境定义
设计以下配置：
- **开发环境**
  - 本地开发设置
  - 调试配置
  - 开发数据库和服务
  - 热重载和开发工具

- **预发布环境**
  - 类似生产的配置
  - 测试数据和场景
  - 集成测试设置
  - 性能测试配置

- **生产环境**
  - 优化性能设置
  - 安全强化
  - 监控和日志记录
  - 备份和灾难恢复

### 3. 配置管理
- **环境变量**：安全变量管理
- **配置文件**：结构化配置文件（JSON、YAML 等）
- **秘密管理**：敏感数据的安全处理
- **运行时配置**：动态配置加载
- **配置验证**：确保有效配置

### 4. 秘密和安全
- **API 密钥管理**：安全存储和轮换
- **数据库凭据**：连接字符串安全
- **加密密钥**：密钥管理和轮换
- **证书管理**：SSL/TLS 证书处理
- **访问控制**：谁可以修改配置

### 5. 功能标志和开关
- **功能标志系统**：按环境启用/禁用功能
- **渐进式发布**：基于百分比的功能部署
- **A/B 测试配置**：实验配置
- **紧急开关**：快速禁用功能的能力

### 6. 数据库配置
- **连接管理**：连接池大小、超时、SSL
- **迁移配置**：数据库模式管理
- **备份设置**：自动化备份配置
- **读/写分离**：数据库路由配置

### 7. 外部服务配置
- **API 端点**：每个环境不同的端点
- **服务凭据**：外部服务的身份验证
- **速率限制**：API 调用限制和节流
- **超时配置**：服务调用超时
- **重试逻辑**：故障处理和重试

### 8. 监控和日志记录
- **日志级别**：每个环境不同的详细程度
- **监控服务**：APM 和指标配置
- **警报配置**：错误和性能警报
- **分析**：使用情况跟踪和分析设置

### 9. 性能配置
- **缓存策略**：Redis、内存缓存设置
- **CDN 配置**：内容分发网络设置
- **资源限制**：内存、CPU、连接限制
- **优化设置**：压缩、最小化等

### 10. 部署配置**
- **构建设置**：环境特定的构建配置
- **容器配置**：Docker/Kubernetes 设置
- **基础设施即代码**：Terraform、CloudFormation 模板
- **CI/CD 变量**：流水线特定配置

## 实施示例：

请提供：
- **每个环境的配置文件示例**
- **带有描述的环境变量模板**
- **秘密管理设置**（AWS Secrets Manager、Azure Key Vault 等）
- **功能标志实现**示例
- **配置加载代码**示例

## 最佳实践：
- 配置验证和错误处理
- 文档和变更管理
- 备份和恢复程序
- 安全扫描和合规性
- 配置漂移检测和修复

## 工具和集成：
- 推荐配置管理工具
- 秘密管理服务集成
- 功能标志服务推荐
- 监控和警报设置
- 文档和变更跟踪

## 迁移策略：
如果我有现有配置：
- 如何迁移到新系统
- 向后兼容性考虑
- 回滚程序
- 测试新配置系统

请提供具体的、可立即在所有环境中使用的可实施示例。
```

---

## 获得更好结果的提示：

- **列出您的所有环境**——包括任何特殊的，如 QA、演示
- **包括您的部署流水线**——代码如何在环境之间移动
- **提及合规性要求**——SOC2、GDPR、行业特定
- **指定您的云提供商**——用于平台特定建议
- **包括团队访问模式**——谁需要访问哪些配置

# Environment Configuration Assistant

**Use this when:** You need to set up and manage configuration across different environments (development, staging, production).

**Skill Level:** Intermediate to Advanced

---

## Copy This Prompt:

```
I need help setting up comprehensive environment configuration management for my application. Please help me design a robust system for managing settings across different environments.

## Project Context:
- **Application Type**: [Web app, API, microservice, mobile backend, etc.]
- **Technology Stack**: [Languages, frameworks, deployment platforms]
- **Environments Needed**: [Development, staging, production, testing, etc.]
- **Deployment Platform**: [AWS, Azure, Google Cloud, Vercel, Heroku, self-hosted]
- **Team Size**: [Solo, small team, large team]

## Current Configuration:
[Describe your current configuration setup, if any]

## Configuration Requirements:
- **Database Settings**: [Connection strings, credentials, etc.]
- **API Keys**: [Third-party services, payment processors, etc.]
- **Feature Flags**: [A/B testing, gradual rollouts, etc.]
- **Security Settings**: [CORS, rate limiting, encryption keys]
- **Performance Settings**: [Caching, connection pools, timeouts]

## Environment Configuration Strategy:

Please create a comprehensive configuration management system that includes:

### 1. Configuration Architecture
- Overall configuration strategy and principles
- Environment hierarchy and inheritance
- Configuration file structure and organization
- Secret management approach

### 2. Environment Definitions
Design configurations for:
- **Development Environment**
  - Local development settings
  - Debug configurations
  - Development database and services
  - Hot reload and development tools

- **Staging Environment**
  - Production-like configuration
  - Test data and scenarios
  - Integration testing setup
  - Performance testing configuration

- **Production Environment**
  - Optimized performance settings
  - Security hardening
  - Monitoring and logging
  - Backup and disaster recovery

### 3. Configuration Management
- **Environment Variables**: Secure variable management
- **Configuration Files**: Structured config files (JSON, YAML, etc.)
- **Secret Management**: Secure handling of sensitive data
- **Runtime Configuration**: Dynamic configuration loading
- **Configuration Validation**: Ensuring valid configurations

### 4. Secrets and Security
- **API Key Management**: Secure storage and rotation
- **Database Credentials**: Connection string security
- **Encryption Keys**: Key management and rotation
- **Certificate Management**: SSL/TLS certificate handling
- **Access Control**: Who can modify configurations

### 5. Feature Flags and Toggles
- **Feature Flag System**: Enabling/disabling features by environment
- **Gradual Rollouts**: Percentage-based feature deployment
- **A/B Testing Configuration**: Experiment configuration
- **Emergency Toggles**: Quick feature disable capabilities

### 6. Database Configuration
- **Connection Management**: Pool sizes, timeouts, SSL
- **Migration Configuration**: Database schema management
- **Backup Settings**: Automated backup configuration
- **Read/Write Splitting**: Database routing configuration

### 7. External Service Configuration
- **API Endpoints**: Different endpoints per environment
- **Service Credentials**: Authentication for external services
- **Rate Limiting**: API call limits and throttling
- **Timeout Configuration**: Service call timeouts
- **Retry Logic**: Failure handling and retries

### 8. Monitoring and Logging
- **Log Levels**: Different verbosity per environment
- **Monitoring Services**: APM and metrics configuration
- **Alert Configuration**: Error and performance alerts
- **Analytics**: Usage tracking and analytics setup

### 9. Performance Configuration
- **Caching Strategy**: Redis, in-memory caching settings
- **CDN Configuration**: Content delivery network setup
- **Resource Limits**: Memory, CPU, connection limits
- **Optimization Settings**: Compression, minification, etc.

### 10. Deployment Configuration
- **Build Settings**: Environment-specific build configuration
- **Container Configuration**: Docker/Kubernetes settings
- **Infrastructure as Code**: Terraform, CloudFormation templates
- **CI/CD Variables**: Pipeline-specific configuration

## Implementation Examples:

Please provide:
- **Configuration file examples** for each environment
- **Environment variable templates** with descriptions
- **Secret management setup** (AWS Secrets Manager, Azure Key Vault, etc.)
- **Feature flag implementation** examples
- **Configuration loading code** examples

## Best Practices:
- Configuration validation and error handling
- Documentation and change management
- Backup and recovery procedures
- Security scanning and compliance
- Configuration drift detection and remediation

## Tools and Integrations:
- Recommend configuration management tools
- Secret management service integration
- Feature flag service recommendations
- Monitoring and alerting setup
- Documentation and change tracking

## Migration Strategy:
If I have existing configuration:
- How to migrate to the new system
- Backwards compatibility considerations
- Rollback procedures
- Testing the new configuration system

Please provide specific, implementable examples that I can use immediately across all my environments.
```

---

## Tips for Better Results:

- **List all your environments**——包括任何特殊的，如 QA、演示
- **包括您的部署流水线**——代码如何在环境之间移动
- **提及合规性要求**——SOC2、GDPR、行业特定
- **指定您的云提供商**——用于平台特定建议
- **包括团队访问模式**——谁需要访问哪些配置
