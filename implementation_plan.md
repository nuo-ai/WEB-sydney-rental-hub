# Implementation Plan

[Overview]
将 docs/temp/demo.html 的移动端找房 UI 自上而下拆解为一组可复用的 Vue 3 组件（atoms/molecules/organisms/pages），复用现有 shadcn-vue 基础组件与 Tailwind 体系，先实现静态交互与本地状态，后续再接入真实数据与鉴权。

本次工作聚焦于：
- 统一移动端容器（≤420px）和分层（Header/Content/BottomSheet/TabBar）。
- 拆分并实现：Header+FilterBar、PropertyCard/List、BottomTabBar、三个底部弹层（位置/排序/筛选）。
- 封装通用 BottomSheet 容器，覆盖遮罩、拖动/关闭、内容滚动等交互。
- 定义 TypeScript 类型，明确 props/事件/联动规则，保证后续可接后端 API。
采用“小步快跑+向后兼容”的策略：一次只动 1–2 个文件，先保证 demo 同款 UI 行为闭环，再逐步对接数据。

[Types]
本次仅新增前端类型，统一在 apps/vue-juwo/src/types/ui.ts 中维护，便于跨组件复用与升级。

详细类型定义
- 基础数据结构
  - export type District = string
  - export interface Property {
      id: string
      imageUrl: string
      price: number
      period: '每周'
      address: string      // 可包含换行
      beds: number
      baths: number
      cars: number
      availableText: string
      favorited: boolean
    }
  - export type SortOption = '最新上架' | '最新发布' | '离我最近' | '默认排序'
  - export type TabKey = 'home' | 'discover' | 'find' | 'messages' | 'account'

- 位置筛选
  - export interface DistrictGroups { [letter: string]: District[] }
  - export interface LocationFilterModel {
      selected: District[]   // 多选
    }

- 价格/筛选
  - export interface PriceRange { label: string; min?: number; max?: number }
  - export interface FilterState {
      price:
        | { min?: number; max?: number }   // 手动输入
        | { rangeKey?: string }            // 选择段位
      rentTypes: string[]                  // ['整租','合租']
      bedrooms: string[]                   // ['1室','2室','3室','4室','5室及以上']
      amenities: string[]                  // ['带家具', ...]
    }

- 组件间事件（约定）
  - BottomSheet：open/close 由父组件控制，子组件内部仅 emit('close') 通知父级
  - TagGroup：v-model（update:modelValue）
  - SortModal：v-model 单选（update:modelValue）
  - LocationFilterModal：v-model 选区（update:modelValue），并提供 confirm/clear
  - FilterModal：emit('apply', FilterState) / emit('clear')

[Files]
新增组件与页面文件；尽量不修改或删除现有文件，仅按需复用/组合。

- 新增文件（路径与用途）
  - apps/vue-juwo/src/types/ui.ts
    - 存放本文定义的全部类型
  - apps/vue-juwo/src/components/base/BaseButton.vue
    - 对 shadcn Button 的轻封装，统一 variant/size/icon 插槽
  - apps/vue-juwo/src/components/base/BaseIcon.vue
    - 图标封装（优先 lucide-vue-next），支持 name/size/color
  - apps/vue-juwo/src/components/base/BaseTag.vue
    - 标签/Chip 组件，支持 selected/disabled，供筛选与已选展示
  - apps/vue-juwo/src/components/base/BaseBadge.vue
    - 圆角计数角标，供“已选数量”显示
  - apps/vue-juwo/src/components/base/BaseInputNumber.vue
    - 数字输入（最小/最大），用于价格输入
  - apps/vue-juwo/src/components/base/BaseAvatar.vue
    - 头像组件（用于“我的”页）

  - apps/vue-juwo/src/components/molecules/FilterButton.vue
    - 单个筛选入口按钮（label/icon/active）
  - apps/vue-juwo/src/components/molecules/PriceBar.vue
    - 价格+周期显示
  - apps/vue-juwo/src/components/molecules/SpecsList.vue
    - 卧室/浴室/车位三元组
  - apps/vue-juwo/src/components/molecules/MenuItem.vue
    - “我的”页菜单项（文案+chevron）
  - apps/vue-juwo/src/components/molecules/TagGroup.vue
    - 单选/多选标签组（mode:'single'|'multiple'）

  - apps/vue-juwo/src/components/organisms/AppHeader.vue
    - 头部：城市 + FilterBar（位置/排序/筛选）
  - apps/vue-juwo/src/components/organisms/FilterBar.vue
    - 三个 FilterButton 排列，转发点击事件
  - apps/vue-juwo/src/components/organisms/PropertyCard.vue
    - 单个房源卡片：图片/价格/收藏/地址/规格/可入住
  - apps/vue-juwo/src/components/organisms/PropertyList.vue
    - 卡片列表，props: items: Property[]
  - apps/vue-juwo/src/components/organisms/BottomTabBar.vue
    - 底部导航：五个 Tab，props: active:TabKey；emit('change', TabKey)
  - apps/vue-juwo/src/components/organisms/BottomSheet.vue
    - 通用底部弹层容器（基于 shadcn Sheet/Dialog 定制）
  - apps/vue-juwo/src/components/organisms/LocationFilterModal.vue
    - 位置筛选组合：已选/热门/A-Z 列表/字母索引/清除/确定
  - apps/vue-juwo/src/components/organisms/SortModal.vue
    - 排序单选
  - apps/vue-juwo/src/components/organisms/FilterModal.vue
    - 价格段+自定义输入、出租方式、户型、配套
  - apps/vue-juwo/src/components/organisms/DistrictPanels.vue
    - 按字母分组的区域列表 + 热门分区
  - apps/vue-juwo/src/components/organisms/AlphabetIndex.vue
    - 右侧 A-Z 索引，emit('jump', letter)
  - apps/vue-juwo/src/components/organisms/SelectedTags.vue
    - 已选区域 Tag 列表，支持移除

  - apps/vue-juwo/src/views/FindPropertyPage.vue
    - 找房页拼装（Header/List/BottomSheets/TabBar）
  - apps/vue-juwo/src/views/MyAccountPage.vue
    - “我的”页占位，头像/昵称/积分/菜单

