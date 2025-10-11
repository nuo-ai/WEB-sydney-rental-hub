# SRH Design (Astro) — Tokens & Components 工具站点

位置：`tools/design-site-astro`（作为“工具站点”，不属于产品应用，放在 tools/ 更合理）

用途：
- 在浏览器里实时调参设计 Token（颜色、间距、字号/行高、阴影、比例等）
- 预览多种卡片状态（badges、meta 组合、长地址/价格）
- 导出 JSON 或 SCSS 以回填到小程序/WEB 项目（`apps/uni-app/src/uni.scss`）

## 正确安装与启动

工作区已在根 `pnpm-workspace.yaml` 添加了 `tools/*`，并在根 `package.json` 配置了快捷脚本。

1) 在仓库根目录安装依赖
```
pnpm install
```

2) 启动 Astro 工具站点（端口默认 4321）
- 方式 A（推荐，根脚本已配置 filter）：

pnpm astro:dev

- 方式 B（进入站点目录单独启动）：

cd tools/design-site-astro
pnpm dev


3) 访问
- 首页：http://localhost:4321
- Tokens Playground：http://localhost:4321/tokens
- Components 画廊：http://localhost:4321/components

4) 生产构建与本地预览
```
pnpm astro:build
pnpm astro:preview
```

## 使用说明

- 初始 Token 存放于：`tools/design-site-astro/public/tokens/srh.json`
- 在 `/tokens` 页面
  - 左侧面板实时调整 Token
  - 右侧卡片即时更新
  - 支持“复制 JSON”与“复制 SCSS”（回填到 `apps/uni-app/src/uni.scss` 的 `$srh-*` 变量）
- 在 `/components` 页面
  - 查看 badges（Inspection today / Added yesterday / Deposit taken / Build to Rent）
  - 不同 meta 组合（bed/bath/car/study）
  - 长地址/高价格的适配情况

## 关于 “为什么不是 tools 目录？” 与安装提醒

- 我们将 Astro 工具站点放在 `tools/` 下，因为它是“设计/开发辅助工具站点”，不属于产品应用，符合 monorepo 的分层约定（`apps/` 放产品级应用，如 web/uni-app）。
- 你执行的：
  ```
  cd apps && npm i @astrouxds/tokens
  ```
  这一步并不是在安装 Astro 框架，`@astrouxds/tokens` 是 RUX 的设计 Token 包，和 Astro 无直接关系；且在 `apps/` 目录安装容易在工作区外生成“游离”的 node_modules/ 或 package.json。

纠正方式（建议）
- 不需要在 `apps/` 目录安装任何东西。直接回到仓库根目录，执行：


 pnpm install
  pnpm astro:dev

  
- 如果你已在 `apps/` 生成了多余的 `package.json`/`node_modules` 等，请手动删除（遵循你项目的文件系统规则由你来执行），保持 `apps/` 仅包含各子应用目录。

## 与小程序/WEB 的联动

- Astro 工具站点用于“实时调参”和“导出”，不会直接影响产品样式。
- 当确定参数后：
  - 复制 SCSS 到 `apps/uni-app/src/uni.scss`（`$srh-*` 变量）
  - 构建后，小程序与 H5（通过 `:root --srh-*`）可保持一致外观

## 后续可选增强

- 扩展 Token 维度：分隔线/边框、禁用态、强调色、动画、z-index、暗色模式
- 增补组件：Badge、MetaItem、Button 的独立示例与组合场景
- 数据基线：采样 50+ 竞品卡片，计算 min/median/max 给出建议范围
