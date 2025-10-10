# 当前上下文与焦点
**最后更新**：2025-10-11

## 当前焦点 (Current Focus)
- 在 Monorepo 中接入并验证 uni-app + uni-ui 子应用，形成可运行的最小实例并建立后续扩展规范。

## 刚完成的工作
- 新建子包 apps/uni-app（Vite + Vue3 + uni-app 官方模板）。
- 在子包内接入 @dcloudio/uni-ui，并安装 sass（dev）以支持样式编译。
- 在 apps/uni-app/src/pages.json 配置 easycom 规则（自动按 `^uni-(.*)` 解析到 `@dcloudio/uni-ui/lib/uni-$1/uni-$1.vue`）。
- 修改首页示例页，引入 `<uni-badge>` 并正常渲染（验证 uni-ui 生效）。
- 启动 H5 开发服务成功（Vite dev server 已运行，终端提供本地/网络访问 URL）。
- 处理安装问题：通过删除根 node_modules 并执行 `pnpm install` 与 `pnpm --filter ./apps/uni-app add @dcloudio/uni-ui`、`add -D sass` 修复 EPERM 报错。

## 重要提醒/已知告警
- Peer 依赖告警：`@vue/server-renderer` 期望 3.4.21，但当前 `vue` 为 3.5.22（不影响当前开发；后续可评估 pin 版本消警）。
- Dart Sass 提示 legacy JS API 将在 2.0 移除（信息性告警）。

## 下一步行动 (Next Actions)
1. 在 apps/uni-app 中落地基础组件基线（按钮/表单/列表等）并对接设计令牌（与现有 tokens 管道映射策略）。
2. 按平台进行构建验证（如 mp-weixin），梳理差异与条件编译策略。
3. 为子包添加最小自动化校验（lint/format/简单 e2e 或页面快照）与统一运行脚本（通过 turbo/pnpm）。
4. 记录安装/运行手册（Monorepo 场景下的 `pnpm --filter` 与 easycom 经验）至 docs。
