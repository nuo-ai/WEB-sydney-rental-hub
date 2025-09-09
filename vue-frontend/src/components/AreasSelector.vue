<template>
  <div class="areas-selector">
    <div class="areas-header">
      <div class="search-wrapper">
        <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"/>
          <path d="m21 21-4.35-4.35"/>
        </svg>
        <input
          v-model="keyword"
          type="text"
          class="areas-search"
          :placeholder="placeholderText"
          @input="onSearch"
          aria-label="搜索区域"
        />
        <button
          v-if="keyword"
          class="clear-search-btn"
          type="button"
          @click="keyword = ''"
          aria-label="清除搜索"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 6 6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>
      <button
        class="clear-all-btn"
        type="button"
        :disabled="(selected || []).length === 0"
        @click="clearAll"
      >
        清空全部
      </button>
    </div>

    <div class="areas-body" role="listbox" aria-multiselectable="true">
      <template v-if="loading">
        <div class="loading-row">加载区域列表中…</div>
      </template>
      <template v-else-if="grouped.length === 0">
        <div class="empty-row">未找到匹配的区域</div>
      </template>
      <template v-else>
        <div
          v-for="group in grouped"
          :key="group.letter"
          class="group"
        >
          <div class="group-title" :id="`group-${group.letter}`">{{ group.letter }}</div>
          <ul class="group-list">
            <li
              v-for="a in group.items"
              :key="areaKey(a)"
              class="area-item"
              :class="{ selected: isSelected(a) }"
            >
              <label class="area-row">
                <input
                  type="checkbox"
                  class="check"
                  :checked="isSelected(a)"
                  @change="() => toggle(a)"
                  :aria-label="`选择 ${displayName(a)}`"
                />
                <span class="area-name">{{ displayName(a) }}</span>
              </label>
            </li>
          </ul>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
// 中文注释（为什么）：
// - 将“区域目录”封装为独立组件，负责 A→Z 分组、多选、清空，并在变更时请求父级更新计数（不应用）。
// - 数据来源统一走 store.getAllAreas()，内部含15分钟缓存，避免反复请求。
// - 视觉遵循“中性、无圆角”规范；仅使用基础元素，避免品牌化控件。

import { ref, computed, onMounted, watch } from 'vue'
import { usePropertiesStore } from '@/stores/properties'

