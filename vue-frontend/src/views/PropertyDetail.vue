<template>
  <div class="property-detail-page">
    <!-- 优先显示已有数据，即使还在加载更多信息 -->
    <template v-if="property">
      <!-- 加载提示（在有数据时显示为小提示） -->
      <div v-if="loading" class="loading-indicator">
        <el-icon class="is-loading" :size="16"><Loading /></el-icon>
        <span>正在加载更多信息...</span>
      </div>
      <!-- 图片展示区域 - Domain风格 -->
      <header class="image-header">
        <!-- 图片容器 -->
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

          <!-- 返回按钮 - 左上角 -->
          <button @click="goBack" class="back-btn">
            <el-icon :size="20"><ArrowLeft /></el-icon>
          </button>

          <!-- Share和Save按钮 - 右上角 -->
          <div class="image-actions">
            <button @click="shareProperty" class="image-action-btn">
              <el-icon :size="20"><Share /></el-icon>
              <span>Share</span>
            </button>
            <div class="action-divider"></div>
            <button @click="toggleFavorite" class="image-action-btn">
              <el-icon :size="20">
                <component :is="isFavorite ? 'StarFilled' : 'Star'" />
              </el-icon>
              <span>Save</span>
            </button>
          </div>

          <!-- Photos按钮和Inspect按钮 - 左下角 -->
          <div class="image-bottom-controls">
            <button @click="handleInspections" class="inspect-btn-overlay">
              <el-icon :size="18"><Calendar /></el-icon>
              <span>Inspect {{ nextInspectionTime }}</span>
            </button>
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

      <!-- 主体内容 - Domain风格卡片布局 -->
      <main class="content-container">
        <!-- 白色信息卡片 -->
        <section class="info-card">
          <!-- 可用状态标签 -->
          <div class="availability-badge">
            <span class="status-dot"></span>
            <span class="status-text">available now</span>
          </div>
          
          <!-- 价格 -->
          <div class="price-wrapper">
            <span class="price-currency">$</span>
            <span class="price-amount">{{ property.rent_pw }}</span>
            <span class="price-period">per week</span>
          </div>

          <!-- 地址 -->
          <div class="address-wrapper">
            <h1 class="address-main">{{ property.address }}</h1>
            <p class="address-suburb">{{ property.suburb }}, NSW {{ property.postcode || '' }}</p>
          </div>

          <!-- 房源特征 - Domain风格图标 -->
          <div class="property-features">
            <div class="feature">
              <svg class="feature-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="10" rx="2" ry="2"/>
                <rect x="7" y="7" width="10" height="4" rx="1" ry="1"/>
              </svg>
              <span class="feature-value">{{ property.bedrooms || 0 }}</span>
              <span class="feature-label">Bed</span>
            </div>
            <div class="feature">
              <svg class="feature-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="5" y="12" width="14" height="8" rx="1"/>
                <path d="M5 12V7a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v5"/>
              </svg>
              <span class="feature-value">{{ property.bathrooms || 0 }}</span>
              <span class="feature-label">Bath</span>
            </div>
            <div class="feature">
              <svg class="feature-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="7" rx="1"/>
                <path d="M5 11V9a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v2"/>
                <circle cx="7.5" cy="15.5" r="1.5"/>
                <circle cx="16.5" cy="15.5" r="1.5"/>
              </svg>
              <span class="feature-value">{{ property.parking_spaces || 0 }}</span>
              <span class="feature-label">Car</span>
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
            <h2>{{ property.property_headline || property.address }}</h2>
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
  Location, House, Ticket, Van, MoreFilled, Guide, Calendar,
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

