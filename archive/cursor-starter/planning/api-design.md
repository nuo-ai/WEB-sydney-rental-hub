# API 设计助手

**适用场景：** 当您需要为您的应用程序设计 REST API、GraphQL API 或其他 API 接口时使用。

**技能水平：** 中级到高级

---

## 复制此提示：

```
我需要帮助为我的应用程序设计一个全面的 API。请帮助我创建一个结构良好、可扩展且遵循最佳实践的 API 设计。

## 项目背景：
- **应用类型**：[Web 应用、移动应用、微服务等]
- **API 类型**：[REST、GraphQL、gRPC、WebSocket 等]
- **主要用例**：[API 将用于什么？]
- **预期规模**：[请求数量、并发用户数等]
- **数据关系**：[简要描述您的数据模型]

## API 需求：
- **核心功能**：[您的 API 需要支持哪些主要操作？]
- **身份验证**：[公开、API 密钥、OAuth、JWT 等]
- **数据格式**：[JSON、XML、Protocol Buffers 等]
- **特殊要求**：[实时更新、文件上传、Webhook 等]

## API 设计请求：

请创建一个全面的 API 设计，包括：

### 1. API 架构概述
- 整体 API 结构和设计模式
- 推荐的架构方法（REST、GraphQL 等）
- 资源识别和命名约定
- URL 结构和端点组织

### 2. 端点设计
为每个主要资源提供：
- **资源端点** 及正确的 HTTP 方法
- **URL 模式** 和路径参数
- 用于筛选、排序、分页的 **查询参数**
- **请求/响应结构（schema）** 及示例
- 针对不同场景的 **HTTP 状态码**

### 3. 身份验证与授权
- 身份验证策略和实现
- 授权级别和权限
- API 密钥管理（如果适用）
- 安全最佳实践和注意事项

### 4. 数据建模
- 请求和响应的数据结构
- 验证规则和约束
- 关系处理（嵌套资源、引用）
- 错误响应格式

### 5. API 功能
- 针对大数据集的 **分页** 策略
- **筛选和排序** 功能
- **版本控制** 方法和策略
- **速率限制** 的实现
- **缓存** 头部信息和策略

### 6. 错误处理
- 标准化的错误响应格式
- 全面的错误码和消息
- 验证错误处理
- 开发环境下的调试信息

### 7. 文档结构
- API 文档格式（OpenAPI/Swagger）
- 请求和响应示例
- 身份验证示例
- SDK/客户端库的考量

### 8. 性能考量
- 常用操作的优化策略
- 数据库查询优化
- 缓存策略
- 批量操作设计

### 9. 测试策略
- API 测试方法
- 测试数据要求
- 自动化测试建议
- 性能测试考量

### 10. 未来考量
- 可扩展性规划
- 向后兼容策略
- 弃用政策
- 迁移策略

## 具体 API 示例：

请提供以下具体示例：
- 主要资源的 **CRUD 操作**
- 带有多个参数的 **复杂查询**
- 提高效率的 **批量操作**
- **文件上传/下载** 端点（如果需要）
- **实时功能**（WebSocket、服务器发送事件）

## 附加要求：
- 遵循 RESTful 原则和 HTTP 标准
- 包括正确的 HTTP 头部信息和状态码
- 考虑移动和 Web 客户端的需求
- 优化开发者体验
- 规划监控和分析

如果您需要有关特定用例或技术需求的更多详细信息，请随时提出澄清问题。
```

---

## 获得更好结果的提示：

- **提供您的数据模型** - 实体之间的关系
- **指明客户端类型** - Web、移动、第三方集成
- **提及性能要求** - 响应时间、吞吐量
- **包括安全要求** - 合规性、数据敏感性
- **明确复杂性** - 是简单的 CRUD 还是复杂的业务逻辑

---
# API Design Assistant

**Use this when:** You need to design REST APIs, GraphQL APIs, or other API interfaces for your application.

**Skill Level:** Intermediate to Advanced

---

## Copy This Prompt:

```
I need help designing a comprehensive API for my application. Please help me create a well-structured, scalable API design that follows best practices.

## Project Context:
- **Application Type**: [Web app, mobile app, microservice, etc.]
- **API Type**: [REST, GraphQL, gRPC, WebSocket, etc.]
- **Primary Use Cases**: [What will the API be used for?]
- **Expected Scale**: [Number of requests, concurrent users, etc.]
- **Data Relationships**: [Brief description of your data model]

## API Requirements:
- **Core Functionality**: [What are the main operations your API needs to support?]
- **Authentication**: [Public, API keys, OAuth, JWT, etc.]
- **Data Format**: [JSON, XML, Protocol Buffers, etc.]
- **Special Requirements**: [Real-time updates, file uploads, webhooks, etc.]

## API Design Request:

Please create a comprehensive API design that includes:

### 1. API Architecture Overview
- Overall API structure and design patterns
- Recommended architectural approach (REST, GraphQL, etc.)
- Resource identification and naming conventions
- URL structure and endpoint organization

### 2. Endpoint Design
For each major resource, provide:
- **Resource endpoints** with proper HTTP methods
- **URL patterns** and path parameters
- **Query parameters** for filtering, sorting, pagination
- **Request/response schemas** with examples
- **HTTP status codes** for different scenarios

### 3. Authentication & Authorization
- Authentication strategy and implementation
- Authorization levels and permissions
- API key management (if applicable)
- Security best practices and considerations

### 4. Data Modeling
- Request and response data structures
- Validation rules and constraints
- Relationship handling (nested resources, references)
- Error response formats

### 5. API Features
- **Pagination** strategy for large datasets
- **Filtering and sorting** capabilities
- **Versioning** approach and strategy
- **Rate limiting** implementation
- **Caching** headers and strategies

### 6. Error Handling
- Standardized error response format
- Comprehensive error codes and messages
- Validation error handling
- Debug information for development

### 7. Documentation Structure
- API documentation format (OpenAPI/Swagger)
- Example requests and responses
- Authentication examples
- SDK/client library considerations

### 8. Performance Considerations
- Optimization strategies for common operations
- Database query optimization
- Caching strategies
- Bulk operations design

### 9. Testing Strategy
- API testing approach
- Test data requirements
- Automated testing recommendations
- Performance testing considerations

### 10. Future Considerations
- Scalability planning
- Backwards compatibility strategy
- Deprecation policies
- Migration strategies

## Specific API Examples:

Please provide concrete examples for:
- **CRUD operations** for main resources
- **Complex queries** with multiple parameters
- **Batch operations** for efficiency
- **File upload/download** endpoints (if needed)
- **Real-time features** (WebSocket, Server-Sent Events)

## Additional Requirements:
- Follow RESTful principles and HTTP standards
- Include proper HTTP headers and status codes
- Consider mobile and web client needs
- Optimize for developer experience
- Plan for monitoring and analytics

Please ask clarifying questions if you need more details about specific use cases or technical requirements.
```

---

## Tips for Better Results:

- **Include your data model** - relationships between entities
- **Specify client types** - web, mobile, third-party integrations
- **Mention performance requirements** - response times, throughput
- **Include security requirements** - compliance, data sensitivity
- **Be clear about complexity** - simple CRUD vs complex business logic
