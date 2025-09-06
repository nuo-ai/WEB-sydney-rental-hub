<template>
  <!-- 移动端全屏搜索面板（Teleport 到 body，避免层级/滚动问题） -->
  <teleport to="body">
    <div v-if="visible" class="search-overlay" role="dialog" aria-modal="true">
      <!-- 头部：返回 / 输入 / 清空 -->
      <div class="overlay-header">
        <button class="icon-btn" aria-label="返回" @click="close">
          <ChevronLeft class="spec-icon" />
        </button>

        <div class="header-input">
          <Search class="search-prefix" aria-hidden="true" />
          <input
            ref="inputRef"
            v-model="query"
            type="search"
            :placeholder="t('search.ph')"
            class="input"
            autocomplete="off"
            autocapitalize="none"
            spellcheck="false"
            @input="onInput"
          />
          <button v-if="query" class="icon-btn" aria-label="清空" @click="clearQuery">
            <X class="spec-icon" />
          </button>
        </div>
        <div class="header-actions">
          <button class="filter-text-btn" type="button" @click="openFilterFromOverlay">
            {{ filterLabel }}
          </button>
          <button class="icon-btn" aria-label="搜索">
            <Search class="spec-icon" />
          </button>
        </div>
      </div>

      <!-- 已选 chips 标签区（横向滚动） -->
      <div v-if="selectedLocations.length" class="chips-row">
        <div
          v-for="loc in selectedLocations"
          :key="loc.id"
          class="chip"
          :class="{ active: loc.id === lastSelectedId }"
          :title="loc.fullName || loc.name"
        >
          <MapPin v-if="loc.type === 'suburb'" class="chip-icon" aria-hidden="true" />
          <Hash v-else class="chip-icon" aria-hidden="true" />
          <span class="chip-text">{{ loc.name }}</span>
          <button class="chip-remove" aria-label="移除" @click="removeLocation(loc.id)">
            <X class="chip-remove-icon" />
          </button>
          <span v-if="loc.id === lastSelectedId" class="chip-caret" aria-hidden="true"></span>
        </div>
      </div>

      <!-- 列表内容区（内部滚动） -->
      <div class="overlay-content">
        <!-- 匹配结果（Locations / Postcodes） -->
        <section v-if="query">
          <div class="section-title">
            <Search class="title-icon" aria-hidden="true" />
            <span>RESULTS</span>
          </div>

          <div v-if="isLoading" class="loading">
            <span class="spinner" aria-hidden="true"></span>
            <span>搜索中...</span>
          </div>

          <template v-else>
            <button
              v-for="(sug, idx) in filteredSuggestions"
              :key="`${sug.id}-${idx}`"
              class="row"
              @click="toggleSuggestion(sug)"
            >
              <div class="row-left">
                <MapPin v-if="sug.type === 'suburb'" class="row-icon" aria-hidden="true" />
                <Hash v-else class="row-icon" aria-hidden="true" />
                <div class="row-text">
                  <div class="row-title">{{ sug.fullName || sug.name }}</div>
                  <div class="row-sub">{{ (sug.count ?? 0) }} 套房源</div>
                </div>
              </div>
              <div class="row-right">
                <span class="pill" :class="{ selected: isSelected(sug) }">
                  <PlusCircle class="pill-icon" aria-hidden="true" />
                </span>
              </div>
            </button>

            <div v-if="!filteredSuggestions.length" class="empty">
              无匹配结果
            </div>
            <!-- 空态兜底：即使存在 query，也展示推荐区域，便于继续添加 -->
            <template v-if="!filteredSuggestions.length">
              <div class="section-title">
                <Lightbulb class="title-icon" aria-hidden="true" />
                <span>SUGGESTED FOR YOU</span>
              </div>
              <template v-if="nearby.length">
                <button
                  v-for="(sug, idx) in nearby"
                  :key="`fallback-nearby-${sug.id || idx}`"
                  class="row"
                  @click="toggleSuggestion(sug)"
                >
                  <div class="row-left">
                    <MapPin v-if="sug.type === 'suburb' || !sug.type" class="row-icon" aria-hidden="true" />
                    <Hash v-else class="row-icon" aria-hidden="true" />
                    <div class="row-text">
                      <div class="row-title">{{ sug.fullName || sug.name }}</div>
                      <div class="row-sub" v-if="sug.postcode">NSW, {{ sug.postcode }}</div>
                    </div>
                  </div>
                  <div class="row-right">
                    <span class="pill" :class="{ selected: isSelected(sug) }">
                      <PlusCircle class="pill-icon" aria-hidden="true" />
                    </span>
                  </div>
                </button>
              </template>
              <div v-else class="empty">
                暂无推荐，可更换关键字
              </div>
            </template>
          </template>
        </section>

        <!-- 推荐区域（nearby） -->
        <section v-else>
          <div class="section-title">
            <Lightbulb class="title-icon" aria-hidden="true" />
            <span>SUGGESTED FOR YOU</span>
          </div>

          <div v-if="isLoading" class="loading">
            <span class="spinner" aria-hidden="true"></span>
            <span>加载中...</span>
          </div>

          <template v-else>
            <button
              v-for="(sug, idx) in nearby"
              :key="`nearby-${sug.id || idx}`"
              class="row"
              @click="toggleSuggestion(sug)"
            >
              <div class="row-left">
                <MapPin v-if="sug.type === 'suburb' || !sug.type" class="row-icon" aria-hidden="true" />
                <Hash v-else class="row-icon" aria-hidden="true" />
                <div class="row-text">
                  <div class="row-title">{{ sug.fullName || sug.name }}</div>
                  <div class="row-sub" v-if="sug.postcode">NSW, {{ sug.postcode }}</div>
                </div>
              </div>
              <div class="row-right">
                <span class="pill" :class="{ selected: isSelected(sug) }">
                  <PlusCircle class="pill-icon" aria-hidden="true" />
                </span>
              </div>
            </button>

            <div v-if="!nearby.length" class="empty">
              暂无推荐，可输入关键字搜索
            </div>
          </template>
        </section>
      </div>
    </div>
  </teleport>
