<template>
  <div class="property-detail-container">
    <main class="main-content">
      <div class="container">
        <!-- 加载状态 -->
        <div v-if="loading" class="loading-spinner">
          <el-skeleton animated>
            <template #template>
              <div class="image-skeleton mb-4"></div>
              <el-skeleton-item variant="h1" class="mb-2" />
              <el-skeleton-item variant="text" class="mb-4" />
              <div class="flex gap-4 mb-4">
                <el-skeleton-item variant="button" />
                <el-skeleton-item variant="button" />
                <el-skeleton-item variant="button" />
              </div>
            </template>
          </el-skeleton>
        </div>

        <!-- 错误状态 -->
        <div v-else-if="error" class="error-message">
          <el-alert :title="error" type="error" show-icon />
        </div>

        <!-- 房源详情内容 - Clean Modern Design -->
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
                  <i class="fas fa-share-alt"></i>
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
                
                <!-- 轮播控制按钮 -->
                <template v-if="images.length > 1">
                  <button 
                    @click="previousImage" 
                    class="carousel-btn prev-btn"
                    :disabled="currentImageIndex === 0"
                  >
                    <el-icon><ArrowLeft /></el-icon>
                  </button>
                  <button 
                    @click="nextImage" 
                    class="carousel-btn next-btn"
                    :disabled="currentImageIndex === images.length - 1"
                  >
                    <el-icon><ArrowRight /></el-icon>
                  </button>
                  
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
                </template>
              </div>
              
              <!-- 无图片占位符 -->
              <div v-else class="no-image-placeholder">
                <el-icon :size="60"><Picture /></el-icon>
                <p class="text-gray-500 mt-2">暂无图片</p>
              </div>
            </div>
          </div>

          <!-- 2. 主信息卡片 -->
          <div class="info-card">
            <!-- 可用状态 -->
            <div class="availability-row">
              <span class="blue-dot">•</span>
              <span class="availability-text">{{ availabilityText }}</span>
            </div>

            <!-- 价格 -->
            <div class="price-row">
              <span class="price-amount">${{ property.rent_pw }}</span>
              <span class="price-period">per week</span>
            </div>

            <!-- 地址 -->
            <div class="address-row">
              <span class="address-text">{{ property.address }}</span>
            </div>
            
            <!-- 规格 -->
            <div class="specs-row">
              <div class="spec">
                <i class="fas fa-bed spec-icon"></i>
                <span>{{ property.bedrooms || 0 }}</span>
              </div>
              <div class="spec">
                <i class="fas fa-bath spec-icon"></i>
                <span>{{ property.bathrooms || 0 }}</span>
              </div>
              <div class="spec">
                <i class="fas fa-car spec-icon"></i>
                <span>{{ property.parking_spaces || 0 }}</span>
              </div>
            </div>
            
            <!-- 看房时间 -->
            <div v-if="property.inspection_times" class="inspection-row">
              <div class="inspection-label">Inspection Sat 30 Aug, 9:45 am</div>
            </div>
          </div>

          <!-- 3. Location 卡片 -->
          <div class="location-card">
            <h3 class="card-title">Location</h3>
            <div class="map-placeholder">
              <div class="map-image">
                <!-- 地图占位符 -->
                <img src="https://maps.googleapis.com/maps/api/staticmap?center={{ property.latitude }},{{ property.longitude }}&zoom=15&size=400x200&markers=color:red%7C{{ property.latitude }},{{ property.longitude }}&key=AIzaSyB41DRUbKWJHPxaFjMAwdrzWzbVKartNGg" 
                     alt="Location map" 
                     v-if="property.latitude && property.longitude"
                     @error="(e) => e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200"%3E%3Crect fill="%23f0f0f0" width="400" height="200"/%3E%3Ctext x="50%25" y="50%25" text-anchor="middle" dy=".3em" fill="%23999" font-family="Arial" font-size="14"%3EMap Loading...%3C/text%3E%3C/svg%3E'" />
                <div v-else class="map-fallback">
                  <i class="fas fa-map-marker-alt"></i>
                  <p>Map view unavailable</p>
                </div>
              </div>
            </div>
            <div class="travel-times-link">
              <i class="far fa-clock"></i>
              <span>See travel times</span>
              <span class="subtitle">Find out travel times from this property to your destination</span>
            </div>
          </div>

          <!-- 4. Property features 卡片 -->
          <div class="features-card" v-if="property.property_features && property.property_features.length">
            <h3 class="card-title">Property features</h3>
            <div class="features-list">
              <div v-for="(feature, index) in visibleFeatures" :key="index" class="feature-item">
                <i :class="getFeatureIcon(feature)"></i>
                <span>{{ feature }}</span>
              </div>
            </div>
            <button 
              v-if="property.property_features.length > 6" 
              @click="showAllFeatures = !showAllFeatures"
              class="show-more-btn"
            >
              {{ showAllFeatures ? 'Show less' : `Show ${property.property_features.length - 6} more` }}
              <i :class="showAllFeatures ? 'fas fa-chevron-up' : 'fas fa-chevron-down'"></i>
            </button>
          </div>

          <!-- 3. 操作按钮组 -->
          <!-- This section is now replaced by the sticky footer -->

          <!-- 5. 描述卡片 -->
          <div class="description-card" v-if="property.description">
            <div class="agent-header">
              <h3 class="property-title">{{ property.suburb }} modern apartment</h3>
              <p class="property-id">PROPERTY ID: {{ property.listing_id }}</p>
            </div>
            <div class="description-content">
              <p class="description-text" :class="{ 'expanded': isDescriptionExpanded }">
                {{ property.description }}
              </p>
            </div>
            <button 
              v-if="property.description && property.description.length > 200"
              @click="toggleDescription"
              class="read-more-btn"
            >
              {{ isDescriptionExpanded ? 'Read less' : 'Read more' }}
              <i :class="isDescriptionExpanded ? 'fas fa-chevron-up' : 'fas fa-chevron-down'"></i>
            </button>
          </div>

          <!-- 5. 地图位置 -->
          <div class="location-section">
            <div class="location-header">
              <h3 class="section-title">Location</h3>
              <el-button text class="expand-map-btn">
                <i class="fas fa-expand-arrows-alt"></i>
              </el-button>
            </div>
            <div class="map-container" id="detail-map">
              <div class="map-placeholder">
                <el-icon :size="40" color="#cbd5e1"><Location /></el-icon>
                <p class="text-gray-500">地图功能开发中</p>
              </div>
            </div>
          </div>

          <!-- 6. 通勤时间计算器 -->
          <div v-if="property && property.latitude && property.longitude" class="commute-section">
            <CommuteCalculator :property="property" />
          </div>

          <!-- Inspection times are now a tag, this section can be removed if not repurposed -->
        </div>
      </div>
    </main>
    <!-- 粘性底部操作栏 -->
    <footer v-if="property" class="sticky-footer">
      <button class="footer-btn enquire-btn" @click="handleEmail">Enquire</button>
      <button class="footer-btn inspect-btn" @click="handleInspections">Inspect</button>
    </footer>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, computed, ref, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'
