# 产品上下文 (Product Context)

**文档状态**: 生存文档 (Living Document)
**最后更新**: 2025-10-14（核对 apps/web 当前实现）

---

## 核心用户故事 (MVP - P0 优先级)

以 **Lucy**（海外留学生）为代表的核心用户需求：

1. **自动补全区域搜索**：SearchBar 通过 `services/places.js` 统一封装 Google Places API，开发模式下提供 mock 数据，支持邮编/郊区关键词模糊匹配并回写到筛选器。
2. **高级日期范围筛选**：FilterPanel + FilterTabs 支持日期范围、入住窗口与检查时间（Inspection）多组合筛选，提交后通过 Pinia + URL query 保持刷新幂等。
3. **比较与收藏**：房源卡片支持收藏、加入对比、发起联系；收藏、浏览历史、对比列表分别持久化到 `localStorage` 并在 `/profile`、`/compare` 回显。
4. **发起联系**：详情页 CTA 使用统一的联系流程（`handleContactProperty`），触达客服/经纪人；弹窗在登录态与游客态之间自动切换提示。
5. **回顾与发现**：Profile 视图聚合收藏与浏览历史，支持列表跳转、清空记录；Favorites 视图展示收藏夹，可直接发起联系。
6. **跨设备同步路线图**：当前仅本地持久化（localStorage），跨设备同步需依赖账号体系与后端接口，记录在路线图（progress.md）。

---

## 核心交互流程

### 主要用户路径
1. **首页** (`/`) → 区域搜索 + 日期筛选 → 房源列表实时更新，数据来自 Pinia `properties` store 并带分页/虚拟滚动（本地配置开关）。
2. **收藏触发** → 登录提示（若 `auth.testMode` 关闭则走真实流程）→ 收藏写入 store + localStorage → `/favorites` 列表同步刷新。
3. **详情页** (`/details/:id` / `/details-new/:id`) → 加载房源详情 + 记录浏览历史 → 收藏、加入对比、联系 CTA。
4. **个人中心** (`/profile`) → 查看收藏列表 + 浏览历史 → 支持跳转详情或清除记录。
5. **对比视图** (`/compare`) → 集中展示对比清单（来源于 store.compareIds）。
6. **通勤助手** (`/commute`) → 使用 Google Maps API（dev 模式提供 mock）计算通勤时间，需要登录（`meta.requiresAuth`）。

### 跨端体验
- **PC 端**：FilterTabs 提供分组入口，真正的筛选逻辑托管给 FilterPanel。
- **移动端**：直接使用全屏 FilterPanel，底部固定 CTA。
- **状态同步**：所有筛选编辑在面板点击“应用”后写入 Pinia 和 URL；刷新或分享链接可还原同一状态。

### 2025-10-07 战略更新（小程序 → App → Android）
- **平台节奏**: 先上线小程序版，验证流程后再同步到 App 与 Android，所有设计规范以小程序为基线。
- **组件与工具**: 引入 TorUI 作为跨端组件库，并确保在 VS Code 环境下可配置主题与调试。
- **Design Token 行动**: 已完成对核心组件（包括按钮、卡片、输入框、标签页、切换开关、复选框等）的设计令牌提取和文档化。为后续的UI统一实现奠定了基础。
- **MVP 业务聚焦**: 优先完成房源筛选/排序/搜索-查看-收藏-客服下单，第二阶段才扩展地铁/火车站点与帖子发布/付费通知等增强功能。

---

## 技术约束

所有实现必须遵循 systemPatterns.md 中的"API 设计与契约一致性"规范（详情端点为列表端点的超集）。