const props = defineProps({
  // 由父组件（FilterPanel）传入当前已选区域数组（store.selectedLocations）
  selected: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['update:selected', 'requestCount'])

const store = usePropertiesStore()

const loading = ref(false)
const allAreas = ref([]) // { id?, type?, name?, suburb?, postcode?, fullName? }
const keyword = ref('')

const placeholderText = '搜索区域'

// 归一化：将任意后端/服务返回的区域对象，转为 store.selectedLocations 规范
const normalizeArea = (raw) => {
  if (!raw) return null
  const name =
    (typeof raw.name === 'string' && raw.name) ||
    (typeof raw.suburb === 'string' && raw.suburb) ||
    (typeof raw.label === 'string' && raw.label) ||
    (raw.postcode ? String(raw.postcode) : '')

  const postcode = raw.postcode
    ? String(Math.floor(raw.postcode))
    : raw.code
      ? String(raw.code)
      : raw.postcode_str
        ? String(raw.postcode_str)
        : ''

  // 判定类型：明确给出 postcode/type 的优先，其次通过正则判断
  const isPostcode =
    raw.type === 'postcode' ||
    (/^\d{4}$/.test(String(raw.name || '')) && !raw.suburb) ||
    (/^\d{4}$/.test(postcode) && !name)

  const type = isPostcode ? 'postcode' : (raw.type || 'suburb')

  const id =
    raw.id ||
    (type === 'postcode'
      ? `postcode_${postcode}`
      : `suburb_${name}`)

  const fullName =
    type === 'postcode'
      ? postcode
      : (postcode ? `${name} NSW ${postcode}` : name)

  return {
    id,
    type,
    name,
    postcode,
    fullName,
  }
}

// 显示名称：postcode 用邮编，suburb 用全名（含NSW/邮编，若有）
const displayName = (raw) => {
  const a = normalizeArea(raw)
  if (!a) return ''
  return a.type === 'postcode' ? (a.postcode || a.name) : (a.fullName || a.name)
}

// A→Z 分组 + 关键字过滤
const filteredAreas = computed(() => {
  const kw = keyword.value.trim().toLowerCase()
  // 中文注释：移除所有邮编，仅保留 suburb
  const source = allAreas.value.filter((raw) => {
    const a = normalizeArea(raw)
    return a && a.type !== 'postcode'
  })
  if (!kw) return source
  return source.filter((raw) => {
    const a = normalizeArea(raw)
    const text = [a?.name, a?.fullName].filter(Boolean).join(' ').toLowerCase()
    return text.includes(kw)
  })
})

const grouped = computed(() => {
  const groups = new Map()
  const getLetter = (a) => {
    const c = (a?.name || a?.fullName || a?.postcode || '').toString().charAt(0).toUpperCase()
    return /^[A-Z]$/.test(c) ? c : '#'
  }
  for (const raw of filteredAreas.value) {
    const a = normalizeArea(raw)
    if (!a) continue
    const L = getLetter(a)
    if (!groups.has(L)) groups.set(L, [])
    groups.get(L).push(raw)
  }
  const arr = Array.from(groups.entries())
    .sort((x, y) => (x[0] === '#' ? 1 : y[0] === '#' ? -1 : x[0].localeCompare(y[0])))
    .map(([letter, items]) => ({
      letter,
      items: items.sort((r1, r2) => {
        const a1 = normalizeArea(r1)
        const a2 = normalizeArea(r2)
        return (a1?.name || '').localeCompare(a2?.name || '')
      }),
    }))
  return arr
})

const onSearch = () => {
  // 中文注释：输入即过滤，交由 computed 实时生效
}

const areaKey = (raw) => {
  const a = normalizeArea(raw)
  return a?.id || JSON.stringify(a)
}

const isSelected = (raw) => {
  const a = normalizeArea(raw)
  if (!a) return false
  return (props.selected || []).some((s) => s.id === a.id)
}

const toggle = (raw) => {
  const a = normalizeArea(raw)
  if (!a) return
  const curr = Array.isArray(props.selected) ? [...props.selected] : []
  const idx = curr.findIndex((s) => s.id === a.id)
  if (idx >= 0) {
    curr.splice(idx, 1)
  } else {
    curr.push(a)
  }
  emit('update:selected', curr)
  // 中文注释：选择交互仅触发计数刷新请求，不应用到结果
  emit('requestCount')
}

const clearAll = () => {
  emit('update:selected', [])
  emit('requestCount')
}

const ensureAreasLoaded = async () => {
  try {
    loading.value = true
    const list = await store.getAllAreas?.()
    // 中文注释：加载后即过滤掉所有邮编，仅保留 suburb
    allAreas.value = Array.isArray(list)
      ? list.filter((raw) => {
          const a = normalizeArea(raw)
          return a && a.type !== 'postcode'
        })
      : []
  } catch {
    allAreas.value = []
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await ensureAreasLoaded()
})

// 监听 store 数据就绪后再尝试填充（防止首次打开时为空导致“静态搜索框”体验）
watch(
  () => [store.allProperties.length, store.filteredProperties.length],
  async () => {
    if (!allAreas.value || allAreas.value.length === 0) {
      await ensureAreasLoaded()
    }
  },
  { immediate: false }
)
</script>

<style scoped>
.areas-selector {
  margin-top: 10px;
  border-top: 1px solid var(--filter-color-border-default);
  padding-top: 10px;
}

.areas-header {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.search-wrapper {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  color: var(--filter-color-text-secondary);
  pointer-events: none;
  z-index: 1;
}

.areas-search {
  width: 100%;
  padding: 12px 16px 12px 40px;
  font-size: 14px;
  color: var(--color-text-primary);
  background: var(--filter-color-bg-primary);
  border: 1px solid var(--filter-color-border-default);
  border-radius: 6px;
  outline: none;
  transition: all 0.2s ease;
}

.areas-search:focus {
  border-color: var(--filter-search-focus-border);
  box-shadow: var(--filter-shadow-focus);
}

.areas-search:hover:not(:focus) {
  border-color: var(--filter-search-hover-border);
}

.clear-search-btn {
  position: absolute;
  right: 8px;
  background: none;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.clear-search-btn:hover {
  background: var(--filter-color-hover-bg);
  color: var(--filter-color-text-primary);
}

.clear-all-btn {
  flex: none;
  padding: 12px 16px;
  font-size: 14px;
  font-weight: 500;
  background: var(--filter-color-bg-primary);
  color: var(--filter-color-text-secondary);
  border: 1px solid var(--filter-color-border-default);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.clear-all-btn:hover:not(:disabled) {
  background: var(--filter-color-bg-secondary);
  color: var(--filter-color-text-primary);
  border-color: var(--filter-color-border-strong);
}

.clear-all-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: var(--filter-color-bg-secondary);
}

.areas-body {
  max-height: 280px;
  overflow: auto;
  -webkit-overflow-scrolling: touch;
  border: 1px solid var(--filter-color-border-default);
  border-radius: 6px;
  background: var(--filter-color-bg-primary);
}

.loading-row,
.empty-row {
  padding: 20px 16px;
  font-size: 14px;
  color: var(--color-text-secondary);
  background: var(--filter-color-bg-secondary);
  text-align: center;
  border-radius: 6px;
}

.group {
  /* 分组容器 */
}

.group-title {
  position: sticky;
  top: 0;
  background: var(--filter-group-title-bg);
  z-index: 2;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  color: var(--filter-color-text-primary);
  border-bottom: 1px solid var(--filter-group-title-border);
  letter-spacing: 0.025em;
}

.group-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.area-item {
  border-bottom: 1px solid var(--filter-color-border-subtle);
  transition: background-color 0.15s ease;
}

.area-item:last-child {
  border-bottom: none;
}

.area-item:hover {
  background: var(--filter-color-hover-bg);
}

.area-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  cursor: pointer;
  transition: all 0.15s ease;
  min-height: 48px;
}

.check {
  width: 18px;
  height: 18px;
  border-radius: 3px;
  accent-color: var(--filter-checkbox-accent);
  cursor: pointer;
  transition: transform 0.15s ease;
}

.check:hover {
  transform: scale(1.05);
}

.area-name {
  font-size: 14px;
  color: var(--color-text-primary);
  user-select: none;
  line-height: 1.4;
  flex: 1;
}

/* 选中状态的行样式 */
.area-item:has(.check:checked) {
  background: var(--filter-color-selected-bg);
  border-color: var(--filter-color-selected-border);
}

.area-item:has(.check:checked) .area-name {
  color: #374151;
  font-weight: 600;
}

/* 如果浏览器不支持 :has，使用 JavaScript 类名回退 */
.area-item.selected {
  background: var(--filter-color-selected-bg);
  border-color: var(--filter-color-selected-border);
}

.area-item.selected .area-name {
  color: #374151;
  font-weight: 600;
}
</style>
