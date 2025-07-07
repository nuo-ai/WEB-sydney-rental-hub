## Brief overview
用户明确要求使用中文进行沟通的规则。这是一个全局性的沟通偏好设置，适用于所有与该用户的交互。

## Communication style
- 始终使用中文与用户沟通
- 保持专业和技术性的表达方式
- 代码注释和文档可以使用中文
- 用户界面文本应当优先考虑中文

## Development workflow
- 采用UI-first开发策略，先构建完整的静态UI再集成后端
- 当功能变得过于复杂时，用户倾向于回退到更简单的版本
- 重视代码的可维护性和清晰的回退路径
- 使用Memory Bank文档系统来跟踪项目状态和决策

## Coding best practices
- 优先使用原生HTML/CSS/JS而非框架，保持简洁性
- 后端使用FastAPI + GraphQL架构
- PostgreSQL + PostGIS用于地理空间数据处理
- 前后端分离部署策略

## Project context
- 专注于悉尼租房平台，面向中国学生群体
- 以通勤时间到大学作为主要搜索条件
- 移动优先的设计理念
- 所有用户界面内容使用中文

## Other guidelines
- 在实现复杂功能前，确保用户理解并同意方案
- 保持功能的可选性和可回退性
- 重视简洁性胜过功能复杂性
- 定期更新Memory Bank文档以保持项目状态同步
