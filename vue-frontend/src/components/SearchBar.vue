<template>
  <div class="search-bar-container">
    <!-- 搜索输入框 -->
    <div class="search-input-container">
      <el-input
        ref="searchInputRef"
        v-model="searchQuery"
        :placeholder="effectivePlaceholder"
        size="large"
        class="search-input"
        :aria-label="isMobile.value ? '点击打开筛选面板' : '搜索区域'"
        :role="isMobile.value ? 'button' : 'searchbox'"
        @input="handleInput"
        @keydown="handleKeydown"
        @focus="handleFocus"
        @blur="handleBlur"
      >
        <template #prefix>
          <Search class="spec-icon search-icon" />
        </template>
      </el-input>

      <!-- 内嵌低调区域标签（占位显示），仅在未聚焦/未输入且有选区时展示 -->
      <div
        v-if="showInlineChips"
        class="inline-chips-overlay"
        @click="focusInput"
        role="group"
        aria-label="已选择的区域"
      >
        <span
          v-for="loc in displayedLocations"
          :key="'inline-' + loc.id"
          class="inline-chip"
          :title="formatInlineLocation(loc)"
        >
          <span class="inline-chip-text">{{ formatInlineLocation(loc) }}</span>
          <button
            class="inline-chip-remove"
            type="button"
            :aria-label="`移除 ${formatInlineLocation(loc)}`"
            title="移除"
            @click.stop="removeLocation(loc.id)"
          >
            ×
          </button>
        </span>
        <span v-if="hiddenCount > 0" class="inline-chip inline-chip-more">+{{ hiddenCount }}</span>
      </div>

      <!-- 自动补全建议列表 -->
      <div
        v-if="
          showSuggestions &&
          (filteredSuggestions.length > 0 || nearbySuggestions.length > 0 || isLoadingSuggestions)
        "
        class="location-suggestions"
      >
        <!-- 搜索结果 -->
        <div v-if="searchQuery && (filteredSuggestions.length > 0 || isLoadingSuggestions)">
          <div v-if="filteredSuggestions.length > 0" class="suggestions-section-title">
            搜索结果
          </div>
          <div
            v-for="(suggestion, index) in filteredSuggestions"
            :key="suggestion.id"
            class="suggestion-item"
            :class="{ active: currentSuggestionIndex === index, selected: isSelected(suggestion) }"
            @click="toggleSuggestion(suggestion)"
          >
            <div class="suggestion-content">
              <div class="suggestion-text">
                <div class="suggestion-name">{{ suggestion.fullName }}</div>
                <div class="suggestion-count">{{ suggestion.count }} 套房源</div>
              </div>
              <span class="suggestion-action">{{ isSelected(suggestion) ? '已选' : '添加' }}</span>
            </div>
          </div>
        </div>

        <!-- 相邻区域推荐 -->
        <div v-if="!searchQuery && nearbySuggestions.length > 0">
          <div class="suggestions-section-title">SUGGESTED FOR YOU</div>
          <div class="nearby-suggestions-grid">
            <div
              v-for="suggestion in nearbySuggestions"
              :key="suggestion.id"
              class="nearby-suggestion-item"
              @click="selectLocation(suggestion)"
            >
              <span class="nearby-name">{{ suggestion.name }}, NSW, {{ suggestion.postcode }}</span>
            </div>
          </div>
        </div>

        <!-- 加载中状态 -->
        <div v-if="isLoadingSuggestions" class="loading-suggestions">
          <span class="spinner" aria-hidden="true"></span>
          搜索中...
        </div>
      </div>
    </div>
    <SearchOverlay
      v-if="showOverlay"
      @close="showOverlay = false"
      @open-filter-panel="onOverlayOpenFilter"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, inject } from 'vue'
import { usePropertiesStore } from '@/stores/properties'
import { locationAPI } from '@/services/api'
import SearchOverlay from './SearchOverlay.vue'
import { Search } from 'lucide-vue-next'

// 建议列表最大返回条数（覆盖 36 条邮编）
const SUGGESTION_LIMIT = 100

// 组件事件
const emit = defineEmits(['search', 'locationSelected', 'openFilterPanel']) // 说明：新增 openFilterPanel，用于在搜索框内图标触发统一筛选面板

/* 状态管理 */
const propertiesStore = usePropertiesStore()

/* 轻量 i18n：统一占位与拦截提示文案 */
const t = inject('t') || ((k) => k)

