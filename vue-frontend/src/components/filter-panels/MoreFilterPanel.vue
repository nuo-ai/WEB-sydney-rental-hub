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
import { usePropertiesStore } from '@/stores/properties'
import BaseButton from '@/components/base/BaseButton.vue'

// 中文注释：更多（高级）筛选面板。仅在“应用”时提交到 store；与其它分离式面板一致。

const emit = defineEmits(['close'])
const router = useRouter()
const t = inject('t') || ((k) => k)

/* 本地状态（默认值：未勾选）仅保留“带家具” */
const furnished = ref(false)

/* 计数相关（应用（N）） */
const previewCount = ref(null)
const countLoading = ref(false)
let _countTimer = null
let _countSeq = 0 // 中文注释：计数请求序号，丢弃过期响应，避免“应用（N）”回退
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

/* 计数：将草稿覆盖到当前已应用条件（保障必要关联） */
const computePreviewCount = async () => {
  const seq = ++_countSeq
  try {
    countLoading.value = true
    const draft = buildFilterParams()
    // 中文注释：当“更多”分组为空（未勾选）时，也要从 base 中剔除旧键：clear → mark，再计算预览
    if (Object.keys(draft).length === 0) {
      propertiesStore.clearPreviewDraft('more')
      propertiesStore.markPreviewSection('more')
    } else {
      propertiesStore.updatePreviewDraft('more', draft)
    }
    const n = await propertiesStore.getPreviewCount()
    if (seq === _countSeq) {
      previewCount.value = Number.isFinite(n) ? n : 0
    }
  } catch (e) {
    if (seq === _countSeq) {
      previewCount.value = null
    }
    console.warn('获取更多筛选预估数量失败', e)
  } finally {
    if (seq === _countSeq) {
      countLoading.value = false
    }
  }
}

/* 监听与首算（300ms 防抖） */
watch(furnished, () => {
  if (_countTimer) clearTimeout(_countTimer)
  _countTimer = setTimeout(() => computePreviewCount(), 300)
})
onMounted(() => computePreviewCount())

/* 清除：重置并触发计数 */
const clearAll = () => {
  furnished.value = false
  // 中文注释：清理并标记该分组参与预览（即便草稿为空也删除 base 中旧键）
  propertiesStore.clearPreviewDraft('more')
  propertiesStore.markPreviewSection('more')
  if (_countTimer) clearTimeout(_countTimer)
  _countTimer = setTimeout(() => computePreviewCount(), 300)
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
    const currentQuery = { ...router.currentRoute.value.query }
    const newQuery = { ...currentQuery }

    // 带家具：仅当为 true 时写入
    if (filterParams.isFurnished === true) {
      newQuery.isFurnished = '1'
    } else {
      delete newQuery.isFurnished
    }

    // 幂等比对
    if (JSON.stringify(newQuery) !== JSON.stringify(currentQuery)) {
      await router.replace({ query: newQuery })
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
  background: var(--filter-panel-bg);
  border-radius: var(--filter-panel-radius);
}

/* 头部 */
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--filter-panel-padding);
  border-bottom: 1px solid var(--filter-panel-header-border);
}

.panel-title {
  font-size: var(--filter-panel-title-font-size);
  font-weight: var(--filter-panel-title-font-weight);
  color: var(--filter-panel-title-color);
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: var(--filter-close-btn-color);
  cursor: pointer;
  padding: var(--filter-close-btn-padding);
  border-radius: var(--filter-close-btn-radius);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: var(--filter-transition-fast);
}

.close-btn:hover {
  background: var(--filter-close-btn-hover-bg);
  color: var(--filter-close-btn-hover-color);
}

.spec-icon {
  width: var(--filter-close-btn-size);
  height: var(--filter-close-btn-size);
}

/* 内容 */
.panel-content {
  padding: var(--filter-panel-padding);
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: var(--filter-space-md);
  margin-bottom: var(--filter-space-xl);
}

.form-label {
  font-size: var(--filter-font-size-sm);
  color: var(--filter-color-text-secondary);
  font-weight: var(--filter-font-weight-medium);
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
