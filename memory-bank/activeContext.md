# 当前上下文与焦点
**最后更新**：2025-10-11

## 当前焦点 (Current Focus)
- “双色系统”Design Tokens 全面落地并贯通构建与预览：
  - 品牌色与主行动色角色分离：color.brand.{primary,hover,active}、color.action.primary
  - 中性色与语义补全：background.{page,surface,hover,disabled}、text.{placeholder,disabled,on.action}、border-interactive
- 以 Astro 工具站作为本阶段唯一可视化调参与验收环境（暂不启用 Storybook）

## 刚完成的工作 (Latest)
- 主题与构建
  - 更新 tokens/themes/{light,dark}.json 为“双色系统”结构；修复 dark 主题 brand 单值导致的 29 个引用缺失
  - Style Dictionary 输出双作用域 CSS 变量：
    - :root → packages/ui/src/styles/tokens.css
    - [data-theme='dark'] → packages/ui/src/styles/tokens.dark.css
  - 构建通过（Token collisions 警告 3 项，不影响产物）
- Astro 集成与路径修正
  - 三页接入：/（导航）、/tokens（调参与导出）、/components（多状态画廊）
  - 统一导入 tokens.css / tokens.dark.css；实现 data-theme 切换（localStorage + prefers-color-scheme）
  - 修正相对路径（../../../../packages/ui/src/styles/*）
- 规范文档
  - 新增 docs/ui-design-system-v1.0.md（双色系统色彩、字体、间距、断点、集成与维护策略）

## 下一步行动 (Next · P0)
1) 组件层令牌对齐：逐步将组件引用迁移到新语义（brand/action/semantic）并移除旧别名
2) 构建告警治理：启用 verbose 定位 3 处 Token collisions，统一命名与路径
3) 可视化完善：/tokens 增加颜色色板、间距标尺、圆角/阴影示例；/components 补充 hover/active/disabled 变体
4) 导出→回填闭环：提供“导出清单 + 半自动回填 apps/uni-app/src/uni.scss”脚本（先文档化，谨慎自动写）
5) 小程序真机校验：验证字体回退、字距/行高与深色下对比度

## 重要约束 (Constraints)
- 本阶段以 Astro 为设计系统验证环境；Storybook 暂不启用，避免多环境复杂度
- 小程序不支持运行时 setProperty，统一采用静态构建；H5 端支持 --srh-* 运行时调参

## 相关命令 (Ops)
- 构建 Tokens：pnpm run build:tokens
- 启动 Astro 工具站：pnpm --filter @srh/design-site-astro dev（端口占用自动切换）
- 访问：/、/tokens、/components（按钮“切换暗色”验证主题）
