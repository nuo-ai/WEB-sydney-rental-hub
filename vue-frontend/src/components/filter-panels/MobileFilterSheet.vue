<template>
  <!-- 严格参考 1.html 的“筛选 Modal”布局 -->
  <div class="mobile-filter-sheet">
    <!-- Header -->
    <div class="modal-header">
      <span class="title">筛选条件：</span>
      <button class="clear-button" type="button" @click="onClear">清除条件</button>
    </div>

    <!-- Content -->
    <div class="modal-content">
      <!-- 租金标签分段 -->
      <div class="filter-section">
        <h3 class="filter-section-title">租金 (AUD/周)：</h3>
        <div class="tag-group" data-selection-mode="single">
          <div
            v-for="opt in pricePresets"
            :key="opt.key"
            class="filter-tag"
            :class="{ selected: pricePreset === opt.key }"
            @click="onSelectPricePreset(opt)"
          >
            {{ opt.label }}
          </div>
        </div>
      </div>

      <!-- 自定义价格 -->
      <div class="filter-section">
        <div class="price-inputs">
          <input type="number" placeholder="最低" v-model.number="minPrice" @input="clearPricePreset" />
          <span>-</span>
          <input type="number" placeholder="最高" v-model.number="maxPrice" @input="clearPricePreset" />
        </div>
      </div>

      <!-- 出租方式（UI占位，后端暂未映射） -->
      <div class="filter-section">
        <h3 class="filter-section-title">出租方式：</h3>
        <div class="tag-group two-columns" data-selection-mode="multiple">
          <div
            v-for="opt in rentTypes"
            :key="opt"
            class="filter-tag"
            :class="{ selected: rentTypeSet.has(opt) }"
            @click="toggleRentType(opt)"
          >
            {{ opt }}
          </div>
        </div>
      </div>

      <!-- 户型（多选，但为兼容当前契约，将转换为“最少卧室数”） -->
      <div class="filter-section">
        <h3 class="filter-section-title">户型：</h3>
        <div class="tag-group" data-selection-mode="multiple">
          <div
            v-for="opt in bedroomOpts"
            :key="opt"
            class="filter-tag"
            :class="{ selected: bedroomSet.has(opt) }"
            @click="toggleBedroom(opt)"
          >
            {{ opt }}
          </div>
        </div>
      </div>

      <!-- 配套设施 -->
      <div class="filter-section">
        <h3 class="filter-section-title">配套设施：</h3>
        <div class="tag-group single-column" data-selection-mode="multiple">
          <div
            class="filter-tag"
            :class="{ selected: furnished }"
            @click="furnished = !furnished"
          >
            带家具
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="modal-footer">
      <button class="confirm-button" type="button" @click="onConfirm">确定</button>
    </div>
  </div>
</template>

<script setup>
/*
  移动端“筛选”面板（高度 85%，结构与 1.html 一致）：
  - 价格预设(单选) + 自定义价格输入
  - 出租方式(多选)：UI 占位，当前后端未接入，暂不写入参数
  - 户型(多选)：转换为“至少N室”，如选择[2室,3室] → bedrooms='3'；选择“5室及以上”→ bedrooms='5+'
  - 配套设施：带家具 → isFurnished=true
  - 点击“确定”构造参数并调用 store.applyFilters，更新 URL
*/
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'
import { sanitizeQueryParams, isSameQuery } from '@/utils/query'

const emit = defineEmits(['close'])
const router = useRouter()
const store = usePropertiesStore()

// 价格预设
const pricePresets = [
  { key: 'lt500', label: '500 以下', min: null, max: 500 },
  { key: '500-1000', label: '500-1000', min: 500, max: 1000 },
  { key: '1000-1500', label: '1000-1500', min: 1000, max: 1500 },
  { key: '1500-2000', label: '1500-2000', min: 1500, max: 2000 },
  { key: '2000-2500', label: '2000-2500', min: 2000, max: 2500 },
  { key: 'gt2500', label: '2500 以上', min: 2500, max: null },
]
const pricePreset = ref('')
const minPrice = ref(null)
const maxPrice = ref(null)
const onSelectPricePreset = (opt) => {
  if (pricePreset.value === opt.key) {
    pricePreset.value = ''
    minPrice.value = null
    maxPrice.value = null
    return
  }
  pricePreset.value = opt.key
  minPrice.value = opt.min
  maxPrice.value = opt.max
}
const clearPricePreset = () => {
  pricePreset.value = ''
}

// 出租方式（UI 仅占位）
const rentTypes = ['整租', '合租']
const rentTypeSet = ref(new Set())
const toggleRentType = (name) => {
  const next = new Set(rentTypeSet.value)
  if (next.has(name)) next.delete(name)
  else next.add(name)
  rentTypeSet.value = next
}

