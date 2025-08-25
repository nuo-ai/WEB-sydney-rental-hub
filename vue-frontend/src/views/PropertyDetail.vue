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

        <!-- 房源详情内容 -->
        <div v-else-if="property" class="property-detail-content">
          <!-- 1. 图片轮播区域 -->
          <div class="image-carousel-container">
            <!-- 悬浮导航按钮 -->
            <div class="header-actions">
              <el-button @click="goBack" circle class="header-btn" :icon="ArrowLeft" />
              <div class="right-actions">
                <el-button @click="toggleFavorite" circle class="header-btn">
                   <i :class="isFavorite ? 'fas fa-star' : 'far fa-star'" style="color: #000;"></i>
                </el-button>
                <el-button @click="shareProperty" circle class="header-btn" :icon="Share" />
              </div>
            </div>

            <div class="image-carousel" :class="{ 'single-image': images.length === 1 }">
              <div v-if="images.length > 0" class="carousel-wrapper">
                <img 
                  :src="images[currentImageIndex]" 
                  :alt="`房源图片 ${currentImageIndex + 1}`"
                  class="carousel-image"
                  @error="handleImageError"
                />
                
                <!-- 轮播控制按钮 -->
                <template v-if="images.length > 1">
                  <button 
                    @click="previousImage" 
                    class="carousel-btn prev-btn"
                    :disabled="currentImageIndex === 0"
                  >
                    <i class="el-icon-arrow-left"></i>
                  </button>
                  <button 
                    @click="nextImage" 
                    class="carousel-btn next-btn"
                    :disabled="currentImageIndex === images.length - 1"
                  >
                    <i class="el-icon-arrow-right"></i>
                  </button>
                  
                  <!-- 图片计数器 -->
                  <div class="image-counter">
                    {{ currentImageIndex + 1 }} / {{ images.length }}
                  </div>
                </template>
              </div>
              
              <!-- 无图片占位符 -->
              <div v-else class="no-image-placeholder">
                <i class="el-icon-picture text-6xl text-gray-300"></i>
                <p class="text-gray-500 mt-2">暂无图片</p>
              </div>
            </div>
          </div>

          <!-- 2. 核心信息区 -->
          <div class="core-info-section">
            <!-- 可用状态 -->
            <div class="availability-status">
              <span class="status-dot"></span>
              <span>{{ availabilityText }}</span>
            </div>

            <!-- 价格、地址、收藏 -->
            <div class="property-header">
              <div class="property-main-info">
                <h1 class="property-price">${{ property.rent_pw }} / week</h1>
                <div class="property-address-group">
                  <div class="address-line">
                    <h2 class="property-address">{{ property.address }}</h2>
                    <el-button @click="copyAddress" text class="copy-btn">
                      <i class="far fa-copy"></i>
                    </el-button>
                  </div>
                  <p class="property-suburb">{{ property.suburb }}, {{ property.postcode }}</p>
                </div>
              </div>
              <div class="property-actions">
                <!-- Actions moved to header -->
              </div>
            </div>
            
            <!-- 房型与可入住日期 -->
            <div class="property-specs">
              <div class="specs-row-single">
                <span class="spec-text">{{ propertySpecsText }}</span>
              </div>
              <div v-if="firstInspectionText" class="inspection-tag">
                <i class="far fa-calendar-check"></i>
                <span>{{ firstInspectionText }}</span>
              </div>
              <div class="availability-info">
                <p v-if="property.available_date" class="available-date">
                  可入住日期: {{ formatDate(property.available_date) }}
                </p>
                <p v-if="property.bond_amount" class="bond-info">
                  押金: ${{ property.bond_amount }}
                </p>
                <p v-if="property.is_furnished" class="furnished-info">
                  <i class="fas fa-couch"></i> 已配家具
                </p>
              </div>
            </div>
          </div>

          <!-- 3. 操作按钮组 -->
          <!-- This section is now replaced by the sticky footer -->

          <!-- 4. 房源描述 -->
          <div class="description-section">
            <h3 class="section-title">Property Description</h3>
            <div class="description-content">
              <p 
                class="description-text" 
                :class="{ 'expanded': isDescriptionExpanded }"
              >
                {{ property.description }}
              </p>
              <el-button 
                v-if="property.description && property.description.length > 200"
                type="primary" 
                link 
                @click="toggleDescription"
                class="read-more-btn"
              >
                {{ isDescriptionExpanded ? 'Read less' : 'Read more' }}
              </el-button>
            </div>
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
                <i class="el-icon-location text-4xl text-gray-400"></i>
                <p class="text-gray-500">地图功能开发中</p>
              </div>
            </div>
          </div>

          <!-- Inspection times are now a tag, this section can be removed if not repurposed -->
        </div>
      </div>
    </main>
    <!-- 粘性底部操作栏 -->
    <footer v-if="property" class="sticky-footer">
      <el-button class="footer-btn enquire-btn" @click="handleEmail">Enquire</el-button>
      <el-button class="footer-btn inspect-btn" @click="handleInspections">Inspect</el-button>
    </footer>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'
