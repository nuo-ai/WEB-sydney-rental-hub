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

      <!-- 移除图片上的按钮 -->

      <!-- 新房源标签 -->
      <div v-if="isNewProperty" class="property-status-tag">New</div>
    </div>

    <!-- 房源内容区域 -->
    <div class="property-content" @click="handleCardClick">
      <!-- 价格和操作按钮行 -->
      <div class="property-header">
        <div class="property-price english-text">
          {{ formatPrice(property.rent_pw) }}
          <span class="price-unit">per week</span>
        </div>
        <div class="property-actions">
          <!-- 收藏按钮 -->
          <button
            class="action-btn favorite-btn"
            :class="{ 'is-favorite': isFavorite }"
            @click.stop="toggleFavorite"
            title="Save"
          >
            <Star :class="{ 'is-favorite': isFavorite }" class="spec-icon" />
          </button>
          <!-- 更多选项按钮 -->
          <el-dropdown trigger="click" @command="handleMoreAction">
            <button class="action-btn more-btn" @click.stop>
              <MoreHorizontal class="spec-icon" />
            </button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="share">
                  <Share2 class="spec-icon" />
                  <span>Share</span>
                </el-dropdown-item>
                <el-dropdown-item command="hide">
                  <EyeOff class="spec-icon" />
                  <span>Hide</span>
                  <div style="font-size: 12px; color: #999; margin-left: 24px">
                    Remove from results
                  </div>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>

      <!-- 地址信息 - 两行显示，保持英文 -->
      <div class="property-address english-text">
        <div class="property-address-primary">{{ streetAddress }},</div>
        <div class="property-address-secondary">{{ locationInfo }}</div>
      </div>

      <!-- 房型信息 - Lucide 图标 + 数字 -->
      <div class="property-features spec-row">
        <div class="feature-item spec-item">
          <BedDouble class="spec-icon" />
          <span class="spec-text">{{ property.bedrooms || 0 }}</span>
        </div>
        <div class="feature-item spec-item">
          <Bath class="spec-icon" />
          <span class="spec-text">{{ property.bathrooms || 0 }}</span>
        </div>
        <div class="feature-item spec-item">
          <CarFront class="spec-icon" />
          <span class="spec-text">{{ property.parking_spaces || 0 }}</span>
        </div>
      </div>

      <!-- 底部信息区域 -->
      <div class="property-footer">
        <!-- 空出日期 - 中文显示 -->
        <div class="availability-text chinese-text">
          空出日期: {{ formatAvailabilityDate(property.available_date) }}
        </div>

        <!-- 开放时间 - 中文显示 -->
        <div v-if="hasValidInspectionTime" class="inspection-text chinese-text">
          开放时间: {{ formatInspectionTime(property.inspection_times) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { BedDouble, Bath, CarFront, Star, MoreHorizontal, Share2, EyeOff } from 'lucide-vue-next' // 导入 Lucide 图标
import { usePropertiesStore } from '@/stores/properties'

const props = defineProps({
  property: {
    type: Object,
    required: true,
  },
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
  return props.property.images.filter((url) => url && typeof url === 'string' && url.trim() !== '')
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

const isNewProperty = computed(() => {
  return props.property.listing_id > 2500
})

const hasValidInspectionTime = computed(() => {
  const times = props.property.inspection_times
  if (!times || typeof times !== 'string' || times.trim() === '') {
    return false
  }

  // 检查是否包含有效的日期/时间信息
  const hasValidContent = /\d/.test(times) &&
    (times.includes('day') || times.includes('Day') ||
     times.includes('周') || times.includes(':'))

  return hasValidContent
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
  // 严格验证输入
  if (!timeString || typeof timeString !== 'string' || timeString.trim() === '') {
    return ''
  }

  const trimmed = timeString.trim()

  // 检查是否包含有效的时间信息
  if (!/\d/.test(trimmed)) {
    return ''
  }

  // 执行中文转换
  let formatted = trimmed
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

const toggleFavorite = () => {
  propertiesStore.toggleFavorite(props.property.listing_id)
}

// 处理更多操作菜单
const handleMoreAction = (command) => {
  if (command === 'share') {
    // 实现分享功能
    const shareUrl = `${window.location.origin}/property/${props.property.listing_id}`
    navigator.clipboard.writeText(shareUrl)
    ElMessage.success('链接已复制到剪贴板')
  } else if (command === 'hide') {
    // 实现隐藏功能
    propertiesStore.hideProperty(props.property.listing_id)
    ElMessage.info('已从搜索结果中移除')
  }
}
</script>

<style scoped>
/* 房源卡片样式 - 复用现有设计 */
.property-card {
  width: 580px;
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-default);
  border-radius: 6px;
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

/* Element Plus轮播样式定制 - 去除圆圈，垂直居中 */
.property-carousel :deep(.el-carousel__container) {
  height: 386px;
}

/* 轮播箭头 - 无背景，直接显示箭头 */
.property-carousel :deep(.el-carousel__arrow) {
  background: transparent !important;
  color: white !important;
  width: 40px !important;
  height: 60px !important;
  font-size: 24px !important;
  opacity: 0.7;
  transition: opacity 0.3s ease !important;
  border: none !important;
  box-shadow: none !important;
  top: 50% !important;
  transform: translateY(-50%) !important;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
}

/* 左箭头位置 */
.property-carousel :deep(.el-carousel__arrow--left) {
  left: 10px !important;
}

/* 右箭头位置 */
.property-carousel :deep(.el-carousel__arrow--right) {
  right: 10px !important;
}

/* 鼠标悬停在图片区域时箭头更明显 */
.property-image-container:hover .property-carousel :deep(.el-carousel__arrow) {
  opacity: 1;
}

/* 鼠标悬停在箭头上时 */
.property-carousel :deep(.el-carousel__arrow):hover {
  background: transparent !important;
  color: white !important;
  opacity: 1;
  transform: translateY(-50%) scale(1.1) !important;
}

/* 移除Element Plus的点击效果 */
.property-carousel :deep(.el-carousel__arrow):focus,
.property-carousel :deep(.el-carousel__arrow):active {
  background: transparent !important;
  color: white !important;
  outline: none !important;
}

/* 图片计数器 - 更简洁 */
.image-counter {
  position: absolute;
  bottom: 12px;
  left: 12px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  font-size: 11px;
  font-weight: 400;
  padding: 3px 8px;
  border-radius: 4px;
  z-index: 10;
}

/* 房源头部区域 - 价格和操作按钮 */
.property-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

/* 操作按钮容器 */
.property-actions {
  display: flex;
  align-items: center;
  gap: 2px; /* 按钮更紧凑 */
}

/* 通用操作按钮样式 */
.action-btn {
  background: transparent;
  border: none;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #9b9b9b;
  padding: 0;
}

.action-btn:hover {
  color: #6b6b6b;
}

.action-btn:focus,
.action-btn:active {
  outline: none;
  background: transparent;
}

.action-btn .spec-icon {
  width: 22px;
  height: 22px;
}

/* 收藏按钮样式 */
.favorite-btn .spec-icon.is-favorite {
  color: #ff5824;
  fill: #ff5824;
}

/* 更多选项按钮 */

/* 新房源标签 - 更优雅 */
.property-status-tag {
  position: absolute;
  top: 12px;
  left: 12px;
  background: #22c55e;
  color: white;
  font-size: 10px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  z-index: 10;
}

/* 下拉菜单项统一样式 */
:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
}

:deep(.el-dropdown-menu__item) .spec-icon {
  margin-right: 8px;
  width: 16px; /* 匹配下拉菜单的紧凑布局 */
  height: 16px;
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

/* 房型信息图标 - Lucide */
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

.feature-item span {
  color: #000000;
  font-weight: 600;
  font-size: 14px;
}

/* 底部信息区域 */
.property-footer {
  border-top: 1px solid #e5e7eb;
  margin-top: 8px;
  padding-top: 8px;
  margin-bottom: 0;
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

/* 响应式适配 */
@media (max-width: 767px) {
  .property-card {
    width: 100vw;
    max-width: 100vw;
    margin-left: calc(50% - 50vw);
    margin-right: calc(50% - 50vw);
    margin-top: 0;
    margin-bottom: 20px;
    border-radius: 0; /* 满屏出血：去圆角 */
  }

  .property-image-container {
    height: 250px;
  }

  .property-carousel :deep(.el-carousel__container) {
    height: 250px;
  }
}

@media (min-width: 768px) {
  .property-card {
    width: 580px;
    margin: 0 0 20px 0;
  }
}
</style>