- 可能修改的现有文件（不删除）
  - apps/vue-juwo/src/views/ListingsView.vue
    - 若已存在房源页，可迁移为 FindPropertyPage（保留旧文件避免破坏）
  - apps/vue-juwo/src/components/ui/*.vue
    - 继续复用 shadcn Button/Card/Sheet 等，按需微调样式类名（不改 API）

- 配置文件
  - Tailwind 配色通过 apps/vue-juwo/tailwind.config.js 扩展 theme.extend.colors.primary 等
  - 无需改动 Vite/TS 配置；如引入 lucide-vue-next，仅添加依赖

[Functions]
新增以 UI 纯函数为主，便于复用与测试；函数集中在 apps/vue-juwo/src/utils/ui.ts。

- 新增函数
  - formatPrice(price:number): string
    - 目的：以 $xxx 形式展示周租金
  - groupDistricts(districts:string[]): DistrictGroups
    - 目的：按首字母分组，用于 A-Z 滚动面板
  - scrollToLetter(container:HTMLElement, letterAnchor:HTMLElement): void
    - 目的：点击索引滚到对应分组
  - isRangeSelected(FilterState): boolean
    - 目的：判断当前是否处于“价格段”选择模式

- 组件内事件（示例签名）
  - PropertyCard.vue
    - emits: 'toggle-favorite' (id:string), 'more-actions' (id:string)
  - SortModal.vue
    - v-model: modelValue: SortOption
  - LocationFilterModal.vue
    - v-model: modelValue: District[]
    - emits: 'confirm' (District[]), 'clear' ()
  - FilterModal.vue
    - emits: 'apply' (FilterState), 'clear' ()

- 修改/移除函数
  - 无（本阶段仅新增，不移除现有逻辑）

[Classes]
本阶段不新增/修改类（Vue 3 组合式/单文件组件为主），该章节记录为空以保持计划模板完整性。

- New classes: N/A
- Modified classes: N/A
- Removed classes: N/A

[Dependencies]
依赖变更最小化；优先复用现有 shadcn-vue/Tailwind。

- 新增（如未存在）
  - lucide-vue-next：图标库（按需引入）
- 版本或配置变更
  - 无强制；如安装 lucide-vue-next，按官方文档在组件内直接 import 图标使用

[Testing]
采用“可视验收 + 轻量单元/组件测试”的混合策略。

- 手工/视觉验收（关键路径）
  - 弹层开/关：遮罩点击关闭、确定/清除关闭；弹层高度与滚动不遮挡 Header/TabBar
  - 位置选择：热门与列表双向联动；Badge 计数正确；清除后计数隐藏
  - 价格段与输入框：任一修改能正确联动与互斥
  - 卡片收藏：本地选中态切换，多个卡片互不影响
  - Tab 切换：活跃态高亮；切换页面不遗留弹层
- 组件测试（Vitest + Vue Test Utils，选做）
  - TagGroup：single/multiple 行为
  - SortModal：默认恢复逻辑
  - FilterModal：价格段与输入框联动
  - BottomSheet：遮罩点击/emit('close') 行为

[Implementation Order]
从底层容器到页面拼装，按最小风险路径推进。

1. BottomSheet 通用容器（organisms/BottomSheet.vue）
2. AppHeader + FilterBar + 三按钮事件骨架
3. LocationFilterModal（含热门/A-Z/已选/清除/确定）
4. SortModal（单选 + 默认恢复）
5. FilterModal（价格段/输入框联动 + 其它组）
6. PropertyCard + PropertyList（样式与交互）
7. FindPropertyPage 拼装 + BottomTabBar + MyAccount 占位
8. 主题变量与样式统一（Tailwind 扩展/全局 CSS vars）

附：Plan Document Navigation Commands
- Read Overview section
  sed -n '/\\[Overview\\]/,/\\[Types\\]/p' implementation_plan.md | cat
- Read Types section
  sed -n '/\\[Types\\]/,/\\[Files\\]/p' implementation_plan.md | cat
- Read Files section
  sed -n '/\\[Files\\]/,/\\[Functions\\]/p' implementation_plan.md | cat
- Read Functions section
  sed -n '/\\[Functions\\]/,/\\[Classes\\]/p' implementation_plan.md | cat
- Read Classes section
  sed -n '/\\[Classes\\]/,/\\[Dependencies\\]/p' implementation_plan.md | cat
- Read Dependencies section
  sed -n '/\\[Dependencies\\]/,/\\[Testing\\]/p' implementation_plan.md | cat
- Read Testing section
  sed -n '/\\[Testing\\]/,/\\[Implementation Order\\]/p' implementation_plan.md | cat
- Read Implementation Order section
  sed -n '/\\[Implementation Order\\]/,$p' implementation_plan.md | cat
