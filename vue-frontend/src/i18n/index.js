/**
 * 轻量 i18n 插件（无外部依赖）
 * 目的：在不引入新依赖的前提下，为项目提供 $t 文案访问能力
 * 原因：遵循“小步、向后兼容、不新增依赖”的约束；默认语言 zh-CN
 */

const MESSAGES = {
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
      anyPrice: '不限价格'
    }
  }
}

// 简单的深度取值
function get(obj, path) {
  if (!obj) return undefined
  return String(path)
    .split('.')
    .reduce((o, k) => (o != null ? o[k] : undefined), obj)
}

// 默认导出：作为 Vue 插件使用
export default {
  install(app, options = {}) {
    const locale = options.locale || 'zh-CN'
    const fallbackLocale = options.fallbackLocale || 'zh-CN'
    const messages = options.messages || MESSAGES

    // t: 读取当前 locale 的文案，失败回退到 fallback，再回退 key
    const t = (key) => {
      const val = get(messages[locale], key)
      if (val != null) return val
      const fb = get(messages[fallbackLocale], key)
      return fb != null ? fb : key
    }

    // 全局 $t，可直接在模板使用
    app.config.globalProperties.$t = t
    // 也提供注入（可在组合式 API 中 inject('t') 使用）
    app.provide('t', t)
  }
}

// 同步导出默认文案，便于后续扩展/覆盖
export { MESSAGES }
