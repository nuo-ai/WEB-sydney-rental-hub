<template>
  <div class="property-card fade-in">
    <!-- 图片轮播区域 -->
    <div class="property-image-container">
      <el-carousel
        v-if="validImages.length > 0"
        :height="imageHeight"
        indicator-position="none"
        arrow="always"
        @change="onCarouselChange"
        class="property-carousel"
      >
        <el-carousel-item v-for="(image, index) in validImages" :key="index">
          <img 
            :src="image" 
            :alt="`房源图片 ${index + 1}`"
            @error="handleImageError"
            class="carousel-image"
            @click="handleCardClick"
          />
        </el-carousel-item>
      </el-carousel>
      
      <!-- 备用单图片显示 -->
      <img 
        v-else
        :src="placeholderImage"
        alt="房源图片"
        class="single-image"
        @click="handleCardClick"
      />
      
      <!-- 图片计数器 (仅多图片时显示) -->
      <div v-if="validImages.length > 1" class="image-counter">
        {{ currentImageIndex + 1 }} / {{ validImages.length }}
      </div>
      
      <!-- 收藏按钮 -->
      <button 
        class="favorite-btn"
        :class="{ 'is-favorite': isFavorite }"
        @click.stop="toggleFavorite"
      >
        <i :class="favoriteIconClass"></i>
      </button>
      
      <!-- 新房源标签 -->
      <div v-if="isNewProperty" class="property-status-tag">
        New
      </div>
    </div>
    
    <!-- 房源内容区域 -->
    <div class="property-content" @click="handleCardClick">
      <!-- 价格显示 - 保持英文格式 -->
      <div class="property-price english-text">
        {{ formatPrice(property.rent_pw) }}
        <span class="price-unit">per week</span>
      </div>
      
      <!-- 地址信息 - 两行显示，保持英文 -->
      <div class="property-address english-text">
        <div class="property-address-primary">{{ streetAddress }},</div>
        <div class="property-address-secondary">{{ locationInfo }}</div>
      </div>
      
      <!-- 房型信息 - Font Awesome图标 + 数字 -->
      <div class="property-features">
        <div class="feature-item">
          <i class="fa-solid fa-bed"></i>
          <span>{{ property.bedrooms || 0 }}</span>
        </div>
        <div class="feature-item">
          <i class="fa-solid fa-bath"></i>
          <span>{{ property.bathrooms || 0 }}</span>
        </div>
        <div class="feature-item">
          <i class="fa-solid fa-car"></i>
          <span>{{ property.parking_spaces || 0 }}</span>
        </div>
      </div>
      
      <!-- 房源特色 - 中文显示 -->
      <div v-if="propertyFeatures.length > 0" class="property-amenities chinese-text">
        <span v-for="feature in propertyFeatures" :key="feature" class="amenity-tag">
          {{ feature }}
        </span>
      </div>
      
      <!-- 底部信息区域 -->
      <div class="property-footer">
        <!-- 空出日期 - 中文显示 -->
        <div class="availability-text chinese-text">
          空出日期: {{ formatAvailabilityDate(property.available_date) }}
        </div>
        
        <!-- 开放时间 - 中文显示 -->
        <div v-if="property.inspection_times" class="inspection-text chinese-text">
          开放时间: {{ formatInspectionTime(property.inspection_times) }}
        </div>
      </div>
      
      <!-- 操作按钮 -->
      <div class="property-actions" @click.stop>
        <el-button 
          class="action-btn favorite-action"
          :type="isFavorite ? 'primary' : 'default'"
          :icon="isFavorite ? 'StarFilled' : 'Star'"
          @click="toggleFavorite"
        >
          {{ isFavorite ? '已收藏' : '收藏' }}
        </el-button>
        
        <el-button 
          type="primary"
          class="action-btn contact-action"
          @click="handleContact"
        >
          联系我们
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { usePropertiesStore } from '@/stores/properties'

// 组件属性
const props = defineProps({
  property: {
    type: Object,
    required: true
  }
})

// 组件事件
const emit = defineEmits(['click', 'contact'])

