<template>
  <el-dialog
    v-model="visible"
    fullscreen
    :show-close="false"
    class="add-location-modal"
    :append-to-body="true"
  >
    <template #header>
      <div class="modal-header">
        <button class="close-btn" @click="handleClose">
          <i class="fas fa-times"></i>
        </button>
        <h2 class="modal-title">Add location</h2>
      </div>
    </template>

    <div class="modal-content">
      <!-- 搜索区域 -->
      <div class="search-section">
        <div class="search-input-wrapper">
          <i class="fas fa-search search-icon"></i>
          <input
            ref="searchInput"
            v-model="searchQuery"
            type="text"
            class="search-input"
            placeholder="Address"
            @input="handleInput"
          />
          <button v-if="searchQuery" class="clear-btn" @click="clearSearch">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <p class="search-hint">Search for your location's address</p>
      </div>

      <!-- 搜索结果 -->
      <div class="search-results">
        <!-- 预设地址 -->
        <div v-if="!searchQuery && presetLocations.length > 0" class="preset-section">
          <h3 class="section-title">Popular locations</h3>
          <div
            v-for="location in presetLocations"
            :key="location.place_id || location.placeId"
            class="result-item"
            @click="selectLocation(location)"
          >
            <i class="fas fa-graduation-cap" v-if="location.type === 'university'"></i>
            <i class="fas fa-train" v-else-if="location.type === 'station'"></i>
            <i class="fas fa-map-marker-alt" v-else></i>
            <div class="result-info">
              <div class="result-name">{{ location.name }}</div>
              <div class="result-address">{{ location.address }}</div>
            </div>
          </div>
        </div>

        <!-- 搜索建议 -->
        <div v-else-if="searchResults.length > 0" class="results-list">
          <div
            v-for="result in searchResults"
            :key="result.place_id"
            class="result-item"
            @click="selectResult(result)"
          >
            <i class="fas fa-map-marker-alt"></i>
            <div class="result-info">
              <div class="result-address">{{ result.description }}</div>
            </div>
          </div>
        </div>

        <!-- 搜索中 -->
        <div v-else-if="isSearching" class="searching-state">
          <i class="fas fa-spinner fa-spin"></i>
          <span>Searching...</span>
        </div>

        <!-- 无结果 -->
        <div v-else-if="searchQuery && !isSearching" class="no-results">
          <i class="fas fa-search"></i>
          <p>No results found</p>
          <p class="no-results-hint">Try a different search term</p>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import placesService from '@/services/places'
import universities from '@/data/universities.sydney.json'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue', 'select'])

// 响应式状态
const visible = ref(props.modelValue)
const searchInput = ref(null)
const searchQuery = ref('')
const searchResults = ref([])
const isSearching = ref(false)
const searchTimeout = ref(null)

// 预设地址（澳洲常用地点）
const presetLocations = ref([])

// Session token for Google Places API billing optimization
let sessionToken = null

// 监听props变化
watch(
  () => props.modelValue,
  (newVal) => {
    visible.value = newVal
    if (newVal) {
      // 聚焦输入框
      nextTick(() => {
        searchInput.value?.focus()
      })
    }
  },
)

// 监听visible变化
watch(visible, (newVal) => {
  emit('update:modelValue', newVal)
})

// Use Google Places Autocomplete API
const searchPlaces = async (query) => {
  try {
    // Create a new session token if needed
    if (!sessionToken) {
      sessionToken = placesService.createSessionToken()
    }

    const results = await placesService.searchPlaces(query, sessionToken)
    return results
  } catch (error) {
    console.error('Places search error:', error)
    ElMessage.error('Failed to search locations. Please try again.')
    return []
  }
}

// 处理输入
const handleInput = () => {
  // 清除之前的定时器
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }

  // 如果搜索框为空，显示预设地址
  if (!searchQuery.value.trim()) {
    searchResults.value = []
    isSearching.value = false
    return
  }

  // 延迟搜索（防抖）
  isSearching.value = true
  searchTimeout.value = setTimeout(async () => {
    try {
      const results = await searchPlaces(searchQuery.value)
      // 仅保留“大学”类型；若无，则用本地大学清单做模糊匹配降级
      let filtered = (results || []).filter(
        (r) => Array.isArray(r.types) && r.types.includes('university'),
      )
      if (filtered.length === 0) {
        const q = searchQuery.value.toLowerCase()
        filtered = universities
          .filter((u) =>
            (u.name + ' ' + (u.campus || '') + ' ' + u.address).toLowerCase().includes(q),
          )
          .slice(0, 8)
          .map((u) => ({
            place_id: u.placeId || `local-${u.id}`,
            description: `${u.name}${u.campus ? ' (' + u.campus + ')' : ''}, ${u.address}`,
            types: ['university'],
          }))
      }
      searchResults.value = filtered
    } catch (error) {
      console.error('Search failed:', error)
      searchResults.value = []
    } finally {
      isSearching.value = false
    }
  }, 300)
}

// 清空搜索
const clearSearch = () => {
  searchQuery.value = ''
  searchResults.value = []
  isSearching.value = false
  searchInput.value?.focus()
}

