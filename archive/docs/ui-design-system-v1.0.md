# Sydney Rental Hub UI 设计系统基础规范 V1.0

> [!ARCHIVED]
> 本文档描述的是早期（橙色品牌）版本的 token 结构，已与当前蓝色主题实现不符，仅保留做历史参考。

## 1. 设计哲学

本规范旨在为 Sydney Rental Hub 提供一套统一、高效、可扩展的 UI 设计语言。其核心是设计令牌 (Design Tokens)，通过将设计决策（如颜色、间距、字体）抽象为可复用的变量，确保产品在不同平台和功能模块间保持高度的视觉一致性，并极大提升开发与迭代效率。

---

## 2. 色彩 (Color)

我们的色彩系统采用双色分离策略，明确区分品牌色 (Brand Color) 与主行动色 (Primary Action Color)，并完整支持亮色 (Light Mode) 与暗色 (Dark Mode) 主题。

- 品牌色: 用于彰显品牌身份、装饰性元素和特定营销场景。
- 主行动色: 用于驱动用户操作，如按钮、链接、表单控件等。
- 中性色: 构成界面的骨架，用于背景、表面、文字和边框。
- 语义色: 用于状态反馈（成功、警告、错误）。

说明
- 本规范中的 CSS 变量名与当前构建产物对齐：
  - 品牌主色变量为 --color-brand-primary（而非 --color-brand）
  - 主行动色为 --color-action-primary
  - 其他变量与构建产物保持一致（如 --color-background-page、--color-text-primary、--color-border）

### 色彩令牌 (Color Tokens)

```css
/* =============================================
   亮色主题 (默认)
   ============================================= */
:root {
  /* 品牌色 (Identity) */
  --color-brand-primary: #F28C00; /* juwo 橙色 (建议值) */

  /* 主行动色 (Action) */
  --color-action-primary: #0066FF;

  /* 语义色 (Semantic) */
  --color-success: #0F8A07;
  --color-warning: #F2BD00;
  --color-error: #ED1245;

  /* 中性色 - 背景 (Background) */
  --color-background-page: #F7F7F8;        /* 页面最底层背景 */
  --color-background-surface: #FFFFFF;      /* 卡片、输入框等表面背景 */
  --color-background-hover: #F2F2F3;        /* 列表项等悬停背景 */
  --color-background-disabled: #EDEEF0;     /* 禁用状态背景 */

  /* 中性色 - 文字 (Text) */
  --color-text-primary: #1D2129;         /* 主要文字 */
  --color-text-secondary: #65676B;       /* 次要文字 */
  --color-text-on-action: #FFFFFF;       /* 在行动色背景上的文字 */
  --color-text-placeholder: #A0A3A8;     /* 占位符文字 */
  --color-text-disabled: #A0A3A8;        /* 禁用状态文字 */

  /* 中性色 - 边框 (Border) */
  --color-border: #D8D8D9;
  --color-border-interactive: #A0A3A8; /* 可交互元素的边框 */
}

/* =============================================
   暗色主题
   ============================================= */
[data-theme='dark'] {
  /* 品牌色 (Identity) */
  --color-brand-primary: #F29E2E; /* 提升亮度以适应暗色背景 */

  /* 主行动色 (Action) */
  --color-action-primary: #409CFF;

  /* 语义色 (Semantic) */
  --color-success: #18D39E;
  --color-warning: #FFE900;
  --color-error: #FF4D79;

  /* 中性色 - 背景 (Background) */
  --color-background-page: #121212;
  --color-background-surface: #1E1E1E;
  --color-background-hover: #2C2C2C;
  --color-background-disabled: #3A3B3C;

  /* 中性色 - 文字 (Text) */
  --color-text-primary: #E4E6EB;
  --color-text-secondary: #B0B3B8;
  --color-text-on-action: #FFFFFF;
  --color-text-placeholder: #65676B;
  --color-text-disabled: #65676B;

  /* 中性色 - 边框 (Border) */
  --color-border: #464853;
  --color-border-interactive: #65676B;
}
```

---

## 3. 字体 (Typography)

字体系统基于 16px 的基础字号和 1.25 的比例系数 (Major Third) 建立，以创造富有韵律感和清晰层级的文本。所有单位均使用 rem 以保证无障碍性。

### 字体令牌 (Typography Tokens)

| Token Name          | Value (rem) | Equivalent (px) | 用途建议            |
| :------------------ | :---------- | :-------------- | :------------------ |
| `--font-size-xs`    | `0.75rem`   | `12px`          | 极小辅助文字、标签    |
| `--font-size-sm`    | `0.875rem`  | `14px`          | 辅助文字、说明        |
| `--font-size-base`  | `1rem`      | `16px`          | 正文 (Body)          |
| `--font-size-lg`    | `1.25rem`   | `20px`          | 小标题 (H4)          |
| `--font-size-xl`    | `1.563rem`  | `25px`          | 次标题 (H3)          |
| `--font-size-2xl`   | `1.953rem`  | `31px`          | 主标题 (H2)          |
| `--font-size-3xl`   | `2.441rem`  | `39px`          | 一级大标题 (H1)      |

