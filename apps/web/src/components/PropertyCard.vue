<template>
  <Card class="property-card fade-in bg-background text-foreground border border-border rounded-[var(--radius)] shadow-sm hover:shadow-lg transition-all duration-200">
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
            :alt="$t('propertyCard.imageAlt')"
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
        :alt="$t('propertyCard.imageAlt')"
        class="single-image"
        @click="handleCardClick"
      />

      <!-- 图片计数器 (仅多图片时显示) -->
      <div v-if="validImages.length > 1" class="image-counter typo-meta">
        {{ currentImageIndex + 1 }} / {{ validImages.length }}
      </div>

      <!-- 移除图片上的按钮 -->

      <!-- 新房源标签 -->
      <div v-if="isNewProperty" class="property-status-tag typo-badge">
        {{ $t('propertyCard.newBadge') }}
      </div>
    </div>

    <!-- 房源内容区域 -->
    <div class="property-content" @click="handleCardClick">
      <!-- 价格和操作按钮行 -->
      <div class="property-header">
        <div class="property-price english-text typo-price">
          {{ formatPrice(property.rent_pw) }}
          <span class="price-unit typo-price-unit">{{ $t('propertyCard.perWeek') }}</span>
        </div>
        <div class="property-actions">
          <!-- 收藏按钮 -->
          <button
            class="action-btn favorite-btn focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            :class="{ 'is-favorite': isFavorite }"
            @click.stop="toggleFavorite"
            :title="$t('propertyCard.save')"
          >
            <Star :class="{ 'is-favorite': isFavorite }" class="spec-icon" />
          </button>
          <!-- 更多选项按钮 -->
          <el-dropdown trigger="click" @command="handleMoreAction">
            <button class="action-btn more-btn focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2" @click.stop>
              <MoreHorizontal class="spec-icon" />
            </button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="share">
                  <Share2 class="spec-icon" />
                  <span class="typo-body-sm">{{ $t('propertyCard.share') }}</span>
                </el-dropdown-item>
                <el-dropdown-item command="hide">
                  <EyeOff class="spec-icon" />
                  <span class="typo-body-sm">{{ $t('propertyCard.hide') }}</span>
                  <div class="typo-body-xs text-secondary" style="margin-left: 24px">
                    {{ $t('propertyCard.hideHint') }}
                  </div>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>

      <!-- 地址信息 - 两行显示，保持英文 -->
      <div class="property-address">
        <div class="property-address-primary english-text typo-address">
          {{ streetAddress }},
        </div>
        <div class="property-address-secondary english-text typo-address-secondary">
          {{ locationInfo }}
        </div>
      </div>

      <!-- 房型信息 - Lucide 图标 + 数字 -->
      <div class="property-features spec-row">
        <div class="feature-item spec-item">
          <BedDouble class="spec-icon" />
          <span class="spec-text typo-metric">{{ property.bedrooms || 0 }}</span>
        </div>
        <div class="feature-item spec-item">
          <Bath class="spec-icon" />
          <span class="spec-text typo-metric">{{ property.bathrooms || 0 }}</span>
        </div>
        <div class="feature-item spec-item">
          <CarFront class="spec-icon" />
          <span class="spec-text typo-metric">{{ property.parking_spaces || 0 }}</span>
        </div>
      </div>

      <!-- 底部信息区域 -->
      <div class="property-footer">
        <!-- 空出日期 - 中文显示 -->
        <div class="availability-text chinese-text typo-body-sm">
          {{ $t('propertyCard.availableDateLabel') }}:
          {{ formatAvailabilityDate(property.available_date) }}
        </div>

        <!-- 开放时间 - 中文显示 -->
        <div v-if="hasValidInspectionTime" class="inspection-text chinese-text typo-body-sm">
          {{ $t('propertyCard.inspectionTimeLabel') }}:
          {{ formatInspectionTime(property.inspection_times) }}
        </div>
      </div>
    </div>
  </Card>
</template>

