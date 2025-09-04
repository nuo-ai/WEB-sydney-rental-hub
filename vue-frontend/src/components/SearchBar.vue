<template>
  <div class="search-bar-container">
    <!-- 选中的区域标签 -->
    <div v-if="selectedLocations.length > 0" class="location-tags">
      <span 
        v-for="location in selectedLocations" 
        :key="location.id"
        class="location-tag"
      >
        <i class="fa-solid fa-map-marker-alt"></i>
        <span>{{ location.name }}</span>
        <button 
          class="remove-location-btn"
          @click="removeLocation(location.id)"
        >
          <i class="fa-solid fa-times"></i>
        </button>
      </span>
    </div>

    <!-- 搜索输入框 -->
    <div class="search-input-container">
      <el-input
        v-model="searchQuery"
        :placeholder="searchPlaceholder"
        clearable
        size="large"
        class="search-input"
        @input="handleInput"
        @keydown="handleKeydown"
        @focus="handleFocus"
      >
        <template #prefix>
          <i class="fa-solid fa-magnifying-glass search-icon"></i>
        </template>
      </el-input>

      <!-- 自动补全建议列表 -->
      <div 
        v-if="showSuggestions && (filteredSuggestions.length > 0 || nearbySuggestions.length > 0 || isLoadingSuggestions)" 
        class="location-suggestions"
      >
        <!-- 搜索结果 -->
        <div v-if="searchQuery && (filteredSuggestions.length > 0 || isLoadingSuggestions)">
          <div v-if="filteredSuggestions.length > 0" class="suggestions-section-title">
            <i class="fa-solid fa-magnifying-glass"></i>
            搜索结果
          </div>
          <div
            v-for="(suggestion, index) in filteredSuggestions"
            :key="suggestion.id"
            class="suggestion-item"
            :class="{ 'active': currentSuggestionIndex === index }"
            @click="selectLocation(suggestion)"
          >
            <div class="suggestion-content">
              <i :class="suggestion.type === 'suburb' ? 'fa-solid fa-map-marker-alt' : 'fa-solid fa-hashtag'" class="suggestion-icon"></i>
              <div class="suggestion-text">
                <div class="suggestion-name">{{ suggestion.fullName }}</div>
                <div class="suggestion-count">{{ suggestion.count }} 套房源</div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 相邻区域推荐 -->
        <div v-if="!searchQuery && nearbySuggestions.length > 0">
          <div class="suggestions-section-title">
            <i class="fa-solid fa-lightbulb"></i>
            SUGGESTED FOR YOU
          </div>
          <div class="nearby-suggestions-grid">
            <div
              v-for="suggestion in nearbySuggestions"
              :key="suggestion.id"
              class="nearby-suggestion-item"
              @click="selectLocation(suggestion)"
            >
              <i class="fa-solid fa-circle-dot"></i>
              <span class="nearby-name">{{ suggestion.name }}, NSW, {{ suggestion.postcode }}</span>
            </div>
          </div>
        </div>
        
        <!-- 加载中状态 -->
        <div v-if="isLoadingSuggestions" class="loading-suggestions">
          <i class="fa-solid fa-spinner fa-spin"></i>
          搜索中...
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { usePropertiesStore } from '@/stores/properties'
import { locationAPI } from '@/services/api'

// 组件事件
const emit = defineEmits(['search', 'locationSelected'])

// 状态管理
const propertiesStore = usePropertiesStore()

// 响应式数据
const searchQuery = ref('')
const showSuggestions = ref(false)
const currentSuggestionIndex = ref(-1)
const locationSuggestions = ref([])
const nearbySuggestions = ref([])
const isLoadingSuggestions = ref(false)

// 计算属性
const selectedLocations = computed(() => propertiesStore.selectedLocations)

const searchPlaceholder = computed(() => {
  if (selectedLocations.value.length > 0) {
    return '继续搜索区域或邮编...'
  }
  return '输入区域或邮编，例如 "Ultimo" 或 "2007"'
})

// 删除这行，改为使用响应式数据
// const locationSuggestions = computed(() => propertiesStore.locationSuggestions)