const nextInspectionTime = computed(() => {
  if (inspectionTimes.value.length > 0) {
    const inspection = inspectionTimes.value[0]
    // 简化显示格式，例如 "Mon 6am"
    return inspection.time || 'Soon'
  }
  return ''
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
/* Domain.com.au 像素级还原样式 */
@import '@/assets/design-tokens.css';

.property-detail-page {
  min-height: 100vh;
  background-color: #f5f6f7;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* 加载和错误状态 */
.loading-state,
.error-state {
  padding: 24px;
  max-width: 768px;
  margin: 0 auto;
}

/* 加载指示器 */
.loading-indicator {
  position: fixed;
  top: 80px;
  right: 16px;
  background: rgba(255, 255, 255, 0.95);
  padding: 8px 16px;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 8px;
  z-index: 20;
  font-size: 14px;
  color: #6e7881;
}

.skeleton-image {
  height: 280px;
  background: #e8e8e8;
  margin-bottom: 0;
}

.skeleton-content {
  padding: 20px 16px;
  background: white;
}

/* 图片区域 - Domain 精确尺寸 */
.image-header {
  position: relative;
  width: 100%;
  margin: 0;
  max-width: 1905px;
  margin-left: auto;
  margin-right: auto;
}

/* 返回按钮 - 左上角圆形 */
.back-btn {
  position: absolute;
  top: 16px;
  left: 16px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.95);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #2e3a4b;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 1);
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* Share和Save按钮组 - 右上角 */
.image-actions {
  position: absolute;
  top: 16px;
  right: 16px;
  display: flex;
  background: #fefefe;
  border: 1px solid #cfd1d7;
  border-radius: 4px;
  overflow: hidden;
  z-index: 10;
}

.image-action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: background 0.2s ease;
  color: #808296;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 14px;
  font-weight: 400;
}

.image-action-btn:hover {
  background: rgba(0, 0, 0, 0.03);
}

.image-action-btn span {
  font-size: 14px;
  color: #808296;
}

.action-divider {
  width: 1px;
  height: 42px;
  background: #cfd1d7;
}

/* 底部控制按钮 - 左下角 */
.image-bottom-controls {
  position: absolute;
  bottom: 16px;
  left: 16px;
  z-index: 10;
}

.inspect-btn-overlay {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #ffffff;
  border: 1px solid #d0d3d9;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
  font-weight: 500;
  color: #6e7086;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
}

.inspect-btn-overlay:hover {
  background: #f8f8f8;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12);
}

.image-container {
  position: relative;
  width: 100%;
  height: 280px; /* 移动端高度 */
  background: #e8e8e8;
  overflow: hidden;
}

.property-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  cursor: pointer;
}

/* 平板尺寸 */
@media (min-width: 768px) {
  .image-container {
    height: 400px;
  }
}

/* 桌面尺寸 - Domain 精确规格 */
@media (min-width: 1200px) {
  .image-container {
    height: 592px; /* Domain 桌面端精确高度 */
  }
  
  .property-image {
    width: 100%;
    height: 100%;
    object-fit: contain; /* 保持图片比例 */
    object-position: center;
    background: #000; /* 黑色背景填充空白区域 */
  }
}

/* 超大屏幕 */
@media (min-width: 1905px) {
  .image-header {
    border-radius: 0; /* 确保无圆角 */
  }
  
  .image-container {
    max-width: 1680px; /* 图片最大宽度 */
    margin: 0 auto;
  }
}

.no-image {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
  gap: 8px;
  font-size: 14px;
}

.image-indicators {
  position: absolute;
  bottom: 12px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 4px;
}

.indicator {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  transition: all 0.2s ease;
}

.indicator.active {
  width: 24px;
  border-radius: 3px;
  background: white;
}


/* 内容容器 */
.content-container {
  padding: 0;
  margin: 0;
  background: #f5f6f7;
}

/* 信息卡片 - 白色背景带阴影 */
.info-card {
  background: white;
  padding: 20px 16px;
  margin: 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  border-bottom: 1px solid #e4e5e7;
}

/* 可用状态标签 */
.availability-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #00b200;
  border-radius: 50%;
  flex-shrink: 0;
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
  font-size: 14px;
  font-weight: 400;
  color: #00b200;
  line-height: 1;
}

/* 价格显示 */
.price-wrapper {
  display: flex;
  align-items: baseline;
  margin-bottom: 12px;
  line-height: 1;
}

.price-currency {
  font-size: 24px;
  font-weight: 700;
  color: #2e3a4b;
  margin-right: 2px;
}

.price-amount {
  font-size: 32px;
  font-weight: 700;
  color: #2e3a4b;
  letter-spacing: -0.5px;
}

.price-period {
  font-size: 16px;
  font-weight: 400;
  color: #6e7881;
  margin-left: 8px;
}

/* 地址显示 */
.address-wrapper {
  margin-bottom: 20px;
}

.address-main {
  font-size: 18px;
  font-weight: 600;
  color: #2e3a4b;
  margin: 0 0 4px 0;
  line-height: 1.3;
}

.address-suburb {
  font-size: 14px;
  font-weight: 400;
  color: #6e7881;
  margin: 0;
  line-height: 1.3;
}

/* 房源特征 */
.property-features {
  display: flex;
  gap: 24px;
  align-items: center;
}

.feature {
  display: flex;
  align-items: center;
  gap: 6px;
}

.feature-icon {
  width: 20px;
  height: 20px;
  color: #6e7881;
  flex-shrink: 0;
}

.feature-value {
  font-size: 16px;
  font-weight: 500;
  color: #2e3a4b;
  margin: 0 2px;
}

.feature-label {
  font-size: 14px;
  font-weight: 400;
  color: #6e7881;
}


/* See travel times button - 符合 Figma 设计稿 */
.see-travel-times-btn {
  width: 100%;
  padding: var(--space-3-5) var(--space-4);
  margin-top: var(--space-4);
  background: var(--bg-base);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xs);
  display: flex;
  align-items: center;
  gap: var(--space-3-5);
  cursor: pointer;
  transition: var(--transition-all);
  text-align: left;
}

