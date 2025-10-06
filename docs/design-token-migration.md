# 设计令牌迁移清单（2025-09）

本清单对比了历史文件 `src/assets/design-tokens.css` 与现行的
`src/styles/design-tokens.css`，梳理仍需关注的旧变量，并给出推荐迁移策略。
所有令牌均以 `src/styles/design-tokens.css` 作为单一事实来源。

| Legacy Token | 建议动作 | 推荐替代/备注 |
| --- | --- | --- |
| `--color-primary` | 使用语义令牌 | `--color-text-primary`（页面主文字色）|
| `--color-secondary` | 使用语义令牌 | `--color-text-secondary`（次要文字）|
| `--color-background` | 切换语义别名 | `--color-bg-page`（整页背景）|
| `--color-surface` | 切换语义别名 | `--color-bg-card`（卡片/白板背景）|
| `--color-border` | 切换语义别名 | `--color-border-default`（通用边框）|
| `--color-accent` | 废弃 | 统一改用 `--brand-primary` / `--brand-primary-hover` 等品牌色语义 |
| `--font-primary` | 替换字体栈 | `--font-system`（已包含中英文系统字体）|
| `--font-size-base` | 使用排印语义 | `--text-base`（16px）|
| `--font-weight-bold` | 已在现行文件 | 继续沿用 `--font-weight-bold` |
| `--spacing-sm` | 对齐全局间距 | `--space-sm`（8px）|
| `--spacing-md` | 对齐全局间距 | `--space-4`（16px，基于尺寸刻度）|
| `--spacing-lg` | 废弃 | `--space-6`（24px），严禁再新增 `spacing-*` 命名 |
| `--spacing-xl` | 对齐全局间距 | `--space-8`（32px）|
| `--radius-sm` / `--radius-md` / `--radius-lg` | 已在现行文件 | 继续沿用相同命名 |

> 备注：所有组件/页面样式若仍引用 `src/assets/design-tokens.css`，需改为依赖
> `src/styles/design-tokens.css`，否则将绕过全局设计系统。
