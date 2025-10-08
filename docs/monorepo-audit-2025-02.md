# Monorepo 结构与环境配置审计（2025 年 2 月）

> 本报告对 Sydney Rental Hub 仓库（pnpm + Turborepo 主导）进行了结构、依赖与环境的全面盘点，目标是让团队在 30/60/90 天内落地一套可持续的多语言工作流。

## 1. 执行摘要（Executive Summary）
- **单一工作流尚未成型**：根目录声明 `pnpm@9.1.0` 并以 Turborepo 运行标准任务，但 `apps/web` 与 `apps/mcp-server` 仍提交各自的 `package-lock.json`，削弱了 Workspace 去重效果，也可能让 CI/CD 在不同包管理器之间往返。建议以「只保留 pnpm 锁文件」为第一治理动作。【F:package.json†L1-L17】【F:apps/web/package-lock.json†L1-L34】【F:apps/mcp-server/package-lock.json†L1-L34】
- **关键目录游离于 workspace 之外**：`pnpm-workspace.yaml` 只包含 `apps/*` 与不存在的 `packages/*`，`crawler/`、`database/`、`vue-frontend/` 等 Python 或遗留资产无法参与 Turbo 编排，意味着它们的测试、Lint 与依赖健康度全凭人工维护。【F:pnpm-workspace.yaml†L1-L4】【F:crawler/CLAUDE.md†L1-L52】【F:database/README.md†L1-L84】【F:vue-frontend/前端盘点.md†L1-L80】
- **Python 栈与 Node 工具链割裂**：FastAPI 后端通过 `scripts/run_backend.py` 调用 `pnpm --filter`，但真实依赖位于未加锁的 `requirements.txt`；`apps/backend/package.json` 也未声明任何 Node 依赖，只提供 Python 命令代理。新成员需要手工拼装环境，可复现性极低。【F:scripts/run_backend.py†L1-L34】【F:apps/backend/package.json†L1-L12】【F:requirements.txt†L1-L44】
- **环境变量指南不覆盖多栈需求**：`.env.example` 聚焦模型 API Key 与数据库池化参数，没有前端 `VITE_` 前缀示例，也缺少后端强制字段（如 `DATABASE_URL`）。部署脚本（Netlify、后端脚本）默认具备 pnpm，缺乏「多工具链 fallback」说明，易在不同平台踩坑。【F:.env.example†L1-L29】【F:netlify.toml†L1-L14】【F:scripts/run_backend.py†L1-L34】
- **知识资产缺少自动化守护**：仓库强调 `/memory-bank` 是唯一真理来源，却没有任何 lint 或构建任务确保文档与代码同步；同理，`vue-frontend/` 留存大量设计系统资产但未纳入流水线，需要明确留存/归档策略。【F:README.md†L1-L32】【F:vue-frontend/前端盘点.md†L1-L80】

## 2. 成熟度雷达图（Maturity Snapshot）
| 能力域 (Domain) | 当前等级* | 核心缺口 (Key Gap) | 下一步 (Next Move) |
| --- | --- | --- | --- |
| 依赖治理 Dependency Hygiene | 2 / 5 | npm 与 pnpm 双轨、Python 无锁文件 | 清理 npm 锁文件，评估 `uv`/`pip-tools` 锁定策略。【F:apps/web/package-lock.json†L1-L34】【F:apps/mcp-server/package-lock.json†L1-L34】【F:requirements.txt†L1-L44】 |
| Workspace 可观测性 Workspace Coverage | 2 / 5 | `crawler/`、`database/`、`vue-frontend/` 未纳入 Turbo | 补充 workspace 配置或以独立管线覆盖健康检查。【F:pnpm-workspace.yaml†L1-L4】【F:crawler/CLAUDE.md†L1-L52】【F:database/README.md†L1-L84】 |
| 环境可复现性 Environment Reproducibility | 1 / 5 | 后端启动依赖 pnpm，Python 依赖未锁 | 提供纯 Python 启动脚本和锁文件，记录安装步骤。【F:scripts/run_backend.py†L1-L34】【F:requirements.txt†L1-L44】 |
| 配置管理 Configuration Management | 2 / 5 | `.env.example` 未覆盖前后端需求 | 拆分多份模板或补充变量注释，降低踩坑成本。【F:.env.example†L1-L29】 |
| 知识资产可靠性 Knowledge Base Reliability | 1 / 5 | `/memory-bank`/`vue-frontend` 无守护任务 | 增加 Markdown lint、Storybook 构建或归档流程。【F:README.md†L1-L32】【F:vue-frontend/前端盘点.md†L1-L80】 |

