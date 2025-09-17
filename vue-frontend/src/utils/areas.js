// 区域实体规范化工具（为什么需要这个文件）
// - 解决“刷新后顶部 Chips 与下方列表不同步”的根因：两套 id 体系（后端 raw.id vs 前端生成的 id）并存
// - 统一规范：任何进入前端状态/组件对比用到的区域对象，都必须先 canonicalize（规范化）
// - 规范后的 id 规则固定：suburb_${name} / postcode_${code}，确保跨数据源/刷新后一致
//
// 设计权衡：
// - 保留后端原始字段（通过 ...raw 回拷），如 postcode 节点的 suburbs 聚合，供“邮编 → 多个 suburb”映射使用
// - 只覆盖前端需要稳定的关键字段：id/type/name/postcode/fullName
//
// 用法：
// import { canonicalizeArea, canonicalIdOf, isSameArea } from '@/utils/areas'
// const a = canonicalizeArea(raw)               // 统一 id/type/展示名
// const id = canonicalIdOf(rawOrNormalized)     // 任意对象一律取规范 id
// isSameArea(a, b)                              // 按规范 id 判断是否同一实体

/**
 * 规范化一个区域对象，生成稳定的 id/type/name/postcode/fullName
 * @param {any} raw 可能来自后端接口/回退推导/URL 恢复的原始对象
 * @returns {object} 规范化后的对象（保留其余原始字段）
 */
export function canonicalizeArea(raw) {
  if (!raw) return null

  // 提取 suburb 名称（优先级按常见字段）
  const name =
    (typeof raw.name === 'string' && raw.name.trim()) ||
    (typeof raw.suburb === 'string' && raw.suburb.trim()) ||
    (typeof raw.label === 'string' && raw.label.trim()) ||
    ''

  // 提取 postcode（转为 4 位字符串；部分数据可能是小数或 number）
  let postcode = null
  if (raw.postcode != null) {
    try {
      postcode = String(Math.floor(raw.postcode)).trim()
    } catch {
      postcode = String(raw.postcode).trim()
    }
  } else if (raw.code != null) {
    postcode = String(raw.code).trim()
  } else if (raw.postcode_str != null) {
    postcode = String(raw.postcode_str).trim()
  }

  // 判定类型：
  // - 若原始就声明了 'postcode'，直接按邮编处理
  // - 否则只要能识别出 4 位纯数字的邮编且没有更强的 suburb 线索，就按 suburb 处理（UI 仅展示 suburb）
  const isPostcode =
    String(raw.type).toLowerCase() === 'postcode' ||
    (!!postcode && /^\d{4}$/.test(postcode) && (!name || /^\d{4}$/.test(name)))

  const type = isPostcode ? 'postcode' : 'suburb'

  // 生成规范 id
  const safeName = (name || '').trim()
  const safePostcode = (postcode || '').trim()
  const id = type === 'postcode' ? `postcode_${safePostcode}` : `suburb_${safeName}`

  // 生成展示名（fullName）
  const fullName =
    type === 'postcode'
      ? safePostcode
      : safePostcode
        ? `${safeName} NSW ${safePostcode}`
        : safeName

  // 返回时保留原始字段，覆盖关键字段为规范值
  return {
    ...raw,
    id,
    type,
    name: type === 'postcode' ? safePostcode || safeName : safeName,
    postcode: safePostcode || '',
    fullName,
  }
}

/**
 * 获取对象的规范 id（容错：即使传入 raw，也会先做规范化）
 * @param {any} a
 * @returns {string}
 */
export function canonicalIdOf(a) {
  if (!a) return ''
  if (a.id && typeof a.id === 'string' && /^((suburb|postcode)_)/.test(a.id)) {
    return a.id
  }
  const c = canonicalizeArea(a)
  return c ? c.id : ''
}

/**
 * 判断两个区域是否为同一实体（按规范 id 比较）
 * @param {any} a
 * @param {any} b
 * @returns {boolean}
 */
export function isSameArea(a, b) {
  return canonicalIdOf(a) === canonicalIdOf(b)
}
