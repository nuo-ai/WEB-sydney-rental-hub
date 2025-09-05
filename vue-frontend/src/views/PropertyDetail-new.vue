<template>
  <div class="property-detail-container">
    <main class="main-content">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-spinner">
        <el-skeleton animated>
          <template #template>
            <div class="image-skeleton"></div>
            <div class="content-skeleton"></div>
          </template>
        </el-skeleton>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="error-message">
        <el-alert :title="error" type="error" show-icon />
      </div>

      <!-- 房源详情内容 -->
      <div v-else-if="property" class="property-detail-content">
        <!-- 1. 图片展示区 -->
        <div class="image-section">
          <!-- 顶部导航按钮 -->
          <div class="image-nav-header">
            <button @click="goBack" class="nav-icon-btn">
              <i class="fas fa-chevron-left"></i>
            </button>
            <div class="nav-right-actions">
              <button @click="toggleFavorite" class="nav-icon-btn">
                <i :class="isFavorite ? 'fas fa-star' : 'far fa-star'"></i>
              </button>
              <button @click="shareProperty" class="nav-icon-btn">
                <i class="fas fa-upload"></i>
              </button>
            </div>
          </div>

          <!-- 图片容器 -->
          <div class="image-container">
            <div v-if="images.length > 0">
              <img
                :src="images[currentImageIndex]"
                :alt="`Property image ${currentImageIndex + 1}`"
                class="main-image"
                @error="handleImageError"
              />

              <!-- 左右切换按钮 -->
              <template v-if="images.length > 1">
                <button
                  @click="previousImage"
                  class="carousel-nav prev"
                  :disabled="currentImageIndex === 0"
                >
                  <i class="fas fa-chevron-left"></i>
                </button>
                <button
                  @click="nextImage"
                  class="carousel-nav next"
                  :disabled="currentImageIndex === images.length - 1"
                >
                  <i class="fas fa-chevron-right"></i>
                </button>
              </template>

              <!-- 图片计数器 -->
              <div class="image-counter" v-if="images.length > 1">
                {{ currentImageIndex + 1 }} of {{ images.length }}
              </div>

              <!-- 图片指示点 -->
              <div class="image-dots" v-if="images.length > 1">
                <span
                  v-for="(img, index) in images"
                  :key="index"
                  :class="['dot', { active: index === currentImageIndex }]"
                  @click="currentImageIndex = index"
                ></span>
              </div>
            </div>

            <!-- 无图片占位符 -->
            <div v-else class="no-image-placeholder">
              <i class="fas fa-image"></i>
              <p>No images available</p>
            </div>
          </div>
        </div>

        <!-- 2. 主信息卡片 -->
        <div class="info-card">
          <!-- 可用状态 -->
          <div class="availability-badge">
            <i class="far fa-check-circle"></i>
            <span>{{ availabilityText }}</span>
          </div>

          <!-- 价格 -->
          <div class="price-section">
            <h1 class="price-amount">
              ${{ property.rent_pw }} <span class="price-period">per week</span>
            </h1>
          </div>

          <!-- 地址 -->
          <div class="address-section">
            <p class="property-address">{{ property.address }}</p>
          </div>

          <!-- 规格 -->
          <div class="property-specs spec-row">
            <div class="spec-item">
              <BedDouble class="spec-icon" />
              <span class="spec-text">{{ property.bedrooms || 0 }}</span>
            </div>
            <div class="spec-item">
              <Bath class="spec-icon" />
              <span class="spec-text">{{ property.bathrooms || 0 }}</span>
            </div>
            <div class="spec-item">
              <CarFront class="spec-icon" />
              <span class="spec-text">{{ property.parking_spaces || '-' }}</span>
            </div>
          </div>

          <!-- 看房时间 -->
          <div v-if="property.inspection_times" class="inspection-row">
            <div class="inspection-label">Inspection: {{ property.inspection_times }}</div>
          </div>
        </div>

        <!-- 3. Location 卡片 -->
        <div class="location-card">
          <h3 class="card-title">Location</h3>
          <div class="map-container">
            <div class="map-placeholder">
              <i class="fas fa-map-marked-alt"></i>
              <p>{{ property.suburb }}</p>
            </div>
          </div>
          <div class="travel-times-link">
            <div class="travel-times-content">
              <i class="far fa-clock"></i>
              <div>
                <span class="travel-title">See travel times</span>
                <span class="travel-subtitle"
                  >Find out travel times from this property to your destination</span
                >
              </div>
            </div>
            <i class="fas fa-chevron-right"></i>
          </div>
        </div>

        <!-- 4. Property features 卡片 -->
        <div
          class="features-card"
          v-if="property.property_features && property.property_features.length"
        >
          <h3 class="card-title">Property features</h3>
          <div class="features-list">
            <div v-for="(feature, index) in visibleFeatures" :key="index" class="feature-item">
              <component :is="getFeatureIconComponent(feature)" class="spec-icon" />
              <span>{{ feature }}</span>
            </div>
          </div>
          <button
            v-if="property.property_features.length > 6"
            @click="showAllFeatures = !showAllFeatures"
            class="show-more-btn"
          >
            <span>{{
              showAllFeatures ? 'Show less' : `Show ${property.property_features.length - 6} more`
            }}</span>
            <i :class="showAllFeatures ? 'fas fa-chevron-up' : 'fas fa-chevron-down'"></i>
          </button>
        </div>

        <!-- 5. 描述卡片 -->
        <div class="description-card" v-if="property.description">
          <h3 class="property-title">{{ property.suburb }} modern apartment</h3>
          <p class="property-id">PROPERTY ID: {{ property.listing_id }}</p>
          <div class="apply-info">
            <span>APPLY: Send through an enquiry and you'll receive the link to apply</span>
          </div>
          <div class="description-content">
            <p class="description-text" :class="{ expanded: isDescriptionExpanded }">
              {{ property.description }}
            </p>
          </div>
          <button
            v-if="property.description && property.description.length > 200"
            @click="toggleDescription"
            class="read-more-btn"
          >
            <span>{{ isDescriptionExpanded ? 'Read less' : 'Read more' }}</span>
            <i :class="isDescriptionExpanded ? 'fas fa-chevron-up' : 'fas fa-chevron-down'"></i>
          </button>
        </div>

        <!-- 6. 通勤计算器 -->
        <div v-if="property && property.latitude && property.longitude" class="commute-section">
          <CommuteCalculator :property="property" />
        </div>
      </div>
    </main>

    <!-- 底部操作栏 -->
    <footer v-if="property" class="sticky-footer">
      <button class="footer-btn enquire-btn" @click="handleEmail">Enquire</button>
      <button class="footer-btn inspect-btn" @click="handleInspections">Inspect</button>
    </footer>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'
