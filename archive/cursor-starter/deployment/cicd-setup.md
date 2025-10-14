# CI/CD 流水线设置

**使用场景：** 当您需要为项目设置自动化构建、测试和部署流水线时。

**技能水平：** 中级到高级

---

## 复制此提示：

```
我需要帮助为我的项目设置 CI/CD 流水线。请帮助我设计和实现自动化构建、测试和部署工作流。

## 项目背景：
- **项目类型**：[Web 应用、API、移动应用、库等]
- **技术栈**：[语言、框架、构建工具]
- **代码仓库**：[GitHub、GitLab、Bitbucket 等]
- **部署目标**：[AWS、Azure、Google Cloud、Vercel、Heroku、自托管等]
- **团队规模**：[独立开发者、小型团队、大型团队]

## 当前状态：
- **现有设置**：[您目前有任何 CI/CD 设置吗？如果有，是什么？]
- **构建过程**：[您目前如何构建和测试？]
- **部署过程**：[您目前如何部署？]
- **痛点**：[您正在尝试自动化哪些手动步骤？]

## 要求：
- **自动化目标**：[哪些过程需要自动化？]
- **环境**：[开发、预发布、生产等]
- **测试要求**：[单元测试、集成测试、端到端测试]
- **安全要求**：[秘密管理、安全扫描等]
- **性能要求**：[构建速度、部署速度]

## CI/CD 流水线设计：

请创建一个全面的 CI/CD 设置，包括：

### 1. 流水线策略
- 推荐最适合您设置的 CI/CD 平台
- 设计整体流水线架构
- 解释分支策略和工作流
- 定义环境晋升策略

### 2. 构建流水线
- 自动化构建配置
- 依赖管理和缓存
- 构建优化策略
- 工件生成和存储

### 3. 测试流水线
- 自动化测试执行（单元、集成、端到端）
- 测试并行化和优化
- 代码覆盖率报告
- 测试结果通知

### 4. 安全与质量
- 安全漏洞扫描
- 代码质量检查和 Linting
- 依赖漏洞扫描
- 静态分析工具集成

### 5. 部署流水线
- 部署策略（蓝绿部署、滚动更新、金丝雀发布）
- 环境特定配置
- 数据库迁移处理
- 回滚程序

### 6. 监控与通知
- 构建和部署通知
- 性能监控设置
- 错误跟踪和警报
- 仪表盘和报告

### 7. 配置文件
提供完整、即用的配置文件，用于：
- CI/CD 平台配置（GitHub Actions、GitLab CI 等）
- 构建脚本和命令
- 环境变量管理
- 部署配置

### 8. 最佳实践
- 流水线安全最佳实践
- 性能优化技巧
- 常见问题排查
- 扩展性考虑

## 具体交付物：
- 完整的 CI/CD 配置文件
- 分步设置说明
- 环境设置指南
- 安全配置清单
- 故障排除指南

请提供实用、可立即实施的生产就绪配置。
```

---

## 获得更好结果的提示：

- **指定您当前的工具**以及您拥有的任何限制
- **包括您的部署频率**——每日、每周、按需
- **提及合规性要求**——SOC2、GDPR 等
- **明确您的基础设施**——云提供商、本地部署、混合
- **包括任何需要集成的现有自动化**

# CI/CD Pipeline Setup

**Use this when:** You need to set up automated build, test, and deployment pipelines for your project.

**Skill Level:** Intermediate to Advanced

---

## Copy This Prompt:

```
I need help setting up a CI/CD pipeline for my project. Please help me design and implement automated build, test, and deployment workflows.

## Project Context:
- **Project Type**: [Web app, API, mobile app, library, etc.]
- **Technology Stack**: [Languages, frameworks, build tools]
- **Repository**: [GitHub, GitLab, Bitbucket, etc.]
- **Deployment Target**: [AWS, Azure, Google Cloud, Vercel, Heroku, self-hosted, etc.]
- **Team Size**: [Solo developer, small team, large team]

## Current State:
- **Existing Setup**: [What CI/CD, if any, do you currently have?]
- **Build Process**: [How do you currently build and test?]
- **Deployment Process**: [How do you currently deploy?]
- **Pain Points**: [What manual steps are you trying to automate?]

## Requirements:
- **Automation Goals**: [What processes need to be automated?]
- **Environments**: [Development, staging, production, etc.]
- **Testing Requirements**: [Unit tests, integration tests, e2e tests]
- **Security Requirements**: [Secret management, security scanning, etc.]
- **Performance Requirements**: [Build speed, deployment speed]

## CI/CD Pipeline Design:

Please create a comprehensive CI/CD setup that includes:

### 1. Pipeline Strategy
- Recommend the best CI/CD platform for your setup
- Design the overall pipeline architecture
- Explain branching strategy and workflows
- Define environment promotion strategy

### 2. Build Pipeline
- Automated build configuration
- Dependency management and caching
- Build optimisation strategies
- Artifact generation and storage

### 3. Testing Pipeline
- Automated test execution (unit, integration, e2e)
- Test parallelisation and optimisation
- Code coverage reporting
- Test result notifications

### 4. Security & Quality
- Security vulnerability scanning
- Code quality checks and linting
- Dependency vulnerability scanning
- Static analysis tools integration

### 5. Deployment Pipeline
- Deployment strategies (blue-green, rolling, canary)
- Environment-specific configurations
- Database migration handling
- Rollback procedures

### 6. Monitoring & Notifications
- Build and deployment notifications
- Performance monitoring setup
- Error tracking and alerting
- Dashboard and reporting

### 7. Configuration Files
Provide complete, ready-to-use configuration files for:
- CI/CD platform configuration (GitHub Actions, GitLab CI, etc.)
- Build scripts and commands
- Environment variable management
- Deployment configurations

### 8. Best Practices
- Pipeline security best practices
- Performance optimisation tips
- Troubleshooting common issues
- Scaling considerations

## Specific Deliverables:
- Complete CI/CD configuration files
- Step-by-step setup instructions
- Environment setup guide
- Security configuration checklist
- Troubleshooting guide

Please provide practical, production-ready configurations that can be implemented immediately.
```

---

## Tips for Better Results:

- **Specify your current tools** and any constraints you have
- **Include your deployment frequency** - daily, weekly, on-demand
- **Mention compliance requirements** - SOC2, GDPR, etc.
- **Be clear about your infrastructure** - cloud provider, on-premise, hybrid
- **Include any existing automation** that needs to be integrated
