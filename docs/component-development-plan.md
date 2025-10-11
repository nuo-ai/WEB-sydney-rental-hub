# 原子组件开发计划 (Atomic Component Development Plan)

## 1. 对组件清单的评估与建议

您提供的原子组件清单非常出色，分类清晰、覆盖全面，为我们的设计系统奠定了坚实的基础。我的理解与您完全一致。

在此基础上，我补充两点微小建议，供您参考：

*   **补充 `Link` (链接) 组件**: 建议将 `Link` 作为一个独立的原子组件。虽然它看起来像文本，但其交互行为（如 `hover`, `visited` 状态）和无障碍性要求（`a` 标签）与普通文本或按钮有本质区别。明确定义它，有助于保持整个系统交互的一致性。
*   **形式化 `Typography` (字体)**: 我们可以将字体样式（如 `H1`, `H2`, `Body`, `Caption` 等）也定义为一组特殊的、非交互的“原子元素”。虽然它们不是组件，但将它们的 `font-size`, `font-weight`, `line-height` 等用 Token 固化下来，是原子设计阶段至关重要的一步。

## 2. 核心工作流建议：Token-First (令牌先行)

为了确保每个组件都天生支持主题化、易于维护，并与我们的设计语言保持一致，我强烈建议采用 **"Token-First"** 的开发工作流。

**流程如下：**

1.  **定义组件级 Token**: 对于清单中的每一个组件（例如 `Button`），我们不直接写 CSS。而是先在 `tokens/components/` 目录下为其创建一个 `button.json` 文件。
2.  **声明组件角色**: 在 `button.json` 中，我们用“角色”来描述按钮的各个可配置属性。例如：
    *   `--button-primary-background-color` (主按钮背景色)
    *   `--button-primary-text-color` (主按钮文字颜色)
    *   `--button-border-radius` (按钮圆角)
    *   `--button-padding-vertical` (垂直内边距)
3.  **映射到全局 Token**: 将这些组件角色映射到我们已经定义好的全局 Token。例如：
    *   `--button-primary-background-color` 的值应为 `{color.brand.primary.value}`。
    *   `--button-border-radius` 的值应为 `{radius.md.value}`。
4.  **处理状态与变体**: 在 JSON 文件中，清晰地定义 `hover`, `active`, `disabled` 等状态，以及 `primary`, `secondary` 等变体的 Token 值。
5.  **构建**: 运行 `npm run build:tokens` 脚本。这个脚本会自动将 `button.json` 编译成 CSS 自定义属性，并注入到全局的 `tokens.css` 文件中。
6.  **开发组件**: 最后，在 Storybook 或实际项目中开发 React/Vue 组件时，组件的样式**只使用**这些刚刚生成的组件级 CSS 变量（例如 `background-color: var(--button-primary-background-color);`）。

**这样做的好处是：**
*   **彻底解耦**: 组件的实现与具体的设计值（颜色、间距）完全分离。
*   **维护性极高**: 未来需要调整所有主按钮的圆角时，只需修改 `button.json` 中一个 Token 的值并重新构建，所有按钮都会自动更新。
*   **主题化原生支持**: 因为组件 Token 引用的是全局 Token，而全局 Token 已经实现了亮/暗色主题切换，所以我们的组件天生就支持主题化。

## 3. 下一步行动计划：开发 `Button` 组件

我建议我们从清单中的第一个，也是最重要的组件——**`Button`** 开始，作为实践 "Token-First" 工作流的范例。

**具体步骤：**
1.  创建 `tokens/components/button.json` 文件。
2.  在该文件中定义 `Button` 的 `primary`, `secondary`, `tertiary`, `danger` 四种变体，以及 `default`, `hover`, `active`, `disabled` 四种状态的颜色、边框、内外边距、圆角等 Token。
3.  运行 `npm run build:tokens`。
4.  在 `packages/ui` 中创建 `Button` 组件的 Storybook 故事 (`Button.stories.jsx`)，用于开发和展示。
5.  实现 `Button` 组件的样式，确保其只使用 `var(--button-*)` 形式的 CSS 变量。

---

您是否同意以上建议，特别是 "Token-First" 的工作流和从 `Button` 组件开始的行动计划？如果同意，我将立即开始执行第一步。