import { ElMessage } from 'element-plus'
import CommuteCalculator from '@/components/CommuteCalculator.vue'
import {
  BedDouble,
  Bath,
  CarFront,
  AirVent,
  Shield,
  Home,
  DoorClosed,
  Waves,
  Dumbbell,
  Lock,
  WashingMachine,
  CookingPot,
  CheckCircle,
} from 'lucide-vue-next'

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

const visibleFeatures = computed(() => {
  if (!property.value || !property.value.property_features) return []
  if (showAllFeatures.value) {
    return property.value.property_features
  }
  return property.value.property_features.slice(0, 6)
})

const availabilityText = computed(() => {
  if (!property.value || !property.value.available_date) {
    return 'Available now'
  }

  const availDate = new Date(property.value.available_date)
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  if (availDate <= today) {
    return 'Available now'
  }

  const day = availDate.getDate().toString().padStart(2, '0')
  const month = (availDate.getMonth() + 1).toString().padStart(2, '0')
  const year = availDate.getFullYear()

  return `Available from ${day}/${month}/${year}`
})

// 方法
const goBack = () => {
  router.back()
}

const toggleFavorite = () => {
  if (property.value) {
    propertiesStore.toggleFavorite(property.value.listing_id)
    ElMessage.success(isFavorite.value ? '已移除收藏' : '已添加收藏')
  }
}

