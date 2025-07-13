## 简要概述
本指南包含悉尼租房平台API开发的核心规范，涵盖RESTful API设计、性能优化、安全实践和项目结构规范。适用于FastAPI后端服务和Supabase数据库交互场景。

## 沟通风格
- **首要原则：项目所有参与者（包括AI）的日常沟通和讨论应优先使用中文，以确保信息传达的准确性。**
- 技术讨论使用中文，代码注释使用英文
- 问题描述需包含：现象、复现步骤、预期结果
- 重大架构变更前需提交设计文档（markdown格式）

## 开发流程规范
- API开发遵循OpenAPI 3.0规范
- 所有接口需提供Swagger文档
- 数据库变更需通过迁移脚本实现（位于/database目录）
- 重要功能需提供验证查询（参考database/verification_queries.sql）

## API设计原则
- RESTful资源命名使用复数形式（如`/api/properties`）
- 响应格式统一：
  ```json
  {
    "data": {},
    "meta": {
      "pagination": {}
    }
  }
  ```
- 错误响应包含标准错误码：
  ```json
  {
    "error": {
      "code": "INVALID_PARAM",
      "message": "参数校验失败"
    }
  }
  ```

## 性能优化要求
- 列表接口必须实现分页（默认每页20条）
- 高频查询必须添加数据库索引
- 耗时操作异步处理（使用Celery或后台任务）
- 启用Gzip压缩（FastAPI middleware）

## 安全规范
- 所有API必须包含API密钥认证
- 敏感路由启用速率限制（例如登录接口）
- 数据库访问使用最小权限原则
- 错误消息不返回堆栈跟踪（生产环境）

## 测试要求
- 核心业务逻辑测试覆盖率 ≥ 80%
- 包含性能测试脚本（位于/scripts目录）
- 新接口需提供Postman测试集合
- 数据库变更需提供回滚脚本

## 项目上下文
- 主分支：main
- 开发分支：feat/*
- 紧急修复分支：hotfix/*
- 配置管理：环境变量优先（.env文件）
- 文档位置：/docs/PRD

## 其他规范
- 日志格式：[时间] [级别] [模块] 消息
- 监控：关键指标通过Discord通知
- 部署：GitHub Actions自动化
- 技术栈：
  - 后端：Python + FastAPI
  - 数据库：Supabase(PostgreSQL)
  - 前端：Vue.js + Taro