// 响应式数据
const searchQuery = ref('')
const showSuggestions = ref(false)
const currentSuggestionIndex = ref(-1)
const locationSuggestions = ref([])
const nearbySuggestions = ref([])
const isLoadingSuggestions = ref(false)

/* 移动端全屏 Overlay 状态 */
const showOverlay = ref(false)
/* 引用输入框实例，便于手动 blur 避免 focus 触发 */
const searchInputRef = ref(null)

/* 视口断点：移动端不常驻 chips（仅在 Overlay/Filter 内显示） */
const isMobile = ref(false)
const checkIsMobile = () => {
  if (typeof window !== 'undefined') {
    isMobile.value = window.innerWidth <= 767
  }
}
checkIsMobile()

/* 桌面端 chips：最多展示 2 个，其余以 +N 摘要 */
const displayedLocations = computed(() => selectedLocations.value.slice(0, 2))
const hiddenCount = computed(() => Math.max(0, (selectedLocations.value?.length || 0) - 2))

/* 保留 +N 摘要仅在输入框内部回显，不提供顶部常驻 chips 与点击跳转 */

// 计算属性
const selectedLocations = computed(() => propertiesStore.selectedLocations)

const searchPlaceholder = computed(() => t('search.ph'))
const effectivePlaceholder = computed(() => ((selectedLocations.value?.length || 0) > 0 ? '' : searchPlaceholder.value))

/* 输入焦点与内嵌标签可见性控制 */
const isInputFocused = ref(false)
const showInlineChips = computed(() => {
  // 未聚焦 + 未输入 + 未打开 Overlay（移动端） + 有选区
  return (
    !isInputFocused.value &&
    !showOverlay.value &&
    !searchQuery.value &&
    (selectedLocations.value?.length || 0) > 0
  )
})
/* 格式化标签文案：Suburb, NSW, 2017 / 2017 */
const formatInlineLocation = (loc) => {
  if (!loc) return ''
  // 中文注释：内联回显仅显示 suburb 名称；postcode 仅显示自身
  return loc.type === 'suburb' ? String(loc.name || '') : String(loc.name || '')
}

// 去重 Key 规范化：同一区域（type+name+postcode）视为同一项
const normalizeKey = (loc) => {
  if (!loc) return ''
  return `${loc.type || ''}|${String(loc.name || '').toLowerCase()}|${loc.postcode || ''}`
}

// 删除这行，改为使用响应式数据
// const locationSuggestions = computed(() => propertiesStore.locationSuggestions)

const filteredSuggestions = computed(() => {
  // 过滤掉已经选择的区域，避免重复显示（使用规范化 Key 去重）
  const keys = new Set(selectedLocations.value.map((s) => normalizeKey(s)))
  return locationSuggestions.value.filter((suggestion) => !keys.has(normalizeKey(suggestion)))
})

// 方法
// 搜索区域建议（调用后端API）
const searchLocationSuggestions = async (query) => {
  if (!query || query.length < 1) {
    locationSuggestions.value = []
    return
  }

  isLoadingSuggestions.value = true
  try {
    const results = await locationAPI.getSuggestions(query, SUGGESTION_LIMIT)
    // 排序（方案B）：无论数字/字母，主排序按名称首字母，其次按邮编数值
    let items = Array.isArray(results) ? results.slice() : []
    items.sort((a, b) => {
      const fa = String(a.fullName ?? a.name ?? '').toLowerCase()
      const fb = String(b.fullName ?? b.name ?? '').toLowerCase()
      const cmp = fa.localeCompare(fb, 'en-AU', { sensitivity: 'base' })
      if (cmp !== 0) return cmp
      const pa = Number(a.postcode ?? a.name)
      const pb = Number(b.postcode ?? b.name)
      if (!Number.isNaN(pa) && !Number.isNaN(pb)) return pa - pb
      return 0
    })
    locationSuggestions.value = items
  } catch (error) {
    console.error('搜索失败:', error)
    locationSuggestions.value = []
  } finally {
    isLoadingSuggestions.value = false
  }
}

// 加载相邻区域建议
const loadNearbySuggestions = async () => {
  if (selectedLocations.value.length === 0) {
    nearbySuggestions.value = []
    return
  }

  const lastLocation = selectedLocations.value[selectedLocations.value.length - 1]
  try {
    const result = await locationAPI.getNearbySuburbs(lastLocation.name)
    // 过滤掉已经选择的区域，避免重复显示（使用规范化 Key 去重）
    const nearbyResults = result.nearby || []
    nearbySuggestions.value = nearbyResults.filter(
      (suggestion) => !selectedLocations.value.some((selected) => normalizeKey(selected) === normalizeKey(suggestion)),
    )
  } catch (error) {
    console.error('获取相邻区域失败:', error)
    nearbySuggestions.value = []
  }
}

