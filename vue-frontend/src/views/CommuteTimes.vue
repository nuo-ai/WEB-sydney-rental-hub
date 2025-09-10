<template>
  <div class="commute-times-page">
    <!-- 顶部导航 -->
    <header class="page-header">
      <button class="back-btn" @click="handleBack">
        <ArrowLeft class="spec-icon" />
      </button>
      <h1 class="page-title typo-heading-card">{{ $t('commute.pageTitle') }}</h1>
    </header>

    <!-- 地图区域 -->
    <section class="map-section">
      <GoogleMap
        v-if="propertyCoordinates"
        :latitude="propertyCoordinates.lat"
        :longitude="propertyCoordinates.lng"
        :height="'40vh'"
        :zoom="13"
        :marker-title="fullAddress"
        :route="routeData"
        :route-endpoints="routeEndpoints"
        :auto-fit="true"
        :fit-padding="24"
        :route-label-text="routeLabelText"
      />
      <div v-else class="map-placeholder">
        <MapPin class="spec-icon map-placeholder-icon" />
        <span class="typo-body-sm">{{ $t('commute.mapLoading') }}</span>
      </div>
    </section>

    <!-- Travel Time 区域 -->
    <section class="travel-time-section">
      <h2 class="section-title typo-heading-card">{{ $t('commute.sectionTitle') }}</h2>
      <p class="from-address typo-body">{{ $t('commute.fromPrefix') }} {{ fullAddress }}</p>

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
          <MapPin class="spec-icon empty-icon" />
          <p class="typo-body">{{ $t('commute.emptyTitle') }}</p>
          <p class="empty-hint typo-body-sm">{{ $t('commute.emptyHint') }}</p>
        </div>
      </div>

      <!-- 添加地址按钮 -->
      <button class="add-location-btn" @click="showAddModal = true">
        <Plus class="spec-icon" />
        <span class="typo-button">{{ $t('commute.addLocation') }}</span>
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
import { ref, computed, onMounted, watch, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCommuteStore } from '@/stores/commute'
import { ArrowLeft, MapPin, Plus } from 'lucide-vue-next'
import { ElMessage, ElMessageBox } from 'element-plus'

import GoogleMap from '@/components/GoogleMap.vue'
import TransportModes from '@/components/commute/TransportModes.vue'
import LocationCard from '@/components/commute/LocationCard.vue'
import AddLocationModal from '@/components/modals/AddLocationModal.vue'
import NameLocationModal from '@/components/modals/NameLocationModal.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const commuteStore = useCommuteStore()

const t = inject('t')

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

// 路线数据：传给 GoogleMap 的 route（支持 { path:[{lat,lng}]} 或 { encodedPolyline }）
// 说明：在视图层计算路线，组件仅负责渲染，保持职责单一、向后兼容
const routeData = ref(null)
const routeEndpoints = ref(null)
const distanceText = ref('')
const durationText = ref('')

// 地图内联标签（仅保留一处显示）：来自 Directions legs[0] 的权威数据
const routeLabelText = computed(() => {
  // 说明：组合“距离 • 时间”，若缺少其一则只显示存在的项，避免出现多余分隔符
  const d = (distanceText.value || '').trim()
  const t = (durationText.value || '').trim()
  if (d && t) return `${d} • ${t}`
  return d || t || ''
})

