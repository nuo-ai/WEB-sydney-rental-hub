<template>
  <div class="property-detail-page">
    <!-- 优先显示已有数据，即使还在加载更多信息 -->
    <template v-if="property">
      <!-- 加载提示（在有数据时显示为小提示） -->
      <div v-if="loading" class="loading-indicator">
        <el-icon class="is-loading" :size="16"><Loading /></el-icon>
        <span>正在加载更多信息...</span>
      </div>
      <!-- 顶部图片区域 -->
      <header class="image-header">
        <!-- 导航栏 -->
        <nav class="nav-bar">
          <button @click="goBack" class="nav-btn">
            <el-icon><ArrowLeft /></el-icon>
          </button>
          <div class="nav-actions">
            <button @click="toggleFavorite" class="nav-btn">
              <el-icon>
                <component :is="isFavorite ? 'StarFilled' : 'Star'" />
              </el-icon>
            </button>
            <button @click="shareProperty" class="nav-btn">
              <el-icon><Share /></el-icon>
            </button>
          </div>
        </nav>

        <!-- 图片展示 -->
        <div class="image-container">
          <el-image
            v-if="images.length > 0"
            :src="images[currentImageIndex]"
            :alt="`房源图片 ${currentImageIndex + 1}`"
            class="property-image"
            @error="handleImageError"
            :preview-src-list="images"
            :initial-index="currentImageIndex"
            preview-teleported
            fit="cover"
            lazy
            @click="handleImageClick"
          />
          <div v-else class="no-image">
            <el-icon :size="48"><Picture /></el-icon>
            <span>暂无图片</span>
          </div>

          <!-- 图片指示器 -->
          <div v-if="images.length > 1" class="image-indicators">
            <span 
              v-for="(img, index) in images" 
              :key="index"
              :class="['indicator', { active: index === currentImageIndex }]"
              @click="currentImageIndex = index"
            ></span>
          </div>
        </div>
      </header>

      <!-- 主体内容 -->
      <main class="content-container">
        <!-- 价格和地址信息 -->
        <section class="info-section">
          <!-- 可用状态 -->
          <div class="status-line">
            <div class="status-indicator">
              <span class="status-dot"></span>
              <span class="status-text">Available {{ availabilityText }}</span>
            </div>
            <button class="more-btn">
              <i class="fas fa-ellipsis-h"></i>
            </button>
          </div>
          
          <!-- 价格 -->
          <div class="price-section">
            <h1 class="price">
              <span class="price-symbol">$</span>{{ property.rent_pw }}
              <span class="price-unit">per week</span>
            </h1>
          </div>

          <!-- 地址 -->
          <div class="address-section">
            <h2 class="address-main">{{ property.address }}</h2>
            <p class="address-suburb">{{ property.suburb }}, NSW {{ property.postcode || '' }}</p>
          </div>

          <!-- 房源规格 -->
          <div class="specs-section">
            <div class="spec-item">
              <i class="fas fa-bed"></i>
              <span class="spec-value">{{ property.bedrooms || 0 }}</span>
              <span class="spec-label">Bed</span>
            </div>
            <div class="spec-item">
              <i class="fas fa-bath"></i>
              <span class="spec-value">{{ property.bathrooms || 0 }}</span>
              <span class="spec-label">Bath</span>
            </div>
            <div class="spec-item">
              <i class="fas fa-car"></i>
              <span class="spec-value">{{ property.parking_spaces || 0 }}</span>
              <span class="spec-label">Car</span>
            </div>
          </div>

          <!-- 看房时间 -->
          <div v-if="inspectionTimes.length > 0" class="inspection-section">
            <div class="inspection-badge">
              <i class="far fa-calendar"></i>
              Inspection: {{ formatInspectionTime(inspectionTimes[0]) }}
            </div>
          </div>
        </section>

        <!-- 位置地图 -->
        <section class="location-section">
          <h2 class="section-title">Location</h2>
          <div class="map-wrapper">
            <!-- 优先使用SimpleMap，避免Google Maps API问题 -->
            <div v-if="property.latitude && property.longitude" class="map-container">
              <SimpleMap 
                :latitude="property.latitude"
                :longitude="property.longitude"
                :zoom="15"
                :height="mapHeight"
                :marker-title="property.address"
              />
              <!-- 静态地图作为后备 -->
              <img 
                v-if="showStaticMap"
                :src="`https://maps.googleapis.com/maps/api/staticmap?center=${property.latitude},${property.longitude}&zoom=15&size=600x250&markers=color:red%7C${property.latitude},${property.longitude}&key=AIzaSyDR-IqWUXtp64-Pfp09FwGvFHnbKjMNuqU`"
                alt="Property Location"
                class="static-map-image"
                @error="handleStaticMapError"
              />
            </div>
            <div v-else class="map-placeholder">
              <el-icon :size="32"><Location /></el-icon>
              <span>位置信息暂不可用</span>
            </div>

            <!-- See travel times button -->
            <button class="see-travel-times-btn" @click="handleSeeTravelTimes">
              <div class="travel-icon-wrapper">
                <i class="fas fa-location-dot"></i>
              </div>
              <div class="travel-btn-content">
                <span class="travel-btn-title">See travel times</span>
                <span class="travel-btn-subtitle">Find out travel times from this property to your destinations</span>
              </div>
            </button>
          </div>
        </section>

        <!-- 房源描述 -->
        <section class="description-section">
          <div class="property-title">
            <h2>{{ property.address }}</h2>
            <p class="property-id">PROPERTY ID: {{ property.listing_id }} (quote when calling)</p>
          </div>
          
          <div v-if="property.description" class="description-content">
            <div class="description-text" :class="{ expanded: isDescriptionExpanded }">
              <MarkdownContent :content="property.description" />
            </div>
            <button 
              v-if="property.description && property.description.length > 300"
              @click="toggleDescription"
              class="read-more-btn"
            >
              {{ isDescriptionExpanded ? 'Read less' : 'Read more' }}
              <el-icon><ArrowRight /></el-icon>
            </button>
          </div>
        </section>

        <!-- Property Features -->
        <section v-if="property.property_features && property.property_features.length > 0" class="features-section">
          <h2 class="section-title">Property features</h2>
          <div class="features-list">
            <div v-for="feature in visibleFeatures" :key="feature" class="feature-item">
              <i :class="getFeatureIcon(feature)"></i>
              <span>{{ feature }}</span>
            </div>
          </div>
          <button 
            v-if="property.property_features.length > 3"
            @click="showAllFeatures = !showAllFeatures"
            class="show-more-btn"
          >
            Show {{ showAllFeatures ? 'less' : `${property.property_features.length - 3} more` }}
            <i :class="showAllFeatures ? 'fas fa-chevron-up' : 'fas fa-chevron-down'"></i>
          </button>
        </section>

        <!-- 通勤计算器 - 已移至独立页面 -->
      </main>

      <!-- 底部固定操作栏 -->
      <footer class="action-footer">
        <el-button class="action-btn enquire-btn" @click="handleEmail">
          Enquire
        </el-button>
        <el-button class="action-btn inspect-btn" @click="handleInspections">
          Inspect
        </el-button>
      </footer>
    </template>
    
    <!-- 骨架屏（仅在没有数据且正在加载时显示） -->
    <div v-else-if="loading && !property" class="loading-state">
      <el-skeleton animated>
        <template #template>
          <div class="skeleton-image"></div>
          <div class="skeleton-content">
            <el-skeleton-item variant="h1" />
            <el-skeleton-item variant="text" />
            <el-skeleton-item variant="text" />
          </div>
        </template>
      </el-skeleton>
    </div>
    
    <!-- 错误状态 -->
    <div v-else-if="error && !property" class="error-state">
      <el-alert :title="error" type="error" show-icon />
    </div>
    
    <!-- Auth Modal -->
    <AuthModal 
      v-if="showAuthModal"
      v-model="showAuthModal"
      @success="handleAuthSuccess"
    />
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'
import { useAuthStore } from '@/stores/auth'
import { 
  ArrowLeft, ArrowRight, ArrowDown, ArrowUp, Share, Star, StarFilled, Picture, 
  Location, House, Ticket, Van, MoreFilled, Guide,
  HomeFilled, Setting, Grid, Sunny, Loading
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import GoogleMap from '@/components/GoogleMap.vue'
import SimpleMap from '@/components/SimpleMap.vue'
import MarkdownContent from '@/components/MarkdownContent.vue'
import AuthModal from '@/components/modals/AuthModal.vue'

const route = useRoute()
const router = useRouter()
const propertiesStore = usePropertiesStore()
const authStore = useAuthStore()

const propertyId = route.params.id

// 响应式状态
const currentImageIndex = ref(0)
const isDescriptionExpanded = ref(false)
const showAllFeatures = ref(false)
const showStaticMap = ref(false)
const showAuthModal = ref(false)

// 计算属性
const property = computed(() => propertiesStore.currentProperty)
const loading = computed(() => propertiesStore.loading)
const error = computed(() => propertiesStore.error)

const images = computed(() => {
  if (!property.value || !property.value.images || !Array.isArray(property.value.images)) {
    return []
  }
  return property.value.images.filter(url => url && typeof url === 'string' && url.trim() !== '')
})

const isFavorite = computed(() => {
  if (!property.value) return false
  return propertiesStore.favoriteIds.includes(property.value.listing_id)
})

const availabilityText = computed(() => {
  if (!property.value || !property.value.available_date) {
    return 'now'
  }
  
  const availDate = new Date(property.value.available_date)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  if (availDate <= today) {
    return 'now'
  }
  
  const options = { day: 'numeric', month: 'short' }
  return availDate.toLocaleDateString('en-US', options)
})

const inspectionTimes = computed(() => {
  if (!property.value || !property.value.inspection_times) return []
  
  if (typeof property.value.inspection_times === 'string') {
    const times = property.value.inspection_times.split(',').map(time => {
      const parts = time.trim().split(' ')
      return {
        date: parts[0] || '',
        time: parts.slice(1).join(' ') || ''
      }
    })
    return times.slice(0, 1) // 只显示第一个
  }
  
  return []
})

const visibleFeatures = computed(() => {
  if (!property.value || !property.value.property_features) return []
  return showAllFeatures.value 
    ? property.value.property_features 
    : property.value.property_features.slice(0, 3)
})

const mapHeight = computed(() => {
  // Responsive map height - 使用固定值而不是动态计算
  return '250px'
})

// 方法
const goBack = () => {
  router.go(-1)
}

const toggleFavorite = () => {
  if (!property.value) return
  
  if (isFavorite.value) {
    propertiesStore.removeFavorite(property.value.listing_id)
    ElMessage.success('已从收藏中移除')
  } else {
    propertiesStore.addFavorite(property.value.listing_id)
    ElMessage.success('已添加到收藏')
  }
}

const shareProperty = () => {
  if (!property.value) return
  
  if (navigator.share) {
    navigator.share({
      title: property.value.address,
      text: `${property.value.address} - $${property.value.rent_pw}/week`,
      url: window.location.href
    }).catch(() => {
      // 用户取消分享或分享失败
    })
  } else {
    navigator.clipboard.writeText(window.location.href)
      .then(() => ElMessage.success('链接已复制到剪贴板'))
      .catch(() => ElMessage.error('复制失败'))
  }
}

const toggleDescription = () => {
  isDescriptionExpanded.value = !isDescriptionExpanded.value
}

const handleEmail = () => {
  if (!property.value) return
  
  const subject = `Enquiry about ${property.value.address}`
  const body = `Hi,\n\nI am interested in the property at:\n${property.value.address}\n$${property.value.rent_pw}/week\n\nPlease send me more information.\n\nThanks!`
  
  window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`
}

const handleInspections = () => {
  if (inspectionTimes.value.length > 0) {
    ElMessage.info('Inspection booking coming soon')
  } else {
    ElMessage.info('No inspection times available')
  }
}

const handleImageError = (event) => {
  console.warn('Image load failed:', event.target.src)
  event.target.src = '/api/placeholder/400/300'
}

const handleImageClick = () => {
  // Fix lightbox styles
  setTimeout(() => {
    const mask = document.querySelector('.el-image-viewer__mask')
    if (mask) {
      mask.style.backgroundColor = '#000000'
      mask.style.opacity = '0.95'
    }
  }, 50)
}

const getFeatureIcon = (feature) => {
  const featureLower = feature.toLowerCase()
  if (featureLower.includes('air condition')) return 'fas fa-snowflake'
  if (featureLower.includes('alarm')) return 'fas fa-shield-alt'
  if (featureLower.includes('balcony')) return 'fas fa-building'
  if (featureLower.includes('wardrobe')) return 'fas fa-door-closed'
  if (featureLower.includes('ensuite')) return 'fas fa-bath'
  if (featureLower.includes('furnished')) return 'fas fa-couch'
  if (featureLower.includes('gym')) return 'fas fa-dumbbell'
  if (featureLower.includes('spa')) return 'fas fa-hot-tub'
  if (featureLower.includes('intercom')) return 'fas fa-phone'
  if (featureLower.includes('laundry')) return 'fas fa-tshirt'
  if (featureLower.includes('pets')) return 'fas fa-paw'
  if (featureLower.includes('pool')) return 'fas fa-swimming-pool'
  if (featureLower.includes('study')) return 'fas fa-book'
  if (featureLower.includes('garden')) return 'fas fa-tree'
  if (featureLower.includes('parking') || featureLower.includes('garage')) return 'fas fa-car'
  if (featureLower.includes('security')) return 'fas fa-lock'
  return 'fas fa-check-circle' // 默认图标
}

const formatInspectionTime = (inspection) => {
  if (!inspection) return ''
  return `${inspection.date} ${inspection.time}`.trim()
}

const handleStaticMapError = () => {
  console.error('Static map failed to load')
  showStaticMap.value = false
}

const handleSeeTravelTimes = () => {
  // 测试模式：直接跳转，不需要登录
  const testMode = true // 设置为 false 启用登录验证
  
  if (testMode || authStore.isAuthenticated) {
    // 如果是测试模式或已登录，直接跳转到通勤页面
    router.push({
      name: 'CommuteTimes',
      query: {
        propertyId: propertyId,
        address: property.value.address,
        suburb: property.value.suburb,
        lat: property.value.latitude,
        lng: property.value.longitude
      }
    })
  } else {
    // 如果未登录，显示登录/注册模态框
    showAuthModal.value = true
  }
}

const handleAuthSuccess = () => {
  showAuthModal.value = false
  // 登录成功后跳转到通勤页面
  handleSeeTravelTimes()
}


// 预加载下一张图片
const preloadNextImage = () => {
  if (images.value.length > 1) {
    const nextIndex = (currentImageIndex.value + 1) % images.value.length
    const img = new Image()
    img.src = images.value[nextIndex]
  }
}

onMounted(async () => {
  // 开始加载数据
  await propertiesStore.fetchPropertyDetail(propertyId)
  
  // 预加载下一张图片
  if (property.value) {
    preloadNextImage()
  }
  propertiesStore.logHistory(propertyId)
  
  // 3秒后显示静态地图作为后备方案
  setTimeout(() => {
    showStaticMap.value = true
  }, 3000)
})
</script>

<style scoped>
.property-detail-page {
  min-height: 100vh;
  background-color: #ffffff;
  padding-bottom: 80px; /* Space for fixed footer */
}

/* Loading & Error States */
.loading-state,
.error-state {
  padding: 24px;
  max-width: 640px;
  margin: 0 auto;
}

/* 加载指示器（小提示） */
.loading-indicator {
  position: fixed;
  top: 80px;
  right: 20px;
  background: rgba(255, 255, 255, 0.95);
  padding: 8px 16px;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 8px;
  z-index: 100;
  font-size: 14px;
  color: #666;
}

.skeleton-image {
  height: 300px;
  background: #f5f5f5;
  margin-bottom: 24px;
}

.skeleton-content {
  padding: 0 16px;
}

/* Header Image Section */
.image-header {
  position: relative;
  width: 100%;
}

.nav-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10;
  background: linear-gradient(180deg, rgba(0,0,0,0.3) 0%, transparent 100%);
}

.nav-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.95);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.nav-btn:active {
  transform: scale(0.95);
}

.nav-actions {
  display: flex;
  gap: 12px;
}

.image-container {
  position: relative;
  width: 100%;
  height: 300px;
  background: #f5f5f5;
  overflow: hidden;
}

.property-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  cursor: pointer;
}

.no-image {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
  gap: 8px;
}

.image-indicators {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 6px;
}

.indicator {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s;
}

.indicator.active {
  width: 20px;
  border-radius: 3px;
  background: rgba(255, 255, 255, 0.9);
}

/* Content Container */
.content-container {
  max-width: 640px;
  margin: 0 auto;
  padding: 0 16px;
}

/* Info Section */
.info-section {
  padding: 20px 0;
  border-bottom: 1px solid #f0f0f0;
}

.status-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #22c55e;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.status-text {
  font-size: 13px;
  font-weight: 500;
  color: #22c55e;
  text-transform: lowercase;
}

.more-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: transparent;
  color: #999;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.more-btn:hover {
  background: #f5f5f5;
}

/* Price Section */
.price-section {
  margin-bottom: 8px;
}

.price {
  font-size: 28px;
  font-weight: 700;
  color: #111;
  margin: 0;
  line-height: 1.2;
  display: flex;
  align-items: baseline;
  gap: 2px;
}

.price-symbol {
  font-size: 20px;
  font-weight: 600;
  color: #666;
}

.price-unit {
  font-size: 14px;
  font-weight: 400;
  color: #666;
  margin-left: 8px;
}

/* Address Section */
.address-section {
  margin-bottom: 20px;
}

.address-main {
  font-size: 16px;
  font-weight: 600;
  color: #111;
  margin: 0 0 4px 0;
  line-height: 1.3;
}

.address-suburb {
  font-size: 14px;
  color: #666;
  margin: 0;
  line-height: 1.3;
}

/* Specs Section */
.specs-section {
  display: flex;
  gap: 32px;
  margin-bottom: 20px;
}

.spec-item {
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
}

.spec-item i {
  font-size: 18px;
  color: #999;
}

.spec-value {
  font-size: 16px;
  font-weight: 600;
  color: #111;
}

.spec-label {
  font-size: 13px;
  color: #999;
  margin-left: 2px;
}

.inspection-section {
  margin-top: 12px;
}

.inspection-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: #fef3c7;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  color: #92400e;
}

.inspection-badge i {
  font-size: 14px;
}

/* See travel times button - 符合 Figma 设计稿 */
.see-travel-times-btn {
  width: 100%;
  padding: 14px 16px;
  margin-top: 16px;
  background: #ffffff;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.see-travel-times-btn:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background: #fafafa;
}

.see-travel-times-btn:active {
  transform: translateY(1px);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.travel-icon-wrapper {
  width: 40px;
  height: 40px;
  background: #f0f0f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.travel-icon-wrapper i {
  font-size: 18px;
  color: #FF5824;
}

.travel-btn-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.travel-btn-title {
  font-size: 15px;
  font-weight: 600;
  color: #1a1a1a;
  letter-spacing: -0.2px;
}

.travel-btn-subtitle {
  font-size: 13px;
  color: #888;
  line-height: 1.4;
  letter-spacing: -0.1px;
}

/* Location Section */
.location-section {
  padding: 24px 0;
  border-bottom: 1px solid #e5e5e5;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #000;
  margin: 0 0 16px 0;
}

.map-wrapper {
  position: relative;
}

.map-container {
  position: relative;
  width: 100%;
  height: 250px;
  border-radius: 8px;
  overflow: hidden;
  background: #f5f5f5;
}

.static-map-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 1;
}

/* Google Map styles are handled by the GoogleMap component */

.map-placeholder {
  width: 100%;
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 8px;
  color: #999;
  gap: 8px;
}

.travel-times-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 12px;
  font-size: 14px;
  color: #007bff;
  text-decoration: none;
  cursor: pointer;
}

.travel-times-link:hover {
  text-decoration: underline;
}

/* Description Section */
.description-section {
  padding: 24px 0;
  border-bottom: 1px solid #f0f0f0;
}

.property-title {
  margin-bottom: 16px;
}

.property-title h2 {
  font-size: 20px;
  font-weight: 600;
  color: #111;
  margin: 0 0 6px 0;
  line-height: 1.3;
}

.property-id {
  font-size: 12px;
  font-weight: 500;
  color: #999;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.description-content {
  position: relative;
}

.description-text {
  max-height: 150px;
  overflow: hidden;
  transition: max-height 0.5s ease;
  position: relative;
}

.description-text::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 40px;
  background: linear-gradient(to bottom, transparent, white);
  pointer-events: none;
  opacity: 1;
  transition: opacity 0.3s;
}

.description-text.expanded {
  max-height: none;
}

.description-text.expanded::after {
  opacity: 0;
}

.read-more-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-top: 10px;
  padding: 0;
  border: none;
  background: none;
  font-size: 14px;
  font-weight: 500;
  color: #007bff;
  cursor: pointer;
  transition: color 0.2s;
}

.read-more-btn:hover {
  color: #0056b3;
}

/* Features Section */
.features-section {
  padding: 24px 0;
  border-bottom: 1px solid #f0f0f0;
}

.features-section .section-title {
  margin-bottom: 20px;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-bottom: 16px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 0;
  font-size: 14px;
  color: #444;
  border-bottom: 1px solid #f8f8f8;
  transition: background 0.2s;
}

.feature-item:last-child {
  border-bottom: none;
}

.feature-item i {
  font-size: 18px;
  color: #007bff;
  width: 24px;
  text-align: center;
}

.show-more-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid #e5e5e5;
  border-radius: 20px;
  background: white;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  transition: all 0.2s;
}

.show-more-btn:hover {
  background: #f5f5f5;
}

/* Commute Section */
.commute-section {
  padding: 24px 0;
}

/* Fixed Footer */
.action-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px;
  background: white;
  border-top: 1px solid #e5e5e5;
  display: flex;
  gap: 16px;
  z-index: 100;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.05);
}

.action-btn {
  flex: 1;
  height: 48px;
  border-radius: 24px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.enquire-btn {
  background: #007bff;
  color: white;
}

.enquire-btn:hover {
  background: #0056b3;
}

.inspect-btn {
  background: #ff5722;
  color: white;
}

.inspect-btn:hover {
  background: #f4511e;
}

/* Responsive Design */
@media (min-width: 768px) {
  .image-container {
    height: 400px;
  }

  .content-container {
    padding: 0 24px;
  }

  .price {
    font-size: 32px;
  }
  
  .address-main {
    font-size: 18px;
  }
  
  .spec-value {
    font-size: 18px;
  }
}

@media (min-width: 1024px) {
  .image-container {
    height: 500px;
  }

  .price {
    font-size: 36px;
  }
  
  .address-main {
    font-size: 20px;
  }
  
  .property-title h2 {
    font-size: 22px;
  }
}

/* Dark overlay for lightbox */
:deep(.el-image-viewer__mask) {
  background-color: #000000 !important;
  opacity: 0.95 !important;
}
</style>