// 防抖函数
const debounce = (func, delay) => {
  let timeoutId
  return function (...args) {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => func.apply(this, args), delay)
  }
}

// 防抖搜索
const debouncedSearch = debounce((query) => {
  searchLocationSuggestions(query)
}, 300)

// 事件处理
const handleFocus = () => {
  isInputFocused.value = true

  // 移动端直接打开筛选面板，不再使用 SearchOverlay
  if (typeof window !== 'undefined' && window.innerWidth <= 767) {
    // 阻止输入框获得焦点，避免键盘弹出
    searchInputRef.value?.blur()
    emit('openFilterPanel')
    return
  }

  // 桌面端保持原有逻辑
  showSuggestions.value = true
  // 如果没有输入内容且有选中的区域，加载相邻区域推荐
  if (!searchQuery.value && selectedLocations.value.length > 0) {
    loadNearbySuggestions()
  }
}

const handleBlur = () => {
  isInputFocused.value = false
}

// 中文注释：点击内嵌标签区域时，将焦点回到输入框，便于继续键入
const focusInput = () => {
  searchInputRef.value?.focus?.()
}

// 中文注释：移除一个已选择的区域标签
const removeLocation = (id) => {
  try {
    propertiesStore.removeSelectedLocation(id)
  } catch (e) {
    console.warn('移除区域失败', e)
  }
}

/* 承接 SearchOverlay 内“筛选”按钮事件：关闭 Overlay 并打开筛选面板 */
const onOverlayOpenFilter = () => {
  showOverlay.value = false
  emit('openFilterPanel')
}

const handleInput = (value) => {
  searchQuery.value = value
  currentSuggestionIndex.value = -1

  if (selectedLocations.value.length === 0) {
    showSuggestions.value = true
    debouncedSearch(value) // 调用API搜索
  } else {
    // 已选区域：仍然展示建议列表，用于继续添加区域/邮编
    showSuggestions.value = true
    debouncedSearch(value)
  }
}

const handleKeydown = (event) => {
  const suggestions = filteredSuggestions.value

  switch (event.key) {
    case 'ArrowDown':
      event.preventDefault()
      if (suggestions.length > 0) {
        currentSuggestionIndex.value = Math.min(
          currentSuggestionIndex.value + 1,
          suggestions.length - 1,
        )
      }
      break

    case 'ArrowUp':
      event.preventDefault()
      if (suggestions.length > 0) {
        currentSuggestionIndex.value = Math.max(currentSuggestionIndex.value - 1, -1)
      }
      break

    case 'Enter':
      event.preventDefault()
      if (currentSuggestionIndex.value >= 0 && suggestions[currentSuggestionIndex.value]) {
        toggleSuggestion(suggestions[currentSuggestionIndex.value])
      } else if (suggestions.length > 0) {
        // 未选择具体项时，默认选中或取消第一条，便于连续多选
        toggleSuggestion(suggestions[0])
      } else if (selectedLocations.value.length === 0 && searchQuery.value.trim()) {
        // 无建议且尚未选择区域时，触发一次搜索
        debouncedSearch(searchQuery.value)
      }
      break

    case 'Escape':
      event.preventDefault()
      showSuggestions.value = false
      currentSuggestionIndex.value = -1
      break
  }
}

const selectLocation = async (location) => {
  // 检查是否已经选中（使用规范化 Key 去重）
  const exists = selectedLocations.value.some((loc) => normalizeKey(loc) === normalizeKey(location))
  if (exists) return

  // 1) 添加选中区域为标签
  propertiesStore.addSelectedLocation(location)

  // 2) 按产品期望：清空输入内容，关闭下拉，重置高亮索引（避免手动删除）
  searchQuery.value = ''
  showSuggestions.value = false
  currentSuggestionIndex.value = -1

  // 3) 立即清空当前候选，避免残留闪烁；后续再次输入会重新搜索
  locationSuggestions.value = []
  nearbySuggestions.value = []
  isLoadingSuggestions.value = false

  emit('locationSelected', location)

  // 保持输入框可继续操作的连贯性（不 blur）
  // 如需在选择后展示“相邻区域推荐”，可在下一次 focus 且 searchQuery 为空时由 handleFocus 触发
}