import { ArrowLeft, ArrowRight, Share, DocumentCopy, Location, Star, StarFilled, Picture } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import CommuteCalculator from '@/components/CommuteCalculator.vue';

const route = useRoute()
const router = useRouter()
const propertiesStore = usePropertiesStore()

const propertyId = route.params.id

// 响应式状态
const currentImageIndex = ref(0)
const isDescriptionExpanded = ref(false)
const scrolled = ref(false)
const showAllFeatures = ref(false)

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

const visibleFeatures = computed(() => {
  if (!property.value || !property.value.property_features) return []
  if (showAllFeatures.value) {
    return property.value.property_features
  }
  return property.value.property_features.slice(0, 6)
})

const availabilityText = computed(() => {
  if (!property.value || !property.value.available_date) {
    return 'Available now';
  }
  
  const availDate = new Date(property.value.available_date)
  const today = new Date()
  today.setHours(0, 0, 0, 0);
  
  if (availDate <= today) {
    return 'Available now';
  }
  
  // Format date as "Available from DD/MM/YYYY"
  const day = availDate.getDate().toString().padStart(2, '0');
  const month = (availDate.getMonth() + 1).toString().padStart(2, '0');
  const year = availDate.getFullYear();
  
  return `Available from ${day}/${month}/${year}`;
});



