/* 
  文件职责：集中定义找房 UI 相关的 TypeScript 类型，确保组件间契约一致
  为什么：提前固化 props/事件/数据结构，便于小步快跑时保持向后兼容与可维护性
  技术权衡：本阶段以“静态交互”为主，字段尽量贴合 demo.html；后续接入后端再做增量扩展
*/

// 业务基础：地区名称（与 UI 文案一致即可，后续可接后端字典）
export type District = string

// 页面 Tab 标识（用于底部导航状态同步）
export type TabKey = 'home' | 'discover' | 'find' | 'messages' | 'account'

// 排序选项（与筛选弹层文案保持一致）
export type SortOption = '最新上架' | '最新发布' | '离我最近' | '默认排序'

// 周期文字（当前固定“每周”，保留独立类型便于未来扩展）
export type Period = '每周'

// 房源卡片数据结构（用于 PropertyCard / PropertyList）
export interface Property {
  id: string
  imageUrl: string
  price: number
  period: Period
  // 地址可能包含换行（示例：街道 + 城市/邮编），在前端用 <br /> 或样式断行
  address: string
  beds: number
  baths: number
  cars: number
  // 可入住文案（示例：“立即入住”/“11月1日”）
  availableText: string
  // 收藏本地态（后续接入账号后由后端返回）
  favorited: boolean
}

// 字母分组的地区列表，用于位置筛选 A-Z 面板
export interface DistrictGroups {
  [letter: string]: District[]
}

// 位置筛选的 v-model 结构（多选）
export interface LocationFilterModel {
  selected: District[]
}

// 价格段项（用于“价格段”单选组）
export interface PriceRange {
  label: string
  min?: number
  max?: number
}

// 综合筛选的状态（价格段与自定义输入互斥）
// 业务规则：
// - 选中“价格段”时，price 应为 { rangeKey }，自定义输入清空
// - 手动输入 min/max 时，price 应为 { min, max }，应清空段位选中
export interface FilterState {
  price:
    | { min?: number; max?: number } // 自定义输入
    | { rangeKey?: string } // 单选价格段 key（与 PriceRange.label 或内部 key 对应）
  rentTypes: string[] // ['整租','合租'] 等
  bedrooms: string[] // ['1室','2室','3室','4室','5室及以上']
  amenities: string[] // ['带家具', ...]
}