const shareProperty = async () => {
  if (!property.value) return

  const shareUrl = window.location.href
  const shareText = `Check out this property: ${property.value.address} - $${property.value.rent_pw}/week`

  if (navigator.share) {
    try {
      await navigator.share({
        title: 'Property Details',
        text: shareText,
        url: shareUrl,
      })
    } catch (err) {
      console.warn('Share cancelled', err)
    }
  } else {
    navigator.clipboard
      .writeText(shareUrl)
      .then(() => ElMessage.success('链接已复制'))
      .catch(() => ElMessage.error('复制失败'))
  }
}

const toggleDescription = () => {
  isDescriptionExpanded.value = !isDescriptionExpanded.value
}

const featureIconMap = {
  'air condition': AirVent,
  alarm: Shield,
  balcony: Home,
  wardrobe: DoorClosed,
  pool: Waves,
  gym: Dumbbell,
  parking: CarFront,
  garage: CarFront,
  security: Lock,
  laundry: WashingMachine,
  dishwasher: CookingPot,
}

const getFeatureIconComponent = (feature) => {
  const featureLower = feature.toLowerCase()
  for (const key in featureIconMap) {
    if (featureLower.includes(key)) {
      return featureIconMap[key]
    }
  }
  return CheckCircle
}

const handleEmail = () => {
  if (!property.value) return
  ElMessage.info('Enquiry功能开发中')
}

const handleInspections = () => {
  if (!property.value) return
  ElMessage.info('Inspect功能开发中')
}

const previousImage = () => {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--
  }
}

const nextImage = () => {
  if (currentImageIndex.value < images.value.length - 1) {
    currentImageIndex.value++
  }
}

const handleImageError = (event) => {
  event.target.src =
    'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="300"%3E%3Crect fill="%23f0f0f0" width="400" height="300"/%3E%3Ctext x="50%25" y="50%25" text-anchor="middle" dy=".3em" fill="%23999"%3EImage not available%3C/text%3E%3C/svg%3E'
}

onMounted(() => {
  propertiesStore.fetchPropertyDetail(propertyId)
  propertiesStore.logHistory(propertyId)
})
</script>

<style scoped>
/* 全局样式 */
.property-detail-container {
  min-height: 100vh;
  background-color: #f8f8f8;
  padding-bottom: 70px;
}

.main-content {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  background: white;
}

/* 加载和错误状态 */
.loading-spinner,
.error-message {
  padding: 40px;
  text-align: center;
}

.image-skeleton {
  height: 300px;
  background: #f0f0f0;
  margin-bottom: 20px;
}

.content-skeleton {
  height: 400px;
  background: #f0f0f0;
}

/* 1. 图片区域 */
.image-section {
  position: relative;
  background: #000;
}

.image-nav-header {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  z-index: 10;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), transparent);
}

.nav-icon-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.5);
  border: none;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 16px;
  backdrop-filter: blur(4px);
}

.nav-icon-btn:active {
  transform: scale(0.95);
}

.nav-right-actions {
  display: flex;
  gap: 8px;
}

.image-container {
  position: relative;
  width: 100%;
  height: 300px;
  background: #f0f0f0;
  overflow: hidden;
}

.main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.5);
  border: none;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 14px;
  backdrop-filter: blur(4px);
}

.carousel-nav.prev {
  left: 12px;
}

.carousel-nav.next {
  right: 12px;
}

.carousel-nav:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.image-counter {
  position: absolute;
  bottom: 60px;
  right: 16px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  backdrop-filter: blur(4px);
}

.image-dots {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 4px;
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s;
}

.dot.active {
  background: white;
  width: 8px;
  height: 8px;
}

.no-image-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
}

.no-image-placeholder i {
  font-size: 48px;
  margin-bottom: 12px;
}

/* 2. 主信息卡片 */
.info-card {
  padding: 16px;
  background: white;
  border-bottom: 1px solid #e8e8e8;
}

.availability-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
}

.blue-dot {
  color: #0066ff;
  font-size: 16px;
  line-height: 1;
}

.availability-text {
  font-size: 13px;
  color: #333;
}

