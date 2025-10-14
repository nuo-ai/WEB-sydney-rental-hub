# 项目进展与演进（精简版）

**说明**: 仅保近 30 天关键里程碑，详细过程请查看对应 commit/PR

## 近期重要里程碑（2025-10）

### Web 主题层重构：Tailwind v4 + EP 桥接（完成）
- **2025-10-14｜apps/web 统一主题**:
  - 引入 Tailwind v4（@tailwindcss/postcss，preflight=false），新增核心 HSL 变量 theme.css 与 Element Plus 桥接 el-theme-bridge.css。
  - darkMode 支持 .dark 与 [data-theme="dark"]；/globals-demo 与 /cards-demo 验证统一视觉与可访问性（focus-visible 使用 --ring）。
  - 修复从 /cards-demo 跳转详情 404：CardsDemo 预注入 store.currentProperty，详情页 onMounted fetch guard。
  - DevServer 固定在 5174 并开启 strictPort，避免 Google Maps Host 限制与端口漂移。
- **后续计划**: P0 变量收敛（卡片/详情命中项），P1 密度统一（Tailwind 间距/字号量表），P2 试点 shadcn-vue（保留 EP 复杂组件）。

### Button 组件令牌化与接入（完成）
- **2025-10-13｜组件层 Token 与组件对齐**:
  - 完成 component.button.* 定义与构建（Web CSS + WXSS）；BaseButton 改为消费 --component-button-*；新增 link，移除 danger；支持 sm/md/lg。
  - 待办：新增 size.{sm|md|lg}.height Token；清零 Style Dictionary “Token collisions(3)”（verbose 定位）。

### 原子组件样式抓取与清单修正 (进行中)
- **2025-10-11｜清单修正与数据迁移**:
  - **纠正偏差**: 废弃了不完整的旧版分析清单，并以用户提供的完整模板作为新的工作基准。
  - **数据迁移**: 将所有已测量的精确数据 (`Button`, `Input`, `Checkbox`, `Divider`) 成功填充到新清单的正确结构中，并纠正了错误推断，确保了数据的准确性。为后续系统化的数据抓取工作奠定了坚实基础。
- **2025-10-11｜第一轮数据抓取完成**:
  - **分析对象**: `realestate.com.au` 租房主页。
  - **覆盖组件**: 成功抓取 `Button` (4个变体), `Input`, `Checkbox` (2个状态), `Divider` 在 `default` 状态下的样式。
  - **成果**: 所有数据已记录在 `docs/component-analysis-checklist.md`，为 Token 定义阶段提供了基础数据。
  - **遗留问题**: 因工具限制，`:hover`, `:active` 等交互状态的样式无法自动抓取，需要手动测量。

### 双色系统 Design Tokens 与 Astro 接入（完成）
- 主题令牌：color.brand.{primary,hover,active} 与 color.action.primary；中性色/语义补全（background.*、text.*、border-interactive）
- 构建：Style Dictionary 输出 :root 与 [data-theme='dark'] 两套 CSS 变量（packages/ui/src/styles/tokens*.css），小程序 wxss 同步生成
- 工具站：三页统一引入 tokens.css/tokens.dark.css，提供 data-theme 暗色切换（localStorage + prefers-color-scheme）
- 文档：新增 docs/ui-design-system-v1.0.md，可直接对外分享
- 备注：构建有 Token collisions 警告 3 项，不影响产物，后续清零

### 可视化设计 Token 工具站（Astro）
- **2025-10-11｜Astro 工具站落地与文字系统扩展**:
  - **站点创建**: 在 `tools/design-site-astro` 新增 Astro 站点，含 `/tokens`（实时调参）、`/components`（多状态画廊）页面。
  - **文字系统 Token**: 扩展 `public/tokens/srh.json` 与 `apps/uni-app/src/uni.scss`，新增中/英文字体族、字重、字距、文本级别（XS~XL），并在 Astro 页面与 uni-app CSS 变量桥接层同步。
  - **工作区集成**: `pnpm-workspace.yaml` 纳入 `tools/*`；根 `package.json` 新增 `astro:dev/build/preview` 快捷脚本。
  - **价值**: 建立“可视化调参→导出→回填”闭环，替代 Storybook，满足“所有 Token 直观渲染”需求。

### Monorepo 下的 uni-app + uni-ui 接入
- **2025-10-11｜子应用接入与验证**:
  - **子包创建**: 新建 apps/uni-app（Vite + Vue3 + uni-app 官方模板）。
  - **组件库接入**: 安装并配置 @dcloudio/uni-ui；在 pages.json 启用 easycom 规则（`^uni-(.*)`）。
  - **验证**: 首页增加 `<uni-badge>` 并成功渲染；H5 开发服务启动（Vite）。
  - **问题处理**: 通过清理 node_modules 与 `pnpm install`、分包安装依赖修复 EPERM 报错；Sass legacy JS API 仅为信息性告警。
  
