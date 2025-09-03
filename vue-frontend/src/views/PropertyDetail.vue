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
                <i :class="isFavorite ? 'fa-solid fa-star' : 'fa-regular fa-star'"></i>
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
          <!-- 价格 -->
          <div class="price-wrapper">
            <span class="price-text">${{ property.rent_pw }} per week</span>
          </div>

          <!-- 地址 -->
          <div class="address-wrapper">
            <h1 class="address-main">{{ property.address }}</h1>
            <p class="address-subtitle">{{ property.suburb }}, NSW {{ property.postcode || '' }}</p>
          </div>

          <!-- 房源特征 -->
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

          <!-- 可用日期和押金 -->
          <div class="availability-info">
            <span class="availability-label">Available from {{ getAvailableDate() }}</span>
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
                :src="staticMapUrl"
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

        <!-- Property Description -->
        <section class="description-section" v-if="property.property_headline || property.description">
          <h2 class="section-title">Property Description</h2>

          <div class="description-content">
            <div class="description-text" :class="{ expanded: isDescriptionExpanded }">
              <!-- 使用后端字段渲染，移除硬编码占位文本
                   原因：与后端数据契约对齐（详情端点为超集），避免错误展示 -->
              <p v-if="property.property_headline" class="description-headline">{{ property.property_headline }}</p>
              <p v-if="property.description">{{ property.description }}</p>
            </div>
            <button
              @click="toggleDescription"
              class="read-more-btn"
            >
              {{ isDescriptionExpanded ? 'Read less' : 'Read more' }}
            </button>
          </div>
        </section>

        <!-- Property Features - 两列布局 -->
        <section class="features-section" v-if="allFeatures.length > 0">
          <h2 class="section-title">Property Features</h2>
          <div class="features-two-column">
            <div
              v-for="feature in displayedFeatures"
              :key="feature"
              class="feature-list-item"
            >
              {{ feature }}
            </div>
          </div>
          <button
            @click="showAllFeatures = !showAllFeatures"
            class="view-less-btn"
          >
            {{ showAllFeatures ? 'View less' : 'View all features' }}
          </button>
        </section>

        <!-- Inspection Times - 按Figma设计卡片式布局 -->
        <section v-if="inspectionTimes.length > 0" class="inspection-section">
          <h2 class="section-title">Inspection times</h2>
          <div class="inspection-list">
            <div
              v-for="(inspection, index) in inspectionTimes"
              :key="index"
              class="inspection-item"
            >
              <div class="inspection-date">
                <div class="date-day">{{ inspection.date }}</div>
                <div class="date-time">{{ inspection.time }}</div>
              </div>
              <button class="add-to-calendar-btn">
                <el-icon><Calendar /></el-icon>
              </button>
            </div>
          </div>
          <button class="add-to-planner-btn">
            <el-icon><Plus /></el-icon>
            Add all to planner
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
  ArrowLeft, Share, Picture,
  Location, Calendar,
  Loading, Plus
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import SimpleMap from '@/components/SimpleMap.vue'
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

/* 特征映射：以服务端数据为准，兼容多种JSON形态
   为什么：消除前端硬编码，确保与后端事实数据一致且可扩展（系统契约一致性） */
const BOOL_FEATURE_MAP = {
  has_air_conditioning: 'Air conditioning',
  is_furnished: 'Furnished',
  has_balcony: 'Balcony',
  has_dishwasher: 'Dishwasher',
  has_laundry: 'Internal Laundry',
  has_built_in_wardrobe: 'Built-in wardrobes',
  has_gym: 'Gym',
  has_pool: 'Pool',
  has_parking: 'Parking',
  allows_pets: 'Pets allowed',
  has_security_system: 'Security system',
  has_storage: 'Storage',
  has_study_room: 'Study',
  has_garden: 'Garden',
  has_intercom: 'Intercom',
  has_gas: 'Gas',
  has_heating: 'Heating',
  has_ensuite: 'Ensuite',
  is_north_facing: 'North facing',
  is_newly_built: 'Newly built',
  has_water_view: 'Water view',
}