</template>

<script setup>
/*
  为什么这样实现：
  - 移动端采用全屏 Overlay（100dvh + safe-area），避免下拉浮层在小屏的可用性问题
  - Teleport 到 body，规避父容器 overflow/层级影响
  - 逻辑最小复制：先直接调用 locationAPI，与 SearchBar 共享 stores（后续再抽 useLocationSearch 复用）
  - 字号 ≥16px，避免 iOS auto-zoom；滚动锁定 body，关闭后恢复
*/
import { ref, watch, onMounted, onUnmounted, computed, inject, nextTick } from 'vue'
import { usePropertiesStore } from '@/stores/properties'
import { locationAPI } from '@/services/api'
import { Search, MapPin, Hash, PlusCircle, X, ChevronLeft, Lightbulb } from 'lucide-vue-next'

const emit = defineEmits(['close', 'open-filter-panel', 'openFilterPanel'])

const t = inject('t') || ((k) => k)
const propertiesStore = usePropertiesStore()

/* i18n 文案回退：当 t('filter.short') 缺失或返回 key 时，回退到“筛选” */
const filterLabel = computed(() => {
  const v = t('filter.short')
  return v && v !== 'filter.short' ? v : '筛选'
})

const visible = ref(true)
const query = ref('')
const suggestions = ref([])
const nearby = ref([])
const isLoading = ref(false)
const inputRef = ref(null)
/* 记录最近一次选中的 chip，用于高亮与“光标”提示 */
const lastSelectedId = ref(null)

/* 选中区域（从 store 读取），保持单一数据源 */
const selectedLocations = computed(() => propertiesStore.selectedLocations || [])

/* 过滤掉已选的建议，避免重复展示 */
const filteredSuggestions = computed(() => {
  const list = suggestions.value || []
  const selected = selectedLocations.value || []
  const same = (a, b) =>
    (a?.id && b?.id && a.id === b.id) ||
    ((a?.type || '') === (b?.type || '') && (a?.name || '') === (b?.name || ''))
  return list.filter((s) => !selected.some((sel) => same(s, sel)))
})

/* 搜索逻辑（防抖） */
let debounceTimer = null
const debouncedSearch = (val) => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(async () => {
    if (!val) {
      suggestions.value = []
      return
    }
    isLoading.value = true
    try {
      const res = await locationAPI.getSuggestions(val, 100)
      suggestions.value = Array.isArray(res) ? res : []
    } finally {
      isLoading.value = false
    }
  }, 300)
}

