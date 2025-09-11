# 颜色令牌映射报告（第一版）

目的：将历史散落的 #hex/rgb 统一映射到全局 CSS 变量（tokens），确保“前端表现”一致，可全站联动替换。

说明：
- 本文档仅为“落点对照表”，不立即改动业务代码。
- 后续按此表逐步 replace 到 `var(--*)`，并由 Stylelint 护栏防止回退为硬编码。
- 若遇到语义未覆盖的色值，优先补充“语义令牌”，再替换引用。

---

## 一、常见文本色（Text）

| 硬编码 | 推荐令牌 | 语义说明 |
|---|---|---|
| `#333` | `var(--color-text-primary)` | 主文案 |
| `#2d2d2d`/`#2e3a4b`/`#1a1a1a`/`#111` | `var(--color-text-primary)` | 主文案（统一归并为主色） |
| `#666`/`#60606d`/`#6e7881` | `var(--color-text-secondary)` | 次级文案 |
| `#999`/`#757d8b`/`#7f8194` | `var(--text-muted)` | 弱化文案/占位/辅助说明 |

备注：`var(--color-text-primary/secondary)` 与 `var(--text-muted)` 已在 `src/style.css` 定义。

---

## 二、背景/弱底（Background/Surface）

| 硬编码 | 推荐令牌 | 语义说明 |
|---|---|---|
| `#fff` | `var(--color-bg-card)` 或 `#fff`（仅 tokens 层） | 卡片/面背景 |
| `#f7f8fa`/`#f8f9fa`/`#f0f0f0` | `var(--bg-hover)` 或 `var(--surface-3)` | 列表项 hover 或弱底（统一使用） |
| `#f5f5f5` | `var(--surface-2)` | 弱底 |
| `#f0f2f5` | `var(--surface-3)` | 较强弱底 |
| `#e8e8e8` | `var(--surface-4)` | 最强弱底（接近边界） |
| `#000` 遮罩 | `var(--overlay-dark-75)` | 统一遮罩透明度（已定义） |

备注：优先使用 `var(--bg-hover)` 表达“悬浮弱底”，其它统一映射到 `surface-*`。

---

## 三、边界线（Border/Divider）

| 硬编码 | 推荐令牌 |
|---|---|
| `#e5e5e5`/`#e3e3e3`/`#d0d3d9` | `var(--color-border-default)`（优先）或 `var(--color-border-strong)` |

备注：`--color-border-strong` 已在 `style.css` 定义（中性加深）。

---

## 四、链接/品牌蓝（Link/Brand）

| 场景 | 硬编码 | 推荐令牌 |
|---|---|---|
| 链接默认/悬浮 | `#007bff`/`#0056b3` | `var(--link-color)`/`var(--link-hover-color)` |
| 主按钮/CTA | 多种蓝（含 `#06f`） | `var(--juwo-primary)`/`var(--juwo-primary-light)` |

说明：链接与按钮分语义管理，避免相互影响。

---

## 五、语义状态（待补充令牌后替换）

| 场景 | 硬编码 | 建议新增语义令牌（将在 style.css 新增） |
|---|---|---|
| Danger/错误 | `#e4002b`/`#dc2626`/`#b91c1c` | `--semantic-danger` / `--semantic-danger-hover` |
| Warning/警告 | `#ff5722`/`#f4511e`/`#f59e0b`/`#fff3cd`/`#856404` | `--semantic-warning` / `--semantic-warning-weak` |
| Success/成功 | `#6fc168` | `--semantic-success` |
| Brand Yellow（收藏态） | `#ffd700`/`#ffed4e` | `--semantic-favorite` / `--semantic-favorite-hover` |
| 社交色（Google/Facebook） | `#ea4335`/`#1877f2` | 保留品牌色，但封装为 `--brand-google` / `--brand-facebook` |

后续会在全局 tokens 中新增上述变量（仅新增，不改现值），再逐步替换业务引用。

---

## 六、图标/描边（Icon/Stroke/Fill）

| 硬编码 | 推荐令牌 |
|---|---|
| `fill`/`stroke` 使用具色值 | `currentColor`（优先）或对应文本/品牌令牌 |
| 仅 icon-only | `currentColor`，配合外层文本色 |

---

## 七、阴影（Shadow）

| 硬编码（rgba） | 推荐令牌 |
|---|---|
| 任意 box-shadow rgba | `var(--shadow-sm/md/lg/xl)`（已统一） |

---

## 八、示例替换（片段）

- 文本：`color: #333;` → `color: var(--color-text-primary);`
- 边界：`border: 1px solid #e5e5e5;` → `border: 1px solid var(--color-border-default);`
- 背景：`background: #f5f5f5;` → `background: var(--surface-2);`
- 链接：`color: #007bff;` → `color: var(--link-color);`
- 遮罩：`background: #000; opacity: 0.95;` → `background: var(--overlay-dark-75);`
- 图标：`fill: #666;` → `fill: currentColor;` + 外层 `color: var(--color-text-secondary);`

---

## 九、替换优先级（建议分批执行）

1) 高曝光视图与组件：PropertyDetail*、SearchBar、Navigation、MarkdownContent、Auth/Email modals  
2) 基础组件与公共片段：图标/描边、边界线、空状态/占位  
3) 低频页面与长尾样式

---

## 十、配套护栏（已落地）

- Stylelint 扩大规则覆盖：对 `color/background/border/fill/stroke/box-shadow/outline` 强制 `var(--*)`（透明/继承值白名单除外）
- Page Tokens：统一页面骨架间距/左右留白/底部导航防遮挡
- 标准页面样板：`views/_PageScaffoldExample.vue` 可直接复制使用

---

若需我继续：我将先在 style.css 补充“语义状态令牌”，随后从 PropertyDetail 与 SearchBar/Navigation 开始做第一轮安全替换（单组件/单文件粒度的小步补丁）。