// 户型（多选 → 兼容映射为 bedrooms 最少值）
const bedroomOpts = ['1室', '2室', '3室', '4室', '5室及以上']
const bedroomSet = ref(new Set())
const toggleBedroom = (label) => {
  const next = new Set(bedroomSet.value)
  if (next.has(label)) next.delete(label)
  else next.add(label)
  bedroomSet.value = next
}
const bedroomsParam = computed(() => {
  if (bedroomSet.value.size === 0) return ''
  // 取“最大”选择作为下限，例如选了2和3 -> 3；选了“5室及以上” -> '5+'
  const mapVal = (s) => (s.includes('5') ? '5+' : s.replace('室', ''))
  const nums = Array.from(bedroomSet.value).map(mapVal).map((v) => (v.endsWith('+') ? 999 : Number(v)))
  const maxRaw = Math.max(...nums)
  if (maxRaw === 999) return '5+'
  return String(maxRaw)
})

// 家具
const furnished = ref(false)

// 清除
const onClear = () => {
  pricePreset.value = ''
  minPrice.value = null
  maxPrice.value = null
  rentTypeSet.value = new Set()
  bedroomSet.value = new Set()
  furnished.value = false
}

// 构造参数
const buildFilterParams = () => {
  const p = {}
  if (minPrice.value != null && minPrice.value !== '') p.price_min = Number(minPrice.value)
  if (maxPrice.value != null && maxPrice.value !== '') p.price_max = Number(maxPrice.value)
  if (bedroomsParam.value) p.bedrooms = bedroomsParam.value
  if (furnished.value === true) p.isFurnished = true
  return p
}

const updateUrlQuery = async (filterParams) => {
  try {
    const currentQuery = { ...(router.currentRoute.value.query || {}) }
    const merged = { ...currentQuery }

    // URL 同步：尽量对齐现有键
    if (filterParams.price_min != null) merged.price_min = String(filterParams.price_min)
    else delete merged.price_min
    if (filterParams.price_max != null) merged.price_max = String(filterParams.price_max)
    else delete merged.price_max
    if (filterParams.bedrooms) merged.bedrooms = String(filterParams.bedrooms)
    else delete merged.bedrooms
    if (filterParams.isFurnished === true) merged.isFurnished = '1'
    else delete merged.isFurnished

    const nextQuery = sanitizeQueryParams(merged)
    const currQuery = sanitizeQueryParams(currentQuery)
    if (!isSameQuery(currQuery, nextQuery)) {
      await router.replace({ query: nextQuery })
    }
  } catch (e) {
    console.warn('同步 URL 查询参数失败（筛选）：', e)
  }
}

const onConfirm = async () => {
  try {
    const p = buildFilterParams()
    // 合并多个分组键，显式声明影响的 sections，便于 Store 删除旧键
    await store.applyFilters(p, { sections: ['price', 'bedrooms', 'more'] })
    await updateUrlQuery(p)
    try { store.clearPreviewDraft('price'); store.clearPreviewDraft('bedrooms'); store.clearPreviewDraft('more') } catch {}
    emit('close')
  } catch (e) {
    console.error('应用筛选失败:', e)
  }
}
</script>

<style scoped>
/* 结构与 1.html 对齐 */

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  flex-shrink: 0;
}
.title {
  font-size: 16px;
  color: var(--color-text-primary);
  font-weight: 500;
}
.clear-button {
  font-size: 14px;
  color: var(--color-text-secondary);
  background: none;
  border: none;
  cursor: pointer;
}

.modal-content {
  flex: 1;
  overflow: auto;
  padding: 0 16px;
}

/* 分区 */
.filter-section { margin-bottom: 24px; }
.filter-section-title {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 12px;
  color: var(--color-text-primary);
}

/* 标签组 */
.tag-group {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}
.tag-group.single-column { grid-template-columns: 1fr; }
.tag-group.two-columns { grid-template-columns: repeat(2, 1fr); }

.filter-tag {
  padding: 12px 16px;
  background-color: var(--color-bg-secondary, #f8f9fa);
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  border: 1px solid transparent;
  transition: background-color 0.2s, color 0.2s, border-color 0.2s;
  text-align: left;
}
.filter-tag.selected {
  background-color: #e6f9f9;
  color: var(--juwo-primary);
  border-color: var(--juwo-primary);
}

/* 价格输入 */
.price-inputs {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 10px;
}
.price-inputs input {
  width: 100%;
  padding: 8px;
  border: 1px solid var(--color-border-default);
  border-radius: 6px;
  text-align: center;
  box-sizing: border-box;
}
.price-inputs span { color: var(--color-text-secondary); }

/* Footer */
.modal-footer {
  padding: 16px;
  border-top: 1px solid var(--color-border-default);
  flex-shrink: 0;
  background-color: #fff;
}
.confirm-button {
  width: 100%;
  padding: 12px;
  background-color: var(--juwo-primary);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
}
</style>
