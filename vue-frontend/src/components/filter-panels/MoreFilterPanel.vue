<template>
  <div class="more-filter-panel">
    <!-- 面板头部 -->
    <div class="panel-header">
      <h3 class="panel-title chinese-text sr-only">{{ moreLabel }}</h3>
      <button class="close-btn" tabindex="-1" @click="$emit('close')" aria-label="关闭更多筛选面板">
        <svg class="spec-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
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



      <!-- 底部操作按钮 -->
      <div class="panel-footer">
        <button class="link-clear" type="button" aria-label="清除更多筛选条件" @click="clearAll">清除</button>
        <el-button type="primary" class="apply-btn" size="default" :loading="countLoading" :disabled="countLoading" @click="apply">
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
const applyText = computed(() => (typeof previewCount.value === 'number' ? `应用（${previewCount.value}）` : '应用'))
const srLiveText = computed(() => (typeof previewCount.value === 'number' ? `可用结果 ${previewCount.value} 条` : ''))

/* 构建参数（仅 isFurnished） */
const buildFilterParams = () => {
  const p = {}
  // 中文注释：当未勾选时用 undefined 显式清除草稿中的 isFurnished，避免遗留影响预览
  p.isFurnished = furnished.value === true ? true : undefined
  return p
}

/* 计数：将草稿覆盖到当前已应用条件（保障必要关联） */
const computePreviewCount = async () => {
  try {
    countLoading.value = true
    const draft = buildFilterParams()
    // 中文注释：将“更多”面板草稿合并进全局预览草稿，统一由 Store 计算预览计数
    propertiesStore.updatePreviewDraft('more', draft)
    const n = await propertiesStore.getPreviewCount()
    previewCount.value = Number.isFinite(n) ? n : 0
  } catch (e) {
    previewCount.value = null
    console.warn('获取更多筛选预估数量失败', e)
  } finally {
    countLoading.value = false
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
  // 中文注释：清理“更多”分组的全局草稿，避免残留影响其它面板的预览口径
  propertiesStore.clearPreviewDraft('more')
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
    await propertiesStore.applyFilters(filterParams)
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
  background: #fff;
  border-radius: 8px;
}

/* 头部 */
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid var(--color-border-default);
}
.panel-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}
.close-btn {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.close-btn:hover {
  background: #f5f5f5;
  color: var(--color-text-primary);
}
.spec-icon {
  width: 20px;
  height: 20px;
}

/* 内容 */
.panel-content {
  padding: 16px;
}
.form-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}
.form-label {
  font-size: 13px;
  color: var(--color-text-secondary);
}

/* 底部操作 */
.panel-footer {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}
.cancel-btn {
  flex: 1;
  background: white;
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
}
.apply-btn:hover {
  background-color: var(--juwo-primary-light);
  border-color: var(--juwo-primary-light);
}

/* 细节 */
.w-full { width: 100%; }

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

/* 清除按钮样式（与其他面板一致） */
.link-clear {
  background: transparent;
  border: none;
  color: var(--color-text-secondary);
  text-decoration: underline;
  cursor: pointer;
  padding: 0;
  margin-right: auto;
}
.link-clear:hover {
  color: var(--color-text-primary);
}
</style>
