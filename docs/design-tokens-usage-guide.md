# SRH Design Tokens 使用说明（About & Onboarding）

面向对象：
- 新加入的前端/全栈工程师、设计系统贡献者、微信小程序和 Web（Vue3）开发同学
你将学到：
- Token 的来源、目录结构、构建产物、在 Web/Vue3 与小程序中的具体使用方式
- 主题切换、单位转换（px→rpx）规则、命名规范、常见问题与贡献指南

---

## 1. 核心概念

- 源 Token（平台无关）
  - 存放在 `tokens/base/`, `tokens/components/`, `tokens/themes/` 目录
  - 描述颜色/字号/间距/圆角/阴影/语义色等，不包含平台信息
- 平台产物（平台相关）
  - 由构建脚本从“源 Token”生成不同平台可消费的文件
  - Web（Vue3）使用 CSS 变量，微信小程序使用 WXSS + `rpx` 尺寸

目录总览：
- 源数据
  - tokens/base/**/*.json
  - tokens/components/**/*.json
  - tokens/themes/light.json, tokens/themes/dark.json
- 构建脚本
  - scripts/build-tokens.js
- 平台产物（构建后生成）
  - Web（Vue3）：packages/ui/src/styles/tokens.css, tokens.dark.css
  - 小程序：apps/mini-program/src/styles/generated/light.wxss, dark.wxss

---

## 2. 如何构建

- 使用 pnpm（Monorepo 标准方式）：
  - pnpm run build:tokens
  - pnpm run build:tokens:watch
- 其他包管理器（如需本地替代）：
  - npm run build:tokens
  - yarn build:tokens
- 使用 Turbo（可选，配合 pipeline 统一调度）：
  - turbo run build:tokens

构建日志中会显示已处理主题、生成文件列表与耗时。

---

## 3. 平台产物与使用方式

### 3.1 Web（Vue3）

产物文件：
- packages/ui/src/styles/tokens.css（浅色）
  - 顶层选择器是 `:root`
- packages/ui/src/styles/tokens.dark.css（深色）
  - 顶层选择器是 `[data-theme='dark']`

在应用中引入（任选其一场景）：
- 在应用入口（如 main.ts）或全局样式（如 src/styles/main.css）中引入：
  - import 'packages/ui/src/styles/tokens.css'
  - import 'packages/ui/src/styles/tokens.dark.css'
- 或在 index.html 通过 `<link>` 方式引入构建后的 CSS 文件（按你的打包策略调整路径）

使用 CSS 变量：
- 任意 CSS 中使用：`color: var(--color-text-primary);`
- 间距、圆角、阴影：`padding: var(--space-md); border-radius: var(--radius-md); box-shadow: var(--shadow-md);`

切换暗色主题（运行时）：
- 在根节点（如 `<html>` 或 `<body>`）添加/移除 `data-theme="dark"`
- 示例（伪代码）：
  - document.documentElement.setAttribute('data-theme', 'dark') // 开启暗色
  - document.documentElement.removeAttribute('data-theme') // 切回浅色

注意：
- Web 侧不做 px→rpx 转换，保持 CSS 变量原样输出
- tokens.dark.css 只覆盖暗色相关变量，浅色变量在 tokens.css 的 `:root` 中定义

### 3.2 微信小程序（WXSS）

产物文件：
- apps/mini-program/src/styles/generated/light.wxss
  - 顶层选择器是 `.light-theme`
- apps/mini-program/src/styles/generated/dark.wxss
  - 顶层选择器是 `.dark-theme`

在小程序中引入：
- 在 app.wxss 或页面 wxss 文件中 `@import` 上述产物（根据你的工程结构调整相对路径）
  - @import "src/styles/generated/light.wxss";
  - @import "src/styles/generated/dark.wxss";

启用主题：
- 在根节点容器（如页面根节点）切换类名
  - 浅色：`<view class="light-theme">...</view>`
  - 深色：`<view class="dark-theme">...</view>`

使用 CSS 变量（微信小程序支持）：
- color: var(--color-text-primary);
- padding: var(--space-md);
- border-radius: var(--radius-md);

单位与数值转换规则（构建时自动处理）：
- px→rpx 转换（仅以下类型且值以 px 结尾时转换）：
  - dimension、sizing、spacing、borderRadius、fontSizes
  - 例：16px → 32rpx（转换比率 1px:2rpx）
- line-height（若以 px 结尾）：转换为纯数值（去单位）
- font-weight（若以 px 结尾的异常写法）：转换为数值（建议后续统一使用数值如 400/500/600）

---

## 4. 命名规范与变量形态

命名转换：
- Style Dictionary 使用 `attribute/cti` + `name/kebab`：
  - color.brand.primary → `--color-brand-primary`
  - color.semantic.text.primary → `--color-semantic-text-primary`
  - radius.md → `--radius-md`
  - shadow.md → `--shadow-md`

