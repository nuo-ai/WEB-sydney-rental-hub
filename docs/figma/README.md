Figma UI Kit 集成说明

目标
- 从 Figma 文件中提取结构、设计 Tokens（颜色/字体/间距/圆角/阴影）、以及图标清单，生成可落地的映射草稿，最终与现有 tokens/ 与 UI 组件库对齐。

来源
- Figma 链接: https://www.figma.com/design/lXOwmixlbhaJZWc4w2pk1s/1011-UI-kit?node-id=1-1220

当前状态（阻塞）
- 2025-10-11 使用 MCP 工具 get_figma_data(fileKey=lXOwmixlbhaJZWc4w2pk1s, nodeId=1:1220) 失败，Figma API 返回 403 Forbidden。
- 常见原因：当前使用的 Figma Personal Access Token（PAT）所属账号对该文件没有访问权限。注意：浏览器“公开可查看”不等同于 API 可读；API 读取需要“令牌所属用户”对该文件具备权限。

解决方案（任选其一）
A) 将 Figma 文件共享给令牌所属账号（推荐）
- 打开 Figma 文件 → 右上角 Share → 邀请令牌对应的 Figma 账号（邮箱）为 Viewer 或更高权限。
- 我方无法从令牌值推断邮箱，请提供该邮箱或直接邀请你自己的可用账号并更换令牌（见方案 B）。

B) 更换为你个人可访问该文件的 Figma PAT
- 在 Figma 个人设置 → Personal access tokens → 生成新 Token（具备对目标文件访问的账号）。
- 更新本地 MCP 服务器配置中的 --figma-api-key（或对应配置项），重启 MCP 服务器后重试。
  说明：本项目当前的 Figma MCP 服务通过命令行参数 --figma-api-key=... 启动，替换后需要重启才能生效。

C) 手动导出（临时替代）
- 图标：在 Figma 中批量导出为 SVG，提供命名清单（建议 kebab-case，无尺寸后缀），我方将放入 packages/ui/src/icons/。
- Tokens：导出或截图颜色/字体/间距/圆角/阴影变量命名与数值清单；我方据此生成 tokens 映射草稿。

一旦解除 403 后的自动化流程
1) 抓取节点结构与元数据
   - 工具：get_figma_data(fileKey=lXOwmixlbhaJZWc4w2pk1s, nodeId=1:1220)
   - 输出：docs/figma/raw.json（仅存元数据，便于审阅与变更追踪）
2) 生成设计 Tokens 映射草稿
   - 输出：docs/figma/token-draft.md
   - 内容：颜色/字体/间距/圆角/阴影 → 对应 tokens/base/* 与 tokens/components/* 的落地建议，附前端表现说明（如“色板-主色-500：用于按钮主态背景，深蓝”）。
3) 图标清单
   - 输出：docs/figma/icons-checklist.md（节点ID、建议命名、目标目录、是否已有同名）
4) 经批准后执行批量下载 SVG
   - 目录：packages/ui/src/icons/
   - 命名规范：kebab-case，例如 home, home-filled, chevron-left
5) 可选：新增 Storybook 文档页“Figma 基线映射”用于对照与评审

命名与目录约定
- 图标目录：packages/ui/src/icons/
  - 文件命名：kebab-case（小写，用连字符），不带尺寸/颜色后缀（由样式控制）
- Tokens 映射：
  - 基础：tokens/base/colors|typography|spacing|radius|shadows
  - 组件：tokens/components/*（将 Figma 组件属性与我们组件库属性对齐）
- 文档：docs/figma/*
  - raw.json：原始抓取结果
  - token-draft.md：映射草稿（可评审）
  - icons-checklist.md：图标抽取清单

变更影响与回滚
- 当前仅新增文档与后续草稿文件，不影响现有构建。
- 如需回滚，删除 docs/figma/* 或未采用的 SVG 资源文件即可。

进度与后续
- 阻塞点：需解决 Figma API 403（为令牌授予文件访问或更换有权限的令牌）
- 解除后将自动继续：抓取 raw.json → 产出 token-draft.md → 图标清单 → 经批准后下载 SVG → 可选 Storybook 对照页
