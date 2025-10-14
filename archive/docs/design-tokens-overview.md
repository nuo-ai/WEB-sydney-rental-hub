# 设计令牌目录（Draft）

> **目的**  
> 本目录用于全程追踪颜色、字体、图标、标签、间距等核心设计令牌。内容遵循 Shopify Polaris 的结构：**类别 → Token 名称 → 说明 → 真实页面截图**，并补充交互式可视化与健康状态，确保设计与开发随时对齐。

---

## 1. 命名与文档规则

| 维度 | 规范说明 |
| --- | --- |
| Token 命名 | 统一使用 `category.intent.variant` 形式，示例：`color.primary.brand`；禁止再新增 `spacing-*`、`color-*` 等无语义命名。 |
| 描述字段 | 每个 token 必须说明“前端真实用途 + 所在界面”，帮助业务快速理解视觉影响。 |
| 截图来源 | 真实页面或 Storybook 组件，需在截图中标注 token 名称。全部截图统一存放在 `docs/image/tokens/<category>/<token>.png`。 |
| 状态标记 | 在表格中维护 “已接入 / 待迁移 / 实验中”，可视化时也需同步。 |
| 变更流程 | 任意 token 调整必须同步更新此文档、Storybook 展示、Figma / TorUI 主题；提交 PR 前需附上新的截图或交互示例链接。 |

---

## 2. 令牌分类总览

### 2.1 颜色（Colors）

| Token | 使用场景说明 | 视觉值 / 备注 | 截图 | 状态 |
| --- | --- | --- | --- | --- |
| `color.primary.brand` | 主操作按钮背景、重要引导交互 | HEX: `#0057FF` / 兼容暗色方案 | ![Primary Button](image/tokens/color/color.primary.brand.png) | 待补充 |
| `color.text.primary` | 主体文字、列表主要信息 | `var(--color-text-primary)` → #09121D | ![Typography Primary](image/tokens/color/color.text.primary.png) | 待补充 |
| `color.bg.card` | 卡片/浮层背景、筛选面板 | `var(--color-bg-card)` → #FFFFFF | ![Card Background](image/tokens/color/color.bg.card.png) | 待补充 |

> **待办**：补齐所有颜色 Token，确保每行附真实截图，并在 Storybook 中同步状态。

---

### 2.2 字体（Typography）

| Token | 使用场景说明 | 字号 / 行高 / 字重 | 截图 | 状态 |
| --- | --- | --- | --- | --- |
| `type.heading.lg` | 页面主标题（房源详情 H1） | 字号 32px / 行高 40px / Weight 600 | ![Heading Large](image/tokens/type/type.heading.lg.png) | 待补充 |
| `type.body.md` | 列表正文、筛选描述 | 16px / 24px / Weight 400 | ![Body Medium](image/tokens/type/type.body.md.png) | 待补充 |
| `type.caption.sm` | 二级信息、标签说明 | 12px / 18px / Weight 400 | ![Caption Small](image/tokens/type/type.caption.sm.png) | 待补充 |

---

### 2.3 图标（Icons）

| Token | 使用场景说明 | 尺寸 / 颜色 / 图标集 | 截图 | 状态 |
| --- | --- | --- | --- | --- |
| `icon.size.sm` | 列表指标图标（如面积、卧室数量） | 16px / `currentColor` / lucide | ![Icon Small](image/tokens/icon/icon.size.sm.png) | 待补充 |
| `icon.color.brand` | 品牌高亮图标（收藏、客服 CTA） | `var(--color.primary.brand)` | ![Icon Brand](image/tokens/icon/icon.color.brand.png) | 待补充 |
| `icon.stroke.default` | 通用描边颜色 | 1.5px / 透明度 1 | ![Icon Stroke](image/tokens/icon/icon.stroke.default.png) | 待补充 |

---

### 2.4 标签（Tags & Badges）

| Token | 使用场景说明 | 形态 | 截图 | 状态 |
| --- | --- | --- | --- | --- |
| `tag.status.available` | 房源列表“可租”状态标签 | 背景 `color.success.bg` / 字体 `type.caption.sm` / 圆角 999px | ![Tag Available](image/tokens/tag/tag.status.available.png) | 待补充 |
| `badge.featured.listing` | 首页精选房源标识 | 背景 `color.primary.brand` / 字色白 / 内边距 6×12 | ![Badge Featured](image/tokens/tag/badge.featured.listing.png) | 待补充 |
| `tag.outline.default` | 可点击标签（交通方式筛选） | 边框 `color.border.default` / 圆角 999px / 高度 32 | ![Tag Outline](image/tokens/tag/tag.outline.default.png) | 待补充 |

---

### 2.5 间距（Spacing & Layout）

| Token | 使用场景说明 | 数值 | 截图 | 状态 |
| --- | --- | --- | --- | --- |
| `space.inline.sm` | 房源卡片内元素水平间距 | 8px | ![Spacing Inline Small](image/tokens/space/space.inline.sm.png) | 待补充 |
| `space.block.md` | 模块级竖向间隔（列表段落） | 16px | ![Spacing Block Medium](image/tokens/space/space.block.md.png) | 待补充 |
| `layout.container.max` | 页面主内容最大宽度 | 1200px + 32px side padding | ![Container Layout](image/tokens/space/layout.container.max.png) | 待补充 |

---

## 3. 截图与素材管理

1. 所有截图统一放置在 `docs/image/tokens/<category>/<token>.png`。  
2. 截图需标注 token 名称，可使用 Figma 或浏览器注释工具。  
3. 建议保存 1x/2x 版本，以适配高清屏。  
4. 若 token 发生变化，替换文件并更新 Git 记录，方便差异追踪。

---

## 4. 交互式可视化（Storybook / Playground）

| 任务 | 说明 | 状态 |
| --- | --- | --- |
| `Tokens/Overview` Story | 新增 Storybook 页面，动态读取 `tokens/design-tokens.json`，按类别渲染色板、字体样式、间距可视化。 | 规划中 |
| 真实页面示例 | 在 Story 中嵌入真实页面（房源卡片、筛选面板）片段，支持 hover/active 切换，实时体现 token 效果。 | 规划中 |
| 健康状态指示 | 在 Storybook 展示“已接入 / 待迁移 / 实验中”等标签，与本表格同步。 | 规划中 |
| 自动校验脚本 | 结合 ESLint/Stylelint 或 codemod，阻止旧 token 引用，保障 Story 与文档一致。 | 规划中 |

> **补充说明**：Storybook 页面建成后，请在此处添加访问链接或命令示例，便于快速打开。

---

## 5. 更新流程与验收标准

1. **发起讨论**：涉及 token 变更时，在设计/前端同步原因与影响。  
2. **提交资料**：更新本文件表格、截图、Storybook 示例；必要时在 PR 中附差异图。  
3. **交叉验收**：设计确认视觉，前端确认落地，产品确认业务语义。  
4. **推进状态**：在表格和 Storybook 中同步更新 token 的状态标签。  
5. **记录沉淀**：重大调整需同步 Memory Bank（activeContext / progress），便于后续迭代参考。

---

## 6. 下一步清单

- [ ] 补齐所有令牌条目与真实截图。  
- [ ] 完成 `Tokens/Overview` Storybook 页面，接入可交互展示。  
- [ ] 将 TorUI 主题配置与本表格互通，保持多端一致。  
- [ ] 建立自动化校验（lint/codemod），防止旧 token 复活。  
- [ ] 每周例会检查本目录与 Storybook 是否与设计稿一致。

> 本文为 Draft，后续补齐内容后即可转为正式版本。欢迎在 PR 中持续迭代。