### 设计令牌提取与文档化
- **2025-10-11｜核心组件设计令牌提取完成**:
  - **工作流**: 建立并执行了从Figma组件链接到结构化令牌定义的增量式分析工作流。
  - **覆盖范围**: 成功分析了 `Button`, `Card`, `Input`, `Tabs`, `Toggle`, `Checkbox`, `SearchInput` 等十余个核心UI组件，并将其设计属性映射到 `docs/figma/token-draft.md` 草稿文件中。
  - **图标清单**: 创建并持续更新了 `docs/figma/icons-checklist.md`，为未来的图标系统自动化奠定了基础。
  - **成果**: 为整个设计系统的视觉统一和自动化实现铺平了道路。

### Storybook 实施与设计系统文档化
- **2025-10-11｜Storybook 作为“单一事实来源”成功落地**:
  - **实施**: 在 `packages/ui` 中成功初始化、配置并启动了 Storybook v8，使其成为项目设计系统和组件库的可视化文档中心。
  - **设计规范**: 在 Storybook 中创建了“设计规范 (Foundations)”部分，通过 MDX 文件可视化了颜色、排版、间距和阴影等核心设计令牌。
  - **组件 Stories**: 为 `packages/ui` 中的所有核心基础组件（Group A）以及关键业务组件 `PropertyCard` 创建了标准化的 stories，展示了其各种变体和状态。
  - **问题解决**: 解决了在 `pnpm` Monorepo 环境下启动 Storybook 的一系列依赖和脚本问题，并将最终的可靠启动命令和经验教训沉淀到了技术文档中。

### 设计系统流程与令牌体系升级
- **2025-10-11｜设计系统工作流固化**: 确立并记录了从计划、令牌、组件落地到验收的标准化前端工作流，为后续开发提供了清晰的“章法”。
- **2025-10-11｜强调色与文字系统增强**:
  - **强调色统一**: 确定使用“蓝宝石钢蓝” (`#6699cc`) 作为系统强调色，并创建了 `--accent-*` 令牌，替换了外部设计系统中的香槟金。
  - **文字系统升级**: 引入了场景化行高 (`--line-height-title/body/ui`) 和文本对比度别名 (`--text-contrast-strong/medium/weak`)，以贯彻“去强调即强调”的设计原则。
  - **试点改造**: 在 `PropertyDetail.vue` 的主 CTA 按钮和 `FilterTabs.vue` 的文本颜色中成功应用了新的令牌，验证了新体系的可行性。

### 开发环境稳定性修复
- **2025-10-10｜Storybook 构建系统修复**: 解决了一系列复杂的依赖冲突问题，包括 `storybook`, `vite`, `vitest` 的版本不一致，并通过 `pnpm overrides` 强制统一了版本。同时修复了设计令牌中的重复定义和无效引用，最终使 `@sydney-rental-hub/ui` 包的 Storybook 构建流程恢复正常。

### 核心UI组件令牌化
- **2025-10-10｜核心基础组件令牌化完成**: 对 `BaseBadge`, `BaseChip`, `BaseListItem`, `BaseSearchInput`, `BaseToggle` 进行了彻底的令牌化重构，为其补充了缺失的组件级令牌，并修复了 Storybook 中的渲染问题。此举统一了基础组件的视觉规范，为后续 UI 开发奠定了坚实基础。

### 小程序设计系统增强
- **2025-10-09｜小程序设计系统增强**: 完成了设计令牌系统的增强，添加了组件级别的令牌定义（Button, Card, Input），增强了构建脚本功能，完善了组件测试策略，并更新了 Storybook 集成支持主题切换和视口适配。｜溯源: 当前 commit

### 小程序设计令牌实现
- **2025-10-09｜小程序设计令牌自动化**: 成功配置 Style Dictionary 为小程序平台生成 WXSS 文件，实现 px 到 rpx 的自动转换，为多端设计系统奠定基础。｜溯源: 当前 commit

### 小程序组件库增强
- **2025-10-09｜小程序组件库增强**: 成功创建小程序项目结构，配置设计令牌自动化构建流程，修复单位转换问题，确保生成的 WXSS 文件符合小程序规范。｜溯源: 当前 commit

### 设计系统组件库丰富
- **2025-10-09｜设计系统组件库丰富**: 成功将 `apps/web/src/components/base/` 目录下的 7 个基础组件 (`BaseBadge`, `BaseChip`, `BaseButton`, `BaseIconButton`, `BaseListItem`, `BaseSearchInput`, `BaseToggle`) 迁移至 `@sydney-rental-hub/ui` 包，显著丰富了设计系统组件库。｜溯源: 1ce1a43

### Storybook MDX 解析错误修复
- **2025-10-09｜Storybook MDX 解析错误修复**: 修复了 Typography.mdx 文件中设计令牌变量引用错误，解决了 "Could not parse expression with acorn" 问题，确保所有组件文档能正确显示。｜溯源: 当前 commit