| Token Name              | Value | 用途       |
| :---------------------- | :---- | :--------- |
| `--font-weight-regular` | `400` | 常规字重   |
| `--font-weight-bold`    | `700` | 加粗字重   |

说明
- 代码层 tokens（font.size.*、font.weight.*、font.lineHeight.*）已在 base/token 中定义；上表为产品级通用规范，代码引用以 tokens 构建产物为准。

### 字体栈 (Font Family)

为确保在不同操作系统上获得最佳显示效果，请使用以下字体栈。英文字体在前，中文字体在后。

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
}
```

### 行高 (Line Height)

- 英文/数字: 行高建议设置为字号的 1.5 倍 (`line-height: 1.5;`)
- 中文: 为保证阅读舒适性，行高建议设置为字号的 1.7 倍 (`line-height: 1.7;`)

---

## 4. 间距 (Spacing)

间距系统基于 8px 的基础单位，所有 margin、padding、gap 都应使用以下令牌，以确保布局的节奏感和一致性。

### 间距令牌 (Spacing Tokens)

| Token Name      | Value (rem) | Equivalent (px) |
| :-------------- | :---------- | :-------------- |
| `--spacing-1`   | `0.25rem`   | `4px`           |
| `--spacing-2`   | `0.5rem`    | `8px`           |
| `--spacing-3`   | `0.75rem`   | `12px`          |
| `--spacing-4`   | `1rem`      | `16px`          |
| `--spacing-5`   | `1.25rem`   | `20px`          |
| `--spacing-6`   | `1.5rem`    | `24px`          |
| `--spacing-8`   | `2rem`      | `32px`          |
| `--spacing-10`  | `2.5rem`    | `40px`          |
| `--spacing-12`  | `3rem`      | `48px`          |
| `--spacing-16`  | `4rem`      | `64px`          |

说明
- 代码层 tokens 使用 `space.xs/sm/md/lg/...`；上表为产品级语义分度，使用时可在样式层做映射。

---

## 5. 布局 (Layout)

为适应不同设备，我们采用响应式设计，并定义以下标准断点。

### 断点令牌 (Breakpoint Tokens)

| Token Name        | Min-Width | 目标设备范围     |
| :---------------- | :-------- | :--------------- |
| `--breakpoint-sm` | `640px`   | 手机（横屏）     |
| `--breakpoint-md` | `768px`   | 平板             |
| `--breakpoint-lg` | `1024px`  | 小屏幕桌面       |
| `--breakpoint-xl` | `1280px`  | 标准/大屏幕桌面  |

### 其他令牌

| Token Name               | Value | 用途                            |
| :----------------------- | :---- | :------------------------------ |
| `--border-radius-sm`     | `4px` | 小圆角，用于标签、Tag 等        |
| `--border-radius-md`     | `8px` | 中等圆角，用于按钮、输入框、卡片 |
| `--border-width-default` | `1px` | 默认边框宽度                    |

---

## 6. 实施与集成

构建与产物
- 运行构建（会生成 CSS 变量文件，含亮/暗主题作用域）
  - `pnpm run build:tokens`
  - 产物：
    - `packages/ui/src/styles/tokens.css`（选择器 `:root`）
    - `packages/ui/src/styles/tokens.dark.css`（选择器 `[data-theme='dark']`）

Astro 集成与主题切换
- 在 Astro 页面顶部导入：
  - `import '../../../packages/ui/src/styles/tokens.css'`
  - `import '../../../packages/ui/src/styles/tokens.dark.css'`
- 使用 data-theme 切换暗色：
  - 设为暗色：`document.documentElement.setAttribute('data-theme', 'dark')`
  - 设为浅色：`document.documentElement.removeAttribute('data-theme')`

本地预览（仅 Astro，不使用 Storybook）
- 启动：`pnpm --filter @srh/design-site-astro dev`
- 访问：http://localhost:4321
- 首页、/tokens、/components 均已接入并支持暗色切换

---

## 7. 维护策略与命名规范（摘要）

- 色彩采用“双色系统”：`--color-brand-primary` 与 `--color-action-primary` 角色分离。
- 主题差异通过 `[data-theme='dark']` 覆盖，不直接在组件层面硬编码颜色。
- 基础令牌命名（代码层）：
  - 颜色：`color.brand.primary`、`color.action.primary`、`color.semantic.*`
  - 字体：`font.size.*`、`font.weight.*`、`font.lineHeight.*`
  - 间距：`space.*`，圆角：`radius.*`，阴影：`shadow.*`
- CSS 变量（运行时层）采用 `--color-*`、`--spacing-*`、`--font-size-*` 等形式映射。