const copyAddress = () => {
  if (!property.value) return;
  const fullAddress = `${property.value.address}, ${property.value.suburb}, NSW ${property.value.postcode}`;
  navigator.clipboard.writeText(fullAddress)
    .then(() => ElMessage.success('地址已复制到剪贴板'))
    .catch(() => ElMessage.error('复制失败'));
};

const inspectionTimes = computed(() => {
  if (!property.value || !property.value.inspection_times) return []
  
  // 处理inspection_times字符串或数组
  if (typeof property.value.inspection_times === 'string') {
    return property.value.inspection_times.split(',').map(time => ({
      date: time.split(' ')[0],
      time: time.split(' ')[1] || ''
    }))
  }
  
  return property.value.inspection_times || []
})

// 方法
const goBack = () => {
  router.go(-1)
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
  console.warn('图片加载失败:', event.target.src)
  // 可以设置默认占位图
  event.target.src = '/api/placeholder/400/300'
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
    }).catch(err => console.log('分享失败:', err))
  } else {
    // 备用方案：复制到剪贴板
    navigator.clipboard.writeText(window.location.href)
      .then(() => ElMessage.success('链接已复制到剪贴板'))
      .catch(() => ElMessage.error('复制失败'))
  }
}

const toggleDescription = () => {
  isDescriptionExpanded.value = !isDescriptionExpanded.value
}

// 获取功能图标
const getFeatureIcon = (feature) => {
  const featureLower = feature.toLowerCase()
  
  if (featureLower.includes('air condition')) return 'fas fa-snowflake feature-icon'
  if (featureLower.includes('alarm')) return 'fas fa-shield-alt feature-icon'
  if (featureLower.includes('balcony')) return 'fas fa-building feature-icon'
  if (featureLower.includes('wardrobe')) return 'fas fa-door-closed feature-icon'
  if (featureLower.includes('pool')) return 'fas fa-swimming-pool feature-icon'
  if (featureLower.includes('gym')) return 'fas fa-dumbbell feature-icon'
  if (featureLower.includes('parking') || featureLower.includes('garage')) return 'fas fa-car feature-icon'
  if (featureLower.includes('security')) return 'fas fa-lock feature-icon'
  if (featureLower.includes('laundry')) return 'fas fa-tshirt feature-icon'
  if (featureLower.includes('dishwasher')) return 'fas fa-utensils feature-icon'
  if (featureLower.includes('heating')) return 'fas fa-fire feature-icon'
  if (featureLower.includes('intercom')) return 'fas fa-phone feature-icon'
  
  return 'fas fa-check-circle feature-icon'
}

