<template>
  <!-- 严格参考 1.html：标题+清除条件（含计数徽章）/ 已选chips / 热门标签 / A-Z 列表 + 右侧索引 / 底部确定 -->
  <div class="mobile-area-sheet">
    <!-- Header -->
    <div class="modal-header">
      <span class="title">
        按照位置搜索：
        <span v-show="selectedCount > 0" class="badge">{{ selectedCount }}</span>
      </span>
      <button class="clear-button" type="button" @click="onClear">清除条件</button>
    </div>

    <!-- Content -->
    <div class="modal-content">
      <!-- 已选 chips（与 1.html 一致：可移除 ×） -->
      <div class="selected-districts-display" v-show="selectedList.length > 0">
        <div
          v-for="loc in selectedList"
          :key="loc.id"
          class="selected-district-tag"
        >
          {{ loc.name }}
          <i class="remove-tag-btn" @click="removeOne(loc.id)">×</i>
        </div>
      </div>

      <div class="district-selection-container">
        <div class="district-panels" ref="panelsRef">
          <!-- 热门区域 -->
          <div class="hot-districts-section">
            <h3 class="hot-districts-title">热门区域</h3>
            <div class="hot-districts-tags">
              <div
                v-for="name in hotList"
                :key="name"
                class="hot-district-tag"
                :class="{ selected: isSelectedName(name) }"
                @click="toggleByName(name)"
              >
                {{ name }}
              </div>
            </div>
          </div>

          <!-- A-Z 列表（用现有 AreasSelector，但强制显示分组标题） -->
          <div class="areas-wrapper">
            <AreasSelector
              :selected="draftSelected"
              @update:selected="onUpdateSelected"
              @requestCount="noop"
            />
          </div>
        </div>

        <!-- 右侧字母索引 -->
        <div class="alphabetical-index">
          <a
            v-for="L in letters"
            :key="L"
            class="index-letter"
            href="#"
            @click.prevent="jump(L)"
          >{{ L }}</a>
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
  移动端“位置”面板（严格对齐 1.html 的结构与行为）：
  - 标题“按照位置搜索：” + 计数徽章 + “清除条件”
  - 已选chips（可逐个移除）
  - 热门区域（固定清单，优先验证原型交互）
  - A-Z 分组列表（复用 AreasSelector，但强制显示分组标题；搜索框/清空保留）
  - 右侧字母索引 A…Z，点击滚动到对应分组
  - 底部“确定”按钮，应用筛选（与 AreaFilterPanel 的 applyFilters 一致）
*/
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import AreasSelector from '@/components/AreasSelector.vue'
import { usePropertiesStore } from '@/stores/properties'
import { canonicalizeArea, canonicalIdOf } from '@/utils/areas'
import { sanitizeQueryParams, isSameQuery } from '@/utils/query'

const emit = defineEmits(['close'])
const router = useRouter()
const store = usePropertiesStore()

// 草稿选中（与 AreaFilterPanel 一致，打开即从已应用初始化）
const draftSelected = computed(() => store.draftSelectedLocations || [])
const selectedList = computed(() =>
  (draftSelected.value || []).map((l) => canonicalizeArea(l)).filter(Boolean),
)
const selectedCount = computed(() => selectedList.value.length)

// 右侧字母索引（A-Z）
const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('')
const panelsRef = ref(null)

// 热门清单（参考 1.html）
const hotList = [
  'Burwood', 'Chippendale', 'Haymarket',
  'Kensington', 'Macquarie Park', 'Mascot',
  'Rosebery', 'Sydney', 'Ultimo',
  'Waterloo', 'Wolli Creek', 'Zetland',
]

// 选中/取消（按名称）
const isSelectedName = (name) => {
  const id = canonicalIdOf({ id: `suburb_${name}`, type: 'suburb', name })
  return (draftSelected.value || []).some((l) => canonicalIdOf(l) === id)
}
const toggleByName = (name) => {
  const id = canonicalIdOf({ id: `suburb_${name}`, type: 'suburb', name })
  const curr = Array.isArray(draftSelected.value) ? [...draftSelected.value] : []
  const idx = curr.findIndex((l) => canonicalIdOf(l) === id)
  if (idx >= 0) curr.splice(idx, 1)
  else curr.push({ id: `suburb_${name}`, type: 'suburb', name, fullName: name })
  store.setDraftSelectedLocations(curr)
}

const removeOne = (id) => {
  const curr = Array.isArray(draftSelected.value) ? [...draftSelected.value] : []
  const idx = curr.findIndex((l) => canonicalIdOf(l) === String(id))
  if (idx >= 0) {
    curr.splice(idx, 1)
    store.setDraftSelectedLocations(curr)
  }
}

const onClear = () => {
  store.setDraftSelectedLocations([])
}

