/**
 * 轻量 i18n 插件（无外部依赖）
 * 目标：提供 $t 文案访问能力；默认 zh-CN；支持本地 locales/ 与内置文案合并（新增不破坏）
 */

import zhCN from './locales/zh-CN'

const BUILTIN_MESSAGES = {
  'zh-CN': {
    filter: {
      title: '筛选',
      reset: '重置筛选',
      priceSection: '价格范围 (周租, AUD)',
      bedrooms: '卧室',
      bathrooms: '浴室',
      parking: '车位',
      date: '空出日期',
      dateStart: '开始日期',
      dateEnd: '结束日期',
      to: '至',
      furniture: '家具',
      furnishedOnly: '只显示带家具的房源',
      cancel: '取消',
      showResults: '显示结果',
      anyPrice: '不限价格',
      selectRegionFirst: '请先选择区域后再筛选',
    },
    search: {
      ph: '请先输入区域或邮编，例如 ‘Ultimo’ 或 ‘2000’',
    },
  },
}

// 简单的深度取值
function get(obj, path) {
  if (!obj) return undefined
  return String(path)
    .split('.')
    .reduce((o, k) => (o != null ? o[k] : undefined), obj)
}

function isObject(val) {
  return val && typeof val === 'object' && !Array.isArray(val)
}

function formatMessage(value, params) {
  if (typeof value !== 'string') return value
  if (!params || typeof params !== 'object') return value
  return Object.keys(params).reduce((acc, key) => {
    const pattern = new RegExp(`\\{${key}\\}`, 'g')
    return acc.replace(pattern, params[key])
  }, value)
}

// 递归浅安全合并（右侧覆盖左侧），数组直接覆盖
function deepMerge(target, source) {
  const out = isObject(target) ? { ...target } : {}
  if (!isObject(source)) return out
  for (const key of Object.keys(source)) {
    const sv = source[key]
    const tv = out[key]
    if (isObject(sv) && isObject(tv)) {
      out[key] = deepMerge(tv, sv)
    } else {
      out[key] = sv
    }
  }
  return out
}

// 默认消息：内置 zh-CN 与本地 zh-CN 合并（本地优先）
const DEFAULT_MESSAGES = {
  'zh-CN': deepMerge(BUILTIN_MESSAGES['zh-CN'] || {}, zhCN || {}),
}

// 默认导出：作为 Vue 插件使用
export default {
  install(app, options = {}) {
    const locale = options.locale || 'zh-CN'
    const fallbackLocale = options.fallbackLocale || 'zh-CN'
    const userMessages = options.messages || {}

    // 克隆默认并与用户消息合并（用户 > 默认）
    const base = JSON.parse(JSON.stringify(DEFAULT_MESSAGES))
    const messages = {}
    for (const loc of new Set([...Object.keys(base), ...Object.keys(userMessages)])) {
      messages[loc] = deepMerge(base[loc] || {}, userMessages[loc] || {})
    }

    // t: 读取当前 locale 的文案，失败回退到 fallback，再回退 key
    const t = (key, params) => {
      const val = get(messages[locale], key)
      if (val != null) return formatMessage(val, params)
      const fb = get(messages[fallbackLocale], key)
      return fb != null ? formatMessage(fb, params) : key
    }

    // 全局 $t，可直接在模板使用
    app.config.globalProperties.$t = t
    // 也提供注入（可在组合式 API 中 inject('t') 使用）
    app.provide('t', t)
  },
}

// 同步导出合并后的默认文案（用于外部覆盖/调试）
export { DEFAULT_MESSAGES as MESSAGES }