\* 1=临时性、2=重复性、3=定义化、4=量化、5=优化

## 3. 仓库地图（Repository Map）
| 路径 | 技术栈 / 职责 | 依赖资产 | 自动化现状 | 风险提示 |
| --- | --- | --- | --- | --- |
| `apps/web` | Vue 3 + Vite + Storybook 前端。【F:apps/web/package.json†L1-L44】 | `package.json` + 额外的 `package-lock.json`。【F:apps/web/package-lock.json†L1-L34】 | Turborepo 可运行构建/测试；Netlify 直接用 `pnpm --filter`。【F:turbo.json†L1-L20】【F:netlify.toml†L1-L9】 | 锁文件冲突造成依赖重复，需统一为 pnpm。 |
| `apps/mcp-server` | Node/TS MCP 服务，提供模型上下文协议接口。【F:apps/mcp-server/package.json†L1-L27】 | 提交 npm 锁文件，lint 实际为空指令。【F:apps/mcp-server/package-lock.json†L1-L34】【F:apps/mcp-server/package.json†L11-L17】 | Turbo 可运行 build/test/typecheck，但缺乏真实 lint。 | 缺少质量门禁，建议补齐 ESLint + Prettier。 |
| `apps/backend` | FastAPI + Celery + ETL API。【F:apps/backend/package.json†L1-L12】 | 依赖集中在 `requirements.txt`，无版本锁定。【F:requirements.txt†L1-L44】 | 未纳入 Turbo；脚本通过 pnpm 启动。【F:scripts/run_backend.py†L1-L34】 | Node 工具链成单点，Python 依赖漂移风险高。 |
| `crawler/` | Python 爬虫与特征提取工具。【F:crawler/CLAUDE.md†L1-L52】 | 独立安装说明，未接入 pnpm。 | 无 CI/CD 任务或质量检查。 | 需决定纳管方式（独立虚拟环境或归档）。 |
| `database/` | PostgreSQL 迁移、数据处理脚本。【F:database/README.md†L1-L84】 | 依赖与 `requirements.txt` 重叠但无锁定。 | 未在 Turbo 中定义任务。 | 数据核心却无自动化守护，建议专属管线。 |
| `vue-frontend/` | 旧版设计系统与静态 Storybook 资产。【F:vue-frontend/前端盘点.md†L1-L80】 | 需要独立构建工具链。 | 无自动化；状态未知。 | 明确留存价值或归档清理。 |

## 4. 关键风险叙事（Key Risk Narratives）
1. **双轨锁文件导致依赖失控**：`.npmrc` 规定 hoisted linker，但若开发者运行 `npm install`，`apps/*` 的 npm 锁文件会生成与 pnpm 不兼容的目录结构，可能触发 Turbo 构建失败或 Netlify 构建异常。【F:.npmrc†L1-L1】【F:apps/web/package-lock.json†L1-L34】【F:apps/mcp-server/package-lock.json†L1-L34】【F:netlify.toml†L1-L9】
2. **Python 环境缺乏守护**：`requirements.txt` 既无版本上限也无锁文件，且文件末尾缺换行，实际安装顺序随 pip 解析器变化而漂移；后端脚本仅提示安装 pnpm，而未告知如何直接启动 Python 服务，阻碍了离线或容器化部署。【F:requirements.txt†L1-L44】【F:scripts/run_backend.py†L1-L34】
3. **Workspace 死角阻断可观测性**：`pnpm-workspace.yaml` 中列出的 `packages/*` 目录并不存在，反而遗漏了真实需要维护的 Python 与遗留前端目录，使得仓库根脚本与 Turbo 任务无法覆盖它们，导致这些子系统的健康状态不可见。【F:pnpm-workspace.yaml†L1-L4】【F:crawler/CLAUDE.md†L1-L52】【F:database/README.md†L1-L84】【F:vue-frontend/前端盘点.md†L1-L80】
4. **环境变量文档无法指导跨栈协作**：`.env.example` 未标注前端 `VITE_` 开头变量，后端数据库 URL 仅以注释给出；Netlify/PNPM 的默认假设在多团队协作时信息缺失，可能导致构建失败或后端无法连接数据库。【F:.env.example†L1-L29】【F:netlify.toml†L1-L14】
5. **知识体系缺少自动化校验**：README 将 `/memory-bank` 定义为单一真理，但仓库无 lint/构建任务监督该目录更新；历史的 `vue-frontend/` 设计系统同样缺少 Storybook 构建或废弃声明，造成认知债务。【F:README.md†L1-L32】【F:vue-frontend/前端盘点.md†L1-L80】

