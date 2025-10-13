# 当前上下文与焦点
最后更新：2025-10-13

## 当前焦点（P0）
- 组件层 Design Token 落地与“按钮 Button”对齐（component.button.*）。
- 清理 Token 命名冲突（Token collisions=3），准备 Storybook 文档与灰度接入。

## 刚完成
- 新增 tokens/components/button.json：
  - 变体：primary / secondary / ghost / link
  - 尺寸：sm / md / lg（含 font-size / padding-x / padding-y）
  - 状态：default / hover / active / disabled
  - 通用：gap / icon-gap / radius / font-weight / transition / focus.ring-{color|width}
  - 全部引用基础 Token（{color.*}{font.*}{space.*}{radius.*}）
- 运行构建（Style Dictionary）：生成 Web CSS 变量（:root / [data-theme='dark']）与小程序 WXSS；tokens.css 内已包含 --component-button-*。
- packages/ui/BaseButton.vue 改为消费组件层 Token：
  - 全量替换为 --component-button-* 变量（主/次/幽灵/文本、尺寸、焦点环、过渡）
  - 新增 link 文本按钮；移除 danger 变体

## 下一步（P0）
- 为尺寸新增高度 Token：component.button.size.{sm|md|lg}.height，去除硬编码 32/40/48px。
- 清零 Token collisions（3）：使用 Style Dictionary verbose 定位并统一命名。
- 更新 BaseButton stories：补充 link 变体与尺寸演示；写迁移说明（旧变量→新变量）。
- apps/web 小范围灰度替换旧按钮，验证暗色主题与可访问性（focus-visible/对比度）。

## 重要约束
- 业务代码与组件仅消费“语义层/组件层”Token，禁止硬编码与直接使用原始层。
- 组件改动需先通过 Storybook 评审与 Chromatic 可视化回归后再合并。

## 常用命令
- 构建设计 Tokens：node scripts/build-tokens.js（或 pnpm build:tokens）
- 启动 UI Storybook：pnpm --filter @sydney-rental-hub/ui storybook
- 启动 Web：pnpm --filter @web-sydney/web dev
