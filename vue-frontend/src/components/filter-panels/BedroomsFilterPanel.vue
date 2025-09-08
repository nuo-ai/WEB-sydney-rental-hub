<template>
  <div class="bedrooms-filter-panel">
    <!-- 面板头部 -->
    <div class="panel-header">
      <h3 class="panel-title chinese-text">{{ bedroomsLabel }}</h3>
      <button class="close-btn" tabindex="-1" @click="$emit('close')" aria-label="关闭卧室筛选面板">
        <svg class="spec-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>

    <!-- 面板内容 -->
    <div class="panel-content">
      <!-- 卧室数量选择 -->
      <div class="filter-buttons-group">
        <button
          v-for="option in bedroomOptions"
          :key="option.value"
          class="filter-btn"
          :class="{ active: isBedroomSelected(option.value) }"
          :aria-pressed="isBedroomSelected(option.value)"
          @click="toggleBedroom(option.value)"
        >
          {{ option.label }}
        </button>
      </div>

      <!-- 浴室 -->
      <div class="section">
        <div class="section-label chinese-text">浴室</div>
        <div class="filter-buttons-group">
          <button
            v-for="option in bathroomOptions"
            :key="option.value"
            class="filter-btn"
            :class="{ active: isBathroomSelected(option.value) }"
            :aria-pressed="isBathroomSelected(option.value)"
            @click="toggleBathroom(option.value)"
          >
            {{ option.label }}
          </button>
        </div>
      </div>

      <!-- 车位 -->
      <div class="section">
        <div class="section-label chinese-text">车位</div>
        <div class="filter-buttons-group">
          <button
            v-for="option in parkingOptions"
            :key="option.value"
            class="filter-btn"
            :class="{ active: isParkingSelected(option.value) }"
            :aria-pressed="isParkingSelected(option.value)"
            @click="toggleParking(option.value)"
          >
            {{ option.label }}
          </button>
        </div>
      </div>

      <!-- 底部操作按钮 -->
      <div class="panel-footer">
        <button type="button" class="link-clear" @click="clearAll">{{ anyLabel }}</button>
        <el-button class="cancel-btn" size="default" @click="$emit('close')">
          {{ cancelLabel }}
        </el-button>
        <el-button
          type="primary"
          class="apply-btn"
          size="default"
          :loading="countLoading"
          @click="applyFilters"
        >
          {{ applyText }}
        </el-button>
        <!-- a11y：数量变化通过 aria-live 播报 -->
        <span class="sr-only" aria-live="polite">
          {{ previewCount !== null ? ('可用结果 ' + previewCount + ' 条') : '' }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, computed, watch, onMounted } from 'vue'
import { usePropertiesStore } from '@/stores/properties'
import { useRouter } from 'vue-router'

// 中文注释：卧室筛选专用面板，拆分自原 FilterPanel

const emit = defineEmits(['close'])

// 路由：用于 URL Query 同步
const router = useRouter()

// 注入轻量 i18n（默认 zh-CN；若未提供则回退为 key）
const t = inject('t') || ((k) => k)

// 文案回退，避免显示未注册的 key
const bedroomsLabel = computed(() => {
  const v = t('filter.bedrooms')
  return v && v !== 'filter.bedrooms' ? v : '卧室'
})

const applyLabel = computed(() => {
  const v = t('filter.apply')
  return v && v !== 'filter.apply' ? v : '应用'
})
// “不限”/清空 文案
const anyLabel = computed(() => {
  const v = t('filter.any')
  return v && v !== 'filter.any' ? v : '清空'
})

const cancelLabel = computed(() => {
  const v = t('filter.cancel')
  return v && v !== 'filter.cancel' ? v : '取消'
})

// 状态管理
const propertiesStore = usePropertiesStore()

// 选项数据
const bedroomOptions = [
  // 中文注释：最少卧室数（去除 Studio，后续按需再启用）
  { value: '1', label: '1' },
  { value: '2', label: '2' },
  { value: '3', label: '3' },
  { value: '4+', label: '4+' },
]