// 保证 Google Maps JS 已加载（与 GoogleMap.vue 相同策略，避免多次加载）
const ensureGoogleLoaded = () => {
  if (typeof window !== 'undefined' && window.google && window.google.maps) {
    return Promise.resolve()
  }
  if (typeof window !== 'undefined' && window.googleMapsLoadPromise) {
    return window.googleMapsLoadPromise
  }
  // 使用与组件一致的 key 来源，避免硬编码
  const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || ''
  window.googleMapsLoadPromise = new Promise((resolve, reject) => {
    if (!apiKey || apiKey === 'YOUR_NEW_API_KEY_HERE_REPLACE_ME') {
      reject(new Error('Google Maps API key not configured'))
      return
    }
    const script = document.createElement('script')
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`
    script.async = true
    script.defer = true
    script.onload = () => resolve()
    script.onerror = () => reject(new Error('Failed to load Google Maps'))
    document.head.appendChild(script)
  })
  return window.googleMapsLoadPromise
}

// 计算通勤路线并更新 routeData
const computeRoute = async () => {
  try {
    routeData.value = null
    routeEndpoints.value = null
    distanceText.value = ''
    durationText.value = ''
    const origin = propertyCoordinates.value
    const dest = (authStore.savedAddresses && authStore.savedAddresses[0]) || null
    // 说明：最小可用策略——若无目的地，则不绘制路线
    if (!origin || !dest || !dest.latitude || !dest.longitude) return

    await ensureGoogleLoaded()

    const service = new google.maps.DirectionsService()
    const modeMap = {
      DRIVING: google.maps.TravelMode.DRIVING,
      TRANSIT: google.maps.TravelMode.TRANSIT,
      WALKING: google.maps.TravelMode.WALKING,
      BICYCLING: google.maps.TravelMode.BICYCLING,
    }
    const request = {
      origin,
      destination: { lat: dest.latitude, lng: dest.longitude },
      travelMode: modeMap[selectedMode.value] || google.maps.TravelMode.DRIVING,
    }

    service.route(request, (result, status) => {
      if (status === 'OK' && result?.routes?.length) {
        const r = result.routes[0]
        // 起终点（用于地图 fitBounds 与可选端点标记）
        routeEndpoints.value = {
          origin,
          destination: { lat: dest.latitude, lng: dest.longitude },
        }
        // 优先使用 overview_path（稳定为点列），其次尝试 encoded polyline
        if (Array.isArray(r.overview_path) && r.overview_path.length > 1) {
          const path = r.overview_path.map((p) => ({ lat: p.lat(), lng: p.lng() }))
          routeData.value = { path }
        } else if (r.overviewPolyline?.encodedPath) {
          routeData.value = { encodedPolyline: r.overviewPolyline.encodedPath }
        } else if (
          r.overview_polyline &&
          typeof r.overview_polyline.getEncodedPath === 'function'
        ) {
          routeData.value = { encodedPolyline: String(r.overview_polyline.getEncodedPath()) }
        } else {
          // 最弱降级：不渲染
          routeData.value = null
        }
        // 距离 / 时间摘要（优先实时交通耗时）
        const leg = r.legs && r.legs[0]
        if (leg) {
          distanceText.value = leg.distance?.text || ''
          durationText.value = leg.duration_in_traffic?.text || leg.duration?.text || ''
        }
      } else {
        routeData.value = null
        routeEndpoints.value = null
        distanceText.value = ''
        durationText.value = ''
      }
    })
  } catch {
    // 说明：避免影响页面主流程；路线失败仅降级
    routeData.value = null
  }
}

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

    // 单一目的地策略：如已存在地址，先确认是否替换
    if (authStore.savedAddresses && authStore.savedAddresses.length > 0) {
      try {
        await ElMessageBox.confirm(
          t ? t('commute.confirmReplaceMessage') : '已保存一所大学，是否替换？',
          t ? t('commute.confirmReplaceTitle') : '替换当前大学？',
          {
            confirmButtonText: t ? t('common.replace') : '替换',
            cancelButtonText: t ? t('common.cancel') : '取消',
            type: 'warning',
          },
        )
      } catch {
        // 用户取消替换
        return
      }

      // 执行替换：移除旧地址
      const existing = authStore.savedAddresses[0]
      if (existing?.id) {
        try {
          await authStore.removeUserAddress(existing.id)
        } catch (e) {
          // 忽略移除失败，继续尝试保存新地址
          console.warn('removeUserAddress failed, continue to save new one', e)
        }
      }
    }

    // 保存地址到用户账户（标记为 university）
    await authStore.saveUserAddress({
      address: data.address.formatted_address,
      label: data.label,
      placeId: data.address.place_id,
      latitude: lat,
      longitude: lng,
      // 说明：根据中文标签映射存储类别，学校→university，其它→other
      category: data.label === '学校' ? 'university' : 'other',
    })

    showNameModal.value = false
    selectedAddress.value = null

    ElMessage.success(t ? t('commute.locationAdded') : 'Location added successfully!')
  } catch (error) {
    console.error('Error saving location:', error)
    ElMessage.error(t ? t('commute.locationAddFailed') : 'Failed to save location')
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
    ElMessage.success(t ? t('commute.locationRemoved') : 'Location removed')
  } catch (error) {
    console.error('Failed to remove location', error)
    ElMessage.error(t ? t('commute.locationRemoveFailed') : 'Failed to remove location')
  }
}

/* 监听关键输入变化，动态重算路线
   说明：
   - 选择交通方式改变 → 重算
   - 房源坐标改变 → 重算
   - 用户地址列表更新（含测试模式加载预置地址）→ 重算 */
watch(
  () => [selectedMode.value, propertyCoordinates.value?.lat, propertyCoordinates.value?.lng],
  () => computeRoute(),
)
watch(
  () => authStore.savedAddresses,
  () => computeRoute(),
  { deep: true },
)

// 生命周期
onMounted(() => {
  // 测试模式：跳过登录检查
  const isTest = authStore.testMode

  // 检查是否登录
  if (!isTest && !authStore.isAuthenticated) {
    ElMessage.warning(t ? t('commute.loginRequired') : 'Please login to access this feature')
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
  background: var(--color-bg-page);
  display: flex;
  flex-direction: column;
}

/* 顶部导航 */
.page-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--color-bg-card);
  border-bottom: 1px solid var(--color-border-default);
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
  color: var(--color-text-primary);
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s;
}

.back-btn:hover {
  background: var(--bg-hover);
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

/* 地图区域 */
.map-section {
  height: 40vh;
  position: relative;
  border-bottom: 1px solid var(--color-border-default);
}

.map-placeholder {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: var(--text-muted);
  background: var(--bg-hover);
}
.map-placeholder .map-placeholder-icon {
  width: 32px;
  height: 32px;
}

.route-summary {
  margin-top: 8px;
  font-size: 14px;
  color: var(--color-text-secondary);
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
  color: var(--color-text-primary);
  margin: 0 0 8px 0;
}

.from-address {
  font-size: 14px;
  color: var(--color-text-secondary);
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
  color: var(--text-muted);
}

.empty-state .empty-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 16px;
  color: var(--color-border-default);
}

.empty-state p {
  margin: 8px 0;
  font-size: 16px;
}

.empty-hint {
  font-size: 14px !important;
  color: var(--text-muted);
}

/* 添加地址按钮 */
.add-location-btn {
  width: 100%;
  height: 48px;
  border: 1px solid var(--filter-btn-secondary-border); /* 中文注释：统一走次要按钮描边令牌，移除硬编码红色 */
  border-radius: 8px;
  background: var(--filter-btn-secondary-bg); /* 中文注释：次要按钮默认白底，令牌可全局切换 */
  color: var(--filter-btn-secondary-color); /* 中文注释：文字/图标颜色走次要按钮令牌 */
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all var(--filter-transition-normal); /* 中文注释：统一过渡令牌 */
  margin-top: auto;
}

.add-location-btn:hover {
  /* 中文注释：悬浮态使用统一弱底与加深描边/文字，避免危险色误导 */
  background: var(--filter-color-hover-bg);
  border-color: var(--filter-btn-secondary-hover-border);
  color: var(--filter-btn-secondary-hover-color);
}

.add-location-btn:focus-visible {
  /* 中文注释：键盘可达性——轻微灰色焦点环，使用设计令牌 */
  box-shadow: var(--filter-shadow-focus);
}

.add-location-btn:active {
  transform: translateY(1px);
}

.add-location-btn i {
  font-size: 14px;
  /* 中文注释：图标颜色继承文字色，确保 hover/禁用一致 */
  color: currentColor;
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
