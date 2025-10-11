# SRH Design — Docusaurus 站点

用于维护与预览 Sydney Rental Hub 的 Design Tokens 与组件状态，对齐小程序/WEB 端视觉。

## 目录结构

```
apps/docs-site/
├─ package.json                 # Docusaurus 依赖与脚本
├─ docusaurus.config.js         # 站点配置（导航：Tokens / Components）
├─ README.md
├─ static/
│  └─ tokens/
│     └─ srh.json               # 初始 Token 数据（可编辑）
└─ src/
   ├─ pages/
   │  ├─ index.jsx              # 首页
   │  ├─ tokens.jsx             # Tokens Playground（可调参、导出）
   │  └─ components.jsx         # 多状态组件预览（cards 示例）
   └─ components/
      ├─ TokenPreview.jsx       # Token 调参与 SCSS 导出组件（React）
      └─ Card.jsx               # 通用房源卡片（示例组件）
```

## 快速开始

要求：Node.js >= 18，使用 pnpm（已在根 package.json 指定 packageManager）。

1) 安装依赖（在仓库根目录执行）
```
pnpm install
```

2) 启动文档站（在仓库根目录执行）
```
pnpm docs:dev
```
默认地址：http://localhost:3000

3) 生产构建与本地预览
```
pnpm docs:build
pnpm docs:serve
```

也可在 `apps/docs-site` 目录下单独操作：
```
pnpm start
pnpm build && pnpm serve
```

## 工作流（Token → 预览 → 导出）

- 编辑初始 Token：`apps/docs-site/static/tokens/srh.json`
- 访问 Tokens 页面：顶部导航 “Tokens Playground” 或 http://localhost:3000/tokens
- 左侧调整参数（颜色、阴影、尺寸、字号/行高、imageAspect等），右侧即时预览房源卡片
- 导出：
  - 复制 JSON：用于持久化保存或提交 PR
  - 复制 SCSS：用于回填到 `apps/uni-app/src/uni.scss` 中的 `$srh-*` 变量
- 访问 Components 页面：`/components`，查看多状态对照（不同 badges、meta 组合、地址/价格长度）

## 与小程序/WEB 联动

- uni-app 中已建立 SRH Token（SCSS）与 CSS 变量桥接：`apps/uni-app/src/uni.scss` 的 `:root --srh-*`
- 在 Docusaurus 中调参后：
  1) 若需要静态固化：复制 SCSS 片段，回填到 `apps/uni-app/src/uni.scss` 的 `$srh-*`
  2) H5 可运行时动态设置 `--srh-*`（uni-app 预览页已示例）；小程序端不支持运行时 setProperty，仅静态构建生效

## 常见问题

- 图标/资源 404：`favicon` 未提供也不影响本地开发，可后续补 `static/img/favicon.ico`
- 端口占用：`pnpm docs:dev` 默认 3000，可通过 `--port` 修改
- JSON 缓存：站点已使用 `cache: 'no-store'` 读取 tokens，刷新即可生效

## 下一步可选增强

- 增加更多 token 维度：分隔线/边框、强调色、禁用态、动画、z-index、暗色/高对比主题模板
- 扩展组件库：加入 Badge、MetaItem、Button 的独立示例与组合场景
- 数据基线：采样 50+ 竞品卡片，计算（min/median/max）并给出 token 建议范围