// 判断某建议是否已被选中
const isSelected = (suggestion) => {
  return selectedLocations.value.some((selected) => normalizeKey(selected) === normalizeKey(suggestion))
}

// 切换选择/取消（用于多选复选框或整行点击）
const toggleSuggestion = async (suggestion) => {
  if (isSelected(suggestion)) {
    // 移除规范化 Key 匹配的已选项，避免不同来源 id 不一致导致无法取消
    const selected = selectedLocations.value.find((s) => normalizeKey(s) === normalizeKey(suggestion))
    if (selected) {
      propertiesStore.removeSelectedLocation(selected.id)
      emit('locationSelected', { removed: true, id: selected.id })
    }
    return
  }
  await selectLocation(suggestion)
}

const handleClickOutside = (event) => {
  const container = document.querySelector('.search-bar-container')
  if (!container?.contains(event.target)) {
    showSuggestions.value = false
    currentSuggestionIndex.value = -1
  }
}

// 生命周期
onMounted(async () => {
  document.addEventListener('click', handleClickOutside)
  // 视口监听：桌面/移动切换
  if (typeof window !== 'undefined') {
    window.addEventListener('resize', checkIsMobile)
    checkIsMobile()
  }
  // 初始化时不再加载所有区域数据，改为按需搜索
  // 这样可以避免加载大量数据到前端
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', checkIsMobile)
  }
})

// 监听属性变化
watch(
  () => propertiesStore.searchQuery,
  (newQuery) => {
    if (searchQuery.value !== newQuery) {
      searchQuery.value = newQuery
    }
  },
)
</script>

<style scoped>
/* 搜索栏容器 */
.search-bar-container {
  position: relative;
  width: 100%;

  /* 中文注释：搜索栏变量接入 page-tokens 语义令牌；优先读令牌，保留兜底 */
  --search-height: var(--search-h-desk, 44px);
  --search-height-mob: var(--search-h-mob, 44px);
  --sb-padding-x: var(--search-padding-x, 12px);
  --sb-radius: var(--search-radius, 6px);
  --search-icon-size: var(--search-icon, 16px);
  --filter-chip-radius: var(--search-chip-radius, 16px);
  --filter-chip-gap: var(--search-chip-gap, 8px);
}

/* 区域标签样式 */
.location-tags {
  display: flex;
  flex-wrap: nowrap; /* 单行，不换行 */
  overflow-x: auto; /* 横向滚动 */
  white-space: nowrap;
  gap: 8px;
  margin-bottom: 8px;
  padding-bottom: 4px;
  -webkit-overflow-scrolling: touch;
}

.location-tag {
  background: var(--chip-bg);
  color: var(--color-text-secondary);
  border: none;
  border-radius: 9999px;
  font-size: 13px;
  font-weight: 500;
  padding: 6px 12px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition:
    background-color 0.2s ease,
    color 0.2s ease;
}

.location-tag:hover {
  background: var(--chip-bg-hover);
  color: var(--color-text-primary);
}

.remove-location-btn {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  font-size: 12px;
  padding: 2px;
  border-radius: 999px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
}

.remove-location-btn:hover {
  background: var(--bg-hover);
  color: var(--color-text-primary);
}

/* 搜索输入框 */
.search-input-container {
  position: relative;
}

.search-input :deep(.el-input__wrapper) {
  position: relative; /* 作为绝对定位锚点，保证按钮贴右且不遮挡文字 */
  border-radius: var(--sb-radius);
  border: 1px solid var(--color-border-default);
  transition: all 0.2s ease;
  height: var(--search-height);
  min-height: var(--search-height);

  /* 右侧不再预留筛选按钮空间，保持与输入内边距一致 */
  padding-right: var(--search-suffix-right, 12px);
}

.search-input :deep(.el-input__wrapper):hover {
  border-color: var(--color-border-strong);
}

.search-input :deep(.el-input__wrapper.is-focus) {
  /* 去除点击后的灰色/橙色外框与高亮，保持无 ring */
  border-color: var(--color-border-default);
  box-shadow: none;
}

.search-icon {
  color: var(--color-text-secondary);
  width: var(--search-icon-size);
  height: var(--search-icon-size);
}

/* 说明：控制后缀区域的右内边距，确保图标距输入框右边界为 12px */
.search-input :deep(.el-input__suffix) {
  /* 取消锚点，让 wrapper 成为定位参照，避免文本被覆盖 */
  position: static;
  padding-right: var(--search-suffix-right, 12px); /* icon 右缘距输入框内侧 12px */
}