.see-travel-times-btn:hover {
  box-shadow: var(--shadow-sm);
  background: var(--bg-hover);
}

.see-travel-times-btn:active {
  transform: translateY(1px);
  box-shadow: var(--shadow-xs);
}

.travel-icon-wrapper {
  width: calc(var(--space-4) * 2.5); /* 40px */
  height: calc(var(--space-4) * 2.5); /* 40px */
  background: var(--bg-secondary);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.travel-icon-wrapper i {
  font-size: var(--text-lg);
  color: var(--brand-primary);
}

.travel-btn-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.travel-btn-title {
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  letter-spacing: -0.2px;
}

.travel-btn-subtitle {
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  line-height: 1.4;
  letter-spacing: -0.1px;
}

/* 位置部分 */
.location-section {
  padding: 20px 16px;
  background: white;
  margin-top: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #2e3a4b;
  margin: 0 0 16px 0;
}

.map-wrapper {
  position: relative;
}

.map-container {
  position: relative;
  width: 100%;
  height: 200px;
  border-radius: 8px;
  overflow: hidden;
  background: #e8e8e8;
  margin-bottom: 12px;
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
  border-radius: var(--radius-md);
  color: var(--color-secondary);
  gap: var(--spacing-sm);
}

.travel-times-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1-5);
  margin-top: var(--space-3);
  font-size: var(--text-sm);
  color: var(--link-color);
  text-decoration: none;
  cursor: pointer;
}

.travel-times-link:hover {
  text-decoration: underline;
}

/* 描述部分 */
.description-section {
  padding: 20px 16px;
  background: white;
  margin-top: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.property-title {
  margin-bottom: 16px;
}

.property-title h2 {
  font-size: 20px;
  font-weight: 600;
  color: #2e3a4b;
  margin: 0 0 8px 0;
  line-height: 1.3;
}

.property-id {
  font-size: 12px;
  font-weight: 400;
  color: #999;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.description-content {
  position: relative;
}

.description-text {
  font-size: 14px;
  line-height: 1.6;
  color: #6e7881;
  max-height: 120px;
  overflow: hidden;
  transition: max-height 0.3s ease;
  position: relative;
}

.description-text::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50px;
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
  margin-top: 12px;
  padding: 0;
  border: none;
  background: none;
  font-size: 14px;
  font-weight: 500;
  color: #017188;
  cursor: pointer;
  transition: color 0.2s ease;
}

.read-more-btn:hover {
  color: #014a5a;
  text-decoration: underline;
}

/* 特征部分 */
.features-section {
  padding: 20px 16px;
  background: white;
  margin-top: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.features-section .section-title {
  margin-bottom: 16px;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-bottom: var(--spacing-md);
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 0;
  font-size: 14px;
  color: var(--color-primary);
  border-bottom: 1px solid #f0f0f0;
  transition: background 0.2s ease;
}

.feature-item:last-child {
  border-bottom: none;
}

.feature-item i {
  font-size: 18px;
  color: var(--color-accent);
  width: 24px;
  text-align: center;
}

.show-more-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: 20px;
  background: var(--color-surface);
  font-size: 14px;
  font-weight: 500;
  color: var(--color-primary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.show-more-btn:hover {
  background: #f5f5f5;
  border-color: var(--color-primary);
}

/* Commute Section */
.commute-section {
  padding: var(--space-6) 0;
}

/* 底部操作栏 */
.action-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 12px 16px;
  background: white;
  border-top: 1px solid #e4e5e7;
  display: flex;
  gap: 12px;
  z-index: 100;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.08);
}

.action-btn {
  flex: 1;
  height: 48px;
  border-radius: 24px;
  font-size: var(--font-size-base);
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.enquire-btn {
  background: var(--color-accent);
  color: white;
}

.enquire-btn:hover {
  background: #005a6b;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 124, 140, 0.3);
}

.inspect-btn {
  background: #f97f4e; /* Domain橙色 */
  color: white;
}

.inspect-btn:hover {
  background: #e86a3a;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(249, 127, 78, 0.3);
}

/* Responsive Design - Domain响应式 */
@media (min-width: 768px) {
  .image-container {
    height: 400px;
  }

  .content-container {
    padding: 0 var(--spacing-lg);
  }

  .price {
    font-size: 36px;
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
    font-size: 42px;
  }
  
  .address-main {
    font-size: 20px;
  }
  
  .property-title h2 {
    font-size: 28px;
  }
}

/* Dark overlay for lightbox */
:deep(.el-image-viewer__mask) {
  background-color: #000000 !important;
  opacity: 0.95 !important;
}
</style>