const onInput = () => {
  debouncedSearch(query.value)
}

/* 加载附近推荐（基于最后一个已选区域） */
const loadNearby = async () => {
  const sel = selectedLocations.value
  if (!sel.length) {
    nearby.value = []
    return
  }
  const last = sel[sel.length - 1]
  isLoading.value = true
  try {
    const r = await locationAPI.getNearbySuburbs(last.name)
    const list = r?.nearby || []
    nearby.value = list.filter(
      (s) => !selectedLocations.value.some((k) => k.id === s.id),
    )
  } catch {
    nearby.value = []
  } finally {
    isLoading.value = false
  }
}

/* 选择/取消 */
const isSelected = (s) =>
  selectedLocations.value.some((k) => {
    if (k.id && s.id) return k.id === s.id
    return k.type === s.type && k.name === s.name
  })

const selectLocation = (s) => {
  if (isSelected(s)) return
  const item = {
    id: s.id || `${s.type || 'suburb'}_${s.name}`,
    type: s.type || (Number.isNaN(Number(s.name)) ? 'suburb' : 'postcode'),
    name: s.name || s.fullName || '',
    fullName: s.fullName || s.name || '',
    postcode: s.postcode,
  }
  propertiesStore.addSelectedLocation(item)
  lastSelectedId.value = item.id
}

const toggleSuggestion = (s) => {
  if (isSelected(s)) {
    propertiesStore.removeSelectedLocation(s.id)
  } else {
    // 选中后清空关键字并回退到推荐，符合“连续多选”的心智
    selectLocation(s)
    clearQuery()
    loadNearby()
  }
}

const removeLocation = (id) => {
  propertiesStore.removeSelectedLocation(id)
}

/* 控件 */
const clearQuery = () => {
  query.value = ''
  suggestions.value = []
}

/* 从 Overlay 打开筛选面板：关闭自身并发出事件 */
const openFilterFromOverlay = () => {
  unlockScroll()
  visible.value = false
  emit('open-filter-panel')
  emit('openFilterPanel')
}

/* 打开时锁定 body 滚动，关闭恢复 */
const lockScroll = () => {
  document.body.classList.add('srh-overlay-open')
}
const unlockScroll = () => {
  document.body.classList.remove('srh-overlay-open')
}

const close = () => {
  unlockScroll()
  visible.value = false
  emit('close')
}

/* 生命周期 */
onMounted(async () => {
  lockScroll()
  // 首次焦点到输入框
  await nextTick()
  inputRef.value?.focus?.()
  if (selectedLocations.value.length) {
    const last = selectedLocations.value[selectedLocations.value.length - 1]
    lastSelectedId.value = last.id
    loadNearby()
  }
  // 监听返回键（Android/部分 iOS PWA）
  window.addEventListener('popstate', close)
})

onUnmounted(() => {
  unlockScroll()
  window.removeEventListener('popstate', close)
})

watch(query, (val) => {
  if (!val) {
    suggestions.value = []
    // 回退到 nearby 推荐
    if (selectedLocations.value.length) loadNearby()
  }
})

// 选中项变化时，动态刷新推荐（支持 chips 增删）
watch(
  () => propertiesStore.selectedLocations,
  () => {
    if (!query.value) {
      loadNearby()
    }
  },
  { deep: true },
)
</script>

