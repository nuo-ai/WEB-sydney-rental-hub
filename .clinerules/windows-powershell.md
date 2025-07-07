## Brief overview
针对Windows PowerShell环境的特殊命令语法和开发流程规则，基于用户在悉尼租房平台项目中遇到的具体问题和偏好。

## Command syntax
- 绝对不要使用 `&&` 作为命令分隔符，因为PowerShell不支持
- 使用 `;` 分隔多个命令: `cd sydney-rental-mcp; npm start`
- 对于需要curl的场景，使用PowerShell的 `Invoke-WebRequest` 或明确调用 `powershell -Command`
- 避免使用Linux/Unix特有的命令语法

## Development workflow
- 优先使用Python的内置HTTP服务器进行前端测试: `python -m http.server 8080`
- 当服务启动后经常出现"僵住"现象时，立即添加超时机制
- 对于API测试，总是包含超时和详细的错误处理
- 使用分步骤的诊断方法，避免一次性启动多个服务

## Error handling patterns
- 对于连接超时问题，优先检查服务是否真正启动
- 区分 `localhost` 和 `127.0.0.1` 的连接差异
- 在脚本中添加中文错误提示，提高调试效率
- 对于MCP服务器连接问题，按顺序检查：MCP服务器 → 后端API → 数据库

## Troubleshooting approach
- 当系统"僵住"时，首先添加超时机制而不是查找根本原因
- 使用渐进式测试：先测试基本连接，再测试完整功能
- 优先修复让系统可用，然后再优化性能
- 对于重复出现的问题，创建快速诊断脚本

## Project context
- 这是一个多服务架构：前端(8080) + 后端API(8000) + MCP服务器 + PostgreSQL
- 服务间连接问题是常见故障点
- 用户更关心系统是否能正常工作，而非技术细节的完美实现