变量使用形态：
- Web（Vue3）：CSS 变量，`var(--xxx)`；主题通过 `:root` / `[data-theme='dark']` 控制
- 小程序：CSS 变量，`var(--xxx)`；主题通过 `.light-theme` / `.dark-theme` 控制；尺寸单位大多为 `rpx`

---

## 5. 组件映射（给设计/组件开发的桥接）

文件：`tokens/component-mapping.json`

作用：
- 记录组件 UI 与 Token 的绑定关系，帮助你快速在 token 与组件样式之间定位
示例：
- PropertyCard 使用：
  - color.semantic.bg.primary → 卡片背景色
  - shadow.md → 卡片阴影
  - radius.lg → 卡片圆角
  - color.semantic.text.primary → 标题/价格文字颜色
  - color.semantic.text.secondary → 地址/次要信息文字颜色
- PrimaryButton 使用：
  - color.brand.primary / color.brand.hover → 背景/悬停
  - color.semantic.text.inverse → 文字颜色
  - radius.md / font.weight.medium / font.size.md → 圆角/字重/字号

---

## 6. 常见问题（FAQ）

Q1：为什么看不出哪些是 Vue3 用的、哪些是小程序用的？
- 答：区分标准在“产物”而非“源 Token”。`tokens/*.json` 是平台无关的源；生成物才区分：
  - Web：packages/ui/src/styles/tokens.css / tokens.dark.css（`var(--xxx)`、`:root`、`[data-theme='dark']`）
  - 小程序：apps/mini-program/src/styles/generated/*.wxss（`.light-theme`、`.dark-theme`、`rpx`）

Q2：小程序端为什么是 rpx？
- 答：为了适配小程序生态，构建阶段会把尺寸类 px 转换为 rpx（仅特定类型、且值为 px 时）

Q3：字体行高/字重为什么会转为数值？
- 答：行高使用数值有助于跨平台一致；字重本应是数值（400/500/600），历史或错误写法若写成 “px”，构建会转成数字。建议后续在源 Token 中规范为数值。

Q4：如何切换暗色？
- Web：给根节点添加/移除 `data-theme="dark"`
- 小程序：切换容器类名 `.dark-theme` / `.light-theme`

Q5：我新增了 Token，但页面没有变化？
- 答：新增/修改 Token 后需要重新构建（见第 2 节）；同时确认已正确引入产物文件并在样式中通过 `var(--xxx)` 使用

---

## 7. 贡献指南（如何新增/修改 Token）

1) 在 `tokens/base/` 或 `tokens/components/` 中新增/修改相应 JSON（遵循现有结构与命名）
2) 单位：
   - Web 端保持 px（或语义变量），不要直接写 rpx
   - 小程序端 rpx 由构建自动生成
3) 语义优先：优先使用 `color.semantic.*` 等语义 Token，避免在组件中直接使用原子色值
4) 运行构建脚本，确认产物生成成功（见第 2 节）
5) 在组件样式中通过 `var(--xxx)` 消费变量；必要时在 `tokens/component-mapping.json` 中补充映射说明
6) 提交前建议预览 Web/小程序端效果是否一致（以 UI/语义为准）

---

## 8. 最小实践样例

Web（Vue3）：
```css
/* 已引入 tokens.css & tokens.dark.css */
.card {
  background: var(--color-background-surface);
  color: var(--color-text-primary);
  padding: var(--space-md);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
}
```
切换暗色：
```ts
// 切换
document.documentElement.setAttribute('data-theme', 'dark');
// 还原
document.documentElement.removeAttribute('data-theme');
```

小程序（WXSS）：
```css
/* app.wxss 或页面 wxss */
@import "src/styles/generated/light.wxss";
@import "src/styles/generated/dark.wxss";

/* 根容器根据需要使用 .light-theme 或 .dark-theme */
.page {
  background: var(--color-background-surface);
  color: var(--color-text-primary);
  padding: var(--space-md);       /* rpx 尺寸已自动转换 */
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
}
```

---

## 9. 速查对照表

| 场景        | 产物文件路径                                              | 主题选择器             | 变量形态         | 尺寸单位 |
|-------------|-----------------------------------------------------------|------------------------|------------------|----------|
| Web（Vue3） | packages/ui/src/styles/tokens.css / tokens.dark.css       | :root / [data-theme='dark'] | var(--xxx)       | px       |
| 小程序      | apps/mini-program/src/styles/generated/light.wxss / dark.wxss | .light-theme / .dark-theme | var(--xxx)       | rpx（构建自动转换） |

---

## 10. 文件头部注释说明（已内置）

- WXSS 产物（*.wxss）：在构建时生成带有“使用说明”的头部注释（如何引入、主题类名、单位转换规则）
- Web CSS 产物（tokens.css / tokens.dark.css）：构建完成后自动追加“Web 使用说明”的头部注释

---

如需进一步增强：
- 在 `packages/ui/src/styles/` 与 `apps/mini-program/src/styles/generated/` 放置 README.md，指向本指南
- 在 CI 中增加一次构建校验（确保新 Token 不破坏构建）
- 在 `tokens/component-mapping.json` 中逐步完善关键组件与 Token 的映射注释
