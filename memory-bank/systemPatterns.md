# 系统设计模式与最佳实践

---

## 设计系统与主题

- **双色主题**: Style Dictionary 输出 `:root` 与 `[data-theme='dark']` 两套变量，组件通过语义层 Token 自动适配主题。 
- **令牌分层**: 坚持“原始 → 语义 → 组件”三级结构；业务代码只允许消费语义层或组件层。 
  - 组件层命名示例：component.button.*（variants: primary/secondary/ghost/link；sizes: sm/md/lg；states: default/hover/active/disabled）
  - 组件只在组件层取值；页面可用语义层
- **Storybook 为事实来源**: 设计规范与组件使用说明全部记录在 Storybook 8.6.x 内的 MDX 与 stories 中。任何组件改动必须同时更新 Storybook。
- **Astro 站角色**: 设计 Token 工具站用于预览与调参，不承载组件开发职责。
- **Tailwind v4 约束**: 使用 `@tailwindcss/postcss`，禁用 `preflight`；`darkMode` 采用 `['class','[data-theme="dark"]']`；`colors/font/radius/spacing` 映射到核心变量（`hsl(var(--…))`、`var(--font-sans)`、`var(--radius)`）。
- **Element Plus 桥接模式**: 通过 `el-theme-bridge.css` 将核心变量映射到 `--el-color-primary`、`--el-text-color-*`、`--el-bg-color`、`--el-border-color`、`--el-border-radius-base`、`--el-font-family` 等；优先让 EP 继承统一视觉，减少逐组件覆写。
- **可访问性焦点环**: 统一使用 `--ring` 驱动的 `focus-visible` 外观（Tailwind `ring-*` 与 CSS `hsl(var(--ring) / α)` 组合），确保亮/暗模式对比度满足 WCAG AA。

---

## Monorepo 原则

- 使用 `pnpm` + `Turborepo` 统筹所有应用与包。新增项目需在 `pnpm-workspace.yaml` 中登记，并在 `turbo.json` 中定义缓存/依赖关系。 
- 根 `package.json` 提供统一脚本；请优先通过 `pnpm <script>` 而非直接调用子包二进制，以便复用 Turbo 缓存。 
- 共享代码应沉淀到 `packages/*`，业务应用避免彼此直接引用源文件。

---

## 组件开发模式

- **提取流程**: 在业务应用中发现的基础 UI 优先抽离到 `packages/ui`，补充 Storybook stories 与单元测试，再通过工作区引用。 
- **样式约束**: 
  - 组件仅消费组件层 Token（component.*），页面可用语义层；禁止直接消费原始层 
  - 禁止硬编码颜色/间距/字号等数值；必须使用 Design Token。 
  - CSS 自定义属性不得提供 `var(--token, #fff)` 形式的兜底值，以防止绕过暗色主题。 
- **可访问性**: 使用 `@storybook/addon-a11y` 校验组件无障碍问题，并在业务代码中继承同样的语义标签/ARIA 属性。

---

## 数据与服务模式

- **前端数据流**: Vue + Pinia 作为单一数据源；组件只通过 action 修改状态，禁止直接写入 store state。 
- **API 契约**: 后端 FastAPI 提供 REST 接口，响应结构统一 `{ status, data, error, pagination }`。前端通过 axios 拦截器处理错误与鉴权。 
- **缓存策略**: Redis/内存缓存 15 分钟过期，用于加速热门筛选；前端在必要时进行请求去抖。 

---

## 测试与质量

- **单元测试**: Vitest 3.x 运行在各包的 `test` 目标中；组件测试应覆盖主要交互状态。 
- **端到端**: Playwright 用于 URL 幂等和关键用户路径验证，可通过 `pnpm --filter @web-sydney/web exec npx playwright test` 运行。 
- **视觉基线**: Chromatic 连接 Storybook 构建，任何视觉差异需在 PR 中审核并手动批准。 
- **Lint 约束**: ESLint + Stylelint 强制校验代码与样式规范，CI 中会阻断不合规提交。

