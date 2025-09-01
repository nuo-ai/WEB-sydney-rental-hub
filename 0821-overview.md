代码库结构概览
memory-bank/
项目愿景、技术栈、开发计划等文档的唯一真实来源，是新人入门的第一站。

backend/
基于 FastAPI + Strawberry GraphQL 的后端服务：

main.py 配置应用、认证、限流与缓存等。

api/graphql_schema.py 定义 GraphQL 查询与数据模型。

crud/ 包含直接访问数据库的函数（psycopg2）。

models/ 定义属性与通勤相关数据结构。

crawler/
Python 爬虫与特征提取脚本，按配置抓取房源并输出到 CSV/Excel。

database/
PostgreSQL 初始化脚本、迁移脚本与数据处理工具（populate_serviced_routes.py 等）。

frontend/
静态 HTML/JS 原型站点，含 Netlify serverless functions。

react-frontend/
以 Vite + React + TypeScript 实现的新版前端。

mcp-server/
Node/TypeScript 实现的辅助服务（可能用于多聊天协议或 API 代理）。

新人需要了解的重点
阅读 /memory-bank 文档：确保对项目目标、系统架构与当前状态有全面理解。

环境与配置：后端依赖环境变量（数据库、API Key、JWT Secret 等），本地开发可查 memory-bank/techContext.md。

数据流：

数据由 crawler/ 抓取并通过 database/ 脚本导入 PostgreSQL。

backend/crud/ 直接从数据库读写，api/graphql_schema.py 暴露查询接口。

前端交互：frontend/ 和 react-frontend/ 对接同一后端，前者偏原型，后者是正式方向。

任务/计划：memory-bank/activeContext.md 与 progress.md 记录当前迭代与未来路线。

后续学习建议
熟悉 FastAPI + Strawberry GraphQL 的认证、分页、缓存等模式。

深入理解 PostgreSQL + PostGIS 与 psycopg2 的使用。

了解 爬虫配置与数据清洗流程，掌握如何扩展抓取能力。

对前端有兴趣者，可学习 Vite/React/TypeScript 并逐步迁移旧版静态页面。

关注文档中的 “MVP 成功指标” 与 “开发计划”，以任务驱动方式参与开发。

发现的问题与改进建议
后端敏感信息使用默认值
当前 backend/main.py 为 API Key 和 JWT Secret 设置了明文默认值，不利于生产安全。

建议的任务
移除后端硬编码的敏感默认值

启动任务
GraphQL 通勤接口尚未实现
get_university_commute_profile 仍为占位符，crud/commute_crud.py 也仅返回空数据。

建议的任务
实现大学通勤档案的完整查询
查看任务
缺少自动化测试
代码库几乎没有测试，难以验证 GraphQL resolvers 和 CRUD 函数是否正常工作。

建议的任务
为后端增加基础测试套件

启动任务
前端脚本体积庞大且职责混杂
frontend/scripts/main.js 同时处理 UI 增强、收藏、过滤等多种逻辑，可读性和维护性较差。

建议的任务
拆分前端主脚本并引入模块化

启动任务
希望这些说明能帮助你快速融入项目，祝开发顺利！

memory bank 文档是否真正反应了项目的真实面貌？
复制
Memory Bank 文档未能准确反映当前代码库的真实情况。主要不一致包括：

技术栈夸大与不符：techContext.md 声称后端已集成 Celery + Redis 异步任务、20+ 房源筛选、企业级功能等，但在 backend/ 中并未发现任何 Celery 相关文件或配置，Redis 仅用于缓存，功能远未达到文档描述的广度。

前端现状被刻意淡化：文档多次强调“Old frontend（Vanilla JS）功能极其完善、无需 React”，但仓库实际包含 react-frontend/，并且该目录是一个标准的 Vite + React + TypeScript 项目，显然处于活跃开发状态。

时间线与项目状态不匹配：多处文档标注“最后更新：2025-08-20”等未来日期，并描述已完成的大规模迁移和修复工作，与仓库代码和目录结构（例如不存在 Old/ 目录）不符。

这些迹象表明 Memory Bank 文档明显偏离真实项目状态，可能已过期或包含误导信息。

建议的任务
更新 Memory Bank 文档以反映真实项目状态

启动任务
整体而言，建议以代码库现状为准进行理解和开发，不应将 Memory Bank 文档视为可靠依据。

你确定吗？请再仔细查看。
复制
以下为更仔细复核后的结果：

代码库结构与重要说明
memory-bank/
官方声称的“真理之源”，但部分内容带有未来日期（例如 2025-08-19/20）并引用 Old/... 目录，当前仓库中并不存在；建议阅读时对照代码验证。

backend/
FastAPI + Strawberry GraphQL 服务。包含 Celery/Redis 异步任务、缓存、分页、安全（API Key + JWT）、以及房源与通勤相关 CRUD。

crawler/
Python 爬虫脚本，抓取房源并写入 CSV/Excel。

database/
PostgreSQL 初始化和数据处理脚本（如 populate_serviced_routes.py）。

frontend/
旧版静态站点（HTML + Vanilla JS + Netlify Functions），scripts/main.js 超过 500 行。

react-frontend/
基于 Vite + React + TypeScript 的新前端框架，功能较少。

mcp-server/
Node/TypeScript 服务，提供外部接口；当前状态不明，PRODUCTION-DEPLOYMENT.md 描述部署方式。

archive/
存放旧文档和资料。

新手建议

先阅读 memory-bank，但务必与代码比对，因文档可能与实际实现不符。

熟悉后端 .env.example 中的必需环境变量（数据库、API Key、JWT Secret、Redis URL 等）。

数据流：crawler → database → backend → frontend/react-frontend。

前端有双轨并存：frontend 为现成原型，react-frontend 为计划中的正式版本。

后端除了 API 以外，还集成 Celery 异步任务，可通过 /api/tasks/* 触发。

发现的问题与改进任务
后端默认暴露敏感信息
backend/main.py 对 API_KEY 与 SECRET_KEY 设置了明文默认值，存在安全隐患。

建议的任务
移除后端硬编码的敏感默认值

启动任务
通勤 GraphQL 接口未完整实现
get_university_commute_profile 仅返回步行方案；fetch_full_university_commute_profile 仍是占位符，公交/地铁等逻辑缺失。

建议的任务
完善大学通勤档案查询逻辑

启动任务
缺乏自动化测试
仓库未见任何 tests/ 目录，功能回归难以保障。

建议的任务
为后端添加基础测试套件

启动任务
前端主脚本过于臃肿
frontend/scripts/main.js 约 571 行，混合 UI 增强、收藏、过滤等多种逻辑，可读性差。

建议的任务
拆分前端主脚本并模块化

启动任务
如需进一步深入，可逐步熟悉 FastAPI、Strawberry、Celery、PostgreSQL/PostGIS 以及 React/Vite 等技术栈。祝学习顺利！
