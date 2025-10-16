/* 
  文件职责：提供找房 UI 相关的纯函数工具，避免在组件内重复实现
  为什么：将展示格式化、列表分组、滚动定位、筛选判定抽离为无副作用函数，便于测试与复用
  技术权衡：仅实现 demo 所需的最小集合，保持 API 稳定，后续可在不破坏签名的前提下增强
*/

import type { DistrictGroups, FilterState } from '../types/ui'

/**
 * 将数值价格格式化为带 $ 的字符串（千位分隔）
 * 前端表现：列表/卡片顶部显示如“$500”，大于 1000 显示“$1,200”
 */
export function formatPrice(price: number): string {
  if (Number.isNaN(price)) return '$0'
  const int = Math.max(0, Math.trunc(price))
  return `$${int.toLocaleString('en-AU')}`
}

/**
 * 按首字母分组地区列表（A-Z），用于“位置筛选”A-Z 面板
 * 业务规则：
 * - 忽略前后空白与大小写，按首字符分组
 * - 非字母开头（如符号/数字）归入 '#' 组，避免丢失
 * - 每组内部按字母序排序，整体组顺序：A-Z，最后是 '#'
 */
export function groupDistricts(districts: string[]): DistrictGroups {
  const groups: DistrictGroups = {}
  for (const raw of districts) {
    const name = (raw ?? '').trim()
    if (!name) continue
    const first = name[0]?.toUpperCase() ?? '#'
    const key = /[A-Z]/.test(first) ? first : '#'
    if (!groups[key]) groups[key] = []
    groups[key].push(name)
  }
  // 各组去重+排序，保持稳定输出
  for (const k of Object.keys(groups)) {
    const uniq = Array.from(new Set(groups[k]))
    uniq.sort((a, b) => a.localeCompare(b))
    groups[k] = uniq
  }
  return groups
}

/**
 * 将滚动容器滚动到目标锚点（用于 A-Z 右侧索引点击）
 * 前端表现：点击字母后，左侧列表滚动至对应的分组标题位置
 * 权衡：使用容器内部相对 offset 计算，避免全局窗口滚动干扰
 */
export function scrollToLetter(container: HTMLElement | null, anchor: HTMLElement | null): void {
  if (!container || !anchor) return
  const targetTop = anchor.offsetTop - container.offsetTop
  // 限制在可滚动范围内，避免超出
  const maxTop = Math.max(0, container.scrollHeight - container.clientHeight)
  const clamped = Math.min(Math.max(0, targetTop), maxTop)
  try {
    container.scrollTo({ top: clamped, behavior: 'smooth' })
  } catch {
    // 某些环境不支持 smooth；降级为瞬时滚动
    container.scrollTop = clamped
  }
}

/**
 * 判断筛选状态是否处于“价格段选择”模式（而非自定义输入）
 * 业务规则：含有 rangeKey 代表选择段位；含有 min/max 则代表自定义输入
 */
export function isRangeSelected(state: FilterState): boolean {
  return typeof (state?.price as any)?.rangeKey !== 'undefined'
}
