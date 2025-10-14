# 仓库快照生成器

**使用场景：** 当您需要全面了解仓库结构、关键组件和文档空白时。

**技能水平：** 初级到高级

---

## 复制此提示：

```
请分析此仓库并创建一个全面的高级快照，记录项目结构、关键组件，并提供改进建议。

## 仓库分析请求：

请检查代码库并提供详细分析，涵盖：

### 1. 项目概述
- **项目名称和目的**：此项目做什么？
- **技术栈**：使用的主要语言、框架和工具
- **项目类型**：Web 应用、API、库、CLI 工具等
- **目标受众**：这是为谁构建的？
- **当前状态**：开发阶段、成熟度级别

### 2. 架构摘要
- **整体架构**：高级系统设计
- **关键组件**：主要模块、服务或功能
- **数据流**：数据如何在系统中移动
- **外部依赖项**：第三方服务、API、数据库
- **设计模式**：使用的架构模式

### 3. 仓库结构分析
- **目录组织**：代码如何组织
- **关键文件和目录**：最重要的文件
- **配置文件**：环境、构建、部署配置
- **入口点**：主要应用程序入口点
- **构建和部署**：构建过程和部署设置

### 4. 功能分析
- **核心功能**：提供的主要功能
- **用户工作流**：支持的主要用户旅程
- **API 端点**：可用的 API 及其目的（如果适用）
- **数据库模式**：数据模型和关系（如果适用）
- **身份验证**：安全和用户管理方法

### 5. 开发设置
- **先决条件**：所需工具、版本、依赖项
- **安装过程**：如何在本地运行项目
- **开发工作流**：开发人员如何使用此代码库
- **测试策略**：当前的测试方法和覆盖率
- **代码质量**：Linting、格式化、质量门

### 6. 文档评估
当前文档状态和空白：
- **README 质量**：README 是否全面？
- **代码文档**：内联注释和文档字符串
- **API 文档**：端点文档（如果适用）
- **架构文档**：系统设计文档
- **用户文档**：最终用户指南和教程

### 7. 缺失文档建议
识别并建议以下位置：
- **产品需求文档 (PRD)**：建议添加指向 `/docs/requirements/PRD.md` 的链接
- **架构决策记录 (ADR)**：建议 `/docs/decisions/` 目录
- **API 文档**：链接到 `/docs/api/` 或外部文档
- **部署指南**：链接到 `/docs/deployment/` 或部署部分
- **贡献指南**：链接到 `CONTRIBUTING.md`
- **更改日志**：链接到 `CHANGELOG.md`
- **安全策略**：链接到 `SECURITY.md`

### 8. 技术债务和改进
- **代码质量问题**：需要重构的区域
- **性能问题**：潜在的瓶颈或优化
- **安全考虑**：安全漏洞或建议
- **可伸缩性问题**：可能无法很好地扩展的区域
- **依赖管理**：过时或有问题的依赖项

### 9. 项目健康指标
- **代码复杂度**：整体复杂度评估
- **测试覆盖率**：测试完整性
- **文档覆盖率**：项目文档的完善程度
- **可维护性评分**：维护的难易程度
- **技术债务水平**：存在的技术债务量

### 10. 建议和后续步骤
优先建议：
- **关键问题**：必须修复的问题
- **文档改进**：高影响力的文档需求
- **代码质量**：重要的重构机会
- **功能空白**：应添加的缺失功能
- **基础设施**：部署、监控、CI/CD 改进

## 具体分析请求：

请同时提供：
- **快速入门指南**：3 步即可运行项目的过程
- **关键联系点**：在哪里寻求帮助、贡献或报告问题
- **相关资源**：指向相关外部文档的链接
- **项目路线图**：如果代码中明显，则说明下一步计划

## 文档模板建议：

对于缺失的文档，建议特定的模板：
- README 结构改进
- PRD 模板和位置（`/docs/requirements/PRD.md`）
- 架构文档模板（`/docs/architecture/`）
- API 文档结构（`/docs/api/`）
- 贡献指南模板（`CONTRIBUTING.md`）

## 仓库快照格式：

将分析呈现为结构化文档，可作为：
- 新团队成员的**项目入职指南**
- 利益相关者的**技术概述**
- 开发团队的**改进路线图**
- 突出空白的**文档审计**

重点是全面但简洁——提供足够的细节以快速理解项目，同时突出最重要的方面和改进机会。
```

---

## 获得更好结果的提示：

- **在整个仓库上运行此功能**——确保 Cursor 可以访问所有文件
- **定期使用**——随着项目的演变定期运行此功能
- **分享输出**——非常适合新团队成员入职
- **根据建议采取行动**——使用建议来改进您的项目
- **与其他提示结合使用**——使用建议来指导其他文档提示

# Repository Snapshot Generator

**Use this when:** You want a comprehensive overview of your repository structure, key components, and documentation gaps.