// 状态管理
const propertiesStore = usePropertiesStore()

// 响应式数据
const currentImageIndex = ref(0)
const imageHeight = ref('386px')

// 计算属性
const validImages = computed(() => {
  if (!props.property.images || !Array.isArray(props.property.images)) {
    return []
  }
  return props.property.images.filter(url => url && typeof url === 'string' && url.trim() !== '')
})

const placeholderImage = computed(() => {
  const placeholderSvg = `<svg width="580" height="386" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#f3f4f6"/><text x="50%" y="50%" font-family="Inter, sans-serif" font-size="18" dy=".3em" fill="#9ca3af" text-anchor="middle">Property Image</text></svg>`
  return `data:image/svg+xml,${encodeURIComponent(placeholderSvg)}`
})

const streetAddress = computed(() => {
  if (!props.property.address) return '地址未知'
  const addressParts = props.property.address.split(',')
  return addressParts[0]?.trim() || props.property.address
})

const locationInfo = computed(() => {
  const postcode = props.property.postcode ? Math.floor(props.property.postcode) : ''
  return `${props.property.suburb || ''} NSW ${postcode}`.trim().toUpperCase()
})

const isFavorite = computed(() => {
  return propertiesStore.isFavorite(props.property.listing_id)
})

const favoriteIconClass = computed(() => {
  return isFavorite.value ? 'fa-solid fa-star' : 'fa-regular fa-star'
})

const isNewProperty = computed(() => {
  return props.property.listing_id > 2500
})

const propertyFeatures = computed(() => {
  const features = []
  
  // 根据property数据生成中文特色标签
  if (props.property.is_furnished) features.push('带家具')
  if (props.property.has_air_conditioning) features.push('空调')
  if (props.property.has_balcony) features.push('阳台') 
  if (props.property.has_gym) features.push('健身房')
  if (props.property.has_pool) features.push('游泳池')
  if (props.property.has_parking) features.push('停车位')
  
  return features.slice(0, 4) // 最多显示4个特色
})

// 方法
const formatPrice = (price) => {
  if (!price) return 'Price TBA'
  return `$${price}`
}

const formatAvailabilityDate = (dateString) => {
  if (!dateString) return '立即入住'
  
  const availDate = new Date(dateString)
  const today = new Date()
  
  if (availDate <= today) {
    return '立即入住'
  }
  
  // 格式化为中文日期
  const year = availDate.getFullYear()
  const month = availDate.getMonth() + 1
  const day = availDate.getDate()
  
  return `${year}年${month}月${day}日`
}

const formatInspectionTime = (timeString) => {
  if (!timeString) return ''
  
  // 简单的英文到中文时间转换
  let formatted = timeString
  formatted = formatted.replace(/Monday/g, '周一')
  formatted = formatted.replace(/Tuesday/g, '周二')
  formatted = formatted.replace(/Wednesday/g, '周三')
  formatted = formatted.replace(/Thursday/g, '周四')
  formatted = formatted.replace(/Friday/g, '周五')
  formatted = formatted.replace(/Saturday/g, '周六')
  formatted = formatted.replace(/Sunday/g, '周日')
  formatted = formatted.replace(/Mon/g, '周一')
  formatted = formatted.replace(/Tue/g, '周二')
  formatted = formatted.replace(/Wed/g, '周三')
  formatted = formatted.replace(/Thu/g, '周四')
  formatted = formatted.replace(/Fri/g, '周五')
  formatted = formatted.replace(/Sat/g, '周六')
  formatted = formatted.replace(/Sun/g, '周日')
  
  return formatted
}

const onCarouselChange = (index) => {
  currentImageIndex.value = index
}

const handleImageError = (event) => {
  event.target.src = placeholderImage.value
}

const handleCardClick = () => {
  emit('click', props.property)
}

const handleContact = () => {
  emit('contact', props.property)
}

const toggleFavorite = () => {
  propertiesStore.toggleFavorite(props.property.listing_id)
}
</script>

<style scoped>
/* 房源卡片样式 - 复用现有设计 */
.property-card {
  width: 580px;
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
  cursor: pointer;
  margin-bottom: 20px;
}

