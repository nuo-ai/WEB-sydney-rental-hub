# 安全审计助手

**使用场景：** 当您需要识别安全漏洞并提高应用程序的安全态势时。

**技能水平：** 中级到高级

---

## 复制此提示：

```
我需要对我的应用程序进行全面的安全审计。请帮助我识别漏洞、安全风险，并提供改进安全的建议。

## 应用程序上下文：
- **应用程序类型**：[Web 应用、API、移动应用、桌面应用等]
- **技术栈**：[语言、框架、数据库、云服务]
- **用户群**：[面向公众、内部、企业等]
- **数据敏感性**：[个人数据、财务、医疗保健等]
- **合规性要求**：[GDPR、HIPAA、SOC2、PCI-DSS 等]

## 当前安全措施：
[描述任何现有安全措施——身份验证、加密、监控等]

## 要审计的代码/架构：
[在此处粘贴您的代码或描述系统架构]

## 安全审计请求：

请进行彻底的安全评估，涵盖：

### 1. 身份验证与授权
- 审查身份验证机制
- 评估授权控制和访问管理
- 检查是否存在权限提升漏洞
- 评估会话管理安全性
- 审查密码策略和存储

### 2. 输入验证与数据安全
- 识别输入验证漏洞
- 检查是否存在注入攻击（SQL、XSS、LDAP 等）
- 评估数据清理和编码
- 审查文件上传安全性
- 评估客户端和服务器上的数据验证

### 3. 数据保护
- 审查静态和传输中的数据加密
- 评估敏感数据处理和存储
- 检查是否存在数据泄露漏洞
- 评估备份和恢复安全性
- 审查数据保留和删除策略

### 4. 网络与基础设施安全
- 评估网络安全配置
- 审查 API 安全和速率限制
- 检查是否存在不安全的直接对象引用
- 评估 CORS 和 CSP 策略
- 审查 SSL/TLS 配置

### 5. 应用程序安全
- 识别业务逻辑漏洞
- 检查是否存在不安全的加密实践
- 审查错误处理和信息泄露
- 评估日志记录和监控安全性
- 评估第三方依赖项安全性

### 6. 配置与部署安全
- 审查安全配置
- 检查是否存在默认凭据和设置
- 评估环境变量安全性
- 审查部署流水线安全性
- 评估基础设施即代码安全性

## 安全评估报告：

请提供：

### 关键漏洞
- 需要立即关注的高风险安全问题
- 潜在影响和利用场景
- 带有代码示例的具体补救措施

### 主要安全问题
- 需要改进的重要安全问题
- 风险评估和优先级排序
- 推荐的安全增强功能

### 安全最佳实践
- 一般安全改进
- 行业标准建议
- 未来开发的预防措施

### 合规性考虑
- 所提及法规的合规性空白
- 所需的安全控制
- 文档和审计跟踪要求

### 安全测试建议
- 建议的安全测试方法
- 持续安全评估的工具和技术
- 自动化安全扫描集成

### 监控与事件响应
- 安全监控建议
- 事件响应计划
- 警报和通知策略

## 具体关注领域：
请特别注意：
- [您有任何具体的安全问题吗？]
- [您最近听说过的任何安全事件或漏洞]
- [您需要满足的特定合规性要求]

## 请求的交付物：
- 优先排序的安全问题列表
- 具体补救代码示例
- 持续维护的安全清单
- 安全工具和流程建议

请务必彻底但实用，重点关注提供最大安全价值的可操作安全改进。
```

---

## 获得更好结果的提示：

- **包含您的完整系统架构**——不仅仅是代码片段
- **提及您的行业所需的特定合规性要求**
- **明确您处理的数据类型**（PII、财务等）
- **包含您当前的安全措施**以避免重复建议
- **指定您的风险承受能力**和安全预算限制

# Security Audit Assistant

**Use this when:** You need to identify security vulnerabilities and improve the security posture of your application.

**Skill Level:** Intermediate to Advanced

---

## Copy This Prompt:

```
I need a comprehensive security audit of my application. Please help me identify vulnerabilities, security risks, and provide recommendations for improving security.

## Application Context:
- **Application Type**: [Web app, API, mobile app, desktop app, etc.]
- **Technology Stack**: [Languages, frameworks, databases, cloud services]
- **User Base**: [Public-facing, internal, enterprise, etc.]
- **Data Sensitivity**: [Personal data, financial, healthcare, etc.]
- **Compliance Requirements**: [GDPR, HIPAA, SOC2, PCI-DSS, etc.]

## Current Security Measures:
[Describe any existing security measures - authentication, encryption, monitoring, etc.]

## Code/Architecture to Audit:
[PASTE YOUR CODE OR DESCRIBE THE SYSTEM ARCHITECTURE]

## Security Audit Request:

Please conduct a thorough security assessment covering:

### 1. Authentication & Authorization
- Review authentication mechanisms
- Assess authorization controls and access management
- Check for privilege escalation vulnerabilities
- Evaluate session management security
- Review password policies and storage

### 2. Input Validation & Data Security
- Identify input validation vulnerabilities
- Check for injection attacks (SQL, XSS, LDAP, etc.)
- Assess data sanitization and encoding
- Review file upload security
- Evaluate data validation on client and server

### 3. Data Protection
- Review data encryption at rest and in transit
- Assess sensitive data handling and storage
- Check for data leakage vulnerabilities
- Evaluate backup and recovery security
- Review data retention and deletion policies

### 4. Network & Infrastructure Security
- Assess network security configurations
- Review API security and rate limiting
- Check for insecure direct object references
- Evaluate CORS and CSP policies
- Review SSL/TLS configuration

### 5. Application Security
- Identify business logic vulnerabilities
- Check for insecure cryptographic practices
- Review error handling and information disclosure
- Assess logging and monitoring security
- Evaluate third-party dependency security

### 6. Configuration & Deployment Security
- Review security configurations
- Check for default credentials and settings
- Assess environment variable security
- Review deployment pipeline security
- Evaluate infrastructure as code security

## Security Assessment Report:

Please provide:

### Critical Vulnerabilities
- High-risk security issues requiring immediate attention
- Potential impact and exploitation scenarios
- Specific remediation steps with code examples

### Major Security Concerns
- Important security improvements needed
- Risk assessment and prioritization
- Recommended security enhancements

### Security Best Practices
- General security improvements
- Industry standard recommendations
- Preventive measures for future development

### Compliance Considerations
- Compliance gaps for mentioned regulations
- Required security controls
- Documentation and audit trail requirements

### Security Testing Recommendations
- Suggested security testing approaches
- Tools and techniques for ongoing security assessment
- Automated security scanning integration

### Monitoring & Incident Response
- Security monitoring recommendations
- Incident response planning
- Alerting and notification strategies

## Specific Focus Areas:
Please pay special attention to:
- [Any specific security concerns you have]
- [Recent security incidents or vulnerabilities you've heard about]
- [Specific compliance requirements you need to meet]

## Deliverables Requested:
- Prioritized list of security issues
- Specific remediation code examples
- Security checklist for ongoing maintenance
- Recommendations for security tools and processes

Please be thorough but practical, focusing on actionable security improvements that provide the most security value.
```

---

## Tips for Better Results:

- **Include your full system architecture**——不仅仅是代码片段
- **提及您的行业所需的特定合规性要求**
- **明确您处理的数据类型**（PII、财务等）
- **包含您当前的安全措施**以避免重复建议
- **指定您的风险承受能力**和安全预算限制