## 5. 治理路线图（Remediation Roadmap）
### 0-30 天
- 清理 `apps/*` 下的 `package-lock.json` 与冗余 `node_modules`，更新贡献指南强调 `pnpm install` 为唯一入口。【F:apps/web/package-lock.json†L1-L34】【F:apps/mcp-server/package-lock.json†L1-L34】
- 调整 `pnpm-workspace.yaml`，纳入仍活跃的 Python/遗留目录或显式归档它们；同步在 Turbo 中创建占位任务（例如 `lint:python`）。【F:pnpm-workspace.yaml†L1-L4】【F:crawler/CLAUDE.md†L1-L52】
- 为 `.env.example` 增补 web/backend/MCP 三类示例变量，并记录 pnpm 依赖前提。【F:.env.example†L1-L29】

### 30-60 天
- 选型 `uv`、`Poetry` 或 `pip-tools` 为 Python 生成锁文件，确保 `requirements.lock` 与 `requirements.txt` 一致；提供 `Makefile` 或 `invoke` 命令以纯 Python 方式启动后端和任务队列。【F:requirements.txt†L1-L44】【F:apps/backend/package.json†L1-L12】
- 为 MCP/后端加入真实 lint/格式化任务（ESLint、ruff/black），并在 Turbo 中串联。【F:apps/mcp-server/package.json†L11-L17】【F:turbo.json†L1-L20】
- 设计 `/memory-bank` 文档校验（Markdown lint、front-matter 校验），并在 PR 流程中强制执行。【F:README.md†L1-L32】

### 60-90 天
- 建立多环境部署蓝图：明确 Netlify（前端）、Render/railway（后端）、计划任务（爬虫/ETL）的工具链与 secrets 配置，并编写运行手册。【F:netlify.toml†L1-L14】【F:crawler/CLAUDE.md†L1-L52】【F:database/README.md†L1-L84】
- 评估 `vue-frontend/` 资产价值：若保留，迁移到统一 workspace 并恢复 Storybook 构建；若淘汰，归档至 `archive/` 并在 README 标注状态。【F:vue-frontend/前端盘点.md†L1-L80】
- 引入依赖/工作区健康监控（例如定期 `pnpm audit` + `pip check` + `turbo run lint`），并将结果写入周报或仪表盘。【F:package.json†L1-L17】【F:requirements.txt†L1-L44】

## 6. 工具链与环境优化建议（Detailed Recommendations）
### 6.1 Node / PNPM
- 在仓库根目录增加 pre-commit 钩子或 CI 检查，拒绝再次提交 npm 锁文件；在贡献指南明确 `pnpm install` 与 `pnpm dlx turbo` 的使用顺序。【F:package.json†L1-L17】【F:apps/web/package-lock.json†L1-L34】【F:apps/mcp-server/package-lock.json†L1-L34】
- 为 MCP 服务补充真实 lint/format 任务（ESLint + Prettier），并在 Turborepo 中把 `lint` 任务串联起来，避免空指令导致的盲区。【F:apps/mcp-server/package.json†L11-L17】【F:turbo.json†L1-L20】
- 在 Netlify 文档中强调构建前需执行 `pnpm install`，必要时在 `netlify.toml` 中添加 `npm install -g pnpm` 或使用 Netlify 的 `NODE_VERSION` 与 `PNPM_VERSION` 设置，降低锁文件冲突风险。【F:netlify.toml†L1-L9】

