<template>
  <div class="more-filter-panel">
    <!-- 面板头部 -->
    <div class="panel-header">
      <h3 class="panel-title chinese-text sr-only">{{ moreLabel }}</h3>
      <button class="close-btn" tabindex="-1" @click="$emit('close')" aria-label="关闭更多筛选面板">
        <svg
          class="spec-icon"
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          aria-hidden="true"
        >
          <path
            d="M18 6 6 18M6 6l12 12"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </button>
    </div>

    <!-- 面板内容 -->
    <div class="panel-content">
      <!-- 是否带家具 -->
      <div class="form-row">
        <el-checkbox v-model="furnished">
          {{ furnishedLabel }}
        </el-checkbox>
      </div>

      <!-- 底部操作按钮（对齐“区域”面板样式） -->
      <div class="panel-footer">
        <BaseButton variant="ghost" size="small" @click="clearAll">清除</BaseButton>
        <el-button class="cancel-btn" size="default" @click="$emit('close')">
          取消
        </el-button>
        <el-button
          type="primary"
          class="apply-btn"
          size="default"
          @click="apply"
        >
          {{ applyText }}
        </el-button>
        <span class="sr-only" aria-live="polite">{{ srLiveText }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { sanitizeQueryParams, isSameQuery } from '@/utils/query'
import { usePropertiesStore } from '@/stores/properties'
import { BaseButton } from '@sydney-rental-hub/ui'
import { useFilterPreviewCount } from '@/composables/useFilterPreviewCount'

// 中文注释：更多（高级）筛选面板。仅在“应用”时提交到 store；与其它分离式面板一致。

const emit = defineEmits(['close'])
const router = useRouter()
const t = inject('t') || ((k) => k)

/* 本地状态（默认值：未勾选）仅保留“带家具” */
const furnished = ref(false)

/* 计数相关（应用（N）） - 使用通用 composable 统一并发/防抖/清理 */
const { previewCount, scheduleCompute, computeNow } = useFilterPreviewCount(
  'more',
  () => buildFilterParams(),
  { debounceMs: 300 },
)
const applyText = computed(() =>
  typeof previewCount.value === 'number' ? `应用（${previewCount.value}）` : '应用',
)
const srLiveText = computed(() =>
  typeof previewCount.value === 'number' ? `可用结果 ${previewCount.value} 条` : '',
)

/* 构建参数（仅 isFurnished） */
const buildFilterParams = () => {
  const p = {}
  // 中文注释：当未勾选时用 undefined 显式清除草稿中的 isFurnished，避免遗留影响预览
  p.isFurnished = furnished.value === true ? true : undefined
  return p
}

/* 监听与首算（通过 composable 防抖） */
watch(furnished, () => {
  scheduleCompute()
})
onMounted(() => {
  void computeNow()
})

/* 清除：重置并触发计数 */
const clearAll = () => {
  furnished.value = false
  // 中文注释：清理并标记该分组参与预览（即便草稿为空也删除 base 中旧键）
  propertiesStore.clearPreviewDraft('more')
  propertiesStore.markPreviewSection('more')
  scheduleCompute()
}

// i18n 文案（带回退）
const moreLabel = computed(() => {
  const v = t('filter.more')
  return v && v !== 'filter.more' ? v : '更多'
})
const furnishedLabel = computed(() => {
  const v = t('filter.furnished')
  return v && v !== 'filter.furnished' ? v : '带家具'
})

const propertiesStore = usePropertiesStore()

/* 同步 URL（仅写入非空/有效参数） */
const updateUrlQuery = async (filterParams) => {
  try {
    const currentQuery = { ...(router.currentRoute.value.query || {}) }
    const merged = { ...currentQuery }

    // 带家具：仅当为 true 时写入
    if (filterParams.isFurnished === true) {
      merged.isFurnished = '1'
    } else {
      delete merged.isFurnished
    }

    // 幂等比对（sanitize 后对比），相同则不写，避免无意义 replace 循环
    const nextQuery = sanitizeQueryParams(merged)
    const currQuery = sanitizeQueryParams(currentQuery)
    if (!isSameQuery(currQuery, nextQuery)) {
      await router.replace({ query: nextQuery })
    }
  } catch (e) {
    console.warn('同步 URL 查询参数失败（more）：', e)
  }
}

/* 应用筛选（提交到 store） */
const apply = async () => {
  try {
    const filterParams = buildFilterParams()
    await propertiesStore.applyFilters(filterParams, { sections: ['more'] })
    await updateUrlQuery(filterParams)
    // 中文注释：应用成功后清理“更多”分组的预览草稿，避免下次打开显示过期的草稿计数
    propertiesStore.clearPreviewDraft('more')
    emit('close')
  } catch (err) {
    console.error('应用更多筛选失败:', err)
  }
}
</script>

<style scoped>
.more-filter-panel {
  width: 100%;
  background: var(--panel-bg);
  border-radius: var(--panel-radius);
}

/* 头部 */
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--panel-padding);
  border-bottom: 1px solid var(--panel-header-border);
}

.panel-title {
  font-size: var(--panel-title-font-size);
  font-weight: var(--panel-title-font-weight);
  color: var(--panel-title-color);
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: var(--panel-close-color);
  cursor: pointer;
  padding: var(--panel-close-padding);
  border-radius: var(--panel-close-radius);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition-fast);
}

.close-btn:hover {
  background: var(--panel-close-hover-bg);
  color: var(--panel-close-hover-color);
}

.spec-icon {
  width: var(--panel-close-size);
  height: var(--panel-close-size);
}

/* 内容 */
.panel-content {
  padding: var(--panel-padding);
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
  margin-bottom: var(--space-lg);
}

.form-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-medium);
}

/* 底部操作 */
.panel-footer {
  display: flex;
  gap: 12px;
  margin-top: 24px;
  position: sticky;
  bottom: 0;
  background: var(--color-bg-card);
  padding-top: 12px;
  border-top: 1px solid var(--color-border-default);
  z-index: 5;
}

/* sr-only 辅助样式 */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
/* 对齐“区域”面板的按钮样式 */
.cancel-btn {
  flex: 1;
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-default);
  color: var(--color-text-secondary);
}
.cancel-btn:hover {
  border-color: var(--color-border-strong);
  color: var(--color-text-primary);
}
.apply-btn {
  flex: 2;
  background-color: var(--juwo-primary);
  border-color: var(--juwo-primary);
  transition: none !important;
}
.apply-btn:hover {
  background-color: var(--juwo-primary-light);
  border-color: var(--juwo-primary-light);
}
</style>