### Monorepo 治理与设计系统奠基
- **2025-10-09｜Monorepo 基础治理完成**: 统一 pnpm 工作流，清理多余锁文件，扩展 workspace 范围，标准化 `.env.example`，并为 Python 栈引入 `requirements.lock`。｜溯源: 45af8aa
- **2025-10-09｜设计系统脚手架搭建**: 创建 `@sydney-rental-hub/ui` 包，引入 Style Dictionary 实现 Tokens 自动化，并搭建 Storybook 组件开发环境。｜溯源: 724ce82

### 多端战略重排序
- **2025-10-07｜小程序 → App → Android 路线确立**: 决定以小程序作为设计与交互基线，验证后再扩展到 App 与 Android。
- **2025-10-07｜TorUI 评估启动**: 计划引入 TorUI 组件库，确保 VS Code 下支持主题/Design Token 定制与调试。
- **2025-10-07｜Design Token 行动计划**: 以颜色、字体、图标、标签、间距为首轮统一对象，搭建"原子组件 → 业务组件"链路，并参考 Polaris Migrator 的自动化策略。
- **2025-10-07｜MVP 功能聚焦**: 第一阶段聚焦房源筛选/排序/搜索-查看-收藏-客服下单，后续再扩展地铁/站点筛选、帖子发布、付费通知等功能。

## 近期重要里程碑（2025-09）

### 保存搜索功能完成
- **2025-09-16｜保存搜索功能**: Zillow风格弹窗，智能命名，本地存储，完整事件链路｜组件：SaveSearchModal + FilterTabs + HomeView
- **2025-09-16｜事件处理优化**: 修复事件传递断裂，添加用户反馈提示｜技术：Vue事件发射链路完整性
- **2025-09-16｜Profile 管理完成**: 已保存搜索管理（列表/重命名/删除）接入 Profile 页（SavedSearchesManager + Profile 视图）

### 筛选系统 P0 完成
- **2025-09-15｜URL 幂等与状态同步**: 应用后可直链/刷新恢复，不写空键｜溯源：17527a4..c713d9f
- **2025-09-15｜统一预估计数**: "应用（N）"与列表 total 对齐，失败降级｜溯源：e8e25d5..41b7586
- **2025-09-14｜分组边界隔离**: 跨面板不覆盖，仅更新指定分组｜溯源：fceb35f..e8e25d5
- **2025-09-14｜家具筛选语义优化**: ETL 两阶段判定，勾选"有家具"更准确｜溯源：3064c42..f288eef
- **2025-09-16｜筛选向导组件**: FilterWizard 组件开发完成，尚未接入主流程（主页仍使用 FilterPanel），将以特性开关评估接入

### 设计系统合规性冲刺
- **2025-10-05｜Storybook 基础搭建**: 接入 Vue3+Vite Storybook、注册 BaseButton/BaseChip/BaseBadge、PropertyCard、FilterPanel stories，并补充 Tokens 文档页；preview 注入 Pinia/i18n/ElementPlus 与内存 localStorage 以兼容 Chromatic
- **2025-09-12｜导航收敛**: 顶栏聚焦"搜索/收藏/AI助手/我的"｜溯源：47cab8b..125e590
- **2025-09-11｜图标系统统一**: 全站 lucide-vue-next + currentColor｜溯源：fe8f012..2a9dd4d
- **2025-09-11｜规格行变量驱动**: 列表与详情"图标+数字"尺寸间距一致｜溯源：5b7254c..25ff698
- **2025-09-10｜设计令牌护栏**: Stylelint 强制 var(--*)，禁止硬编码色｜溯源：9984dff..0b6e146
- **2025-09-10｜详情页令牌化**: 移除 Font Awesome 与硬编码色｜溯源：aaa5b8b..f201a24

### 用户体验优化
- **2025-09-12｜移动端卡片紧凑**: 高度 250→180，首屏可见更多｜溯源：008be0c..0e36a05
- **2025-09-10｜中文化与文字系统**: UI 中文化，文字节奏统一｜溯源：3e4ea72..c45d86a
- **2025-09-09｜数据同步修复**: 看房时间/空出日期与 CSV 一致｜溯源：53ff509..1b96baa
- **2025-09-08｜排序功能**: 支持价格/日期/区域/看房时间排序｜溯源：7bd269b..54ba6c1

### 性能与稳定性
- **2025-09-08｜筛选系统重构**: V1 契约稳定，V2 映射可回滚｜溯源：48bad16..bade186
- **2025-09-06｜分页参数加固**: 计数/列表彻底解耦｜溯源：commit 范围略
- **2025-09-05｜筛选体验栈**: URL 同步、错误策略、性能观测｜溯源：commit 范围略
- **2025-09-04｜通勤精度修复**: 与 Google Directions 对齐｜溯源：commit 范围略

## 历史重要节点

- **2025-01-30｜虚拟滚动优化**: DOM 节点减少 99.8%，列表加载提升 83%
- **早期｜API 响应优化**: 服务端响应从 8-10 秒降至 0.4-0.5 秒，提升 20 倍
- **早期｜数据库索引**: 筛选查询从 2.2 秒降至 0.59 秒，提升 3.7 倍