### 6.2 Python / 数据管道
- 采用 `uv pip compile` 或 `pip-compile` 生成锁文件，并在 CI 中执行 `pip install -r requirements.lock` 验证；同时为爬虫、数据库脚本划分虚拟环境或使用 `pyproject.toml` 管理共享依赖。【F:requirements.txt†L1-L44】【F:crawler/CLAUDE.md†L1-L52】【F:database/README.md†L1-L84】
- 改写 `scripts/run_backend.py`：在未找到 pnpm 时自动 fallback 为 `python -m uvicorn`，并打印如何安装 Python 依赖的提示；同时在 `apps/backend` 添加 `README` 或 `Makefile`，记录启动命令。【F:scripts/run_backend.py†L1-L34】【F:apps/backend/package.json†L1-L12】
- 为 Celery、ETL 任务建立最小可行的测试（如 schema 校验、静态分析），并将其挂在 Turbo 的 `test` 或自定义 `lint:python` 任务下运行，以形成跨语言一致的质量门槛。【F:turbo.json†L1-L20】【F:database/README.md†L1-L84】

### 6.3 文档与知识资产
- 对 `/memory-bank` 引入 Markdown lint（如 `markdownlint-cli2`）或 front-matter 校验，并把它纳入 `pnpm lint`；同时在 README 添加对 lint 失败场景的指引，确保“真理之源”与代码同步演进。【F:README.md†L1-L32】
- 针对 `vue-frontend/` 制定去留决策：若继续维护，应恢复 Storybook 构建与 tokens 同步；若弃用，迁移到 `archive/` 并更新文档，防止误导新成员。【F:vue-frontend/前端盘点.md†L1-L80】

### 6.4 环境变量与部署
- 把 `.env.example` 拆分为 `env.example.web`、`env.example.backend`、`env.example.mcp` 或在同一文件中增加注释区分用途，并加入 `VITE_PUBLIC_API_BASE`、`DATABASE_URL` 等强制项示例，防止遗漏关键配置。【F:.env.example†L1-L29】
- 在技术文档中补充「多栈部署矩阵」，说明 Netlify（前端）、后端托管平台、定时任务（爬虫/ETL）的触发方式与 Secrets 管理，避免默认假设 pnpm 已安装导致部署失败。【F:netlify.toml†L1-L14】【F:crawler/CLAUDE.md†L1-L52】【F:database/README.md†L1-L84】

## 7. 验证清单（Validation Checklist）
- `pnpm install && pnpm lint --filter ./...`：确认清理锁文件后 workspace 能正确解析依赖，并监控是否仍有 npm 锁文件重新生成。【F:package.json†L1-L17】【F:apps/web/package-lock.json†L1-L34】
- `uv pip compile requirements.txt`（或 `pip-compile`）+ `pip install -r requirements.lock`：验证 Python 依赖是否能被锁定且无冲突。【F:requirements.txt†L1-L44】
- 自定义脚本检查 `pnpm-workspace.yaml` 中不存在的路径（如 `packages/*`），并提醒是否漏掉新增目录；同时确保 `crawler/`、`database/` 等需要维护的子目录被正确纳入。【F:pnpm-workspace.yaml†L1-L4】【F:crawler/CLAUDE.md†L1-L52】【F:database/README.md†L1-L84】
- Lint `/memory-bank`、`docs/` 与 `vue-frontend/`，确保知识资产与设计系统在自动化中得到验证，从而降低“文档漂移”风险。【F:README.md†L1-L32】【F:vue-frontend/前端盘点.md†L1-L80】

---

通过上述治理步骤，团队可在三个季度内完成从「工具链割裂、配置依赖手工经验」向「跨栈自动化、依赖可追踪」的跃迁，为持续交付与多团队协作打下坚实基础。