const allFeatures = computed(() => {
  // 使用后端返回的数据替代硬编码，保证与数据源一致且可扩展
  const p = property.value
  const out = new Set()
  if (!p) return []

  // 1) 解析 property_features（可能是数组/对象/字符串）
  const pf = p.property_features
  if (Array.isArray(pf)) {
    pf.forEach(item => {
      const s = String(item || '').trim()
      if (s) out.add(s)
    })
  } else if (pf && typeof pf === 'object') {
    Object.entries(pf).forEach(([key, val]) => {
      if (typeof val === 'boolean') {
        if (val && BOOL_FEATURE_MAP[key]) out.add(BOOL_FEATURE_MAP[key])
      } else if (val != null && String(val).trim() !== '') {
        out.add(`${key.replace(/_/g, ' ')}: ${val}`)
      }
    })
  } else if (typeof pf === 'string') {
    pf.split(/[\n;,|]/).map(s => s.trim()).filter(Boolean).forEach(s => out.add(s))
  }

  // 2) 合并布尔特征列（仅取 true 的项）
  Object.entries(BOOL_FEATURE_MAP).forEach(([key, label]) => {
    if (p[key] === true) out.add(label)
  })

  // 返回去重后的特征数组
  return Array.from(out)
})

const displayedFeatures = computed(() => {
  if (showAllFeatures.value) {
    return allFeatures.value
  }
  // 移动端2列，所以是 2 * 3 = 6
  return allFeatures.value.slice(0, 6)
})

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


const inspectionTimes = computed(() => {
  if (!property.value || !property.value.inspection_times) return []

  const raw = property.value.inspection_times

  // 统一解析单个时间段字符串
  const parseEntry = (entry) => {
    if (typeof entry !== 'string') return entry
    const parts = entry.split(',')
    return {
      date: parts.slice(0, -1).join(',').trim(),
      time: parts[parts.length - 1]?.trim() || '',
    }
  }

  if (typeof raw === 'string') {
    return raw
      .split(/;|\n|\|/)
      .map((s) => s.trim())
      .filter(Boolean)
      .map(parseEntry)
  }

  if (Array.isArray(raw)) {
    return raw.map(parseEntry)
  }

  return []
})

const nextInspectionTime = computed(() => {
  if (inspectionTimes.value.length > 0) {
    const firstInspection = inspectionTimes.value[0];

    if (firstInspection.date.toLowerCase().includes('appointment')) {
      return 'By Appt.';
    }

    if (firstInspection.date.toLowerCase().includes('cancelled')) {
      return 'Cancelled';
    }

    // Try to get a short day name (e.g., "Sat")
    const dateParts = firstInspection.date.split(' ');
    const day = dateParts.find(p => /^(mon|tue|wed|thu|fri|sat|sun)/i.test(p)) || dateParts[0] || '';

    // Get the first part of the time string
    const timeParts = firstInspection.time.split(' ');
    let startTime = timeParts[0] || '';

    // Remove ":00" to shorten, e.g. "10am" from "10:00am"
    if (/\d{1,2}:\d{2}(am|pm)/.test(startTime)) {
       startTime = startTime.replace(':00', '');
    }

    if (day && startTime && startTime !== 'Details') {
      return `${day.slice(0, 3)} ${startTime}`; // e.g., "Sat 10am"
    }

    if (day) {
        return day.slice(0,3);
    }

    return 'Details'; // Fallback
  }
  return ''; // No inspections
});

const mapHeight = computed(() => {
  // Responsive map height - 使用固定值而不是动态计算
  return '250px'
})

// 生成静态地图 URL（使用环境变量中的 API 密钥）
const staticMapUrl = computed(() => {
  if (!property.value) return ''

  // 从环境变量获取 API 密钥（安全实践：不硬编码密钥）
  const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || ''

  if (!apiKey || apiKey === 'YOUR_NEW_API_KEY_HERE_REPLACE_ME') {
    console.warn('Google Maps API key not configured. Please set VITE_GOOGLE_MAPS_API_KEY in .env file')
    return ''
  }

  const { latitude, longitude } = property.value
  return `https://maps.googleapis.com/maps/api/staticmap?center=${latitude},${longitude}&zoom=15&size=600x250&markers=color:red%7C${latitude},${longitude}&key=${apiKey}`
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
    ElMessage.info('Inspection booking coming soon');
  } else {
    // 根据用户反馈更新
    ElMessage.info('可联系中介预约看房');
  }
};


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

const handleStaticMapError = () => {
  console.error('Static map failed to load')
  showStaticMap.value = false
}