const onUpdateSelected = (newList) => {
  store.setDraftSelectedLocations(Array.isArray(newList) ? newList : [])
}

const noop = () => {}

// 跳转到字母分组（依赖 AreasSelector 中的分组标题 id="group-X"）
const jump = (letter) => {
  const root = panelsRef.value
  if (!root) return
  const listRoot = root.querySelector('.areas-wrapper')
  if (!listRoot) return
  const target = listRoot.querySelector(`#group-${letter}`)
  const scrollHost = root.querySelector('.district-panels')
  if (target && scrollHost) {
    // 计算相对于滚动容器的偏移
    const hostTop = scrollHost.getBoundingClientRect().top
    const targetTop = target.getBoundingClientRect().top
    const delta = targetTop - hostTop
    scrollHost.scrollTop += delta
  }
}

// 应用：构造参数并调用 store.applyFilters，更新 URL，关闭
const buildFilterParams = () => {
  const arr = selectedList.value
  const suburbs = arr
    .filter((l) => l.type === 'suburb')
    .map((l) => l.name)
    .filter(Boolean)
  const params = {}
  if (suburbs.length > 0) params.suburb = suburbs.join(',')
  return params
}

const updateUrlQuery = async (filterParams) => {
  try {
    const currentQuery = { ...(router.currentRoute.value.query || {}) }
    const merged = { ...currentQuery }

    if (filterParams.suburb) merged.suburb = filterParams.suburb
    else delete merged.suburb

    // 清理 include_nearby 等非本面板键
    delete merged.include_nearby

    const nextQuery = sanitizeQueryParams(merged)
    const currQuery = sanitizeQueryParams(currentQuery)
    if (!isSameQuery(currQuery, nextQuery)) {
      await router.replace({ query: nextQuery })
    }
  } catch (e) {
    console.warn('同步 URL 查询参数失败:', e)
  }
}

const onConfirm = async () => {
  try {
    const p = buildFilterParams()
    // 草稿应用为已应用（与 AreaFilterPanel 一致）
    try { store.applySelectedLocations() } catch { /* ignore */ }
    await store.applyFilters(p, { sections: ['area'] })
    await updateUrlQuery(p)
    // 清理预览草稿
    try { store.clearPreviewDraft('area') } catch { /* ignore */ }
    emit('close')
  } catch (e) {
    console.error('应用区域筛选失败:', e)
  }
}

onMounted(async () => {
  try { store.resetDraftSelectedLocations() } catch { /* ignore */ }
  // 预加载区域目录（滚动前确保分组节点渲染）
  await store.getAllAreas?.()
  await nextTick()
})
</script>

<style scoped>
/* 结构样式严格参照 1.html */

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

.badge {
  background-color: var(--juwo-primary);
  color: #fff;
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 12px;
  margin-left: 6px;
}

.modal-content {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* 已选 chips */
.selected-districts-display {
  padding: 16px;
  border-bottom: 1px solid var(--color-border-default);
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.selected-district-tag {
  background-color: #e6f9f9;       /* 贴近 1.html 的浅青 */
  color: var(--juwo-primary);
  padding: 6px 10px;
  border-radius: 4px;
  font-size: 14px;
  display: flex;
  align-items: center;
}
.remove-tag-btn {
  margin-left: 8px;
  cursor: pointer;
  font-style: normal;
  font-weight: bold;
}

/* 主体滚动区域 */
.district-selection-container {
  position: relative;
  flex-grow: 1;
  display: flex;
  overflow: hidden;
}
.district-panels {
  flex-grow: 1;
  overflow-y: auto;
  padding: 0 16px;
}

/* 热门 */
.hot-districts-section {
  padding: 16px 0;
}
.hot-districts-title {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin-bottom: 12px;
}
.hot-districts-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.hot-district-tag {
  padding: 6px 12px;
  background-color: var(--color-bg-secondary, #f8f9fa);
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  border: 1px solid var(--color-bg-secondary, #f8f9fa);
}
.hot-district-tag.selected {
  background-color: #e6f9f9;
  color: var(--juwo-primary);
  border-color: var(--juwo-primary);
}

/* 右侧字母索引 */
.alphabetical-index {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 4px;
}
.index-letter {
  font-size: 12px;
  color: var(--color-text-secondary);
  padding: 2px;
  cursor: pointer;
  text-decoration: none;
}

/* 底部确定按钮 */
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

/* 强制显示 AreasSelector 的分组标题，并保持 1.html 风格 */
.areas-wrapper :deep(.group-title) {
  display: block !important;
  padding: 12px 4px;
  font-size: 16px;
  font-weight: 500;
  color: var(--color-text-primary);
  background-color: var(--color-bg-primary);
}

/* 行为贴近 1.html：列表项更紧凑、hover 高亮 */
.areas-wrapper :deep(.area-row) {
  padding: 14px 8px;
}
</style>