import { ArrowLeft, Share } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const propertiesStore = usePropertiesStore()

const propertyId = route.params.id

// 响应式状态
const currentImageIndex = ref(0)
const isDescriptionExpanded = ref(false)

// 计算属性
const property = computed(() => propertiesStore.currentProperty)
const loading = computed(() => propertiesStore.loading)
const error = computed(() => propertiesStore.error)

const images = computed(() => {
  if (!property.value) return []
  
  const imageUrls = []
  
  // 处理单个图片字段
  if (property.value.image_url) {
    imageUrls.push(property.value.image_url)
  }
  
  // 处理多个图片字段（如果存在）
  for (let i = 1; i <= 10; i++) {
    const imageField = property.value[`image_url_${i}`]
    if (imageField && imageField.trim() && !imageUrls.includes(imageField)) {
      imageUrls.push(imageField)
    }
  }
  
  // 过滤掉无效URL
  return imageUrls.filter(url => 
    url && 
    url.trim() && 
    url !== 'N/A' && 
    !url.includes('placeholder')
  )
})

const isFavorite = computed(() => {
  if (!property.value) return false
  return propertiesStore.favoriteIds.includes(property.value.listing_id)
})

const availabilityText = computed(() => {
  if (!property.value || !property.value.available_date) {
    return 'Availability not specified';
  }
  const availableDate = new Date(property.value.available_date);
  const now = new Date();
  now.setHours(0, 0, 0, 0);

  if (availableDate <= now) {
    return 'Available now';
  } else {
    return `Available from ${formatDate(property.value.available_date)}`;
  }
});

const propertySpecsText = computed(() => {
  if (!property.value) return '';
  const specs = [];
  if (property.value.bedrooms) specs.push(`${property.value.bedrooms} bed`);
  if (property.value.bathrooms) specs.push(`${property.value.bathrooms} bath`);
  if (property.value.parking_spaces) specs.push(`${property.value.parking_spaces} parking`);
  if (property.value.property_type) specs.push(property.value.property_type);
  return specs.join(' • ');
});

const firstInspectionText = computed(() => {
  if (inspectionTimes.value.length > 0) {
    const first = inspectionTimes.value[0];
    return `Inspection ${first.date}, ${first.time}`;
  }
  return null;
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

const formatDate = (dateString) => {
  if (!dateString) return ''
  
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    })
  } catch {
    return dateString
  }
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

onMounted(() => {
  console.log('Component Mounted. Property ID:', propertyId);
  propertiesStore.fetchPropertyDetail(propertyId).then(() => {
    console.log('After fetch, property is:', property.value);
  });
  propertiesStore.logHistory(propertyId);
});
</script>

<style scoped>
.property-detail-container {
  min-height: 100vh;
  background-color: #f0f2f5;
}

.header-actions {
  position: absolute;
  top: 16px;
  left: 16px;
  right: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 20;
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* 1. 图片轮播区域样式 */
.image-carousel-container {
  width: 100%;
  position: relative;
}

.image-carousel {
  width: 100%;
  aspect-ratio: 4/3; /* 移动端 4:3 比例 */
  position: relative;
  overflow: hidden;
  background-color: #f5f5f5;
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

.image-counter {
  position: absolute;
  bottom: 16px;
  right: 16px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 500;
}

.no-image-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
}

/* 2. 核心信息区样式 */
.core-info-section {
  padding: 24px;
}

.availability-status {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  font-size: 14px;
  font-weight: 500;
  color: #2d2d2d;
}

.status-dot {
  width: 8px;
  height: 8px;
  background-color: #007bff;
  border-radius: 50%;
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
.property-specs {
  border-top: 1px solid #e3e3e3;
  padding-top: 16px;
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
  gap: 6px;
  font-size: 14px;
  color: #595959;
}

.sticky-footer {
  position: sticky;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: white;
  padding: 16px 24px;
  display: flex;
  gap: 16px;
  border-top: 1px solid #e3e3e3;
  box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.08);
  z-index: 100;
}

.footer-btn {
  flex: 1;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 6px;
}

.enquire-btn {
  background-color: var(--juwo-primary) !important;
  color: white !important;
  border-color: var(--juwo-primary) !important;
}

.inspect-btn {
  background-color: #e64100 !important;
  color: white !important;
  border-color: #e64100 !important;
}

.spec-item i {
  font-size: 16px;
  color: #999;
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

@media (max-width: 767px) {
  .property-header {
    flex-direction: column;
    gap: 16px;
  }
  
  .property-actions {
    align-self: flex-end;
  }
  
  .specs-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .spec-divider {
    display: none;
  }
}
</style>