.price-row {
  margin-bottom: 8px;
}

.price-amount {
  font-size: 24px;
  font-weight: 600;
  color: #000;
}

.price-period {
  font-size: 14px;
  color: #666;
  margin-left: 4px;
}

.address-row {
  margin-bottom: 12px;
}

.address-text {
  font-size: 14px;
  color: #666;
  line-height: 1.4;
}

.specs-row {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-top: 1px solid #e8e8e8;
  border-bottom: 1px solid #e8e8e8;
}

.spec {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #333;
}

.spec-icon {
  width: 24px;
  height: 24px;
  color: #666;
}

.spec-divider {
  margin: 0 12px;
  color: #d0d0d0;
}

.inspection-row {
  margin-top: 12px;
  padding: 8px 12px;
  background: #f8f8f8;
  border-radius: 6px;
}

.inspection-label {
  font-size: 13px;
  color: #666;
}

/* 3. Location卡片 */
.location-card {
  margin-top: 8px;
  padding: 16px;
  background: white;
  border-bottom: 1px solid #e8e8e8;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #000;
  margin: 0 0 16px 0;
}

.map-container {
  height: 200px;
  background: #f0f0f0;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 16px;
}

.map-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
}

.map-placeholder i {
  font-size: 48px;
  margin-bottom: 12px;
}

.travel-times-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  background: #f8f8f8;
  border-radius: 8px;
  cursor: pointer;
}

.travel-times-content {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.travel-times-content i {
  color: #666;
  margin-top: 2px;
}

.travel-title {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}

.travel-subtitle {
  display: block;
  font-size: 12px;
  color: #999;
  line-height: 1.4;
}

/* 4. Features卡片 */
.features-card {
  margin-top: 8px;
  padding: 16px;
  background: white;
  border-bottom: 1px solid #e8e8e8;
}

.features-list {
  margin-bottom: 16px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.feature-item:last-child {
  border-bottom: none;
}

.feature-item span {
  font-size: 14px;
  color: #333;
}

.show-more-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 12px;
  background: white;
  border: 1px solid #e8e8e8;
  border-radius: 6px;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  transition: background 0.2s;
}

.show-more-btn:hover {
  background: #f8f8f8;
}

/* 5. 描述卡片 */
.description-card {
  margin-top: 8px;
  padding: 16px;
  background: white;
  border-bottom: 1px solid #e8e8e8;
}

.property-title {
  font-size: 18px;
  font-weight: 600;
  color: #000;
  margin: 0 0 8px 0;
}

.property-id {
  font-size: 12px;
  color: #999;
  margin: 0 0 12px 0;
}

.apply-info {
  padding: 8px 12px;
  background: #fff3cd;
  border-radius: 6px;
  margin-bottom: 16px;
}

.apply-info span {
  font-size: 12px;
  color: #856404;
}

.description-content {
  margin-bottom: 12px;
}

.description-text {
  font-size: 14px;
  line-height: 1.6;
  color: #333;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  line-clamp: 4; /* 标准属性，提升兼容性 */
  -webkit-box-orient: vertical;
}

.description-text.expanded {
  -webkit-line-clamp: unset;
  line-clamp: unset; /* 标准属性，提升兼容性 */
}

.read-more-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  background: none;
  border: none;
  font-size: 14px;
  font-weight: 500;
  color: #0066ff;
  cursor: pointer;
}

/* 6. 通勤部分 */
.commute-section {
  margin-top: 8px;
  padding: 16px;
  background: white;
  border-bottom: 1px solid #e8e8e8;
}

/* 底部操作栏 */
.sticky-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  gap: 12px;
  padding: 12px 16px;
  background: white;
  border-top: 1px solid #e8e8e8;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.footer-btn {
  flex: 1;
  height: 44px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: opacity 0.2s;
}

.enquire-btn {
  background-color: #e4002b;
}

.inspect-btn {
  background-color: #e4002b;
}

.footer-btn:active {
  opacity: 0.8;
}

/* 响应式设计 */
@media (min-width: 768px) {
  .image-container {
    height: 400px;
  }

  .main-content {
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  }
}
</style>