const handleSeeTravelTimes = () => {
  // 测试模式：直接跳转，不需要登录
  const isTest = authStore.testMode

  if (isTest || authStore.isAuthenticated) {
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

// 获取可用日期显示
const getAvailableDate = () => {
  if (!property.value || !property.value.available_date) {
    return 'Monday, 1st September 2025'
  }
  const date = new Date(property.value.available_date)
  const options = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }
  return date.toLocaleDateString('en-US', options)
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
/* Domain.com.au 像素级还原样式 - 基于Figma精确设计 */
@import '@/assets/design-tokens.css';

.property-detail-page {
  min-height: 100vh;
  background-color: var(--color-bg-page);  /* 统一与全局页面背景 */
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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

/* 图片区域 - Figma 精确尺寸 */
.image-header {
  position: relative;
  width: 100%;
  margin: 0 auto;
  background: #000;
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
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-default);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
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

/* 桌面尺寸 - Figma 精确规格 */
@media (min-width: 1200px) {
  /* PC 端：限制版心到 1200 并左右各 32px 留白
     原因：与列表/详情统一的“页灰卡白 + 32px 内边距”规范对齐，避免贴边 */
  .image-header {
    max-width: 1200px;
    padding: 0 32px;
    margin: 0 auto;
    background: transparent;
  }

  .image-container {
    /* 改为 4:3 更沉浸，并设置上下界，避免“过扁/过高” */
    aspect-ratio: 4 / 3;
    min-height: 560px;
    max-height: 720px;
    width: 100%;
    max-width: 100%;
    height: auto;
    margin: 0;
    overflow: hidden; /* 防止内部溢出造成滚动条 */
    border-radius: 0; /* 去掉圆角：按产品要求保持直角视觉 */
    box-shadow: var(--shadow-xs, 0 1px 2px rgba(0,0,0,0.06));
  }

  .property-image {
    width: 100%;
    height: 100%;
    object-fit: cover;   /* 保证铺满并裁切 */
    object-position: center;
    border-radius: 0; /* 去掉子元素圆角兜底，避免继承 */
  }

  :deep(.el-image__inner) {
    /* 兜底：Element Plus 内部 <img>，确保在极端情况下仍然 cover */
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
    display: block;
    border-radius: 0; /* 去掉圆角兜底 */
  }
}

/* 超大屏幕 - 1920px设计稿 */
@media (min-width: 1920px) {
  /* 保持 1200 版心 + 32px 内边距，不扩大到 1920，避免出现“另一套主题” */
  .image-header {
    max-width: 1200px;
    padding: 0 32px;
    margin: 0 auto;
  }

  .image-container {
    width: 100%;
    max-width: 100%;
  }

  .content-container {
    max-width: 1200px;
    padding: 0 32px;
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


/* 内容容器 - PC端1683px宽度居中 */
.content-container {
  padding: 0 16px;
  margin: 0 auto;
  background: transparent;
  width: 100%;
  position: relative;
}

/* PC端主内容区域 - 完全改变布局 */
@media (min-width: 1200px) {
  .content-container {
    max-width: 1200px;
    padding: 60px 32px;
    margin: 0 auto;
    position: relative;
    z-index: 5;
  }
}

/* 信息卡片 - 白色背景带阴影 */
.info-card {
  background: white;
  padding: 24px 16px;
  margin: 0;
  min-height: 180px;
  box-shadow: none;
  border-radius: 0;
  border-bottom: 1px solid #e5e5e5;
}

/* PC端信息卡片 - 巨大变化 */
@media (min-width: 1200px) {
  .info-card {
    width: 100%;
    margin: 0;
    padding: 40px 48px;
    background: white;
    box-shadow: none;
    border-radius: 0;
    position: relative;
    z-index: 10;
  }
}

/* 可用日期和押金信息 */
.availability-info {
  margin-top: 8px;
  padding-top: 8px;
}

.availability-label {
  color: #4b5563;
  font-size: 13px;
  font-weight: 400;
}

.divider {
  color: #d0d3d9;
}

.bond-info {
  font-weight: 400;
}

/* 价格显示 - Figma精确样式 */
.price-wrapper {
  margin-bottom: 24px;
}

.price-text {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text-price);
  line-height: 1.2;
}

.price-text .price-unit {
  font-size: 14px;
  color: #666666;
  font-weight: 400;
}

/* PC端价格 - 超大字体 */
@media (min-width: 1200px) {
  .price-wrapper {
    margin-bottom: 32px;
    padding-bottom: 24px;
    border-bottom: 1px solid #e4e5e7;
  }

  .price-text {
    font-size: 48px;
    font-weight: 800;
    color: #000;
  }
}

/* 地址显示 */
.address-wrapper {
  margin-bottom: 20px;
}

.address-main {
  font-size: 15px;
  color: #333333;
  font-weight: 500;
  line-height: 1.3;
  margin-bottom: 4px;
}

.address-subtitle {
  font-size: 13px;
  color: #666666;
  font-weight: 500;
  line-height: 1.3;
}

/* PC端地址 */
@media (min-width: 1200px) {
  .address-main {
    font-size: 22px;
  }

  .address-subtitle {
    font-size: 18px;
  }
}

/* 房源特征 */
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

.feature-type {
  margin-left: 12px;
  padding-left: 20px;
  border-left: 1px solid #d0d3d9;
  font-size: 18px;
  font-weight: 600;
  color: #6e7881;
  font-family: 'Inter', sans-serif;
}

/* PC端特征 */
@media (min-width: 1200px) {
  .property-features {
    gap: 24px;
  }

  .feature-value {
    font-size: 20px;
  }

  .feature-type {
    font-size: 20px;
  }
}


/* See travel times button - 符合 Figma 设计稿 */
.see-travel-times-btn {
  width: 100%;
  padding: var(--space-3-5) var(--space-4);
  margin-top: var(--space-4);
  background: var(--bg-base);
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xs);
  display: flex;
  align-items: center;
  gap: var(--space-3-5);
  cursor: pointer;
  transition: all 0.2s ease;
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
  padding: 24px 16px;
  background: white;
  margin: 0;
  border-radius: 0;
  box-shadow: none;
  border-bottom: 1px solid #e5e5e5;
}

/* PC端位置部分 - 大改 */
@media (min-width: 1200px) {
  .location-section {
    width: 100%;
    margin: 0;
    padding: 40px 48px;
    background: white;
    border-radius: 0;
    box-shadow: none;
  }
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 20px 0;
  font-family: 'Inter', sans-serif;
}

/* PC端标题 */
@media (min-width: 1200px) {
  .section-title {
    font-size: 24px;
    margin: 0 0 24px 0;
  }
}

.map-wrapper {
  position: relative;
}

.map-container {
  position: relative;
  width: 100%;
  height: 250px;
  border-radius: 0;
  overflow: hidden;
  background: #e8e8e8;
  margin-bottom: 16px;
}

/* PC端地图容器 */
@media (min-width: 1200px) {
  .map-container {
    height: 360px; /* Figma地图高度 */
    border-radius: 0;
  }
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

/* Property Description 部分 */
.description-section {
  padding: 24px 16px;
  background: white;
  margin: 0;
  border-radius: 0;
  box-shadow: none;
  border-bottom: 1px solid #e5e5e5;
}

/* PC端描述部分 - 大改 */
@media (min-width: 1200px) {
  .description-section {
    width: 100%;
    margin: 0;
    padding: 40px 48px;
    background: white;
    border-radius: 0;
    box-shadow: none;
  }
}

.description-section .section-title {
  font-size: 23px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 24px 0;
  font-family: 'Inter', sans-serif;
}

.description-content {
  position: relative;
}

.description-text {
  font-size: 14px;
  line-height: 1.6;
  color: var(--color-text-secondary);
  max-height: 120px;
  overflow: hidden;
  transition: max-height 0.3s ease;
  position: relative;
}

.description-text p {
  margin: 0 0 16px 0;
}

.description-text p:last-child {
  margin-bottom: 0;
}

.description-headline {
  font-weight: 700 !important;
  color: var(--color-text-primary) !important;
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
  display: inline-block;
  margin-top: 16px;
  padding: 6px 14px;
  border: 1px solid var(--color-border-default);
  border-radius: 4px;
  background: white;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.read-more-btn:hover {
  background: #f5f6f7;
  border-color: var(--color-text-secondary);
}

/* Property Features 部分 - 两列布局 */
.features-section {
  padding: 24px 16px 33px 16px; /* 调整底部padding以满足33px间距要求 */
  background: white;
  margin: 0;
  border-radius: 0;
  box-shadow: none;
  border-bottom: 1px solid #e5e5e5;
}

/* PC端特性部分 - 大改 */
@media (min-width: 1200px) {
  .features-section {
    width: 100%;
    margin: 0;
    padding: 40px 48px 33px 48px; /* 同样调整底部padding */
    background: white;
    border-radius: 0;
    box-shadow: none;
  }
}

.features-section .section-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 20px 0;
}

.features-section .features-two-column {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr)); /* 移动端默认为2列 */
  gap: 12px 24px; /* 行间距12px(y-3), 列间距24px(x-6) */
  margin-bottom: 28px; /* 更新为28px间距 */
}

/* 桌面端(768px以上)切换为三列 */
@media (min-width: 768px) {
  .features-section .features-two-column {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

.feature-list-item {
  font-size: 15px;
  color: var(--color-text-secondary);
  line-height: 1.5;
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  word-break: break-word; /* 确保长单词可以换行 */
}

.view-less-btn {
  display: inline-block;
  padding: 0;
  font-size: 14px;
  font-weight: 600; /* 加粗以匹配设计 */
  color: var(--juwo-primary, #FF5824); /* 使用品牌主色 */
  background: none;
  border: none;
  cursor: pointer;
  text-decoration: none;
  margin-top: 0; /* 确保自身没有顶部边距 */
}

.view-less-btn:hover {
  text-decoration: underline;
}


/* Inspection Times 部分 - Figma设计 */
.inspection-section {
  padding: 24px 16px;
  background: white;
  margin: 0 0 80px 0;
  border-radius: 0;
  box-shadow: none;
}

.no-inspection-times {
  padding: 20px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  text-align: center;
  color: #6c757d;
  font-family: 'Inter', sans-serif;
  font-size: 15px;
}

/* PC端检查时间部分 - 大改 */
@media (min-width: 1200px) {
  .inspection-section {
    width: 100%;
    margin: 0 0 80px 0;
    padding: 40px 48px;
    background: white;
    border-radius: 0;
    box-shadow: none;
  }
}

.inspection-section .section-title {
  font-size: 23px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 24px 0;
  font-family: 'Inter', sans-serif;
}

.inspection-section .section-subtitle {
  font-size: 14px;
  color: #6e7881;
  margin: 0 0 20px 0;
}

.inspection-list {
  display: flex;
  flex-direction: column;
  gap: 0;
  margin-bottom: 20px;
}

/* PC端检查列表 - 网格布局 */
@media (min-width: 1200px) {
  .inspection-list {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }
}

.inspection-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: white;
  border: 1px solid var(--color-border-default);
  border-radius: 4px;
  margin-bottom: 8px;
}

/* PC端检查项 */
@media (min-width: 1200px) {
  .inspection-item {
    height: 72px;
    padding: 16px 20px;
    margin-bottom: 0;
  }
}

.inspection-item:last-child {
  border-bottom: none;
}

.inspection-date {
  flex: 1;
}

.date-day {
  font-size: 15px;
  font-weight: 700;
  color: var(--color-text-secondary);
  margin-bottom: 4px;
  font-family: 'Inter', sans-serif;
}

.date-time {
  font-size: 15px;
  color: var(--color-text-secondary);
  font-family: 'Inter', sans-serif;
  font-weight: 400;
}

.add-to-calendar-btn {
  width: 40px;
  height: 40px;
  border: 1px solid var(--color-border-default);
  border-radius: 4px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-to-calendar-btn:hover {
  background: #f5f6f7;
  border-color: #017188;
}

.add-to-planner-btn {
  width: 100%;
  max-width: 305px;
  height: 72px;
  padding: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: white;
  border: 1px solid var(--color-border-default);
  border-radius: 4px;
  font-size: 15px;
  font-weight: 700;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Inter', sans-serif;
}

/* PC端添加到计划按钮 */
@media (min-width: 1200px) {
  .add-to-planner-btn {
    margin: 20px auto 0;
  }
}

.add-to-planner-btn:hover {
  background: #f5f6f7;
  border-color: #017188;
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

/* PC端隐藏底部操作栏 */
@media (min-width: 1200px) {
  .action-footer {
    display: none;
  }
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

/* 将 1024 的高度限制为仅在 1024–1199 区间生效
   原因：避免覆盖 1200+ 的 16:9 比例设置（保持栅格与沉浸感一致） */
@media (min-width: 1024px) and (max-width: 1199px) {
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
