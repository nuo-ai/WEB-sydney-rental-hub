<template>
  <div class="property-detail-page">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
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
    <div v-else-if="error" class="error-state">
      <el-alert :title="error" type="error" show-icon />
    </div>

    <!-- 房源详情内容 -->
    <template v-else-if="property">
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
                <component :is="isFavorite ? StarFilled : Star" />
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
          <div class="status-line">
            <span class="status-dot"></span>
            <span class="status-text">{{ availabilityText }}</span>
            <el-button text class="more-btn">
              <el-icon><MoreFilled /></el-icon>
            </el-button>
          </div>

          <div class="price-section">
            <h1 class="price">${{ property.rent_pw }} <span class="price-unit">per week</span></h1>
          </div>

          <div class="address-section">
            <p class="address">{{ property.address }}</p>
            <p class="suburb">{{ property.suburb }}, NSW {{ property.postcode }}</p>
          </div>

          <div class="specs-section">
            <span class="spec-item">
              <el-icon><House /></el-icon> {{ property.bedrooms || 0 }}
            </span>
            <span class="spec-item">
              <el-icon><Ticket /></el-icon> {{ property.bathrooms || 0 }}
            </span>
            <span class="spec-item">
              <el-icon><Van /></el-icon> {{ property.parking_spaces || 0 }}
            </span>
          </div>

          <!-- Inspection Time -->
          <div v-if="inspectionTimes.length > 0" class="inspection-section">
            <div class="inspection-badge">
              Inspection {{ inspectionTimes[0].date }} {{ inspectionTimes[0].time }}
            </div>
          </div>
        </section>

        <!-- 位置地图 -->
        <section class="location-section">
          <h2 class="section-title">Location</h2>
          <div class="map-wrapper">
            <!-- 静态地图 -->
            <div v-if="property.latitude && property.longitude" class="static-map">
              <img
                :src="`https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/pin-l+007bff(${property.longitude},${property.latitude})/${property.longitude},${property.latitude},14,0/600x300@2x?access_token=pk.eyJ1IjoianV3b21hcCIsImEiOiJjbTM2eGhiN3EwMHJnMmxzZW9sZ3N0NnhlIn0.dxPXAtxvnzoNKi_QdPXSyA`"
                alt="Property Location"
                class="map-image"
              />
            </div>
            <div v-else class="map-placeholder">
              <el-icon :size="32"><Location /></el-icon>
              <span>位置信息暂不可用</span>
            </div>

            <!-- See travel times link -->
            <a href="#commute" class="travel-times-link">
              <el-icon><Guide /></el-icon>
              See travel times
            </a>
          </div>
        </section>

        <!-- 房源描述 -->
        <section class="description-section">
          <div class="property-title">
            <h2>{{ property.address }}</h2>
            <p class="property-id">PROPERTY ID: {{ property.listing_id }} (quote when calling)</p>
          </div>

          <div v-if="property.description" class="description-content">
            <p class="description-text" :class="{ expanded: isDescriptionExpanded }">
              {{ property.description }}
            </p>
            <button
              v-if="property.description.length > 200"
              @click="toggleDescription"
              class="read-more-btn"
            >
              {{ isDescriptionExpanded ? 'Read less' : 'Read more' }}
              <el-icon><ArrowRight /></el-icon>
            </button>
          </div>
        </section>

        <!-- Property Features -->
        <section v-if="propertyFeatures.length > 0" class="features-section">
          <h2 class="section-title">Property features</h2>
          <div class="features-list">
            <div v-for="feature in visibleFeatures" :key="feature.name" class="feature-item">
              <el-icon><component :is="feature.icon" /></el-icon>
              <span>{{ feature.name }}</span>
            </div>
          </div>
          <button
            v-if="propertyFeatures.length > 3"
            @click="showAllFeatures = !showAllFeatures"
            class="show-more-btn"
          >
            Show {{ showAllFeatures ? 'less' : `${propertyFeatures.length - 3} more` }}
            <el-icon><component :is="showAllFeatures ? ArrowUp : ArrowDown" /></el-icon>
          </button>
        </section>

        <!-- 通勤计算器 -->
        <section
          v-if="property && property.latitude && property.longitude"
          class="commute-section"
          id="commute"
        >
          <CommuteCalculator :property="property" />
        </section>
      </main>

      <!-- 底部固定操作栏 -->
      <footer class="action-footer">
        <el-button class="action-btn enquire-btn" @click="handleEmail"> Enquire </el-button>
        <el-button class="action-btn inspect-btn" @click="handleInspections"> Inspect </el-button>
      </footer>
    </template>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'
import {
  ArrowLeft,
  ArrowRight,
  ArrowDown,
  ArrowUp,
  Share,
  Star,
  StarFilled,
  Picture,
  Location,
  House,
  Ticket,
  Van,
  MoreFilled,
  Guide,
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import CommuteCalculator from '@/components/CommuteCalculator.vue'

const route = useRoute()
const router = useRouter()
const propertiesStore = usePropertiesStore()

const propertyId = route.params.id

// 响应式状态
const currentImageIndex = ref(0)
const isDescriptionExpanded = ref(false)
const showAllFeatures = ref(false)

// 计算属性
const property = computed(() => propertiesStore.currentProperty)
const loading = computed(() => propertiesStore.loading)
const error = computed(() => propertiesStore.error)

const images = computed(() => {
  if (!property.value || !property.value.images || !Array.isArray(property.value.images)) {
    return []
  }
  return property.value.images.filter((url) => url && typeof url === 'string' && url.trim() !== '')
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
    const times = property.value.inspection_times.split(',').map((time) => {
      const parts = time.trim().split(' ')
      return {
        date: parts[0] || '',
        time: parts.slice(1).join(' ') || '',
      }
    })
    return times.slice(0, 1) // 只显示第一个
  }

  return []
})