---

## 运行时守则

- Turborepo 的缓存依赖 Git 状态，提交前务必 `pnpm lint && pnpm test` 确保缓存未产生陈旧产物。 
- Storybook 8.6.x 依赖与 Vite 插件版本耦合度高，升级时先在 `apps/web` 与 `packages/ui` 分支验证兼容性，再合并到主分支。
- 删除或新增 Token 后必须运行 `pnpm build:tokens` 并同步更新 Storybook/文档站截图，避免不同端出现视觉漂移。

---

## MCP 集成模式（Smithery 托管 · Cline）

- 适用场景：在 Cline 中新增第三方 MCP Server（如 shadcn-vue-mcp），用于增强组件生成/质量检查等能力。
- 首选传输：使用 `type: "streamableHttp"`（HTTP 流式），稳定且免本地进程管理。
- 配置路径（优先级从上到下）：
  1) VSCode 远端存储（当前环境）：`/home/nuoai/.vscode-server/data/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
  2) 备用（本地）：`~/.cline/mcp_config.json`
- 标准配置示例（Smithery 托管 URL，勿暴露敏感值）：
  ```json
  {
    "mcpServers": {
      "shadcn-vue-mcp": {
        "autoApprove": [],
        "disabled": false,
        "timeout": 60,
        "type": "streamableHttp",
        "url": "https://server.smithery.ai/@HelloGGX/shadcn-vue-mcp/mcp?api_key=***&profile=***"
      }
    }
  }
  ```
- 成功要点：
  - 使用字段 `type`，而非 `transport`；值为 `"streamableHttp"`。
  - URL 不可包含 HTML 转义（`&`），应为原始 `&`。
  - 保存后在 Cline MCP 面板点击 Reconnect，或重载 VSCode 窗口以生效。
- 备选（WSL/stdio 桥接，Windows/WSL 环境适用）：
  ```json
  {
    "mcpServers": {
      "shadcn-vue-mcp": {
        "command": "wsl",
        "args": [
          "npx","-y","@smithery/cli@latest","run",
          "@HelloGGX/shadcn-vue-mcp","--key","***"
        ],
        "type": "stdio",
        "timeout": 60,
        "disabled": false,
        "autoApprove": []
      }
    }
  }
  ```
- 回滚与安全：
  - 回滚：将该条目 `disabled: true` 或直接删除；建议保留 `.bak` 备份以便恢复。
  - 安全：安装完成后在 Smithery 控制台轮换/撤销 `api_key`，任何配置与日志中均使用占位符 `***`。

---

## 前端新应用（apps/web-shadcn）模式

- 战略：与 legacy apps/web 完全解耦，在并行子应用中以 Vite + Vue 3 + TypeScript + Tailwind v4 + shadcn-vue 纯净栈重建页面。
- 组件获取：优先使用 shadcn-vue CLI 按需添加组件（Button、Card、Avatar、Badge、Input、Textarea、Separator、Alert、Skeleton、Dialog、Carousel、Sonner）。
- 样式与主题：
  - Tailwind v4 搭配 `@tailwindcss/vite` 插件；`src/style.css` 仅 `@import "tailwindcss"`。
  - 颜色基色使用 Zinc；图标统一 `lucide-vue-next`；Markdown 渲染使用 `markdown-it`。
- 渐进替换策略（与 legacy 对齐）：
  - 图片区域：静态 `<img>` → `Carousel`（轮播与指示点）→ `Dialog`（大图预览）。
  - 提示体系：ElementPlus 的 `ElMessage/Alert/Skeleton` → `Sonner/Alert/Skeleton`。
  - 规格行与分隔：`Card + Separator` 组合替代自定义样式。
  - 描述正文：`markdown-it` 渲染 + Typography（Tailwind）。
  - 地图/添加日历：第三方/自研（非 shadcn），与 UI 解耦。
- 工作流与质量：
  - 小步补丁（replace_in_file 优先），每次只改 1–2 个区域；保持可回滚。
  - 先完成 P0（Toast/Loading/预览/骨架/错误）再进行 P1（Markdown/地图/日历）。
  - 仅消费语义/组件层 Token；禁止硬编码数值；遵守可访问性与焦点环规范。

---

## 新增原则（2025-10-15 增补）

### 1) 像素复刻“蓝图法”
- 不一定需要先画原型图；对标现有网页时，直接做“多断点测量 → 复刻蓝图（结构+度量） → Tokens 落表 → 叠图验收”更高效。
- 蓝图产物：
  - blueprint-raw.json（结构/文案/模块分区）
  - tokens-suggestion.json（colors/radius/shadows/spacing/typography/layout）
  - 断点截图（1440/1024/390）用于视觉回归与叠图
- 合规边界：仅抓“度量与指标”，不保存受版权保护资产（图片/字体/Logo/文案）。

### 2) 有头/无头 80/20 组合
- 80% 通用组件使用“有头 shadcn”（速度快、可访问性稳、一致性高）。
- 20% 高度定制模块（Gallery 缩略条、Sticky CTA、Map Overlay、Floorplan Zoom 等）使用“无头/半无头”以获得像素级可控性。

### 3) TS alias 与声明约定
- 保证 `tsconfig.app.json` 可见：
  - `compilerOptions.baseUrl="."` 与 `paths["@/*"]=["./src/*"]`（避免 vue-tsc -b 引用失败）
  - `include` 至少包含：`"src/env.d.ts"`, `"src/**/*.d.ts"`, `"src/**/*.vue"`, `"src/**/*.ts?(x)"`
- 新建 `src/env.d.ts`：
  ```ts
  /// <reference types="vite/client" />
  declare module '*.vue' {
    import type { DefineComponent } from 'vue'
    const component: DefineComponent<{}, {}, any>
    export default component
  }
  ```
- 第三方库类型：
  - 若无 @types，临时在 env.d.ts `declare module 'xxx'`，后续优先安装官方类型包。

### 4) 蓝图采集执行模式（chrome-mcp · 2025-10-15 增补）
- 断点规范：1440 / 1024 / 390；DPR=2；stabilizationDelayMs=1500；仅采集“度量与指标”，不保存受版权保护资产。
- 选择器发现：优先使用 data-testid 与语义关键词（gallery/summary/price/cta/feature 等），通过 `chrome_get_interactive_elements` 辅助定位。
- 截图策略：
  - 元素截图优先：`chrome_screenshot` + `selector`，`savePng=true`，`storeBase64=false`，减少仓库膨胀与配额风险。
  - 全页截图：受 `MAX_CAPTURE_VISIBLE_TAB_CALLS_PER_SECOND` 限流，需分步、间隔重试；失败时以元素截图为准。
  - 文件落点：默认保存到系统 Downloads（浏览器下载目录）；如需入库，按文件系统规则由人工移动至 `docs/blueprints/domain/<slug>/...`，再将 JSON 中绝对路径改为相对路径。
- 抽取策略（占位 → 回填）：
  - 先写“可靠度量”（如容器 width/height、三断点截图路径）；其余字段（padding/radius/shadow/typography/spacing/button 样式）统一置 `null`，避免错误数据入库。
  - 回填路径A（自动）：定点采集 `window.getComputedStyle(el)` 的关键属性，通过唯一 console 标记/可见节点输出抓取；回填后覆盖 `null`。
  - 回填路径B（半自动）：对照三档 PNG 截图人工核对，逐项回填，确保“参数不遗漏”。
- 模块产物约定：`docs/blueprints/domain/<slug>/modules/<module>.json`
  - 内容包含 `selectors.hint/detected/primaryContainer`、`screenshots.{1440,1024,390}`、`measurements/*`、`styles/*`、`notes/nextActions`。
- 风险与回滚：
  - CSP/扩展隔离可能导致脚本注入与 computedStyle 抽取不稳定；发生时立即切换“截图 + 半自动回填”。
  - 始终优先 replace_in_file 小步补丁；严禁一次性大改与写入不确定值。
