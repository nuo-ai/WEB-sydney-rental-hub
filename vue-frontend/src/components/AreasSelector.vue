<template>
  <div class="areas-selector">
    <div class="areas-header">
      <input
        v-model="keyword"
        type="text"
        class="areas-search"
        :placeholder="placeholderText"
        @input="onSearch"
        aria-label="搜索区域或邮编"
      />
      <button
        class="clear-btn"
        type="button"
        :disabled="(selected || []).length === 0"
        @click="clearAll"
      >
        清空
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

const placeholderText = '搜索区域/邮编'

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
  if (!kw) return allAreas.value
  return allAreas.value.filter((raw) => {
    const a = normalizeArea(raw)
    const text = [a?.name, a?.postcode, a?.fullName].filter(Boolean).join(' ').toLowerCase()
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
    allAreas.value = Array.isArray(list) ? list : []
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
  border-top: 1px solid var(--color-border-default);
  padding-top: 10px;
}

.areas-header {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}

.areas-search {
  flex: 1;
  min-width: 0;
  padding: 10px 12px;
  font-size: 14px;
  color: var(--color-text-primary);
  background: #ffffff;
  border: 1px solid var(--color-border-default);
  border-radius: 0; /* 强约束：无圆角 */
  outline: none;
}

.areas-search:focus {
  border-color: var(--color-border-strong);
}

.clear-btn {
  flex: none;
  padding: 10px 12px;
  font-size: 14px;
  background: #fff;
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border-default);
  border-radius: 0; /* 强约束：无圆角 */
  cursor: pointer;
}

.clear-btn:hover:not(:disabled) {
  background: #f7f8fa;
  color: var(--color-text-primary);
  border-color: var(--color-border-strong);
}

.clear-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.areas-body {
  max-height: 260px;
  overflow: auto;
  -webkit-overflow-scrolling: touch;
  border: 1px solid var(--color-border-default);
  border-radius: 0; /* 强约束：无圆角 */
}

.loading-row,
.empty-row {
  padding: 10px 12px;
  font-size: 13px;
  color: var(--color-text-secondary);
  background: var(--chip-bg, #f7f8fa);
}

.group {
  /* 分组容器 */
}

.group-title {
  position: sticky;
  top: 0;
  background: #fff;
  z-index: 1;
  padding: 6px 10px;
  font-size: 12px;
  color: var(--color-text-secondary);
  border-bottom: 1px solid var(--color-border-default);
}

.group-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.area-item {
  border-bottom: 1px solid var(--color-border-default);
}

.area-item:last-child {
  border-bottom: none;
}

.area-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  cursor: pointer;
}

.check {
  width: 16px;
  height: 16px;
  border-radius: 0; /* 强约束：无圆角 */
  accent-color: var(--color-border-strong); /* 中性色系 */
}

.area-name {
  font-size: 14px;
  color: var(--color-text-primary);
  user-select: none;
}
</style>
