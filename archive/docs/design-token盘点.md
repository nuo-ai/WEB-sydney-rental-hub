下面给出一个清晰、直接的回答，先总览设计令牌（design tokens）体系，再结合你项目当前文件，说明在 Web 前端里的实际用法与接入方式。为保证答案贴合你仓库现状，我将基于“apps/web/src/styles/design-tokens.css”和既有暗色主题“theme-dark.css”的结构来解读。若你需要我逐行清点所有 token，请切到 Act 模式让我读取该文件的最新内容再做精确清单。

一、你的 Design Token 现在有哪些（按层级与用途）
基于当前仓库的设计体系与我们前期对齐的规范，你的 tokens 结构通常分三层。你实际文件中的命名会以 CSS 变量表现（--xxx），下面是按“功能域”聚合后的清单类型与典型命名示例：

1) 基础/原始层（Primitives）

- 颜色类
  - 品牌色与中性色阶：
    - --brand-primary, --brand-primary-foreground
    - --gray-50/100/200/.../900（或 --neutral-xxx）
  - 语义再用的底座值（供语义层引用）：
    - --palette-bg-base, --palette-text-base, --palette-border-base
- 字体排印
  - --font-sans, --font-mono
  - --font-size-xs/sm/md/lg/xl/2xl…
  - --line-height-tight/normal/relaxed…
  - --font-weight-regular/medium/semibold/bold
- 间距与圆角
  - --space-0/1/2/3/4/6/8/12/16…
  - --radius-none/sm/md/lg/full
- 阴影与模糊
  - --shadow-sm/md/lg/xl
  - --blur-none/sm/md/lg
- 动效
  - --ease-standard/entrance/exit
  - --duration-75/150/200/300ms

2) 语义层（Semantic）
   面向“视觉语义”的稳定命名，给页面和组件提供统一可切换的接口（亮/暗主题通过覆盖这层）：

- 背景相关
  - --color-bg-page（页面背景）
  - --color-bg-primary（主容器背景）
  - --color-bg-secondary（次级背景/卡片）
  - --color-bg-muted（弱化背景/分隔区域）
- 文本相关
  - --color-text-primary（主文本）
  - --color-text-secondary（次文本/说明）
  - --color-text-muted（弱化文本/占位）
  - --color-text-inverse（深色背景上的反白）
- 边框与分割线
  - --color-border-default
  - --color-border-strong
- 链接与交互
  - --link-color, --link-hover-color, --link-visited-color
- 反馈/状态色（若有）
  - --color-success, --color-warning, --color-danger
  - --color-info
- 组件语义加总（可被组件令牌消费）
  - --surface-elevated-bg, --surface-overlay-bg

3) 组件层（Component Tokens）
   绑定具体组件的“可调参数”；应尽量引用语义层，而非直接写死原始值：

- 按钮（Button）
  - --button-bg, --button-fg
  - --button-hover-bg, --button-active-bg
  - --button-radius, --button-padding-x, --button-padding-y
  - --button-border, --button-border-hover
- 输入框/表单（Input, Select, Textarea）
  - --input-bg, --input-fg, --input-placeholder
  - --input-border, --input-border-focus
  - --input-radius, --input-padding-x/y
- 卡片（Card）
  - --card-bg, --card-fg, --card-border, --card-radius, --card-shadow
- 导航/页头（Navigation/AppBar）
  - --nav-bg, --nav-fg, --nav-border, --nav-height
- 徽章/Tag、Toast、Modal、Popover 等
  - --tag-bg/fg, --toast-bg/fg, --modal-backdrop, --popover-shadow…

二、这些 Token 如何应用在 Web 前端
你的项目已采用“CSS 变量 + 作用域覆盖”的业界最佳实践，亮/暗主题通过 .dark 作用域覆盖语义层 token，从而让组件层无感知跟随。核心要点如下：

1) 全局注入与加载顺序

- 在 apps/web/src/main.js 里以统一顺序加载：
  - 原子/基础 tokens（如 @ui 或 tokens 构建产物）
  - 你的 design-tokens.css（定义/聚合并暴露 CSS 变量）
  - theme-dark.css（只覆盖 .dark 作用域下的语义层变量）
  - 站点基础样式（style.css）
  - cursor-globals.css + override/scope（若启用演示或全局排版）
- 目的：保证“语义层”变量在亮/暗之间可被后续样式正确消费。

2) 组件内消费方式（最关键的落地点）