/* 让后缀内容贴右对齐，避免看起来“靠左” */
.search-input :deep(.el-input__suffix-inner) {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  width: 100%;
}

/* 说明：筛选图标容器采用绝对定位贴右；视觉尺寸 16×16，命中区域放大到 32×32 增强可点性 */
.filter-icon-btn {
  position: absolute;
  right: var(--search-suffix-right, 12px);
  top: 50%;
  transform: translateY(-50%);
  width: var(--search-suffix-hit, 32px); /* 命中区域 */
  height: var(--search-suffix-hit, 32px); /* 命中区域 */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin: 0;
  border: none;
  background: transparent;
  cursor: pointer;
  color: var(--color-text-secondary);
}

.filter-icon-btn svg {
  width: 22px;
  height: 22px;
  color: var(--color-text-secondary);
}

.filter-icon-btn:hover svg,
.filter-icon-btn:focus svg {
  color: var(--color-text-primary);
}

.filter-icon-btn:focus {
  outline: 2px solid rgb(0 0 0 / 6%);
  outline-offset: 2px;
  border-radius: 0;
}

/* 自动补全建议列表 */
.location-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--color-bg-card);
  border: none;
  border-radius: 8px;
  box-shadow: var(--shadow-lg);
  max-height: 300px;
  overflow-y: auto;
  z-index: 1000;
  margin-top: 4px;
}

/* 内嵌低调标签（覆盖在输入框可视区域，不拦截事件） */
.inline-chips-overlay {
  position: absolute;
  left: 40px; /* 与前缀图标对齐（16px 图标 + 内补白） */
  right: 12px;
  top: 0;
  bottom: 0;
  transform: none;
  height: 100%;
  display: flex;
  align-items: center; /* 垂直居中，使标签在输入框高度内居中对齐 */
  gap: var(--filter-chip-gap);
  /* 允许点击：用于触发聚焦与移除标签 */
  pointer-events: auto;
  overflow: hidden;
  white-space: nowrap;
}

/* 渐变遮罩，避免文字硬切（仅在必要时出现） */
.inline-chips-overlay::after {
  display: none;
  content: none;
}

/* 单个浅灰 chip */
.inline-chip {
  display: inline-flex;
  align-items: center;
  gap: var(--filter-chip-gap);
  padding: var(--filter-chip-padding-y) var(--filter-chip-padding-x);
  border: 1px solid var(--color-border-strong);
  border-radius: var(--filter-chip-radius);
  background: var(--chip-bg);
  color: var(--color-text-primary);
  font-size: var(--filter-chip-font-size);
  font-weight: var(--filter-chip-font-weight);
  line-height: 1;
  min-height: 32px; /* 紧凑高度（≈32px），与输入框内垂直居中配合 */
}

.inline-chip-icon {
  display: none;
}

.inline-chip-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 120px; /* 中文注释：限制单个标签宽度，避免长词撑破输入框 */
}

.inline-chip-more {
  color: var(--color-text-primary);
  background: var(--chip-bg);
  border: 1px solid var(--color-border-strong);
  border-radius: var(--filter-chip-radius);
}
/* Hover 态轻微加深，保持中性风格 */
.inline-chip:hover,
.inline-chip-more:hover {
  background: var(--chip-bg-hover);
  color: var(--color-text-primary);
}

/* 移除按钮：仅按钮可点击，避免误拦截输入 */
.inline-chip-remove {
  pointer-events: auto;
  margin-left: 6px;
  border: none;
  background: transparent;
  color: var(--color-text-secondary);
  cursor: pointer;
  font-size: 14px;
  line-height: 1;
  padding: 0 2px;
  display: inline-flex; /* 与文本中线对齐 */
  align-items: center;  /* 垂直居中 */
}

.inline-chip-remove:hover {
  color: var(--color-text-primary);
}

.suggestion-item {
  padding: 12px 16px;
  border-bottom: 1px solid var(--color-border-default);
  cursor: pointer;
  transition: all 0.2s ease;
}

.suggestion-item:last-child {
  border-bottom: none;
}

.suggestion-item:hover,
.suggestion-item.active {
  background-color: var(--bg-hover);
  color: var(--color-text-primary);
}

.suggestion-content {
  display: flex;
  align-items: center;
  gap: 12px;
  justify-content: space-between;
}

.suggestion-icon {
  color: var(--color-text-secondary);
  width: 16px;
  height: 16px;
  text-align: center;
}