// 浴室与车位的选项（最少 N 语义）
const bathroomOptions = [
  { value: '1', label: '1' },
  { value: '2', label: '2' },
  { value: '3+', label: '3+' },
]
const parkingOptions = [
  { value: '0', label: '0' },
  { value: '1', label: '1' },
  { value: '2+', label: '2+' },
]

// 初始值（从已应用参数恢复），兼容 V1（字符串）与 V2（*_min）
const initialBathrooms = computed(() => {
  const cur = propertiesStore.currentFilterParams || {}
  if (cur.bathrooms) return String(cur.bathrooms).split(',')
  if (cur.bathrooms_min != null) {
    const n = Number(cur.bathrooms_min)
    if (!Number.isNaN(n)) return [n >= 3 ? '3+' : String(n)]
  }
  return []
})
const initialParking = computed(() => {
  const cur = propertiesStore.currentFilterParams || {}
  if (cur.parking) return String(cur.parking).split(',')
  if (cur.parking_min != null) {
    const n = Number(cur.parking_min)
    if (!Number.isNaN(n)) return [n >= 2 ? '2+' : String(n)]
  }
  return []
})

// 从 store 中获取当前筛选状态（仅用于初始化本地状态）
const initialBedrooms = computed(() => {
  const currentFilters = propertiesStore.currentFilterParams || {}
  if (currentFilters.bedrooms) {
    return currentFilters.bedrooms.split(',')
  }
  return []
})

// 本地状态（用于保存用户选择，但不立即应用）
const localBedrooms = ref([...initialBedrooms.value])
const localBathrooms = ref([...initialBathrooms.value])
const localParking = ref([...initialParking.value])

// 结果数量预估（用于“应用（N）”）
const previewCount = ref(null)
const countLoading = ref(false)
let _countTimer = null

const applyText = computed(() => {
  if (typeof previewCount.value === 'number') {
    return `${applyLabel.value}（${previewCount.value}）`
  }
  return applyLabel.value
})

// 清空选择（不限）
const clearAll = () => {
  localBedrooms.value = []
  localBathrooms.value = []
  localParking.value = []
  // 中文注释：清理“卧室”分组的全局草稿，避免残留影响其它面板预览
  propertiesStore.clearPreviewDraft('bedrooms')
  computePreviewCount()
}

// 触发计数（防抖 300ms）
const computePreviewCount = async () => {
  try {
    countLoading.value = true
    const params = buildFilterParams()
    // 中文注释：将“卧室”面板草稿合入全局草稿，由 Store 统一计算预览计数
    propertiesStore.updatePreviewDraft('bedrooms', params)
    const n = await propertiesStore.getPreviewCount()
    previewCount.value = Number.isFinite(n) ? n : 0
  } catch (e) {
    // 中文注释：快速失败，不做本地估算
    previewCount.value = null
    console.warn('获取卧室筛选结果数失败', e)
  } finally {
    countLoading.value = false
  }
}

watch(localBedrooms, () => {
  if (_countTimer) clearTimeout(_countTimer)
  _countTimer = setTimeout(() => computePreviewCount(), 300)
})
watch(localBathrooms, () => {
  if (_countTimer) clearTimeout(_countTimer)
  _countTimer = setTimeout(() => computePreviewCount(), 300)
})
watch(localParking, () => {
  if (_countTimer) clearTimeout(_countTimer)
  _countTimer = setTimeout(() => computePreviewCount(), 300)
})

// 初次打开时计算一次
onMounted(() => {
  computePreviewCount()
})

// 判断卧室选项是否被选中
const isBedroomSelected = (value) => {
  return localBedrooms.value.includes(value)
}

// 切换卧室选择（单选逻辑）
const toggleBedroom = (value) => {
  if (localBedrooms.value.includes(value)) {
    localBedrooms.value = []
  } else {
    localBedrooms.value = [value]
  }
}

// 判断/切换 浴室
const isBathroomSelected = (value) => {
  return localBathrooms.value.includes(value)
}
const toggleBathroom = (value) => {
  if (localBathrooms.value.includes(value)) {
    localBathrooms.value = []
  } else {
    localBathrooms.value = [value]
  }
}

