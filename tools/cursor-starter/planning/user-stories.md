# 用户故事生成

**适用场景：** 当您需要将需求或想法转化为结构良好、带有验收标准的用户故事时使用。

**技能水平：** 初学者到中级

## 复制此提示：

我需要帮助为我的项目创建全面的用户故事。请帮助我将我的需求转化为编写良好、带有清晰验收标准的用户故事。

## 项目背景：

- **项目类型**：小程序
- **目标用户**：赴澳或在澳留学生
- **主要目的**：找房+申请指导+申请代办+周边（卖资料？合租撮合？婚姻中介？）
- **关键功能**：
  - 按区域/地铁沿线-按卧室/价格/入住日期搜索房源
  - 新房源提醒（站内+微信+邮件）
  - 

## 需要转化的需求：

[在此处描述您的需求、功能或想法]

## 用户故事创建请求：

请创建遵循以下结构的用户故事：

### 故事格式：

**作为** [用户类型]
**我希望** [功能]
**以便** [收益/价值]

### 对于每个用户故事，请包括：

#### 1. 用户故事详情

- 遵循标准格式的清晰、简洁的故事
- 特定的用户画像（最终用户、管理员、访客等）
- 定义明确的功能或特性
- 清晰的商业价值或收益

#### 2. 验收标准

- 必须满足的具体的、可测试的条件
- 在适当时使用“鉴于（Given）、当（When）、那么（Then）”格式
- 包括正面和负面场景
- 覆盖边缘情况和错误条件

#### 3. 故事规格

- **故事点/工作量**：粗略的复杂性估算
- **优先级**：高/中/低，基于商业价值
- **依赖关系**：必须先完成的其他故事
- **完成的定义**：什么才算完成

#### 4. 附加详情

- **业务规则**：任何特定的业务逻辑要求
- **技术说明**：重要的技术考量
- **UX/UI 需求**：用户体验要求
- **性能标准**：任何性能要求

## 用户故事类别：

请将故事组织到以下类别中：

### 史诗级故事（Epic）

- 跨越多个冲刺（sprint）的大型功能
- 高层次的用户目标和旅程
- 主要的系统能力

### 功能级故事（Feature）

- 史诗中的中等规模功能
- 完整的用户工作流
- 特定的功能实现

### 任务级故事（Task）

- 小而具体的功能片段
- 单个屏幕或组件
- 单个用户操作或交互

## 故事示例：

对于每个故事，提供如下示例：

**用户故事：**
作为一名注册用户
我希望通过电子邮件重置我的密码
以便在我忘记密码时能够重新访问我的账户

**验收标准：**

- 鉴于我在登录页面
- 当我点击“忘记密码”并输入我的电子邮件时
- 那么我在 5 分钟内会收到一封密码重置邮件
- 鉴于我点击了邮件中的重置链接
- 当我输入一个新密码（满足要求）时
- 那么我的密码被更新，并且我能成功登录
- 鉴于重置链接已超过 24 小时
- 当我尝试使用它时
- 那么我会看到一条错误消息，并且可以请求一个新的链接

## 附加考量：

请确保故事是：

- **独立的（Independent）**：可以单独开发和测试
- **可协商的（Negotiable）**：可以被讨论和完善
- **有价值的（Valuable）**：提供清晰的商业价值
- **可估算的（Estimable）**：可以被估算大小和规划
- **小的（Small）**：可以在合理的时间内完成
- **可测试的（Testable）**：有清晰的验收标准

## 故事优化：

- 将相关的故事分组为史诗
- 识别故事之间的依赖关系
- 对大型故事建议进行拆分
- 根据价值和依赖关系推荐优先级

请专注于创建可操作、可测试并为用户提供清晰价值的故事。

---

## 获得更好结果的提示：

- **如果您已定义了用户画像或类型，请提供它们**
- **具体说明您希望支持的工作流和用户旅程**
- **提及任何需要与新故事集成起来的现有功能**
- **包括影响功能的业务约束或规则**
- **指明您的开发方法论**（Scrum、Kanban 等）

---

# User Story Generation

**Use this when:** You need to convert requirements or ideas into well-structured user stories with acceptance criteria.

**Skill Level:** Beginner to Intermediate

---

## Copy This Prompt:

```
I need help creating comprehensive user stories for my project. Please help me convert my requirements into well-written user stories with clear acceptance criteria.

## Project Context:
- **Project Type**: [Web app, mobile app, API, etc.]
- **Target Users**: [Who are your primary users?]
- **Main Purpose**: [What does your application do?]
- **Key Features**: [List the main features or functionality]

## Requirements to Convert:
[DESCRIBE YOUR REQUIREMENTS, FEATURES, OR IDEAS HERE]

## User Story Creation Request:

Please create user stories that follow this structure:

### Story Format:
**As a** [user type]  
**I want** [functionality]  
**So that** [benefit/value]

### For each user story, please include:

#### 1. User Story Details
- Clear, concise story following the standard format
- Specific user persona (end user, admin, guest, etc.)
- Well-defined functionality or feature
- Clear business value or benefit

#### 2. Acceptance Criteria
- Specific, testable conditions that must be met
- Use "Given, When, Then" format where appropriate
- Include both positive and negative scenarios
- Cover edge cases and error conditions

#### 3. Story Specifications
- **Story Points/Effort**: Rough complexity estimate
- **Priority**: High/Medium/Low based on business value
- **Dependencies**: Other stories that must be completed first
- **Definition of Done**: What constitutes completion

#### 4. Additional Details
- **Business Rules**: Any specific business logic requirements
- **Technical Notes**: Important technical considerations
- **UX/UI Requirements**: User experience requirements
- **Performance Criteria**: Any performance requirements

## User Story Categories:

Please organize stories into these categories:

### Epic Level Stories
- Large features that span multiple sprints
- High-level user goals and journeys
- Major system capabilities

### Feature Level Stories  
- Mid-sized functionality within an epic
- Complete user workflows
- Specific feature implementations

### Task Level Stories
- Small, specific pieces of functionality
- Individual screens or components
- Single user actions or interactions

## Story Examples:

For each story, provide examples like:

**User Story:**
As a registered user  
I want to reset my password via email  
So that I can regain access to my account if I forget my password

**Acceptance Criteria:**
- Given I'm on the login page
- When I click "Forgot Password" and enter my email
- Then I receive a password reset email within 5 minutes
- Given I click the reset link in the email
- When I enter a new password (meeting requirements)
- Then my password is updated and I can log in
- Given the reset link is older than 24 hours
- When I try to use it
- Then I see an error message and can request a new link

## Additional Considerations:

Please ensure stories are:
- **Independent**: Can be developed and tested separately
- **Negotiable**: Can be discussed and refined
- **Valuable**: Provide clear business value
- **Estimable**: Can be sized and planned
- **Small**: Can be completed in a reasonable timeframe
- **Testable**: Have clear acceptance criteria

## Story Refinement:
- Group related stories into epics
- Identify dependencies between stories
- Suggest story splitting for large stories
- Recommend prioritization based on value and dependencies

Focus on creating stories that are actionable, testable, and provide clear value to users.
```

---

## Tips for Better Results:

- **Include user personas** or types if you have them defined
- **Be specific about workflows** and user journeys you want to support
- **Mention any existing features** that new stories should integrate with
- **Include business constraints** or rules that affect functionality
- **Specify your development methodology** (Scrum, Kanban, etc.)