.suggestion-text {
  flex: 1;
}

.suggestion-name {
  font-weight: 500;
  font-size: 14px;
  color: var(--color-text-primary);
  margin-bottom: 2px;
}

.suggestion-count {
  font-size: 12px;
  color: var(--color-text-secondary);
}

/* 复选框样式（多选小方框） */
.suggestion-action {
  flex-shrink: 0;
  color: var(--color-text-secondary);
  font-weight: 600;
  font-size: 12px;
}

.suggestion-item.selected .suggestion-action {
  color: var(--color-text-primary);
}

/* 选中行弱高亮（可按需调整） */
.suggestion-item.selected {
  background-color: var(--chip-bg-selected);
}

/* 新增：区域标题样式 */
.suggestions-section-title {
  padding: 8px 16px;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: var(--surface-2);
  border-bottom: 1px solid var(--divider-color);
  display: flex;
  align-items: center;
  gap: 6px;
}

.suggestions-section-title i {
  font-size: 12px;
  color: var(--text-muted);
}

/* +N 摘要 pill（桌面） */
.more-chip {
  border: none;
  background: var(--chip-bg);
  color: var(--color-text-secondary);
  border-radius: 0;
  padding: 6px 10px;
  font-size: 13px;
  cursor: pointer;
}

.more-chip:hover {
  background: var(--chip-bg-hover);
  color: var(--color-text-primary);
}

/* 新增：相邻区域网格布局 */
.nearby-suggestions-grid {
  padding: 12px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.nearby-suggestion-item {
  padding: 8px 12px;
  border: none;
  border-radius: 0;
  background: var(--chip-bg);
  cursor: pointer;
  transition:
    background-color 0.2s ease,
    color 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.nearby-suggestion-item:hover {
  background: var(--chip-bg-hover);
  color: var(--color-text-primary);
}

.nearby-suggestion-item .suggestion-icon {
  width: 12px;
  height: 12px;
  color: var(--color-text-secondary);
}

.nearby-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 新增：加载状态 */
.loading-suggestions {
  padding: 20px;
  text-align: center;
  color: var(--text-muted);
  font-size: 13px;
}

.loading-suggestions .spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  margin-right: 8px;
  border: 2px solid var(--color-border-default);
  border-top-color: var(--color-border-strong);
  border-radius: 50%;
  animation: sb-spin 1s linear infinite;
}

@keyframes sb-spin {
  to {
    transform: rotate(360deg);
  }
}

/* 响应式适配 */
@media (width <= 767px) {
  .search-bar-container {
    width: 100%;
  }

  .search-input-container {
    width: 334px;
    margin-left: auto;
    margin-right: auto;
  }

  /* 移动端搜索框样式优化：添加点击反馈效果 + 尺寸 334x60 */
  .search-input :deep(.el-input__wrapper) {
    cursor: pointer; /* 指示可点击 */
    transition: background-color 0.2s ease;
    height: var(--search-height-mob);
    min-height: var(--search-height-mob);
    padding-right: var(--search-suffix-right, 12px); /* 移动端无后缀按钮，不再预留额外空间 */
  }

  .search-input :deep(.el-input__wrapper:active) {
    background-color: var(--bg-hover); /* 点击时背景色变化 */
  }

  .search-input :deep(.el-input__inner) {
    height: var(--search-height-mob);
    line-height: var(--search-height-mob);
  }

  /* 移动端彻底隐藏后缀容器，避免任何残留占位 */
  .search-input :deep(.el-input__suffix),
  .search-input :deep(.el-input__suffix-inner) {
    display: none;
  }

  .location-suggestions {
    margin-left: -16px;
    margin-right: -16px;
    border-radius: 0;
    border-left: none;
    border-right: none;
  }

  /* 移动端不常驻 chips（只在 Overlay/筛选面板内管理） */
  .location-tags {
    display: none;
  }

  .location-tags {
    margin-left: -4px;
    margin-right: -4px;
  }

  .suggestion-item {
    padding: 16px;
  }

  /* 移动端隐藏输入框右侧的筛选图标，改为点击整框打开筛选面板（前端表现：点击搜索框整体即可进入筛选） */
  .filter-icon-btn {
    display: none;
  }

  /* 移动端：取消右侧渐变遮罩，防止“缺口”；并与输入框右内边距对齐 */
  .inline-chips-overlay {
    right: 12px;
  }
  .inline-chips-overlay::after {
    display: none;
  }
}
</style>