// 操作按钮处理函数
const handleEmail = () => {
  if (!property.value) return
  
  const subject = `咨询房源: ${property.value.address}`
  const body = `您好，我对以下房源感兴趣：\n\n地址: ${property.value.address}\n价格: $${property.value.rent_pw}/week\n\n请提供更多信息。\n\n谢谢！`
  
  window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`
}

const handleInspections = () => {
  if (inspectionTimes.value.length > 0) {
    ElMessage.info('看房预约功能开发中')
  } else {
    ElMessage.info('暂无看房时间安排')
  }
}

const openLightbox = () => {
  // 打开全屏图片查看器
  handleImageClick();
}

const handleImageClick = () => {
  // Fix lightbox styles after a short delay
  setTimeout(() => {
    const mask = document.querySelector('.el-image-viewer__mask');
    if (mask) {
      mask.style.position = 'fixed';
      mask.style.top = '0';
      mask.style.left = '0';
      mask.style.width = '100%';
      mask.style.height = '100%';
      mask.style.opacity = '0.95';
      mask.style.backgroundColor = '#000000';
    }
    
    // Add image counter
    const wrapper = document.querySelector('.el-image-viewer__wrapper');
    if (wrapper && !wrapper.querySelector('.custom-image-counter')) {
      const counter = document.createElement('div');
      counter.className = 'custom-image-counter';
      counter.style.position = 'absolute';
      counter.style.top = '20px';
      counter.style.left = '50%';
      counter.style.transform = 'translateX(-50%)';
      counter.style.color = 'white';
      counter.style.fontSize = '16px';
      counter.style.fontWeight = 'bold';
      counter.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
      counter.style.padding = '8px 16px';
      counter.style.borderRadius = '20px';
      counter.style.zIndex = '2002';
      
      // Find current image index
      const currentImg = wrapper.querySelector('.el-image-viewer__img');
      if (currentImg && currentImg.src) {
        const currentIndex = images.value.findIndex(img => currentImg.src.includes(img)) + 1;
        counter.textContent = `${currentIndex} / ${images.value.length}`;
      }
      
      wrapper.appendChild(counter);
      
      // Update counter when image changes
      const observer = new MutationObserver(() => {
        const img = wrapper.querySelector('.el-image-viewer__img');
        if (img && img.src) {
          const index = images.value.findIndex(imgSrc => img.src.includes(imgSrc)) + 1;
          counter.textContent = `${index} / ${images.value.length}`;
        }
      });
      
      observer.observe(wrapper, { 
        subtree: true, 
        attributes: true, 
        attributeFilter: ['src'] 
      });
    }
  }, 50);
}

// 滚动监听
const handleScroll = () => {
  scrolled.value = window.scrollY > 50
}

onMounted(() => {
  console.log('Component Mounted. Property ID:', propertyId);
  propertiesStore.fetchPropertyDetail(propertyId).then(() => {
    console.log('After fetch, property is:', property.value);
  });
  propertiesStore.logHistory(propertyId);
  
  // 添加滚动监听
  window.addEventListener('scroll', handleScroll)
});

// 清理监听器
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
});
</script>

<style scoped>
/* 全局容器 */
.property-detail-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* 沉浸式图片展示样式 - Immersive Gallery */
.immersive-gallery-container {
  position: relative;
  width: 100%;
  height: 60vh;
  min-height: 400px;
  max-height: 600px;
  background: #000;
  overflow: hidden;
}

/* 浮动导航栏 */
.floating-header {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  z-index: 100;
  background: transparent;
  transition: all 0.3s ease;
}

.float-nav-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: none;
  color: #333;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.float-nav-btn i {
  color: #333;
}

.float-nav-btn:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: scale(1.05);
}

.float-nav-btn:active {
  transform: scale(0.95);
}

.float-nav-btn.active {
  background: #ff385c;
  color: white;
}

.float-nav-btn.active i {
  color: white;
}

.back-btn {
  background: rgba(255, 255, 255, 0.9);
  color: #333;
}

.float-nav-actions {
  display: flex;
  gap: 8px;
}

/* 消动效果 */
.floating-header {
  transition: all 0.3s ease;
}

.floating-header.scrolled {
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.floating-header.scrolled .float-nav-btn {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 隐藏旧头部 */
.header-actions {
  display: none;
}

/* 图片渐变遮罩 */
.image-gradient-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 150px;
  background: linear-gradient(to top, rgba(0,0,0,0.6), transparent);
  pointer-events: none;
  z-index: 5;
}

/* 图片信息覆盖层 */
.image-info-overlay {
  position: absolute;
  bottom: 80px;
  left: 16px;
  right: 16px;
  z-index: 10;
}

.image-counter-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 13px;
  backdrop-filter: blur(10px);
}

.image-counter-badge i {
  font-size: 14px;
}

/* 缩略图导航条 */
.thumbnail-strip {
  position: absolute;
  bottom: 16px;
  left: 16px;
  right: 16px;
  z-index: 15;
}

.thumbnail-wrapper {
  display: flex;
  gap: 8px;
  padding: 8px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  overflow-x: auto;
  scrollbar-width: none;
}

.thumbnail-wrapper::-webkit-scrollbar {
  display: none;
}

.thumbnail-item {
  position: relative;
  flex-shrink: 0;
  width: 60px;
  height: 60px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.thumbnail-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumbnail-item.active {
  border-color: #5B67CA;
  transform: scale(1.1);
}

.thumbnail-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0);
  transition: background 0.3s;
}

.thumbnail-item:hover .thumbnail-overlay {
  background: rgba(0, 0, 0, 0.2);
}

.thumbnail-more {
  flex-shrink: 0;
  width: 60px;
  height: 60px;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.header-btn {
  background-color: rgba(255, 255, 255, 0.9) !important;
  border: 1px solid rgba(0, 0, 0, 0.05) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 40px;
  height: 40px;
}

.header-btn:hover {
  transform: scale(1.05);
}

.right-actions {
  display: flex;
  gap: 12px;
}

.main-content {
  width: 100%;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 16px;
}

.property-detail-content {
  background: white;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

/* 1. 图片轮播区域样式 */
/* 主图片展示区域 */
.gallery-viewport {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.gallery-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}

.gallery-main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  cursor: zoom-in;
  transition: transform 0.3s ease;
}

.gallery-main-image:hover {
  transform: scale(1.02);
}

@media (min-width: 768px) {
  .image-carousel {
    aspect-ratio: 16/10; /* 平板端 16:10 比例 */
  }
}

@media (min-width: 1024px) {
  .image-carousel {
    aspect-ratio: 16/9; /* 桌面端 16:9 比例 */
  }
}

.carousel-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 10;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.carousel-btn:hover {
  background: white;
  transform: translateY(-50%) scale(1.1);
}

.carousel-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: translateY(-50%) scale(1);
}

.prev-btn {
  left: 16px;
}

.next-btn {
  right: 16px;
}

/* 图片计数器和指示器 */
.image-counter {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  z-index: 10;
}

.image-indicators {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 6px;
  z-index: 10;
  padding: 8px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 20px;
}

.indicator-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s;
}

.indicator-dot.active {
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

/* 2. 核心信息区样式 - Realestate Style */
.core-info-section {
  padding: 16px;
  background: white;
}

/* 新的可用状态样式 */
.availability-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #333;
  font-size: 13px;
  font-weight: 400;
  margin-bottom: 8px;
}

.availability-badge .status-indicator {
  color: #00875a;
  font-size: 20px;
  line-height: 1;
}

/* 价格部分 */
.price-section {
  margin-bottom: 12px;
}

.price-amount {
  font-size: 28px;
  font-weight: 700;
  color: #000;
  margin: 0;
  line-height: 1.2;
}

.price-period {
  font-size: 14px;
  font-weight: 400;
  color: #333;
}

/* 地址部分 */
.address-section {
  margin-bottom: 12px;
}

.address-section .property-address {
  font-size: 15px;
  color: #333;
  margin: 0;
  line-height: 1.5;
  font-weight: 400;
}

/* 旧的状态样式 - 隐藏 */
.availability-status {
  display: none;
}

.status-dot {
  display: none;
}

.property-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.property-main-info {
  flex: 1;
}

.property-price {
  font-size: 26px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 8px 0;
  line-height: 1.2;
}

.property-address-group {
  margin-top: 4px;
}

.address-line {
  display: flex;
  align-items: center;
  gap: 8px;
}

.property-address {
  font-size: 16px;
  font-weight: 500;
  color: #2d2d2d;
  margin: 0;
  line-height: 1.4;
}

.copy-btn {
  padding: 0;
  height: auto;
  color: #999;
}

.copy-btn:hover {
  color: var(--juwo-primary);
}

.property-suburb {
  font-size: 16px;
  color: #595959;
  margin: 0;
  line-height: 1.3;
}

.property-actions {
  /* No longer needed as buttons are moved to header */
  display: none;
}

.action-btn-circle:hover {
  color: var(--juwo-primary);
  border-color: var(--juwo-primary);
}

.favorite-btn.is-favorite {
  color: #ffd700;
  border-color: #ffd700;
}

.favorite-btn.is-favorite:hover {
  color: #ffed4e;
  border-color: #ffed4e;
}

/* 房源规格信息 */
/* 房源规格样式 - Realestate Style */
.property-specs {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-top: 1px solid #e0e0e0;
  border-bottom: 1px solid #e0e0e0;
  margin-top: 4px;
}

.property-specs .spec-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 15px;
  color: #333;
  font-weight: 400;
}

.property-specs .spec-item i {
  font-size: 14px;
  color: #666;
}

.property-specs .spec-divider {
  color: #d4d4d4;
  font-size: 12px;
}

.property-specs .property-type {
  margin-left: auto;
  color: #666;
}

/* 看房时间样式 */
.inspection-time {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 0;
  font-size: 14px;
  color: #666;
}

.inspection-time i {
  color: #999;
}

.inspection-tag {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: #f0f2f5;
  color: #595959;
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 500;
  margin-top: 12px;
}

.specs-row-single {
  margin-bottom: 12px;
}

.spec-text {
  font-size: 16px;
  color: #595959;
  line-height: 1.5;
}

.spec-item {
  display: flex;
  align-items: center;
  gap: 8px; /* Consistent with PropertyCard */
  font-size: 14px;
  color: #595959;
}


/* Sticky Footer - Realestate Style */
.sticky-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: white;
  padding: 12px 16px;
  display: flex;
  gap: 12px;
  border-top: 1px solid #e8e8e8;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.footer-btn {
  flex: 1;
  height: 44px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.footer-btn:active {
  opacity: 0.8;
}

.enquire-btn {
  background-color: #e4002b;
  color: white;
}

.inspect-btn {
  background-color: #e4002b;
  color: white;
}


.availability-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.available-date,
.bond-info,
.furnished-info {
  font-size: 14px;
  color: #595959;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 6px;
}

.furnished-info i {
  color: #999;
}

/* 3. 操作按钮组样式 */
.action-buttons-section {
  padding: 0 24px;
  border-top: 1px solid #e3e3e3;
}

.action-buttons-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  padding: 16px 0;
}

@media (min-width: 768px) {
  .action-buttons-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    max-width: 400px;
  }
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 8px;
  background: transparent;
  border: none;
  color: var(--juwo-primary);
  border-radius: 6px;
  transition: background-color 0.2s ease;
  cursor: pointer;
}

.action-btn:hover {
  background: #fff3f0;
}

.action-btn i {
  font-size: 24px;
}

.action-btn span {
  font-size: 12px;
  font-weight: 600;
  text-align: center;
}

/* 4. 房源描述样式 */
.description-section,
.location-section {
  padding: 24px;
  border-top: 1px solid #e3e3e3;
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: #2d2d2d;
  margin: 0 0 16px 0;
}

@media (min-width: 768px) {
  .section-title {
    font-size: 22px;
  }
}

.description-content {
  position: relative;
}

.description-text {
  font-size: 14px;
  line-height: 1.6;
  color: #595959;
  margin: 0;
  max-height: 96px;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

@media (min-width: 768px) {
  .description-text {
    font-size: 16px;
    max-height: 128px;
  }
}

.description-text.expanded {
  max-height: none;
}

.read-more-btn {
  margin-top: 8px;
  padding: 0;
  font-size: 14px;
  font-weight: 600;
}

@media (min-width: 768px) {
  .read-more-btn {
    font-size: 16px;
  }
}

.commute-section {
  padding: 0 24px 24px 24px;
}

/* 5. 地图样式 */
.location-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.expand-map-btn {
  padding: 0;
  color: #999;
}

.expand-map-btn:hover {
  color: var(--juwo-primary);
}

.map-container {
  height: 192px;
  width: 100%;
  background-color: #f5f5f5;
  border-radius: 6px;
  overflow: hidden;
}

@media (min-width: 768px) {
  .map-container {
    height: 256px;
  }
}

@media (min-width: 1024px) {
  .map-container {
    height: 288px;
  }
}

.map-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
}

/* 6. 看房时间样式 */
.inspection-times {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.inspection-time-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid var(--juwo-primary);
}

.inspection-date {
  font-weight: 600;
  color: #2d2d2d;
}

.inspection-time {
  color: #595959;
  font-size: 14px;
}

/* 加载和错误状态样式 */
.loading-spinner {
  padding: 24px;
}

.image-skeleton {
  height: 200px;
  background: #f0f0f0;
  border-radius: 6px;
}

@media (min-width: 768px) {
  .image-skeleton {
    height: 300px;
  }
}

@media (min-width: 1024px) {
  .image-skeleton {
    height: 400px;
  }
}

.error-message {
  padding: 24px;
}

/* 响应式优化 */
@media (min-width: 768px) {
  .core-info-section,
  .description-section,
  .map-section,
  .inspections-section {
    padding: 32px;
  }
  
  .action-buttons-section {
    padding: 0 32px;
  }
  
  .property-price {
    font-size: 32px;
  }
  
  .property-address {
    font-size: 22px;
  }
  
  .property-suburb {
    font-size: 20px;
  }
  
  .specs-row {
    flex-wrap: nowrap;
  }
  
  .availability-info {
    flex-direction: row;
    gap: 24px;
  }
}

/* Mobile Styles - 沉浸式设计 */
@media (max-width: 767px) {
  .container {
    padding: 0;
  }
  
  .property-detail-content {
    padding-bottom: 80px; /* Space for sticky footer */
  }
  
  .immersive-gallery-container {
    height: 50vh;
    min-height: 350px;
  }
  
  .thumbnail-strip {
    bottom: 8px;
    left: 8px;
    right: 8px;
  }
  
  .thumbnail-item {
    width: 50px;
    height: 50px;
  }
  
  .section-title {
    font-size: 18px;
  }
}

/* Desktop Styles - 沉浸式设计 */
@media (min-width: 768px) {
  .immersive-gallery-container {
    height: 70vh;
    max-height: 700px;
  }
  
  .floating-header {
    padding: 24px;
  }
  
  .float-nav-btn {
    width: 48px;
    height: 48px;
    font-size: 18px;
  }
  
  .thumbnail-item {
    width: 80px;
    height: 80px;
  }
  
  .thumbnail-strip {
    bottom: 24px;
    left: 24px;
    right: auto;
  }
  
  .image-counter-badge {
    font-size: 14px;
    padding: 8px 16px;
  }
  
  .core-info-section {
    padding: 32px;
  }
  
  .sticky-footer {
    position: sticky;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .property-specs .property-type {
    display: none; /* Hide on desktop since it's obvious */
  }
}

/* Lightbox (el-image preview) styles - scoped with :deep() */
:deep(.el-image-viewer__wrapper) {
  z-index: 9999 !important;
}

:deep(.el-image-viewer__mask) {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  width: 100% !important;
  height: 100% !important;
  opacity: 1 !important;
  background-color: #000000 !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
}

:deep(.el-image-viewer__btn) {
  width: 44px !important;
  height: 44px !important;
  font-size: 24px !important;
  background-color: rgba(0, 0, 0, 0.5) !important;
  border-radius: 50% !important;
  opacity: 0.8 !important;
  transition: opacity 0.2s !important;
}

:deep(.el-image-viewer__btn:hover) {
  opacity: 1 !important;
}

:deep(.el-image-viewer__close) {
  top: 40px !important;
  right: 40px !important;
}

:deep(.el-image-viewer__actions) {
  background-color: rgba(0, 0, 0, 0.7) !important;
  border-radius: 22px !important;
  padding: 8px 22px !important;
}

:deep(.el-image-viewer__actions__inner) {
  color: white !important;
}
</style>
