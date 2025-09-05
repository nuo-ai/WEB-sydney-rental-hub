<template>
  <div class="commute-times-page">
    <!-- 顶部导航 -->
    <header class="page-header">
      <button class="back-btn" @click="handleBack">
        <i class="fas fa-arrow-left"></i>
      </button>
      <h1 class="page-title">Location</h1>
    </header>

    <!-- 地图区域 -->
    <section class="map-section">
      <SimpleMap
        v-if="propertyCoordinates"
        :latitude="propertyCoordinates.lat"
        :longitude="propertyCoordinates.lng"
        :height="'40vh'"
        :zoom="13"
        :marker-title="fullAddress"
      />
      <div v-else class="map-placeholder">
        <el-icon :size="32"><Location /></el-icon>
        <span>Loading map...</span>
      </div>
    </section>

    <!-- Travel Time 区域 -->
    <section class="travel-time-section">
      <h2 class="section-title">Travel Time</h2>
      <p class="from-address">From {{ fullAddress }}</p>

      <!-- 交通方式选择 -->
      <TransportModes v-model="selectedMode" @change="handleModeChange" />

      <!-- 地址列表 -->
      <div class="locations-list">
        <!-- 用户保存的地址 -->
        <LocationCard
          v-for="location in userLocations"
          :key="location.id"
          :location="location"
          :mode="selectedMode"
          :from="propertyCoordinates"
          @remove="removeLocation"
        />

        <!-- 空状态 -->
        <div v-if="userLocations.length === 0" class="empty-state">
          <i class="fas fa-map-marked-alt"></i>
          <p>No saved locations yet</p>
          <p class="empty-hint">Add your frequent destinations to see travel times</p>
        </div>
      </div>

      <!-- 添加地址按钮 -->
      <button class="add-location-btn" @click="showAddModal = true">
        <i class="fas fa-plus"></i>
        <span>Add location</span>
      </button>
    </section>

    <!-- 模态框 -->
    <AddLocationModal v-if="showAddModal" v-model="showAddModal" @select="handleAddressSelected" />

    <NameLocationModal
      v-if="showNameModal"
      v-model="showNameModal"
      :address="selectedAddress"
      @confirm="saveLocation"
      @skip="saveLocation"
      @back="handleNameModalBack"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCommuteStore } from '@/stores/commute'
import { Location } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

import SimpleMap from '@/components/SimpleMap.vue'
import TransportModes from '@/components/commute/TransportModes.vue'
import LocationCard from '@/components/commute/LocationCard.vue'
import AddLocationModal from '@/components/modals/AddLocationModal.vue'
import NameLocationModal from '@/components/modals/NameLocationModal.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const commuteStore = useCommuteStore()

// 从路由参数获取房源信息
const propertyId = ref(route.query.propertyId)
const propertyAddress = ref(route.query.address)
const propertySuburb = ref(route.query.suburb)
const propertyLat = ref(parseFloat(route.query.lat))
const propertyLng = ref(parseFloat(route.query.lng))

// 响应式状态
const selectedMode = ref('DRIVING')
const showAddModal = ref(false)
const showNameModal = ref(false)
const selectedAddress = ref(null)

// 计算属性
const fullAddress = computed(() => {
  if (propertyAddress.value && propertySuburb.value) {
    return `${propertyAddress.value}, ${propertySuburb.value}`
  }
  return propertyAddress.value || 'Property address'
})

const propertyCoordinates = computed(() => {
  if (propertyLat.value && propertyLng.value) {
    return {
      lat: propertyLat.value,
      lng: propertyLng.value,
    }
  }
  return null
})

const userLocations = computed(() => authStore.savedAddresses)

// 方法
const handleBack = () => {
  router.back()
}

const handleModeChange = (mode) => {
  selectedMode.value = mode
  commuteStore.setTransportMode(mode)
}

const handleAddressSelected = (address) => {
  showAddModal.value = false
  selectedAddress.value = address
  showNameModal.value = true
}