.property-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

/* 图片容器 */
.property-image-container {
  position: relative;
  width: 100%;
  height: 386px;
  overflow: hidden;
}

.carousel-image,
.single-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Element Plus轮播样式定制 */
.property-carousel :deep(.el-carousel__container) {
  height: 386px;
}

.property-carousel :deep(.el-carousel__arrow) {
  background: rgba(255, 255, 255, 0.9);
  color: #333;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 14px;
}

.property-carousel :deep(.el-carousel__arrow):hover {
  background: white;
}

/* 图片计数器 */
.image-counter {
  position: absolute;
  bottom: 12px;
  left: 12px;
  background: rgba(0, 0, 0, 0.75);
  color: white;
  font-size: 11px;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 4px;
  z-index: 10;
}

/* 收藏按钮 */
.favorite-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
  z-index: 10;
  color: #666;
}

.favorite-btn:hover {
  background: white;
  transform: scale(1.05);
}

.favorite-btn.is-favorite i {
  color: var(--juwo-primary);
}

/* 新房源标签 */
.property-status-tag {
  position: absolute;
  top: 12px;
  left: 12px;
  background: #22c55e;
  color: white;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 4px;
  text-transform: uppercase;
  z-index: 10;
}

/* 房源内容区域 */
.property-content {
  padding: 16px;
}

/* 价格显示 - 匹配现有设计 */
.property-price {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text-price);
  line-height: 1.2;
  margin-bottom: 8px;
}

.price-unit {
  font-size: 14px;
  color: #666666;
  font-weight: 400;
}

/* 地址信息 - 两行显示 */
.property-address {
  margin-bottom: 12px;
}

.property-address-primary {
  font-size: 15px;
  color: #333333;
  font-weight: 500;
  line-height: 1.3;
  margin-bottom: 4px;
}

.property-address-secondary {
  font-size: 13px;
  color: #666666;
  font-weight: 500;
  line-height: 1.3;
}

/* 房型信息图标 - Font Awesome */
.property-features {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
  color: #666666;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.feature-item i {
  font-size: 14px;
  width: 16px;
  text-align: center;
}

.feature-item span {
  color: #000000;
  font-weight: 600;
  font-size: 14px;
}

/* 房源特色标签 */
.property-amenities {
  margin-bottom: 12px;
}

.amenity-tag {
  display: inline-block;
  background: var(--juwo-primary-50);
  color: var(--juwo-primary);
  font-size: 12px;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 6px;
  margin-right: 6px;
  margin-bottom: 4px;
}

/* 底部信息区域 */
.property-footer {
  border-top: 1px solid #e5e7eb;
  margin-top: 8px;
  padding-top: 8px;
  margin-bottom: 16px;
}

.availability-text {
  color: #4b5563;
  font-size: 13px;
  font-weight: 400;
  margin-bottom: 4px;
}

.inspection-text {
  color: #2563eb;
  font-size: 12px;
  font-weight: 500;
}

/* 操作按钮 */
.property-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.action-btn {
  flex: 1;
  font-weight: 600;
}

.favorite-action.el-button--default {
  border-color: var(--color-border-default);
  color: var(--color-text-secondary);
}

.favorite-action.el-button--primary {
  background-color: var(--juwo-primary);
  border-color: var(--juwo-primary);
}

.contact-action {
  background-color: var(--juwo-primary);
  border-color: var(--juwo-primary);
}

/* 响应式适配 */
@media (max-width: 767px) {
  .property-card {
    width: 100%;
    max-width: 580px;
    margin: 0 auto 20px auto;
  }
  
  .property-image-container {
    height: 250px;
  }
  
  .property-carousel :deep(.el-carousel__container) {
    height: 250px;
  }
  
  .property-actions {
    flex-direction: column;
    gap: 8px;
  }
}

@media (min-width: 768px) and (max-width: 1023px) {
  .property-card {
    width: 100%;
    max-width: 400px;
  }
  
  .property-image-container {
    height: 300px;
  }
  
  .property-carousel :deep(.el-carousel__container) {
    height: 300px;
  }
}
</style>