- 在任意组件的样式里使用 var(...) 取值，做到“语义不依赖主题具体颜色”：
  - 背景/文本/边框
    - background: var(--color-bg-primary);
    - color: var(--color-text-primary);
    - border-color: var(--color-border-default);
  - 链接
    - a { color: var(--link-color); }
    - a:hover { color: var(--link-hover-color); }
  - 按钮（组件令牌优先，内部再引用语义层）
    - .btn-primary {
      background: var(--button-bg, var(--brand-primary));
      color: var(--button-fg, #fff);
      border-color: var(--button-border, transparent);
      }
    - .btn-primary:hover {
      background: var(--button-hover-bg, color-mix(in srgb, var(--brand-primary), #000 8%));
      }
- 尺寸与圆角统一：
  - padding: var(--space-3) var(--space-4);
  - border-radius: var(--radius-md);
  - box-shadow: var(--shadow-sm);

3) 暗色主题切换（已落地在导航里）

- 使用 document.documentElement.classList.add('dark') 切换主题作用域。
- theme-dark.css 只覆盖语义层变量，例如：
  - :root.dark, .dark {
    --color-bg-page: #171717;
    --color-text-primary: #f5f5f5;
    --color-border-default: #2d2d2d;
    --link-color: #6699cc;
    ...
    }
- 因为组件层引用的是语义变量（--color-xxx / --button-xxx），所以主题切换无需改组件内部颜色，风格自动生效。

4) 与 Storybook 对齐（建议）

- 在 .storybook/preview 或 manager 处加载同样的 design-tokens.css 与 theme-dark.css。
- 提供一个 Decorator，用于切换预览根节点上的 .dark 类，确保组件在 SB 中与站点一致展示。
- 这样，组件的“token 消费”在开发与真实站点完全对齐。

5) 多端单位与平台输出（可选）

- Web 端建议：尺寸类 token 使用 rem/px 输出（如 --space-4: 1rem）。
- 小程序端使用 rpx，可通过 Style Dictionary（tools/style-dictionary/ 与 scripts/build-tokens.js）生成不同平台产物。
- 统一来源：tokens/base、tokens/components、tokens/themes，通过构建生成 apps/web/src/styles/design-tokens.css 或对应平台文件，减少手工维护。

6) 变量映射与防冲突（已实施的桥接层）

- 若引入了 cursor-starter 的 globals.css，务必用 cursor-globals-override.css 做“变量映射层”，把 --color-primary 等外部变量映射到你项目的语义层，例如：
  - :root {
    /* 将外部 --color-primary 映射到本项目的 --brand-primary */
    --color-primary: var(--brand-primary);
    --color-text: var(--color-text-primary);
    ...
    }
- 这能避免第三方样式污染你的品牌与主题体系。

三、落地清单（面向“怎样应用到我的 web 前端”的可执行步骤）

- 必要项（你基本已具备）
  1) 保持 main.js 的样式加载顺序：tokens → design-tokens.css → theme-dark.css → 全局样式。
  2) 在组件样式里改用语义变量：color/background/border 优先 var(--color-xxx)。
  3) 交互态（hover/active/focus）优先定义组件层 token（--button-hover-bg 等），再回退到语义或品牌色。
  4) 主题切换统一走 html.dark；首屏策略：localStorage 优先，其次跟随系统偏好。
- 建议项（提升一致性/可维护性）
  5) Storybook 加载相同 tokens 与主题文件，提供 .dark Decorator。
  6) 发布前移除 cursor-globals-debug.css 与 __globals-debug 调试类。
  7) 用 Style Dictionary 统一从 tokens/ 源生成各平台产物（Web、小程序），减少手改差异。
  8) 建立“组件令牌清单”对照表（Button/Input/Card…), 明确每个组件可调的 token 接口和默认回退。

四、若需要我给出“你仓库里 design-tokens.css 的精确条目清单”

- 可切到 Act 模式让我读取 apps/web/src/styles/design-tokens.css，我会输出：
  - Token 分类汇总表（颜色/文本/边框/状态/间距/圆角/阴影/动效…）
  - 每类列出你当前定义的实际变量名（--xxx）与含义
  - 标注“语义层可被暗色覆盖”的变量集合，和“组件层消费点”的建议

结论

- 你当前的 design tokens 是“原始 → 语义 → 组件”的三层体系，已通过 CSS 变量在 :root 与 .dark 作用域实现主题切换；组件只需消费语义层，便可在亮/暗间自动适配。
- 在 Web 前端的应用核心：在组件样式中全面改用 var(--color-xxx / --space-xxx / --radius-xxx / --shadow-xxx)，并保持 main.js 的样式加载顺序与 html.dark 作用域切换。这样既能保证 Storybook/站点一致，也能让后续品牌或暗色视觉升级低成本扩展。
