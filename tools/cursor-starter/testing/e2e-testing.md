# 端到端测试策略

**使用场景：** 当您需要创建全面的端到端测试，以验证完整的用户工作流和系统功能时。

**技能水平：** 中级到高级

---

## 复制此提示：

```
我需要帮助为我的应用程序创建一个全面的端到端 (E2E) 测试策略。请帮助我设计和实施测试，以验证完整的用户旅程和系统工作流。

## 应用程序上下文：
- **应用程序类型**：[Web 应用、移动应用、桌面应用等]
- **技术栈**：[前端和后端技术]
- **用户界面**：[Web 浏览器、移动应用、桌面应用]
- **关键用户工作流**：[主要用户旅程和业务流程]
- **测试框架**：[Playwright、Cypress、Selenium 等 - 或请求推荐]

## 当前测试设置：
[描述任何现有的 E2E 测试基础设施以及您已覆盖的内容]

## 关键用户工作流：
[列出需要 E2E 测试覆盖的最重要的用户旅程]

## E2E 测试策略：

请创建一个全面的 E2E 测试方法，包括：

### 1. 测试策略概述
- E2E 测试范围和目标
- 测试金字塔集成（单元、集成、E2E 平衡）
- 测试环境设置和要求
- 浏览器和设备覆盖策略
- 测试执行和 CI/CD 集成

### 2. 用户旅程映射
- **关键用户路径**：最重要的测试工作流
- **正常路径场景**：正常用户流测试
- **边缘情况场景**：不寻常但有效的用户行为
- **错误场景**：用户如何从错误中恢复
- **跨浏览器测试**：跨浏览器兼容性

### 3. 测试场景设计
对于每个主要工作流，创建：
- **完整的用户故事**：从登录到目标完成
- **分步操作**：详细的用户交互流
- **数据要求**：每个场景所需的测试数据
- **预期结果**：成功标准和验证
- **失败场景**：错误处理和恢复

### 4. 身份验证和授权测试
- **用户注册**：帐户创建工作流
- **登录/注销**：身份验证流测试
- **密码重置**：密码恢复过程
- **基于角色的访问**：不同的用户权限级别
- **会话管理**：会话超时和安全

### 5. 核心功能测试
- **CRUD 操作**：创建、读取、更新、删除工作流
- **表单提交**：复杂的表单处理和验证
- **文件操作**：上传、下载、文件管理
- **搜索和过滤**：数据发现和操作
- **导航测试**：菜单导航和路由

### 6. 支付和交易测试
- **结帐流程**：完整的购买工作流
- **支付集成**：支付网关测试
- **订单管理**：订单创建和跟踪
- **退款处理**：退货和退款工作流
- **订阅管理**：定期付款处理

### 7. 移动和响应式测试
- **移动 Web 测试**：触摸交互、响应式设计
- **跨设备测试**：手机、平板电脑、桌面兼容性
- **方向测试**：纵向和横向模式
- **移动性能**：加载时间和响应能力
- **离线功能**：渐进式 Web 应用功能

### 8. API 集成测试
- **前端-后端集成**：API 调用验证
- **实时功能**：WebSocket、服务器发送事件
- **外部服务集成**：第三方 API 测试
- **错误处理**：网络故障和 API 错误
- **数据同步**：实时数据更新

### 9. 性能和负载测试
- **页面加载性能**：关键页面加载时间
- **用户交互速度**：用户操作的响应时间
- **并发用户测试**：多个用户同时操作
- **资源使用**：测试期间的内存和 CPU 使用
- **网络条件**：慢速网络模拟

### 10. 可访问性测试
- **键盘导航**：Tab 键顺序和键盘可访问性
- **屏幕阅读器测试**：屏幕阅读器兼容性
- **颜色对比度**：视觉可访问性验证
- **ARIA 标签**：正确的语义标记
- **焦点管理**：焦点指示器和管理

## 测试实施：

请提供：
- **主要工作流的完整测试代码示例**
- **页面对象模型**：可重用的页面组件
- **测试数据管理**策略和固定数据
- **常见操作的自定义帮助程序和实用程序**
- **不同类型验证的断言模式**

## 测试环境管理：
- **测试数据设置和清理**程序
- **不同测试阶段的环境配置**
- **测试之间的数据库状态管理**
- **外部依赖项的模拟服务**
- **并行测试执行**策略

## CI/CD 集成：
- **部署流水线中的自动化测试执行**
- **测试结果报告**和通知
- **失败测试的屏幕截图和视频捕获**
- **不稳定测试处理**和重试策略
- **性能回归检测**

## 监控和维护：
- **测试结果分析**和报告
- **随着应用程序演变的测试维护**
- **随时间推移的性能趋势跟踪**
- **覆盖率分析**和差距识别
- **测试可靠性**和稳定性改进

## 高级测试场景：
- **多标签页测试**：跨标签页功能
- **后台处理**：长时间运行的操作
- **实时通知**：推送通知、警报
- **地理位置测试**：基于位置的功能
- **国际化**：多语言测试

## 测试文档：
- 测试用例文档和要求
- 测试数据要求和设置
- 浏览器和设备兼容性矩阵
- 已知问题和解决方法
- 测试执行和调试指南

请提供具体的、可立即运行以验证我的关键用户工作流的可实施测试代码。
```

---

## 获得更好结果的提示：

- **规划您的关键用户旅程**——从入口点到完成
- **包含您应用程序的独特功能**——支付、实时等
- **指定浏览器和设备要求**——您需要支持的内容
- **提及您的部署过程**——E2E 测试如何融入 CI/CD
- **包含性能要求**——可接受的加载时间和响应时间