<style scoped>
/* 全屏面板容器 */
.search-overlay {
  position: fixed;
  inset: 0;
  z-index: 10050;
  background: var(--color-bg-page, #fff);
  display: flex;
  flex-direction: column;
  height: 100dvh; /* 可见视口高度，适配 iOS */
  max-height: 100dvh;
  -webkit-text-size-adjust: 100%;
}

/* 头部 */
.overlay-header {
  position: sticky;
  top: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 12px calc(12px + env(safe-area-inset-top, 0px));
  border-bottom: 1px solid var(--color-border-default, #e5e7eb);
  background: #fff;
  z-index: 1;
}

.icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: transparent;
  border: none;
  color: var(--color-text-secondary, #6b7280);
  border-radius: 6px;
}

.icon-btn:active {
  background: #f3f4f6;
}

.spec-icon {
  width: 22px;
  height: 22px;
  color: currentColor;
}

.header-input {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  background: #fff;
  border: 1px solid var(--color-border-default, #e5e7eb);
  border-radius: 8px;
  padding: 0 8px;
}

.header-actions {
  margin-left: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-text-btn {
  background: transparent;
  border: none;
  color: var(--juwo-primary, #ff5824);
  font-weight: 600;
  font-size: 14px;
  padding: 6px 8px;
  border-radius: 6px;
}
.filter-text-btn:active {
  background: #fff6f1;
}

.search-prefix {
  width: 18px;
  height: 18px;
  color: var(--color-text-secondary, #6b7280);
}

.input {
  flex: 1;
  height: 38px;
  border: none;
  outline: none;
  font-size: 16px; /* iOS 防 auto-zoom */
  background: transparent;
  color: var(--color-text-primary, #111827);
}

/* 已选 chips */
.chips-row {
  display: flex;
  gap: 8px;
  padding: 8px 12px;
  overflow-x: auto;
  border-bottom: 1px solid var(--color-border-default, #e5e7eb);
  background: #fff;
}

.chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border: 1px solid var(--color-border-default, #e5e7eb);
  border-radius: 999px;
  background: #fff;
  color: var(--color-text-primary, #111827);
  white-space: nowrap;
}
.chip.active {
  background: #3c475b; /* 深灰底，强调当前选择 */
  border-color: #3c475b;
  color: #fff;
}
.chip.active .chip-icon,
.chip.active .chip-remove {
  color: #fff;
}

/* 活动 chip 的“输入光标”效果 */
.chip-caret {
  width: 2px;
  height: 14px;
  background: currentColor;
  margin-left: 4px;
  align-self: center;
  animation: caret-blink 1s step-end infinite;
}
@keyframes caret-blink {
  50% { opacity: 0; }
}

.chip-icon {
  width: 14px;
  height: 14px;
  color: var(--juwo-primary, #ff5824);
}

.chip-text {
  font-size: 14px;
}

.chip-remove {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  border: none;
  background: transparent;
  color: var(--color-text-secondary, #6b7280);
  border-radius: 999px;
}

.chip-remove-icon {
  width: 14px;
  height: 14px;
}

/* 内容区 */
.overlay-content {
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior: contain;
  padding-bottom: calc(12px + env(safe-area-inset-bottom, 0px));
}

.section-title {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 12px;
  font-size: 11px;
  font-weight: 600;
  color: #666;
  background: #f8f8f8;
  border-bottom: 1px solid #f0f0f0;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.title-icon {
  width: 14px;
  height: 14px;
  color: #999;
}

/* 行项 */
.row {
  width: 100%;
  display: flex;
  justify-content: space-between;
  padding: 14px 12px;
  border-bottom: 1px solid #f1f1f1;
  background: #fff;
  cursor: pointer;
}

.row:active {
  background: #fff6f1;
}

.row-left {
  display: flex;
  gap: 12px;
  align-items: center;
}

.row-icon {
  width: 16px;
  height: 16px;
  color: var(--juwo-primary, #ff5824);
}

.row-text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.row-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary, #111827);
}

.row-sub {
  font-size: 12px;
  color: var(--color-text-secondary, #6b7280);
  margin-top: 2px;
}

.row-right {
  display: flex;
  align-items: center;
}

.pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: 1px solid var(--color-border-default, #e5e7eb);
  border-radius: 999px;
  background: #fff;
  color: var(--color-text-secondary, #6b7280);
}

.pill.selected {
  background: var(--juwo-primary, #ff5824);
  border-color: var(--juwo-primary, #ff5824);
  color: #fff;
}

.pill-icon {
  width: 16px;
  height: 16px;
}

/* 空/加载 */
.loading, .empty {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px;
  color: var(--color-text-secondary, #6b7280);
  font-size: 13px;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #e5e7eb;
  border-top-color: var(--juwo-primary, #ff5824);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 锁定 body 滚动（通过类名控制） */
:global(body.srh-overlay-open) {
  overflow: hidden;
}
</style>
