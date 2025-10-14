# Repository Guidelines

## 项目结构与模块组织
`tokens/` 目录遵循「基础 → 主题 → 组件」三层：`base/` 定义原子尺寸、色彩、排版等中立令牌；`themes/` 以主题（如 `light.json`、`dark.json`）复用基础值并补充语义；`components/` 描述控件的语义变量，名称需与 UI 组件一致。`component-mapping.json` 记录业务组件与令牌的对应关系，便于审查消费链路。构建产物会输出到 `packages/ui/src/styles/`、`apps/mini-program/src/styles/generated/` 和 `packages/ui/dist/`，请勿手动编辑这些生成文件。

## 构建、测试与开发命令
- `pnpm build:tokens`：一次性运行 Style Dictionary，生成 Web、Mini Program 与 JSON/TS 产物。
- `pnpm build:tokens:watch`：监听 `tokens/**/*.json` 变更并增量构建，适合持续调整期间使用。
- `pnpm astro:dev`：在设计站点中实时预览令牌（依赖成功构建的 CSS 输出）。
构建日志若提示 token collision，请立刻排查命名冲突或跨主题引用是否正确。

## 代码风格与命名约定
所有源文件为 JSON，缩进固定 2 空格，键名使用小写加点号层级（例如 `space.3xl`）。`value` 优先引用已有令牌（`{color.gray.50}`），仅在新增叶子节点时填原始十六进制或像素值。`type` 字段必须与 Style Dictionary 约定匹配，如 `color`、`dimension`、`fontWeights`，缺失类型会导致在目标平台表现异常。新增组件令牌时保持与实际组件命名一致，并在 `component-mapping.json` 补充注释说明。

## 测试指南
令牌仓库无独立单元测试，构建即测试。提交前执行 `pnpm build:tokens` 确认构建成功且生成文件头部注释完好。变更影响设计站点或 UI 套件时，请在对应应用中加载新产物进行 smoke check（例如运行 Storybook 或设计站点）并留意暗色/浅色主题是否同步更新。必要时截取新旧对比截图随 PR 提交。

## 提交与 Pull Request 指南
遵循 Conventional Commits，例如 `feat(tokens):`、`fix(tokens):`、`chore(tokens-build):`。保持单一职责提交，并排除自动生成的 CSS/WXSS/TS 产物；需要展示时在 PR 中附加构建日志或差异截图。PR 描述应包含变更动机、影响范围、验证命令和设计产物引用，若涉及跨团队消费请 @ 对应负责人确认。合并前至少通过一次 `pnpm build:tokens`，并确保相关下游应用已更新引用说明。