const saveLocation = async (data) => {
  try {
    // 获取经纬度（处理函数和值两种情况）
    let lat, lng
    if (typeof data.address.geometry.location.lat === 'function') {
      lat = data.address.geometry.location.lat()
      lng = data.address.geometry.location.lng()
    } else {
      lat = data.address.geometry.location.lat
      lng = data.address.geometry.location.lng
    }

    // 保存地址到用户账户
    await authStore.saveUserAddress({
      address: data.address.formatted_address,
      label: data.label,
      placeId: data.address.place_id,
      latitude: lat,
      longitude: lng,
    })

    showNameModal.value = false
    selectedAddress.value = null

    ElMessage.success('Location added successfully!')
  } catch (error) {
    console.error('Error saving location:', error)
    ElMessage.error('Failed to save location')
  }
}

// saveLocationWithoutLabel 函数已被移除，skip事件现在直接调用saveLocation

const handleNameModalBack = () => {
  // 关闭名称模态框，重新打开地址选择模态框
  showNameModal.value = false
  selectedAddress.value = null
  setTimeout(() => {
    showAddModal.value = true
  }, 300)
}

const removeLocation = async (locationId) => {
  try {
    await authStore.removeUserAddress(locationId)
    ElMessage.success('Location removed')
  } catch (error) {
    console.error('Failed to remove location', error)
    ElMessage.error('Failed to remove location')
  }
}

// 生命周期
onMounted(() => {
  // 测试模式：跳过登录检查
  const isTest = authStore.testMode

  // 检查是否登录
  if (!isTest && !authStore.isAuthenticated) {
    ElMessage.warning('Please login to access this feature')
    router.push('/')
    return
  }

  // 设置当前房源信息到store
  if (propertyCoordinates.value) {
    commuteStore.setCurrentProperty({
      id: propertyId.value,
      address: fullAddress.value,
      coordinates: propertyCoordinates.value,
    })
  }

  // 加载用户保存的地址（在测试模式下会加载模拟数据）
  authStore.loadUserAddresses()
})
</script>

<style scoped>
.commute-times-page {
  min-height: 100vh;
  background: white;
  display: flex;
  flex-direction: column;
}

/* 顶部导航 */
.page-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: white;
  border-bottom: 1px solid #e3e3e3;
  padding: 12px 16px;
  padding-top: calc(12px + env(safe-area-inset-top));
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: none;
  color: #333;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s;
}

.back-btn:hover {
  background: #f5f5f5;
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

/* 地图区域 */
.map-section {
  height: 40vh;
  position: relative;
  border-bottom: 1px solid #e3e3e3;
}

.map-placeholder {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: #999;
  background: #f5f5f5;
}

/* Travel Time 区域 */
.travel-time-section {
  flex: 1;
  padding: 20px 16px;
  padding-bottom: calc(20px + env(safe-area-inset-bottom));
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: #333;
  margin: 0 0 8px 0;
}

.from-address {
  font-size: 14px;
  color: #666;
  margin: 0 0 20px 0;
}

/* 地址列表 */
.locations-list {
  margin: 20px 0;
  min-height: 200px;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

.empty-state i {
  font-size: 48px;
  margin-bottom: 16px;
  color: #ddd;
}

.empty-state p {
  margin: 8px 0;
  font-size: 16px;
}

.empty-hint {
  font-size: 14px !important;
  color: #bbb;
}

/* 添加地址按钮 */
.add-location-btn {
  width: 100%;
  height: 48px;
  border: 1px solid #dc2626;
  border-radius: 8px;
  background: white;
  color: #dc2626;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
  margin-top: auto;
}

.add-location-btn:hover {
  background: #fef2f2;
}

.add-location-btn:active {
  transform: translateY(1px);
}

.add-location-btn i {
  font-size: 14px;
}

/* 响应式设计 */
@media (min-width: 768px) {
  .travel-time-section {
    max-width: 640px;
    margin: 0 auto;
    width: 100%;
  }
}
</style>