// 判断/切换 车位
const isParkingSelected = (value) => {
  return localParking.value.includes(value)
}
const toggleParking = (value) => {
  if (localParking.value.includes(value)) {
    localParking.value = []
  } else {
    localParking.value = [value]
  }
}

// 构建筛选参数
const buildFilterParams = () => {
  const filterParams = {}
  // 卧室数量（最少 N；'4+' → '4' 在 Store 映射层处理）
  if (localBedrooms.value.length > 0) {
    filterParams.bedrooms = localBedrooms.value.join(',')
  }
  // 浴室（最少 N；'3+' → 3 在 Store 映射层处理）
  if (localBathrooms.value.length > 0) {
    filterParams.bathrooms = localBathrooms.value.join(',')
  }
  // 车位（最少 N；'2+' → 2 在 Store 映射层处理；'0' 有效）
  if (localParking.value.length > 0) {
    filterParams.parking = localParking.value.join(',')
  }
  return filterParams
}

// 将筛选参数添加到 URL
const updateUrlQuery = async (filterParams) => {
  try {
    const currentQuery = { ...router.currentRoute.value.query }
    const newQuery = { ...currentQuery }

    // 更新卧室参数
    if (filterParams.bedrooms) {
      newQuery.bedrooms = filterParams.bedrooms
    } else {
      delete newQuery.bedrooms
    }

    // 更新浴室参数
    if (filterParams.bathrooms) {
      newQuery.bathrooms = filterParams.bathrooms
    } else {
      delete newQuery.bathrooms
    }

    // 更新车位参数
    if (filterParams.parking) {
      newQuery.parking = filterParams.parking
    } else {
      delete newQuery.parking
    }

    // 仅当查询参数发生变化时才更新 URL
    if (JSON.stringify(newQuery) !== JSON.stringify(currentQuery)) {
      await router.replace({ query: newQuery })
    }
  } catch (e) {
    console.warn('同步 URL 查询参数失败:', e)
  }
}

// 应用筛选
const applyFilters = async () => {
  try {
    const filterParams = buildFilterParams()

    // 应用筛选
    await propertiesStore.applyFilters(filterParams)

    // 更新 URL
    await updateUrlQuery(filterParams)

    // 中文注释：应用成功后清理“卧室”分组的预览草稿，防止下次打开显示过期草稿计数
    propertiesStore.clearPreviewDraft('bedrooms')

    // 关闭面板
    emit('close')
  } catch (error) {
    console.error('应用卧室筛选失败:', error)
  }
}
</script>

<style scoped>
.bedrooms-filter-panel {
  width: 100%;
  background: white;
  border-radius: 8px;
}

/* 面板头部 */
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
  display: flex;
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

/* 面板内容 */
.panel-content {
  padding: 12px; /* 压缩留白，避免内部滚动 */
}

/* 筛选按钮组 */
.filter-buttons-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px; /* 压缩间距，控制面板总高 */
}

.filter-btn {
  padding: 10px 14px;
  border: 1px solid var(--color-border-default);
  border-radius: 0;
  background: white;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 60px;
}

.filter-btn:hover {
  border-color: var(--color-border-strong);
  color: var(--color-text-primary);
  background: #f7f8fa;
}

.filter-btn.active {
  background: #ffefe9; /* 极弱浅橙，非品牌强底色 */
  border-color: var(--color-border-strong);
  color: var(--color-text-primary);
}

/* 底部操作按钮 */
.panel-footer {
  display: flex;
  gap: 8px;
  margin-top: 16px;
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

/* 小节标题 */
.section {
  margin-top: 4px;
}
.section-label {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-bottom: 8px;
}

/* 文本清空按钮（不限） */
.link-clear {
  background: transparent;
  border: none;
  color: var(--color-text-secondary);
  text-decoration: underline;
  cursor: pointer;
  padding: 0;
  margin-right: auto; /* 将清空靠左，其余按钮靠右 */
}
.link-clear:hover {
  color: var(--color-text-primary);
}

/* 屏幕阅读器可见性辅助 */
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
</style>