**Skill Level:** Beginner to Advanced

---

## Copy This Prompt:

```
Please analyze this repository and create a comprehensive high-level snapshot that documents the project structure, key components, and provides suggestions for improvements.

## Repository Analysis Request:

Please examine the codebase and provide a detailed analysis covering:

### 1. Project Overview
- **Project Name and Purpose**: What does this project do?
- **Technology Stack**: Main languages, frameworks, and tools used
- **Project Type**: Web app, API, library, CLI tool, etc.
- **Target Audience**: Who is this built for?
- **Current Status**: Development stage, maturity level

### 2. Architecture Summary
- **Overall Architecture**: High-level system design
- **Key Components**: Main modules, services, or features
- **Data Flow**: How data moves through the system
- **External Dependencies**: Third-party services, APIs, databases
- **Design Patterns**: Architectural patterns used

### 3. Repository Structure Analysis
- **Directory Organization**: How the code is organized
- **Key Files and Directories**: Most important files to understand
- **Configuration Files**: Environment, build, deployment configs
- **Entry Points**: Main application entry points
- **Build and Deploy**: Build process and deployment setup

### 4. Feature Analysis
- **Core Features**: Main functionality provided
- **User Workflows**: Primary user journeys supported
- **API Endpoints**: Available APIs and their purposes (if applicable)
- **Database Schema**: Data models and relationships (if applicable)
- **Authentication**: Security and user management approach

### 5. Development Setup
- **Prerequisites**: Required tools, versions, dependencies
- **Installation Process**: How to get the project running locally
- **Development Workflow**: How developers work with this codebase
- **Testing Strategy**: Current testing approach and coverage
- **Code Quality**: Linting, formatting, quality gates

### 6. Documentation Assessment
Current documentation status and gaps:
- **README Quality**: Is the README comprehensive?
- **Code Documentation**: Inline comments and docstrings
- **API Documentation**: Endpoint documentation (if applicable)
- **Architecture Documentation**: System design documentation
- **User Documentation**: End-user guides and tutorials

### 7. Missing Documentation Suggestions
Identify and suggest locations for:
- **Product Requirements Document (PRD)**: Suggest adding link to `/docs/requirements/PRD.md`
- **Architecture Decision Records (ADRs)**: Suggest `/docs/decisions/` directory
- **API Documentation**: Link to `/docs/api/` or external docs
- **Deployment Guide**: Link to `/docs/deployment/` or deployment section
- **Contributing Guidelines**: Link to `CONTRIBUTING.md`
- **Changelog**: Link to `CHANGELOG.md`
- **Security Policy**: Link to `SECURITY.md`

### 8. Technical Debt and Improvements
- **Code Quality Issues**: Areas needing refactoring
- **Performance Concerns**: Potential bottlenecks or optimizations
- **Security Considerations**: Security gaps or recommendations
- **Scalability Issues**: Areas that might not scale well
- **Dependency Management**: Outdated or problematic dependencies

### 9. Project Health Metrics
- **Code Complexity**: Overall complexity assessment
- **Test Coverage**: Testing completeness
- **Documentation Coverage**: How well documented the project is
- **Maintainability Score**: How easy it is to maintain
- **Technical Debt Level**: Amount of technical debt present

### 10. Recommendations and Next Steps
Prioritized suggestions for:
- **Critical Issues**: Must-fix problems
- **Documentation Improvements**: High-impact documentation needs
- **Code Quality**: Important refactoring opportunities  
- **Feature Gaps**: Missing functionality that should be added
- **Infrastructure**: Deployment, monitoring, CI/CD improvements

## Specific Analysis Requests:

Please also provide:
- **Quick Start Guide**: 3-step process to get the project running
- **Key Contact Points**: Where to find help, contribute, or report issues
- **Related Resources**: Links to relevant external documentation
- **Project Roadmap**: If evident from the code, what's planned next

## Documentation Template Suggestions:

For missing documentation, suggest specific templates:
- README structure improvements
- PRD template and location (`/docs/requirements/PRD.md`)
- Architecture documentation template (`/docs/architecture/`)
- API documentation structure (`/docs/api/`)
- Contributing guidelines template (`CONTRIBUTING.md`)

## Repository Snapshot Format:

Present the analysis as a structured document that could serve as:
- **Project onboarding guide** for new team members
- **Technical overview** for stakeholders
- **Improvement roadmap** for the development team
- **Documentation audit** highlighting gaps

Focus on being comprehensive but concise - provide enough detail to understand the project quickly while highlighting the most important aspects and improvement opportunities.
```

---

## Tips for Better Results:

- **Run this on your entire repository**——确保 Cursor 可以访问所有文件
- **定期使用**——随着项目的演变定期运行此功能
- **分享输出**——非常适合新团队成员入职
- **根据建议采取行动**——使用建议来改进您的项目
- **与其他提示结合使用**——使用建议来指导其他文档提示
