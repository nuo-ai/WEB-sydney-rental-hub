/**
 * useFilterPreviewCount
 * 统一管理“预估计数（应用N）”的逻辑：草稿合并 → 计数请求 → 并发序号守卫 → 防抖 → 卸载清理
 *
 * 为什么：
 * - 各筛选分面（价格/卧室/日期/更多/区域）存在大量重复逻辑
 * - 防止旧响应覆盖新状态（_seq 并发守卫）
 * - 组件卸载时清理 setTimeout，避免内存泄漏与残留请求
 *
 * 前端表现：
 * - 返回的 previewCount 为 number 时，显示“应用（N）/确定（N）”
 * - 为 null 时，视为“计数失败”降级，按钮文案退回“应用/确定”，并就近提示错误（由调用方决定是否提示）
 */

import { ref, onUnmounted } from 'vue'
import { usePropertiesStore } from '@/stores/properties'

/**
 * @param {string} section - 分组名（'price' | 'bedrooms' | 'availability' | 'more' | 'area' ...）
 * @param {() => Record<string, any>} buildDraftFn - 构造当前分面的草稿参数（例如 { minPrice, maxPrice }）
 * @param {{ debounceMs?: number }} options - 可选项：防抖间隔（默认 300ms）
 * @returns {{
 *   previewCount: import('vue').Ref<number|null>,
 *   loading: import('vue').Ref<boolean>,
 *   scheduleCompute: () => void,
 *   computeNow: () => Promise<void>,
 *   cleanup: () => void
 * }}
 */
export function useFilterPreviewCount(section, buildDraftFn, options = {}) {
  // 中文注释：集中存储以便统一管理
  const store = usePropertiesStore()
  const previewCount = ref(null) // number | null；null 表示“失败或不可用”
  const loading = ref(false)

  // 并发守卫与防抖
  let _seq = 0
  let _timer = null
  const debounceMs = typeof options.debounceMs === 'number' ? options.debounceMs : 300

  // 构造并提交草稿，随后请求统一预估口径
  const _compute = async () => {
    const seq = ++_seq
    try {
      loading.value = true
      const draft = (typeof buildDraftFn === 'function' ? buildDraftFn() : {}) || {}

      // 当该分面“空草稿”时，也要把 base 中旧键删除，再计算预估
      if (draft && Object.keys(draft).length > 0) {
        store.updatePreviewDraft(section, draft)
      } else {
        store.clearPreviewDraft(section)
        store.markPreviewSection(section)
      }

      const n = await store.getPreviewCount()
      if (seq === _seq) {
        previewCount.value = Number.isFinite(n) ? Number(n) : null
        loading.value = false
      }
    } catch (e) {
      // 消除 ESLint 未使用变量告警
      void e
      // 失败快速降级：不抛出到组件，交由组件用 null 执行“退回‘应用/确定’+轻量错误提示”
      if (seq === _seq) {
        previewCount.value = null
        loading.value = false
      }
      // 调试：控制台打印，生产可屏蔽
      // console.warn(`[useFilterPreviewCount] compute failed for section=${section}`, e)
    }
  }

  // 防抖触发（用于滑条/按钮快速点击）
  const scheduleCompute = () => {
    if (_timer) clearTimeout(_timer)
    _timer = setTimeout(() => {
      _timer = null
      void _compute()
    }, debounceMs)
  }

  // 立即触发（用于挂载初算/明确场景）
  const computeNow = async () => {
    if (_timer) {
      clearTimeout(_timer)
      _timer = null
    }
    await _compute()
  }

  // 组件卸载清理，避免残留定时器导致“幽灵请求”
  const cleanup = () => {
    if (_timer) {
      clearTimeout(_timer)
      _timer = null
    }
    // 不中断 in-flight 请求，由 _seq 守卫丢弃过期响应
  }

  onUnmounted(() => cleanup())

  return {
    previewCount,
    loading,
    scheduleCompute,
    computeNow,
    cleanup,
  }
}