# End-to-End Testing Strategy

**Use this when:** You need to create comprehensive end-to-end tests that verify complete user workflows and system functionality.

**Skill Level:** Intermediate to Advanced

---

## Copy This Prompt:

```
I need help creating a comprehensive end-to-end (E2E) testing strategy for my application. Please help me design and implement tests that verify complete user journeys and system workflows.

## Application Context:
- **Application Type**: [Web app, mobile app, desktop app, etc.]
- **Technology Stack**: [Frontend and backend technologies]
- **User Interface**: [Web browser, mobile app, desktop app]
- **Key User Workflows**: [Main user journeys and business processes]
- **Testing Framework**: [Playwright, Cypress, Selenium, etc. - or ask for recommendation]

## Current Testing Setup:
[Describe any existing E2E testing infrastructure and what you've already covered]

## Critical User Workflows:
[List the most important user journeys that need E2E testing coverage]

## E2E Testing Strategy:

Please create a comprehensive E2E testing approach that includes:

### 1. Testing Strategy Overview
- E2E testing scope and objectives
- Test pyramid integration (unit, integration, E2E balance)
- Testing environment setup and requirements
- Browser and device coverage strategy
- Test execution and CI/CD integration

### 2. User Journey Mapping
- **Critical User Paths**: Most important workflows to test
- **Happy Path Scenarios**: Normal user flow testing
- **Edge Case Scenarios**: Unusual but valid user behaviors
- **Error Scenarios**: How users recover from errors
- **Cross-Browser Testing**: Compatibility across browsers

### 3. Test Scenarios Design
For each major workflow, create:
- **Complete User Stories**: From login to goal completion
- **Step-by-Step Actions**: Detailed user interaction flows
- **Data Requirements**: Test data needed for each scenario
- **Expected Outcomes**: Success criteria and validations
- **Failure Scenarios**: Error handling and recovery

### 4. Authentication and Authorization Testing
- **User Registration**: Account creation workflows
- **Login/Logout**: Authentication flow testing
- **Password Reset**: Password recovery processes
- **Role-Based Access**: Different user permission levels
- **Session Management**: Session timeout and security

### 5. Core Functionality Testing
- **CRUD Operations**: Create, read, update, delete workflows
- **Form Submissions**: Complex form handling and validation
- **File Operations**: Upload, download, file management
- **Search and Filtering**: Data discovery and manipulation
- **Navigation Testing**: Menu navigation and routing

### 6. Payment and Transaction Testing
- **Checkout Process**: Complete purchase workflows
- **Payment Integration**: Payment gateway testing
- **Order Management**: Order creation and tracking
- **Refund Processing**: Return and refund workflows
- **Subscription Management**: Recurring payment handling

### 7. Mobile and Responsive Testing
- **Mobile Web Testing**: Touch interactions, responsive design
- **Cross-Device Testing**: Phone, tablet, desktop compatibility
- **Orientation Testing**: Portrait and landscape modes
- **Performance on Mobile**: Load times and responsiveness
- **Offline Functionality**: Progressive web app features

### 8. API Integration Testing
- **Frontend-Backend Integration**: API call verification
- **Real-time Features**: WebSocket, Server-Sent Events
- **External Service Integration**: Third-party API testing
- **Error Handling**: Network failures and API errors
- **Data Synchronization**: Real-time data updates

### 9. Performance and Load Testing
- **Page Load Performance**: Critical page load times
- **User Interaction Speed**: Response times for user actions
- **Concurrent User Testing**: Multiple users simultaneously
- **Resource Usage**: Memory and CPU usage during tests
- **Network Conditions**: Slow network simulation

### 10. Accessibility Testing
- **Keyboard Navigation**: Tab order and keyboard accessibility
- **Screen Reader Testing**: Screen reader compatibility
- **Color Contrast**: Visual accessibility validation
- **ARIA Labels**: Proper semantic markup
- **Focus Management**: Focus indicator and management

## Test Implementation:

Please provide:
- **Complete test code examples** for major workflows
- **Page Object Model**: Reusable page components
- **Test data management** strategies and fixtures
- **Custom helpers and utilities** for common operations
- **Assertion patterns** for different types of validations

## Test Environment Management:
- **Test data setup and cleanup** procedures
- **Environment configuration** for different test stages
- **Database state management** between tests
- **Mock services** for external dependencies
- **Parallel test execution** strategies

## CI/CD Integration:
- **Automated test execution** in deployment pipeline
- **Test result reporting** and notifications
- **Screenshot and video capture** for failed tests
- **Flaky test handling** and retry strategies
- **Performance regression detection**

## Monitoring and Maintenance:
- **Test result analysis** and reporting
- **Test maintenance** as application evolves
- **Performance trend tracking** over time
- **Coverage analysis** and gap identification
- **Test reliability** and stability improvements

## Advanced Testing Scenarios:
- **Multi-tab testing**: Cross-tab functionality
- **Background processing**: Long-running operations
- **Real-time notifications**: Push notifications, alerts
- **Geolocation testing**: Location-based features
- **Internationalization**: Multi-language testing

## Test Documentation:
- Test case documentation and requirements
- Test data requirements and setup
- Browser and device compatibility matrix
- Known issues and workarounds
- Test execution and debugging guide

Please provide specific, implementable test code that I can run immediately to validate my critical user workflows.
```

---

## Tips for Better Results:

- **Map out your critical user journeys** - from entry point to completion
- **Include your application's unique features** - payments, real-time, etc.
- **Specify browser and device requirements** - what you need to support
- **Mention your deployment process** - how E2E tests fit into CI/CD
- **Include performance requirements** - acceptable load times and response times