const filteredSuggestions = computed(() => {
  // 过滤掉已经选择的区域，避免重复显示
  return locationSuggestions.value.filter(suggestion => {
    // 检查该建议是否已经在选中的区域列表中
    return !selectedLocations.value.some(selected => selected.id === suggestion.id)
  })
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
    const results = await locationAPI.getSuggestions(query, 10)
    locationSuggestions.value = results
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
    // 过滤掉已经选择的区域，避免重复显示
    const nearbyResults = result.nearby || []
    nearbySuggestions.value = nearbyResults.filter(suggestion => {
      // 检查该建议是否已经在选中的区域列表中
      return !selectedLocations.value.some(selected => 
        selected.id === suggestion.id || 
        (selected.name === suggestion.name && selected.postcode === suggestion.postcode)
      )
    })
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

const debouncedTextSearch = debounce((query) => {
  propertiesStore.setSearchQuery(query)
  emit('search', query)
}, 500)

// 事件处理
const handleFocus = () => {
  showSuggestions.value = true
  // 如果没有输入内容且有选中的区域，加载相邻区域推荐
  if (!searchQuery.value && selectedLocations.value.length > 0) {
    loadNearbySuggestions()
  }
}

const handleInput = (value) => {
  searchQuery.value = value
  currentSuggestionIndex.value = -1
  
  if (selectedLocations.value.length === 0) {
    showSuggestions.value = true
    debouncedSearch(value) // 调用API搜索
  } else {
    // 有选中区域时，进行文本搜索
    debouncedTextSearch(value)
    showSuggestions.value = false
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
          suggestions.length - 1
        )
      }
      break
      
    case 'ArrowUp':
      event.preventDefault()
      if (suggestions.length > 0) {
        currentSuggestionIndex.value = Math.max(
          currentSuggestionIndex.value - 1, 
          -1
        )
      }
      break
      
    case 'Enter':
      event.preventDefault()
      if (currentSuggestionIndex.value >= 0 && suggestions[currentSuggestionIndex.value]) {
        selectLocation(suggestions[currentSuggestionIndex.value])
      } else if (selectedLocations.value.length === 0 && searchQuery.value.trim()) {
        // 直接搜索
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
  // 检查是否已经选中
  const existingIndex = selectedLocations.value.findIndex(loc => loc.id === location.id)
  if (existingIndex !== -1) return

  propertiesStore.addSelectedLocation(location)
  searchQuery.value = ''
  showSuggestions.value = false
  currentSuggestionIndex.value = -1
  locationSuggestions.value = [] // 清空搜索结果
  
  emit('locationSelected', location)
  
  // 加载相邻区域建议
  await loadNearbySuggestions()
}

const removeLocation = async (locationId) => {
  propertiesStore.removeSelectedLocation(locationId)
  
  // 触发重新搜索，传递一个特殊标记表示是移除操作
  emit('locationSelected', { removed: true })
  
  // 重新加载相邻区域建议
  await loadNearbySuggestions()
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
  
  // 初始化时不再加载所有区域数据，改为按需搜索
  // 这样可以避免加载大量数据到前端
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// 监听属性变化
watch(() => propertiesStore.searchQuery, (newQuery) => {
  if (searchQuery.value !== newQuery) {
    searchQuery.value = newQuery
  }
})
</script>

<style scoped>
/* 搜索栏容器 */
.search-bar-container {
  position: relative;
  width: 100%;
}

/* 区域标签样式 */
.location-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 8px;
}

.location-tag {
  background: var(--juwo-primary);
  color: white;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  padding: 6px 12px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}

.location-tag:hover {
  background: var(--juwo-primary-dark);
}

.remove-location-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.8);
  cursor: pointer;
  font-size: 12px;
  padding: 2px;
  border-radius: 2px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
}

.remove-location-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

/* 搜索输入框 */
.search-input-container {
  position: relative;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 6px;
  border: 1px solid var(--color-border-default);
  transition: all 0.2s ease;
}

.search-input :deep(.el-input__wrapper):hover {
  border-color: var(--juwo-primary);
}

.search-input :deep(.el-input__wrapper.is-focus) {
  border-color: var(--juwo-primary);
  box-shadow: 0 0 0 4px rgba(255, 88, 36, 0.1);
}

.search-icon {
  color: var(--color-text-secondary);
  font-size: 16px;
}

/* 自动补全建议列表 */
.location-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  max-height: 300px;
  overflow-y: auto;
  z-index: 1000;
  margin-top: 4px;
}

.suggestion-item {
  padding: 12px 16px;
  border-bottom: 1px solid #f1f1f1;
  cursor: pointer;
  transition: all 0.2s ease;
}

.suggestion-item:last-child {
  border-bottom: none;
}

.suggestion-item:hover,
.suggestion-item.active {
  background-color: var(--juwo-primary-50);
  color: var(--juwo-primary);
}

.suggestion-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.suggestion-icon {
  color: var(--juwo-primary);
  font-size: 14px;
  width: 16px;
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

/* 新增：区域标题样式 */
.suggestions-section-title {
  padding: 8px 16px;
  font-size: 11px;
  font-weight: 600;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: #f8f8f8;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  gap: 6px;
}

.suggestions-section-title i {
  font-size: 12px;
  color: #999;
}

/* 新增：相邻区域网格布局 */
.nearby-suggestions-grid {
  padding: 12px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.nearby-suggestion-item {
  padding: 10px 12px;
  border: 1px solid #e5e5e5;
  border-radius: 20px;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.nearby-suggestion-item:hover {
  background: var(--juwo-primary-50);
  border-color: var(--juwo-primary);
  color: var(--juwo-primary);
}

.nearby-suggestion-item i {
  font-size: 8px;
  color: var(--juwo-primary);
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
  color: #999;
  font-size: 13px;
}

.loading-suggestions i {
  margin-right: 8px;
}

/* 响应式适配 */
@media (max-width: 767px) {
  .search-bar-container {
    width: 100%;
  }
  
  .location-suggestions {
    margin-left: -16px;
    margin-right: -16px;
    border-radius: 0;
    border-left: none;
    border-right: none;
  }
  
  .location-tags {
    margin-left: -4px;
    margin-right: -4px;
  }
  
  .suggestion-item {
    padding: 16px;
  }
}
</style>