// Property features mapping
const propertyFeatures = computed(() => {
  if (!property.value || !property.value.property_features) return []

  const iconMap = {
    'Air conditioning': 'Sunny',
    'Alarm system': 'Bell',
    Balcony: 'Grid',
    'Built-in wardrobes': 'Box',
    Ensuite: 'Ticket',
    Furnished: 'HomeFilled',
    Gym: 'Trophy',
    'Indoor spa': 'Coffee',
    Intercom: 'Phone',
    'Internal laundry': 'Dish',
    'Pets allowed': 'Guide',
    Pool: 'Ship',
    Study: 'Reading',
    Garden: 'Grape',
  }

  return property.value.property_features.map((feature) => ({
    name: feature,
    icon: iconMap[feature] || 'Setting',
  }))
})

const visibleFeatures = computed(() => {
  return showAllFeatures.value ? propertyFeatures.value : propertyFeatures.value.slice(0, 3)
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
    navigator
      .share({
        title: property.value.address,
        text: `${property.value.address} - $${property.value.rent_pw}/week`,
        url: window.location.href,
      })
      .catch((err) => console.error('分享失败:', err))
  } else {
    navigator.clipboard
      .writeText(window.location.href)
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

onMounted(() => {
  propertiesStore.fetchPropertyDetail(propertyId)
  propertiesStore.logHistory(propertyId)
})
</script>

<style scoped>
.property-detail-page {
  min-height: 100vh;
  background-color: #fff;
  padding-bottom: 80px; /* Space for fixed footer */
}

/* Loading & Error States */
.loading-state,
.error-state {
  padding: 24px;
  max-width: 640px;
  margin: 0 auto;
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
  background: linear-gradient(180deg, rgb(0 0 0 / 30%) 0%, transparent 100%);
}

.nav-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgb(255 255 255 / 95%);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s;
  box-shadow: 0 2px 8px rgb(0 0 0 / 10%);
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
  background: rgb(255 255 255 / 50%);
  cursor: pointer;
  transition: all 0.3s;
}

.indicator.active {
  width: 20px;
  border-radius: 3px;
  background: rgb(255 255 255 / 90%);
}

/* Content Container */
.content-container {
  max-width: 640px;
  margin: 0 auto;
  padding: 0 16px;
}

/* Info Section */
.info-section {
  padding: 16px 0;
  border-bottom: 1px solid #e5e5e5;
}

.status-line {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  position: relative;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #007bff;
  border-radius: 50%;
}

.status-text {
  font-size: 14px;
  color: #666;
}

.more-btn {
  margin-left: auto;
  padding: 0;
  color: #999;
}

.price-section {
  margin-bottom: 12px;
}

.price {
  font-size: 24px;
  font-weight: 700;
  color: #000;
  margin: 0;
}

.price-unit {
  font-size: 16px;
  font-weight: 400;
  color: #666;
}

.address-section {
  margin-bottom: 16px;
}

.address {
  font-size: 16px;
  color: #333;
  margin: 0 0 4px;
}

.suburb {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.specs-section {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
}

.spec-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #333;
}

.inspection-section {
  margin-top: 12px;
}

.inspection-badge {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  background: #f0f2f5;
  border-radius: 16px;
  font-size: 13px;
  color: #666;
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
  margin: 0 0 16px;
}

.map-wrapper {
  position: relative;
}

.static-map {
  width: 100%;
  height: 200px;
  border-radius: 8px;
  overflow: hidden;
  background: #f5f5f5;
}

.map-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

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
  border-bottom: 1px solid #e5e5e5;
}

.property-title h2 {
  font-size: 18px;
  font-weight: 600;
  color: #000;
  margin: 0 0 8px;
}

.property-id {
  font-size: 13px;
  color: #999;
  margin: 0 0 16px;
}

.description-text {
  font-size: 14px;
  line-height: 1.6;
  color: #333;
  margin: 0;
  max-height: 72px;
  overflow: hidden;
  transition: max-height 0.3s;
}

.description-text.expanded {
  max-height: none;
}

.read-more-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-top: 8px;
  padding: 0;
  border: none;
  background: none;
  font-size: 14px;
  color: #007bff;
  cursor: pointer;
}

/* Features Section */
.features-section {
  padding: 24px 0;
  border-bottom: 1px solid #e5e5e5;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 16px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: #333;
}

.feature-item .el-icon {
  font-size: 20px;
  color: #666;
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
  box-shadow: 0 -2px 8px rgb(0 0 0 / 5%);
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
@media (width >= 768px) {
  .image-container {
    height: 400px;
  }

  .content-container {
    padding: 0 24px;
  }

  .price {
    font-size: 28px;
  }

  .static-map {
    height: 250px;
  }
}

@media (width >= 1024px) {
  .image-container {
    height: 500px;
  }

  .price {
    font-size: 32px;
  }

  .static-map {
    height: 300px;
  }
}

/* Dark overlay for lightbox */
:deep(.el-image-viewer__mask) {
  background-color: #000 !important;
  opacity: 0.95 !important;
}
</style>