// 选择预设地址
const selectLocation = (location) => {
  const formattedLocation = {
    place_id: location.place_id,
    formatted_address: location.formatted_address,
    name: location.name,
    geometry: {
      location: {
        lat: () => location.latitude,
        lng: () => location.longitude,
      },
    },
  }
  emit('select', formattedLocation)
  handleClose()
}

// 选择搜索结果
const selectResult = async (result) => {
  try {
    isSearching.value = true

    let placeDetails
    // 本地大学项（无 Google placeId）走离线详情
    if (String(result.place_id).startsWith('local-')) {
      const localId = String(result.place_id).replace('local-', '')
      const u = universities.find((x) => x.id === localId)
      if (!u) {
        throw new Error('Local university not found')
      }
      placeDetails = {
        place_id: u.placeId || `local-${u.id}`,
        name: u.campus ? `${u.name} (${u.campus})` : u.name,
        formatted_address: u.address,
        latitude: u.lat,
        longitude: u.lng,
        types: ['university'],
      }
    } else {
      // 在线详情，且仅允许 university
      placeDetails = await placesService.getPlaceDetails(result.place_id)
      if (!Array.isArray(placeDetails.types) || !placeDetails.types.includes('university')) {
        ElMessage.warning('Please select a university')
        isSearching.value = false
        return
      }
    }

    const formattedLocation = {
      place_id: placeDetails.place_id,
      formatted_address: placeDetails.formatted_address,
      name: placeDetails.name || result.main_text || result.description.split(',')[0],
      geometry: {
        location: {
          lat: () => placeDetails.latitude,
          lng: () => placeDetails.longitude,
        },
      },
    }

    // Reset session token after selection (Google billing optimization)
    sessionToken = null

    emit('select', formattedLocation)
    handleClose()
  } catch (error) {
    console.error('Failed to get place details:', error)
    ElMessage.error('Failed to get location details. Please try again.')
  } finally {
    isSearching.value = false
  }
}

// 关闭模态框
const handleClose = () => {
  visible.value = false
  // 重置状态
  searchQuery.value = ''
  searchResults.value = []
  isSearching.value = false
  // Reset session token
  sessionToken = null
}

// 生命周期
onMounted(async () => {
  // 加载本地“大学/校区”清单作为热门项（只含大学，去除非大学）
  presetLocations.value = universities.map((u) => ({
    place_id: u.placeId || `local-${u.id}`,
    placeId: u.placeId || `local-${u.id}`,
    name: u.campus ? `${u.name} (${u.campus})` : u.name,
    formatted_address: u.address,
    address: u.address,
    latitude: u.lat,
    longitude: u.lng,
    type: 'university',
  }))

  // 预加载 Google Maps API（若可用）
  try {
    await placesService.loadGoogleMaps()
  } catch {
    // Google Places API未加载 - 使用本地热门清单降级
  }
})
</script>

<style scoped>
.add-location-modal :deep(.el-dialog__header) {
  padding: 0;
  margin: 0;
}

.add-location-modal :deep(.el-dialog__body) {
  padding: 0;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 顶部导航 */
.modal-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: white;
  padding: 20px;
  border-bottom: 1px solid #e3e3e3;
  display: flex;
  align-items: center;
  gap: 16px;
}

.close-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: none;
  color: #666;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s;
}

.close-btn:hover {
  background: #f5f5f5;
}

.modal-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

/* 内容区域 */
.modal-content {
  flex: 1;
  overflow-y: auto;
}

/* 搜索区域 */
.search-section {
  padding: 20px;
  background: white;
  border-bottom: 1px solid #e3e3e3;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 16px;
  color: #999;
  font-size: 16px;
}

.search-input {
  width: 100%;
  height: 48px;
  padding: 0 40px 0 44px;
  border: 1px solid #e3e3e3;
  border-radius: 8px;
  font-size: 16px;
  color: #333;
  transition: border-color 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #999;
}

.search-input::placeholder {
  color: #999;
}

.clear-btn {
  position: absolute;
  right: 12px;
  width: 28px;
  height: 28px;
  border: none;
  background: none;
  color: #999;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s;
}

.clear-btn:hover {
  background: #f5f5f5;
}

.search-hint {
  margin: 8px 0 0 0;
  font-size: 14px;
  color: #999;
}

/* 搜索结果 */
.search-results {
  flex: 1;
  background: #fafafa;
}

/* 预设地址 */
.preset-section {
  padding: 20px;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #666;
  margin: 0 0 12px 0;
  text-transform: uppercase;
}

/* 结果列表 */
.results-list {
  background: white;
}

.result-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: white;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background 0.2s;
}

.result-item:hover {
  background: #f8f8f8;
}

.result-item:active {
  background: #f0f0f0;
}

.result-item i {
  flex-shrink: 0;
  width: 20px;
  color: #999;
  font-size: 16px;
  text-align: center;
}

.result-info {
  flex: 1;
  min-width: 0;
}

.result-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.result-address {
  font-size: 15px;
  color: #333;
  line-height: 1.4;
}

/* 状态 */
.searching-state,
.no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
  color: #999;
}

.searching-state i,
.no-results i {
  font-size: 32px;
  margin-bottom: 16px;
}

.no-results p {
  margin: 4px 0;
  font-size: 16px;
}

.no-results-hint {
  font-size: 14px !important;
  color: #bbb;
}

/* 动画 */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.fa-spin {
  animation: spin 1s linear infinite;
}
</style>