<script setup>
import { ref, computed, inject, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { BedDouble, Bath, CarFront, Star, MoreHorizontal, Share2, EyeOff } from 'lucide-vue-next' // 导入 Lucide 图标
import { usePropertiesStore } from '@/stores/properties'
import { getCssVarValue } from '@/utils/designTokens'

const t = inject('t')

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

/* 响应式数据 */
const currentImageIndex = ref(0)
/* 根据视口动态设置轮播高度（移动端更紧凑；避免内联 style 覆盖 CSS 的高度） */
const windowWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1024)
const imageHeight = computed(() => (windowWidth.value <= 767 ? '180px' : '386px'))

const _onResize = () => {
  try {
    windowWidth.value = window.innerWidth
  } catch {
    /* no-op */
  }
}
onMounted(() => {
  try {
    window.addEventListener('resize', _onResize, { passive: true })
  } catch {
    /* no-op */
  }
})
onUnmounted(() => {
  try {
    window.removeEventListener('resize', _onResize)
  } catch {
    /* no-op */
  }
})

// 计算属性
const validImages = computed(() => {
  if (!props.property.images || !Array.isArray(props.property.images)) {
    return []
  }
  return props.property.images.filter((url) => url && typeof url === 'string' && url.trim() !== '')
})

const placeholderImage = computed(() => {
  const background = getCssVarValue('--gray-100', '#f3f4f6')
  const foreground = getCssVarValue('--gray-400', '#9ca3af')
  const fontFamily = getCssVarValue('--font-family-en-sans', 'Inter, sans-serif')
  const fontSize = getCssVarValue('--font-size-lg', '18px')
  const placeholderSvg = `<svg width="580" height="386" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="${background}"/><text x="50%" y="50%" font-family="${fontFamily}" font-size="${fontSize}" dy=".3em" fill="${foreground}" text-anchor="middle">${t('propertyCard.imageAlt')}</text></svg>`
  return `data:image/svg+xml,${encodeURIComponent(placeholderSvg)}`
})

const streetAddress = computed(() => {
  if (!props.property.address) return t('propertyCard.unknownAddress')
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
  const hasValidContent =
    /\d/.test(times) &&
    (times.includes('day') || times.includes('Day') || times.includes('周') || times.includes(':'))

  return hasValidContent
})

// 方法
const formatPrice = (price) => {
  if (!price) return t('propertyCard.priceTBA')
  return `$${price}`
}

const formatAvailabilityDate = (dateString) => {
  if (!dateString) return t('propertyCard.availableNow')

  const availDate = new Date(dateString)
  const today = new Date()

  if (availDate <= today) {
    return t('propertyCard.availableNow')
  }

  // 格式化为中文日期
  const year = availDate.getFullYear()
  const month = availDate.getMonth() + 1
  const day = availDate.getDate()

  return t('propertyCard.availableDateFormat', { year, month, day })
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
  propertiesStore.toggleFavorite(props.property)
}

// 处理更多操作菜单
const handleMoreAction = (command) => {
  if (command === 'share') {
    // 实现分享功能
    const shareUrl = `${window.location.origin}/property/${props.property.listing_id}`
    navigator.clipboard.writeText(shareUrl)
    ElMessage.success(t('propertyCard.shareCopied'))
  } else if (command === 'hide') {
    // 实现隐藏功能
    propertiesStore.hideProperty(props.property.listing_id)
    ElMessage.info(t('propertyCard.hideSuccess'))
  }
}
</script>

<style scoped>
/* 房源卡片样式 - 复用现有设计 */
.property-card {
  width: 100%;
  max-width: 580px;
  background: hsl(var(--background));
  border: 1px solid hsl(var(--border));
  border-radius: var(--radius);
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
  color: var(--color-text-inverse) !important; /* 中文注释：使用反色文本令牌，替代命名色 white */
  width: 40px !important;
  height: 60px !important;
  font-size: var(--size-24) !important;
  opacity: 0.7;
  transition: opacity 0.3s ease !important;
  border: none !important;
  box-shadow: none !important;
  top: 50% !important;
  transform: translateY(-50%) !important;
  text-shadow: 0 1px 3px rgb(0 0 0 / 50%);
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
  color: var(--color-text-inverse) !important; /* 中文注释：hover 保持反色文本令牌 */
  opacity: 1;
  transform: translateY(-50%) scale(1.1) !important;
}

/* 移除Element Plus的点击效果 */
.property-carousel :deep(.el-carousel__arrow):focus,
.property-carousel :deep(.el-carousel__arrow):active {
  background: transparent !important;
  color: var(--color-text-inverse) !important; /* 中文注释：focus/active 统一反色文本令牌 */
  outline: none !important;
}

/* 图片计数器 - 更简洁 */
.image-counter {
  position: absolute;
  bottom: 12px;
  left: 12px;
  background: var(--overlay-dark-75);
  color: var(--color-text-inverse); /* 中文注释：反色文本令牌，便于主题切换与高对比 */
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
  color: var(--text-contrast-medium);
  padding: 0;
}

.action-btn:hover {
  color: var(--text-contrast-strong);
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
  color: var(--accent-primary);
  fill: var(--accent-primary);
}

/* 更多选项按钮 */

/* 新房源标签 - 更优雅 */
.property-status-tag {
  position: absolute;
  top: 12px;
  left: 12px;
  background: hsl(var(--primary)); /* 统一走核心主色变量 */
  color: var(--color-text-inverse); /* 中文注释：文本走反色令牌，确保可读性与高对比模式 */
  padding: 4px 10px;
  border-radius: 4px;
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
  color: var(--text-contrast-strong);
  margin-bottom: 8px;
}

.price-unit {
  color: var(--text-contrast-medium);
}

/* 地址信息 - 两行显示 */
.property-address {
  margin-bottom: 12px;
}

.property-address-primary {
  color: var(--text-contrast-strong);
  margin-bottom: 4px;
}

.property-address-secondary {
  color: var(--text-contrast-medium);
}

/* 房型信息图标 - Lucide */
.property-features {
  display: flex;
  align-items: center;
  /* 中文注释：统一房型图标尺寸与间距，通过变量便于全局调参（前端表现：更紧凑、更对齐） */
  /* 覆写全局 spec-* 变量，生效于本卡片 */
  --spec-icon-size: 18px;       /* 图标尺寸 */
  --spec-text-size: 14px;       /* 数字字号 */
  --spec-line-height: 18px;     /* 行高与图标对齐 */
  --spec-item-gap: 12px;        /* 三项之间的水平间距 */
  --spec-icon-gap: 6px;         /* 图标与数字之间的间距 */

  /* 兼容旧的 amenity 变量（保留以便回滚/参考，不参与最终计算） */
  --amenity-icon-size: 18px;    /* 图标视觉尺寸 */
  --amenity-item-gap: 12px;     /* 三项之间的水平间距 */
  --amenity-icon-gap: 6px;      /* 图标与数字之间的间距 */

  gap: 0; /* 间距交由 .spec-row 的 margin-left 控制，避免与 gap 叠加 */
  margin-bottom: 12px;
  color: var(--text-contrast-medium);
}

.feature-item {
  display: flex;
  align-items: center;
  gap: var(--amenity-icon-gap); /* 图标与数字间距 */
}

.feature-item .spec-icon {
  width: var(--amenity-icon-size);
  height: var(--amenity-icon-size);
  flex: 0 0 auto; /* 避免被压缩导致光学不一致 */
}

.feature-item .spec-text {
}

.feature-item span {
  color: var(--text-contrast-strong);
}

/* 底部信息区域 */
.property-footer {
  border-top: 1px solid hsl(var(--border));
  margin-top: 8px;
  padding-top: 8px;
  margin-bottom: 0;
}

.availability-text {
  color: var(--text-contrast-medium);
  margin-bottom: 4px;
}

.inspection-text {
  color: var(--accent-primary);
}

/* 响应式适配 */
@media (width <= 767px) {
  .property-card {
    width: 100vw;
    max-width: 100vw;
    margin: 0 calc(50% - 50vw) 20px;
    border-radius: 0; /* 满屏出血：去圆角 */
  }

  .property-image-container {
    height: 180px;
  }

  .property-carousel :deep(.el-carousel__container) {
    height: 180px;
  }

  /* 更紧凑的移动端内容间距（不影响桌面） */
  .property-content {
    padding: 12px;
  }

  .property-address {
    margin-bottom: 8px;
  }

  .property-features {
    --amenity-item-gap: 8px;
    --amenity-icon-gap: 4px;
    margin-bottom: 8px;
  }
}

@media (width >= 768px) {
  .property-card {
    width: 580px;
    margin: 0 0 20px;
  }
}
</style>
