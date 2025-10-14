<template>
  <div class="property-detail-page">
    <!-- 优先显示已有数据，即使还在加载更多信息 -->
    <template v-if="property">
      <!-- 加载提示（在有数据时显示为小提示） -->
      <div v-if="loading" class="loading-indicator">
        <el-icon class="is-loading" :size="16"><Loading /></el-icon>
        <span>{{ $t('propertyDetail.loadingMore') }}</span>
      </div>
      <!-- 图片展示区域 - Domain风格 -->
      <header class="image-header">
        <!-- 图片容器 -->
        <div class="image-container" ref="imageContainerRef">
          <el-image
            v-if="images.length > 0"
            :src="images[currentImageIndex]"
            :alt="`房源图片 ${currentImageIndex + 1}`"
            class="property-image"
            @load="handleHeroImageLoad"
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
            <span>{{ $t('propertyDetail.noPhotos') }}</span>
          </div>

          <!-- 返回按钮 - 左上角 -->
          <button @click="goBack" class="back-btn focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">
            <el-icon :size="20"><ArrowLeft /></el-icon>
          </button>

          <!-- Share和Save按钮 - 右上角 -->
          <div class="image-actions">
            <button @click="shareProperty" class="image-action-btn focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">
              <el-icon :size="20"><Share /></el-icon>
              <span>{{ $t('propertyCard.share') }}</span>
            </button>
            <div class="action-divider"></div>
            <button @click="toggleFavorite" class="image-action-btn focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2" :class="{ 'fav-active': isFavorite }">
              <Star class="spec-icon" :size="20" aria-hidden="true" />
              <span>{{ $t('propertyCard.save') }}</span>
            </button>
          </div>

          <!-- 图片计数器 - 左下角 -->
          <div class="image-bottom-controls">
            <!-- 这里改为 Photos pill（图标 + 文案 + 数字徽标） -->
            <div class="inspect-btn-overlay image-counter" aria-label="照片数量">
              <Images class="pill-icon spec-icon" aria-hidden="true" />
              <span class="pill-label">{{ $t('propertyDetail.photos') }}</span>
              <span :class="['pill-badge', { 'two-digits': images.length >= 10 }]">{{
                images.length > 99 ? '99+' : images.length
              }}</span>
            </div>

            <!-- 指示点 -->
            <div v-if="images.length > 1" class="image-indicators">
              <span
                v-for="(img, index) in images"
                :key="index"
                :class="['indicator', { active: index === currentImageIndex }]"
                @click="currentImageIndex = index"
              ></span>
            </div>
          </div>
        </div>
      </header>

      <!-- 主体内容 - Domain风格卡片布局 -->
      <main class="content-container">
        <!-- 新增：单张白卡一体化容器 -->
        <div class="content-card">
          <!-- 白色信息卡片 -->
          <section class="info-card">
            <!-- 价格 -->
            <div class="price-wrapper">
              <span class="price-text typo-price">
                ${{ property.rent_pw }}
                <span class="price-unit typo-label">{{ $t('propertyCard.perWeek') }}</span>
              </span>
            </div>

            <!-- 地址 -->
            <div class="address-wrapper">
              <!-- PC端显示完整地址一行 -->
              <h1 class="address-main address-pc typo-address">{{ property.address }}</h1>
              <!-- 移动端显示地址和区号分行 -->
              <div class="address-mobile">
                <h1 class="address-main typo-address">
                  {{
                    property.address && property.address.includes(',')
                      ? property.address.split(',')[0]
                      : property.address
                  }}
                </h1>
                <p class="address-subtitle typo-body-sm">
                  {{ property.suburb }}, NSW {{ property.postcode || '' }}
                </p>
              </div>
            </div>

            <!-- 房源特征 -->
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

            <!-- 可用日期和押金 -->
            <div class="availability-info">
              <span class="availability-label typo-body"
                >{{ $t('propertyCard.availableDateLabel') }}：{{ getAvailableDate() }}</span
              >
            </div>
          </section>

          <!-- 位置地图 -->
          <section class="location-section">
            <h2 class="section-title typo-heading-card">{{ $t('propertyDetail.location') }}</h2>
            <div class="map-wrapper">
              <!-- 使用 GoogleMap 渲染位置，默认锁定中心，保持向后兼容 -->
              <div v-if="property.latitude && property.longitude" class="map-container">
                <GoogleMap
                  :latitude="+property.latitude"
                  :longitude="+property.longitude"
                  :zoom="15"
                  :height="mapHeight"
                  :marker-title="property.address"
                  :lock-center="true"
                />
              </div>
              <div v-else class="map-placeholder">
                <el-icon :size="32"><Location /></el-icon>
                <span>{{ $t('propertyDetail.locationUnavailable') }}</span>
              </div>

              <!-- See travel times button -->
              <button class="see-travel-times-btn" @click="handleSeeTravelTimes">
                <div class="travel-icon-wrapper">
                  <MapPin class="spec-icon" />
                </div>
                <div class="travel-btn-content">
                  <span class="travel-btn-title typo-button">{{
                    $t('propertyDetail.seeTravel')
                  }}</span>
                  <span class="travel-btn-subtitle">{{ $t('propertyDetail.seeTravelSub') }}</span>
                </div>
                <ChevronDown class="travel-chevron" :size="24" />
              </button>
            </div>
          </section>

          <!-- Property Description -->
          <section
            class="description-section"
            v-if="property.property_headline || property.description"
          >
            <h2 class="section-title typo-heading-card">{{ $t('propertyDetail.description') }}</h2>

            <div class="description-content">
              <div class="description-text" :class="{ expanded: isDescriptionExpanded }">
                <!-- 继续显示后端给的标题 -->
                <p v-if="property.property_headline" class="description-headline">
                  {{ property.property_headline }}
                </p>

                <!-- 将正文改为 Markdown 渲染（含换行、列表等），并进行 XSS 清理 -->
                <MarkdownContent
                  v-if="property.description"
                  :content="property.description"
                  :preserve-line-breaks="true"
                />
              </div>
              <button @click="toggleDescription" class="read-more-btn">
                {{ isDescriptionExpanded ? $t('common.readLess') : $t('common.readMore') }}
              </button>
            </div>
          </section>

          <!-- Property Features - 两列布局 -->
          <section class="features-section" v-if="allFeatures.length > 0">
            <h2 class="section-title typo-heading-card">{{ $t('propertyDetail.features') }}</h2>
            <div class="features-two-column">
              <div
                v-for="feature in displayedFeatures"
                :key="feature"
                class="feature-list-item typo-body"
              >
                {{ feature }}
              </div>
            </div>
            <button
              v-if="allFeatures.length > visibleFeaturesCount"
              @click="showAllFeatures = !showAllFeatures"
              class="view-less-btn typo-button"
            >
              {{
                showAllFeatures
                  ? $t('propertyDetail.viewLessFeatures')
                  : $t('propertyDetail.viewAllFeatures')
              }}
            </button>
          </section>

          <!-- Inspection Times - 按Figma设计卡片式布局 -->
          <section class="inspection-section">
            <h2 class="section-title typo-heading-card">
              {{ $t('propertyDetail.inspectionTimes') }}
            </h2>
            <div v-if="inspectionTimes.length > 0" class="inspection-list">
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
            <div v-else class="no-inspection-times">
              {{ $t('propertyDetail.noInspection') }}
            </div>
          </section>

          <!-- 通勤计算器 - 已移至独立页面 -->
        </div>
      </main>

      <!-- 底部固定操作栏 -->
      <footer class="action-footer">
        <el-button class="action-btn enquire-btn typo-button" @click="handleEmail">{{
          $t('propertyDetail.enquire')
        }}</el-button>
        <el-button class="action-btn inspect-btn typo-button" @click="handleInspections">{{
          $t('propertyDetail.inspect')
        }}</el-button>
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
    <AuthModal v-if="showAuthModal" v-model="showAuthModal" @success="handleAuthSuccess" />
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, computed, ref, inject } from 'vue'
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'
import { useAuthStore } from '@/stores/auth'
import { ArrowLeft, Share, Picture, Location, Calendar, Loading } from '@element-plus/icons-vue'
import { BedDouble, Bath, CarFront, ChevronDown, MapPin, Images, Star } from 'lucide-vue-next'
import { ElMessage } from 'element-plus'
import GoogleMap from '@/components/GoogleMap.vue'
import AuthModal from '@/components/modals/AuthModal.vue'
import MarkdownContent from '@/components/MarkdownContent.vue'

const route = useRoute()
const router = useRouter()
const propertiesStore = usePropertiesStore()
const authStore = useAuthStore()
const t = inject('t') || ((k) => k)

const propertyId = route.params.id

// 响应式状态
const currentImageIndex = ref(0)
const isDescriptionExpanded = ref(false)
const showAllFeatures = ref(false)
const showAuthModal = ref(false)
/* 中文注释：为顶部图片容器提供引用，用于根据原图分辨率动态限制高度，避免放大导致模糊 */
const imageContainerRef = ref(null)
let viewerCleanup = null

/* 中文注释：根据图片原始分辨率与容器宽度，计算清晰显示的最大高度，设置到 CSS 变量，避免 1:1 以上的放大 */
const handleHeroImageLoad = (event) => {
  const imgEl = event?.target
  if (!imgEl || !imageContainerRef.value) return
  const naturalW = imgEl.naturalWidth || 0
  const naturalH = imgEl.naturalHeight || 0
  if (!naturalW || !naturalH) return
  const cw = imageContainerRef.value.clientWidth || 0
  if (!cw) return

  // 中文注释：加入 DPR（屏幕倍率）校正，避免高清屏上因 2x/3x 超采样导致的模糊
  const dpr = window.devicePixelRatio || 1
  const requiredPhysicalW = cw * dpr

  // 若原图像素不足以覆盖“容器宽 × DPR”，则按“原图宽 / DPR”的安全展示宽度回退
  const safeDisplayW = naturalW >= requiredPhysicalW ? cw : naturalW / dpr

  // 按原始宽高比推导清晰高度，再做上下界限制，保证“更挺拔”同时不失真
  const computed = Math.floor((naturalH / naturalW) * safeDisplayW)
  const minH = 560
  const maxH = 820
  const clamped = Math.max(minH, Math.min(maxH, computed))
  imageContainerRef.value.style.setProperty('--hero-height', `${clamped}px`)
}

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
    pf.forEach((item) => {
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
    pf.split(/[\n;,|]/)
      .map((s) => s.trim())
      .filter(Boolean)
      .forEach((s) => out.add(s))
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
  // 中文注释：默认折叠展示 2 行；移动端 2 列=4 项，≥768px 3 列=6 项
  return allFeatures.value.slice(0, visibleFeaturesCount.value)
})

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

const inspectionTimes = computed(() => {
  if (!property.value || !property.value.inspection_times) return []

  const raw = property.value.inspection_times

  // 中文注释：过滤无效值，确保不显示 null 或空白内容
  // 统一解析单个时间段字符串
  const parseEntry = (entry) => {
    if (typeof entry !== 'string' || !entry.trim()) return null
    const parts = entry.split(',')
    const date = parts.slice(0, -1).join(',').trim()
    const time = parts[parts.length - 1]?.trim() || ''

    // 中文注释：过滤掉无效的日期时间条目
    if (!date || !time) return null

    return {
      date,
      time,
    }
  }

  let parsed = []

  if (typeof raw === 'string') {
    parsed = raw
      .split(/;|\n|\|/)
      .map((s) => s.trim())
      .filter(Boolean)
      .map(parseEntry)
      .filter(Boolean) // 中文注释：移除解析失败的条目
  } else if (Array.isArray(raw)) {
    parsed = raw.map(parseEntry).filter(Boolean) // 中文注释：移除解析失败的条目
  }

  return parsed
})

/* 中文注释：根据断点动态决定地图高度，统一交由 GoogleMap 组件控制，避免外层容器与内部高度不一致导致灰条 */
const isDesktop = ref(false)
let mq
let mqHandler
onMounted(() => {
  mq = window.matchMedia('(min-width: 1200px)')
  mqHandler = () => {
    isDesktop.value = mq.matches
  }
  mqHandler()
  if (mq.addEventListener) mq.addEventListener('change', mqHandler)
  else if (mq.addListener) mq.addListener(mqHandler)
})
onUnmounted(() => {
  if (mq && mqHandler) {
    if (mq.removeEventListener) mq.removeEventListener('change', mqHandler)
    else if (mq.removeListener) mq.removeListener(mqHandler)
  }
})
const mapHeight = computed(() => (isDesktop.value ? '360px' : '240px'))

/* 中文注释：特征网格列数（与 CSS 断点一致）：<768px 为 2 列，≥768px 为 3 列。
   为什么：保证“默认折叠两行”的展示在不同断点下分别为 4 项和 6 项 */
const isThreeCols = ref(false)
let mqCols
let mqColsHandler
onMounted(() => {
  mqCols = window.matchMedia('(min-width: 768px)')
  mqColsHandler = () => {
    isThreeCols.value = mqCols.matches
  }
  mqColsHandler()
  if (mqCols.addEventListener) mqCols.addEventListener('change', mqColsHandler)
  else if (mqCols.addListener) mqCols.addListener(mqColsHandler)
})
onUnmounted(() => {
  if (mqCols && mqColsHandler) {
    if (mqCols.removeEventListener) mqCols.removeEventListener('change', mqColsHandler)
    else if (mqCols.removeListener) mqCols.removeListener(mqColsHandler)
  }
})
/* 中文注释：默认折叠展示 2 行 → 2*2=4（移动端），3*2=6（≥768px） */
const visibleFeaturesCount = computed(() => (isThreeCols.value ? 6 : 4))

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
    propertiesStore.addFavorite(property.value)
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
      .catch(() => {
        // 用户取消分享或分享失败
      })
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
    ElMessage.info(t('propertyDetail.inspectSoon'))
  } else {
    // 根据用户反馈更新
    ElMessage.info('可联系中介预约看房')
  }
}

const handleImageError = (event) => {
  console.warn('Image load failed:', event.target.src)
  event.target.src = '/api/placeholder/400/300'
}

const handleImageClick = () => {
  // 进入预览层后：1) 黑底保持 2) 右上角计数器 3) 强化等待，避免 teleported DOM 未就绪
  const MAX_TRIES = 40
  const INTERVAL = 50
  let tries = 0

  const apply = () => {
    tries++

    // 1) 保持黑色背景
    const mask = document.querySelector('.el-image-viewer__mask')
    if (mask) {
      mask.style.backgroundColor = 'var(--overlay-bg)'
      mask.style.opacity = '0.95'
    }

    // 2) 注入/更新计数器
    const wrapper = document.querySelector('.el-image-viewer__wrapper')
    if (!wrapper) {
      if (tries < MAX_TRIES) setTimeout(apply, INTERVAL)
      return
    }

    let counter = document.querySelector('.custom-image-counter')
    if (!counter) {
      counter = document.createElement('div')
      counter.className = 'custom-image-counter'
      document.body.appendChild(counter)
    }

    const updateCounter = () => {
      const img = wrapper.querySelector('.el-image-viewer__img')
      const list = Array.isArray(images.value) ? images.value : []
      if (!img || !img.src || list.length === 0) {
        counter.textContent = ''
        return
      }
      // 同时尝试 endsWith/包含匹配，适配不同 URL 形式
      const idx = list.findIndex((u) => u && (img.src.endsWith(u) || img.src.includes(u)))
      const current = idx >= 0 ? idx + 1 : currentImageIndex.value + 1
      counter.textContent = `${current} / ${list.length}`
    }

    // 初次设置
    updateCounter()

    // 使用轻量观察：仅跟踪当前展示图片的 src 变化；若 img 被替换则重绑
    let rafId = 0
    const scheduleUpdate = () => {
      if (rafId) cancelAnimationFrame(rafId)
      rafId = requestAnimationFrame(updateCounter)
    }

    let imgObserver
    const rebindImgObserver = () => {
      if (imgObserver) imgObserver.disconnect()
      const imgEl = wrapper.querySelector('.el-image-viewer__img')
      if (imgEl) {
        imgObserver = new MutationObserver(() => scheduleUpdate())
        imgObserver.observe(imgEl, { attributes: true, attributeFilter: ['src'] })
      }
      scheduleUpdate()
    }
    rebindImgObserver()

    // 仅监听子节点变更，以便在视图内部替换 img 时重绑，不观察 attributes 以避免高频回调
    const wrapperObserver = new MutationObserver(() => rebindImgObserver())
    wrapperObserver.observe(wrapper, { childList: true, subtree: true })

    // 交互兜底：左右箭头点击后刷新计数（若实现不更换 img[src]）
    const prevBtn = document.querySelector('.el-image-viewer__prev')
    const nextBtn = document.querySelector('.el-image-viewer__next')
    if (prevBtn) prevBtn.addEventListener('click', scheduleUpdate, { passive: true })
    if (nextBtn) nextBtn.addEventListener('click', scheduleUpdate, { passive: true })

    // 关闭时清理（并暴露路由离开兜底清理）
    const closeBtn = document.querySelector('.el-image-viewer__close')
    viewerCleanup = () => {
      if (imgObserver) imgObserver.disconnect()
      if (wrapperObserver) wrapperObserver.disconnect()
      if (rafId) cancelAnimationFrame(rafId)
      const c = document.querySelector('.custom-image-counter')
      if (c && c.parentNode) c.parentNode.removeChild(c)
      if (prevBtn) prevBtn.removeEventListener('click', scheduleUpdate)
      if (nextBtn) nextBtn.removeEventListener('click', scheduleUpdate)
      viewerCleanup = null
    }
    if (closeBtn) {
      closeBtn.addEventListener('click', () => viewerCleanup && viewerCleanup(), { once: true })
    }
  }

  setTimeout(apply, INTERVAL)
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
        lng: property.value.longitude,
      },
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

/* 中文注释：统一“空出日期”前端表现与列表一致
   规则：
   - 无日期（缺失/空串） → 显示“立即入住”
   - 日期 ≤ 今天        → 显示“立即入住”
   - 无效日期字符串     → 显示“待定”
   - 其余（未来日期）    → 按中文完整日期显示
   兼容：若后端详情使用驼峰 availableDate，则做一次回退读取 */
const getAvailableDate = () => {
  const p = property.value
  if (!p) return t('propertyDetail.dateTBD')

  // 兼容别名 availableDate，并清理空白
  const raw = (p.available_date ?? p.availableDate ?? '').toString().trim()

  // 与列表卡片规则对齐：无日期 → 立即入住
  if (!raw) {
    return '立即入住'
  }

  const d = new Date(raw)
  // 无效日期字符串 → 待定（避免显示 Invalid Date）
  if (isNaN(d.getTime())) {
    return t('propertyDetail.dateTBD')
  }

  // 与列表一致：日期 ≤ 今天 → 立即入住
  const today = new Date()
  if (d <= today) {
    return '立即入住'
  }

  // 未来日期 → 中文完整日期
  const options = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }
  return d.toLocaleDateString('zh-CN', options)
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
  // 若由列表/演示页预先注入 currentProperty 且与路由 ID 匹配，则跳过接口请求，避免 404
  const prefetched =
    propertiesStore.currentProperty &&
    String(propertiesStore.currentProperty.listing_id) === String(propertyId)

  if (!prefetched) {
    // 正常加载数据
    await propertiesStore.fetchPropertyDetail(propertyId)
  }

  // 预加载下一张图片 / 写入历史
  if (property.value) {
    preloadNextImage()
    propertiesStore.addHistory(property.value)
  } else {
    propertiesStore.logHistory(propertyId)
  }
})

onBeforeRouteLeave(() => {
  if (viewerCleanup) viewerCleanup()
})
</script>

<style scoped>
/* Domain.com.au 像素级还原样式 - 基于Figma精确设计 */
.property-detail-page {
  min-height: 100vh;
  background: hsl(var(--background)); /* 页面背景统一走核心变量 */

  /* 新增：统一字体栈（含中文优先级） */
  --font-ui: inter, 'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', sans-serif;

  font-family: var(--font-sans);
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
  background: hsl(var(--background));
  padding: 8px 16px;
  border-radius: 20px;
  box-shadow: var(--shadow-sm);
  display: flex;
  align-items: center;
  gap: 8px;
  z-index: 20;
  font-size: 14px;
  color: var(--color-text-secondary);
}

.skeleton-image {
  height: 280px;
  background: var(--surface-4);
  margin-bottom: 0;
}

.skeleton-content {
  padding: 20px 16px;
  background: var(--color-bg-card);
}

/* 图片区域 - Figma 精确尺寸 */
.image-header {
  position: relative;
  width: 100%;
  margin: 0 auto;
  background: var(--surface-4);
}

/* 返回按钮 - 左上角圆形 */
.back-btn {
  position: absolute;
  top: 16px;
  left: 16px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-bg-card);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--color-text-secondary);
  box-shadow: var(--shadow-xs);
  z-index: 10;
}

.back-btn:hover {
  background: var(--color-bg-card);
  transform: scale(1.05);
  box-shadow: var(--shadow-sm);
}

/* Share和Save按钮组 - 右上角 */
.image-actions {
  position: absolute;
  top: 16px;
  right: 16px;
  display: flex;
  background: var(--color-bg-card);
  border: 1px solid hsl(var(--border));
  border-radius: 4px;
  overflow: hidden;
  z-index: 10;
}

.image-action-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: background 0.2s ease;
  color: var(--color-text-secondary);
  font-family: var(--font-ui); /* 统一：替换系统字体为变量 */
  font-size: 14px;
  font-weight: 400;
}

.image-action-btn:hover {
  background: hsl(var(--background));
}

.image-action-btn span {
  font-size: 14px;
  color: var(--color-text-secondary);
}

/* 收藏高亮：使用品牌色，图标随 currentColor 继承 */
.image-action-btn.fav-active {
  color: var(--brand-primary);
}

.action-divider {
  width: 1px;
  height: 42px;
  background: var(--color-border-default);
}

/* 底部控制按钮 - 左下角 */
.image-bottom-controls {
  position: absolute;
  bottom: 16px;
  left: 16px;
  z-index: 50; /* 修复点 3：提升层级，避免被图片/预览层/其他覆盖物压住 */
}

.inspect-btn-overlay {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: hsl(var(--background));
  border: 1px solid hsl(var(--border));
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
  box-shadow: var(--shadow-xs);
}

.inspect-btn-overlay:hover {
  background: var(--bg-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

/* 将覆盖按钮样式变为计数器时的非交互徽标状态 */
.inspect-btn-overlay.image-counter {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-width: 118px;
  height: 40px;
  padding: 0 14px;
  background: hsl(var(--background));
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-default);
  border-radius: 4px;
  cursor: default;
  font-family: var(--font-ui);
  font-weight: 400;
  font-size: 14px;
  line-height: 1;
  box-shadow: none;
  box-sizing: border-box;
}

/* 禁止 hover 视觉（若基类有 hover 效果） */
.inspect-btn-overlay.image-counter:hover {
  transform: none;
  filter: none;
  box-shadow: none;
  background: var(--color-bg-card);
}

/* 图标尺寸与对齐 */
.inspect-btn-overlay.image-counter .pill-icon {
  width: 16px;
  height: 16px;
  display: block;
}

/* 文案 */
.inspect-btn-overlay.image-counter .pill-label {
  white-space: nowrap;
  padding-right: 0;
  line-height: 1;
}

/* 数字徽标（圆胶囊） */
.inspect-btn-overlay.image-counter .pill-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  margin-left: 0;
  padding: 0;
  border-radius: 100%;
  background: var(--surface-2);
  color: var(--color-text-secondary);
  font-weight: 600;
  font-size: 12px;
  line-height: 1;
  font-variant-numeric: tabular-nums;
  flex-shrink: 0;
}

/* 两位及以上（含 99+）→ 自动胶囊 */
.inspect-btn-overlay.image-counter .pill-badge.two-digits {
  width: auto;
  padding: 0 4px;
  border-radius: 11px;
}

.image-container {
  position: relative;
  width: 100%;
  height: 280px; /* 移动端高度 */
  background: var(--surface-4);
  overflow: hidden;
}

.property-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  cursor: pointer;
}

/* 平板尺寸 */
@media (width >= 768px) {
  .image-container {
    height: 400px;
  }
}

/* 桌面尺寸 - Figma 精确规格 */
@media (width >= 1200px) {
  /* Hero 全宽 + 自适应左右留白
     为什么：还原截图“更大气”的观感，同时用 clamp 保证在窄屏/超宽屏下都有合理留白与稳定表现 */
  .image-header {
    width: 100%;
    max-width: none; /* 放开版心限制，做 full-bleed 英雄区 */
    padding-inline: clamp(
      16px,
      6vw,
      115px
    ); /* 自适应左右留白：窄屏收敛到 ~16-32px，≥1440 接近 115px */

    margin: 0 auto;
    background: transparent;
  }

  .image-container {
    /* 固定纵横比，避免图片在不同分辨率下“变形”；同时设上下界避免过扁/过高 */
    aspect-ratio: 3 / 2; /* 1.5：比 16:9 更“挺拔”，比 4:3 略矮，贴近“更大气”的观感 */
    width: 100%;
    height: var(
      --hero-height,
      auto
    ); /* 加入分辨率守卫：加载后以 --hero-height 为准，避免放大导致模糊 */

    min-height: 560px;
    max-height: 820px;
    margin: 0;
    overflow: hidden; /* 防止内部溢出造成滚动条 */
    border-radius: 0; /* 去掉圆角：按产品要求保持直角视觉 */
    box-shadow: var(--shadow-xs);
  }

  .property-image {
    width: 100%;
    height: 100%;
    object-fit: cover; /* 保证铺满并裁切 */
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
@media (width >= 1920px) {
  /* 继续使用 Hero 全宽 + clamp 左右留白，避免出现“另一套主题”的观感 */
  .image-header {
    width: 100%;
    max-width: none;
    padding-inline: clamp(16px, 6vw, 115px);
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
  color: var(--text-muted);
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
  background: var(--surface-2);
  cursor: pointer;
  transition: all 0.2s ease;
}

.indicator.active {
  width: 24px;
  border-radius: 3px;
  background: var(--color-bg-card);
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
@media (width >= 1200px) {
  .content-container {
    max-width: none !important;
    width: 100% !important;
    padding-top: 32px;
    padding-bottom: 32px;
    padding-left: 0 !important;
    padding-right: 0 !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
    position: relative;
    z-index: 5;
  }
}

/* 信息卡片 - 白色背景带阴影 */
.info-card {
  background: var(--color-bg-card);
  padding: 24px 16px;
  margin: 0;
  min-height: 180px;
  box-shadow: none;
  border-radius: 0;
  border-bottom: 1px solid hsl(var(--border));
}

/* PC端信息卡片 - 巨大变化 */
@media (width >= 1200px) {
  .info-card {
    width: 100%;
    margin: 0;
    padding: 32px; /* 统一左右 32，与容器对齐 */
    background: hsl(var(--background));
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
  color: var(--color-text-secondary);
  font-size: 16px;
  font-weight: 400;
}

.divider {
  color: var(--color-border-default);
}

.bond-info {
  font-weight: 400;
}

/* 价格显示 - Figma精确样式 */
.price-wrapper {
  margin-bottom: 24px;
}

.price-text {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: 1.2;
}

.price-text .price-unit {
  font-size: 14px;
  color: var(--color-text-secondary);
  font-weight: 400;
}

/* PC端价格 - 超大字体 */
@media (width >= 1200px) {
  .price-wrapper {
    margin-bottom: 32px;
    padding-bottom: 24px;
    border-bottom: 1px solid var(--color-border-default);
  }

  .price-text {
    font-size: 25px;
    font-weight: 700;
    color: var(--color-text-primary);
  }
}

/* 地址显示 */
.address-wrapper {
  margin-bottom: 16px; /* 副标题到图标行 16 的节奏 */
}

.address-main {
  font-size: 16px;
  color: var(--color-text-primary);
  font-weight: 500;
  line-height: 1.3;
  margin-bottom: 4px;
}

.address-subtitle {
  font-size: 13px;
  color: var(--color-text-secondary);
  font-weight: 500;
  line-height: 1.3;
}

/* 移动端和PC端的响应式显示 */
.address-pc {
  display: none; /* 默认在移动端隐藏 */
}

.address-mobile {
  display: block; /* 默认在移动端显示 */
}

/* PC端地址 */
@media (width >= 1200px) {
  .address-main {
    font-size: 16px;
  }

  .address-subtitle {
    font-size: 18px;
  }

  /* PC端显示完整地址一行，隐藏移动端分行显示 */
  .address-pc {
    display: block;
  }

  .address-mobile {
    display: none;
  }
}

/* 房源特征 */
.property-features {
  display: flex;
  align-items: center;
  /* 中文注释：详情页复用全局规格变量，保持与列表卡片一致（前端表现更紧凑、对齐） */
  --spec-icon-size: 18px;     /* 图标尺寸 */
  --spec-text-size: 14px;     /* 数字字号 */
  --spec-line-height: 18px;   /* 数字与图标基线贴合 */
  --spec-item-gap: 12px;      /* 三项之间的水平间距 */
  --spec-icon-gap: 6px;       /* 图标与数字之间的间距 */
  gap: 0; /* 间距交由 .spec-row 的 margin-left 控制，避免与 gap 叠加 */
  margin-bottom: 12px; /* 与列表卡片一致：12px */
  color: var(--color-text-secondary);
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0; /* 由全局 .spec-row/.spec-item 变量控制细节间距 */
}

/* 移除本地对图标尺寸的硬编码，交由全局 spec 变量控制 */

/* 本地仅保留颜色与字重，字号交由全局 spec 变量控制 */
.feature-item span {
  color: var(--color-text-primary);
  font-weight: 600;
}

.feature-type {
  margin-left: 12px;
  padding-left: 20px;
  border-left: 1px solid var(--color-border-default);
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-secondary);
  font-family: var(--font-ui); /* 统一 */
}

/* PC端特征 */
@media (width >= 1200px) {
  .price-wrapper {
    margin-bottom: 32px; /* 价格到地址 32 */
    padding-bottom: 24px; /* 保持内边距 */
    border-bottom: 1px solid var(--color-border-default); /* 保持分隔线 */
  }

  .price-text {
    font-size: 25px;
    font-weight: 700;
    color: var(--color-text-primary);
  }
}

/* See travel times button - 符合 Figma 设计稿 */
.see-travel-times-btn {
  width: 100%;
  padding: var(--space-3-5) var(--space-4);
  margin-top: var(--space-4);
  background: hsl(var(--background));
  border: 1px solid hsl(var(--border));
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
  background: hsl(var(--background));
  margin: 0;
  border-radius: 0;
  box-shadow: none;
  border-bottom: 1px solid var(--color-border-default);
}

/* PC端位置部分 - 大改 */
@media (width >= 1200px) {
  .location-section {
    width: 100%;
    margin: 0;
    padding: 40px 48px;
    background: var(--color-bg-card);
    border-radius: 0;
    box-shadow: none;
  }
}

.section-title {
  font-size: 23px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 20px;
  font-family: var(--font-ui); /* 统一 */
}

/* PC端标题 */
@media (width >= 1200px) {
  .section-title,
  .description-section .section-title {
    font-size: 25px;
    margin: 0 0 24px;
  }
}

.map-wrapper {
  position: relative;
}

.map-container {
  position: relative;
  width: 100%;
  height: auto;
  border-radius: 0;
  overflow: hidden;
  background: var(--surface-4);
  margin-bottom: 16px;
}

/* PC端地图容器 */
@media (width >= 1200px) {
  .map-container {
    height: auto; /* 高度由 GoogleMap 组件控制 */
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
  background: var(--surface-2);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  gap: var(--space-3);
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
  background: var(--color-bg-card);
  margin: 0;
  border-radius: 0;
  box-shadow: none;
  border-bottom: 1px solid var(--color-border-default);
}

/* PC端描述部分 - 大改 */
@media (width >= 1200px) {
  .description-section {
    width: 100%;
    margin: 0;
    padding: 40px 48px;
    background: var(--color-bg-card);
    border-radius: 0;
    box-shadow: none;
  }
}

.description-section .section-title {
  font-size: 23px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 24px;
  font-family: var(--font-ui); /* 统一 */
}

.description-content {
  position: relative;
}

.description-text {
  font-size: 16px;
  line-height: 1.5;
  color: var(--color-text-secondary);
  max-height: 120px;
  overflow: hidden;
  transition: max-height 0.3s ease;
  position: relative;
}

.description-text p {
  margin: 0 0 16px;
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
  background: linear-gradient(to bottom, transparent, var(--color-bg-card));
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
  background: var(--color-bg-card);
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.read-more-btn:hover {
  background: var(--bg-hover);
  border-color: var(--color-text-secondary);
}

/* Property Features 部分 - 两列布局 */
.features-section {
  padding: 24px 16px 33px; /* 调整底部padding以满足33px间距要求 */
  background: var(--color-bg-card);
  margin: 0;
  border-radius: 0;
  box-shadow: none;
  border-bottom: 1px solid var(--color-border-default);
}

/* PC端特性部分 - 大改 */
@media (width >= 1200px) {
  .features-section {
    width: 100%;
    margin: 0;
    padding: 40px 48px 33px; /* 同样调整底部padding */
    background: var(--color-bg-card);
    border-radius: 0;
    box-shadow: none;
  }
}

.features-section .section-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 20px;
}

.features-section .features-two-column {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr)); /* 移动端默认为2列 */
  gap: 12px 24px; /* 行间距12px(y-3), 列间距24px(x-6) */
  margin-bottom: 28px; /* 更新为28px间距 */
}

/* 桌面端(768px以上)切换为三列 */
@media (width >= 768px) {
  .features-section .features-two-column {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

.feature-list-item {
  font-size: 15px;
  color: var(--color-text-secondary);
  line-height: 1.5;
  font-family: var(--font-ui);
  font-weight: 400;
  word-break: break-word; /* 确保长单词可以换行 */
}

.view-less-btn {
  display: inline-block;
  padding: 0;
  font-size: 14px;
  font-weight: 600; /* 加粗以匹配设计 */
  color: var(--accent-primary); /* 试点：文本型 CTA 使用系统强调色 */
  background: none;
  border: none;
  cursor: pointer;
  text-decoration: none;
  margin-top: 0; /* 确保自身没有顶部边距 */
}

.view-less-btn:hover {
  color: var(--accent-hover);
  text-decoration: underline;
}

/* Inspection Times 部分 - Figma设计 */
.inspection-section {
  padding: 24px 16px;
  background: var(--color-bg-card);
  margin: 0 0 80px;
  border-radius: 0;
  box-shadow: none;
}

.no-inspection-times {
  padding: 20px;
  background: var(--bg-base);
  border: 1px solid var(--color-border-default);
  border-radius: 4px;
  text-align: center;
  color: var(--color-text-secondary);
  font-family: var(--font-ui);
  font-size: 15px;
}

/* PC端检查时间部分 - 大改 */
@media (width >= 1200px) {
  .inspection-section {
    width: 100%;
    margin: 0 0 80px;
    padding: 40px 48px;
    background: var(--color-bg-card);
    border-radius: 0;
    box-shadow: none;
  }
}

.inspection-section .section-title {
  font-size: 23px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 24px;
  font-family: var(--font-ui);
}

.inspection-section .section-subtitle {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0 0 20px;
}

.inspection-list {
  display: flex;
  flex-direction: column;
  gap: 0;
  margin-bottom: 20px;
}

/* PC端检查列表 - 网格布局 */
@media (width >= 1200px) {
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
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-default);
  border-radius: 4px;
  margin-bottom: 8px;
}

/* PC端检查项 */
@media (width >= 1200px) {
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
  font-family: var(--font-ui);
}

.date-time {
  font-size: 15px;
  color: var(--color-text-secondary);
  font-family: var(--font-ui);
  font-weight: 400;
}

.add-to-calendar-btn {
  width: 40px;
  height: 40px;
  border: 1px solid var(--color-border-default);
  border-radius: 4px;
  background: var(--color-bg-card);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-to-calendar-btn:hover {
  background: var(--bg-hover);
  border-color: var(--color-border-strong);
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
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-default);
  border-radius: 4px;
  font-size: 15px;
  font-weight: 700;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: var(--font-ui);
}

/* PC端添加到计划按钮 */
@media (width >= 1200px) {
  .add-to-planner-btn {
    margin: 20px auto 0;
  }
}

.add-to-planner-btn:hover {
  background: var(--bg-hover);
  border-color: var(--color-border-strong);
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
  background: var(--color-bg-card);
  border-top: 1px solid hsl(var(--border));
  display: flex;
  gap: 12px;
  z-index: 100;
  box-shadow: var(--shadow-xs);
}

/* PC端隐藏底部操作栏 */
@media (width >= 1200px) {
  .action-footer {
    display: none;
  }
}

.action-btn {
  flex: 1;
  height: 48px;
  border-radius: 24px;
  font-size: var(--text-base);
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.enquire-btn {
  /* 试点：主 CTA 改用系统强调色 */
  background: hsl(var(--primary));
  color: var(--accent-contrast-on);
}

.enquire-btn:hover {
  /* 悬浮使用强调色 hover 阶梯 */
  background: var(--accent-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.inspect-btn {
  background: hsl(var(--primary)); /* 统一 CTA 使用品牌主色 */
  color: var(--color-text-inverse);
}

.inspect-btn:hover {
  background: var(--juwo-primary);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

/* Responsive Design - Domain响应式 */
@media (width >= 768px) {
  .image-container {
    height: 400px;
  }

  .content-container {
    padding: 0 var(--space-4);
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
@media (width >= 1024px) and (width <= 1199px) {
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
  background-color: var(--overlay-bg) !important;
  opacity: 0.95 !important;
}

/* 预览层控制：去圆底，仅图标，位置按移动端设计靠边 */
:deep(.el-image-viewer__btn) {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

/* 关闭按钮：顶左角，仅 X，无圆底；保留命中区 */
:deep(.el-image-viewer__close) {
  top: 12px !important;
  left: 12px !important;
  right: auto !important;
  width: 44px !important;
  height: 44px !important;
  background: transparent !important;
}

/* 左右箭头：外移到更靠边位置，垂直居中 */
:deep(.el-image-viewer__prev),
:deep(.el-image-viewer__next) {
  top: 50% !important;
  transform: translateY(-50%) !important;
  background: transparent !important;
}

:deep(.el-image-viewer__prev) {
  left: 12px !important;
}

:deep(.el-image-viewer__next) {
  right: 12px !important;
}

/* 顶部右侧计数器：白字、轻阴影，稳定不抖动 */
:deep(.custom-image-counter) {
  position: fixed;
  top: 12px;
  right: 12px;
  z-index: 100000; /* 高于 viewer 内部按钮 */
  color: var(--color-text-inverse);
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.2px;
}

/* 单张白卡一体化容器：由父容器统一承载白底与分隔线 */
.content-card {
  background: var(--color-bg-card);
  border: 1px solid hsl(var(--border));
  border-radius: 0; /* 移动端无圆角 */
  overflow: hidden; /* 防止子元素溢出破坏边界 */
  box-shadow: none;
}

/* 在白卡内部，子 section 透明化并移除自身边线与阴影，由父容器统一管理分隔线 */
.content-card .info-card,
.content-card .location-section,
.content-card .description-section,
.content-card .features-section,
.content-card .inspection-section {
  background: transparent;
  border: 0;
  box-shadow: none;
  margin: 0; /* 覆盖 inspection-section 原有的外边距，避免“白卡外溢” */
}

/* 统一分隔线：除首个以外的 section 顶部加1px分隔线 */
.content-card > * + * {
  border-top: 1px solid var(--divider-color);
}

/* 桌面端：轻微圆角与阴影，贴近 Figma 的“单卡”视觉 */
@media (width >= 1200px) {
  .content-card {
    border-radius: 8px;
    box-shadow: none;
  }
}

/* 统一桌面端对齐与内容可读宽度（单张白卡内部） */
@media (width >= 1200px) {
  /* 桌面端版心标准：左右内边距 50px，可读宽度 801px（按设计尺规） */
  .content-card {
    --section-padding-x: 50px;
    --content-measure: 801px;
  }

  /* 1) 统一各区块左右内边距为 50px，保证左边缘对齐 */
  .content-card .info-card,
  .content-card .location-section,
  .content-card .description-section,
  .content-card .features-section,
  .content-card .inspection-section {
    padding: 40px var(--section-padding-x) !important; /* 统一左 50px，对齐 */
  }

  /* 2) 限制区块内直接子元素的最大宽度（标题、地图容器、内容容器等） */
  .content-card section > * {
    max-width: var(--content-measure); /* 801px */
  }

  /* 3) 标题与正文对齐并受同一上限约束 */
  .content-card .section-title {
    max-width: var(--content-measure);
  }

  /* 4) 地图整体宽度跟随可读宽度，避免过宽；同时两侧各留 50px 内边距 */
  .content-card .map-wrapper {
    max-width: var(--content-measure);
  }

  /* 5) 正文段落行长控制，进一步提升可读性 */
  .content-card .description-text {
    max-width: 68ch; /* 典型可读行长 */
  }
}

/* ==== 覆盖层（放在样式结尾，确保权重更高）==== */

/* 1) 扁平化白卡外观：无边框、无圆角、无阴影 */
.content-card {
  box-shadow: none !important; /* 去除白卡阴影 */
  border: none !important; /* 去除白卡四周边线（避免两侧“竖线”） */
  border-radius: 0 !important; /* 去除圆角 */
}

/* 内部子区块：确保无阴影，背景保持白色以便分隔线清晰可见 */
.content-card .info-card,
.content-card .location-section,
.content-card .description-section,
.content-card .features-section,
.content-card .inspection-section {
  box-shadow: none !important;
  background: var(--color-bg-card);
}

/* 2) 移除基于 border-top 的旧分隔线规则，改用伪元素绘制以控制左右对齐 */
.content-card > * + * {
  border-top: none !important; /* 覆盖之前的边框分隔线 */
}

/* 3) 桌面端：分隔线左对齐正文内容（48px 内边距），右对齐地图右缘（与 --content-measure 一致） */
@media (width >= 1200px) {
  /* 让每个区块能承载绝对定位的伪元素 */
  .content-card > * {
    position: relative;
  }

  .content-card > * + *::before {
    content: '';
    position: absolute;
    left: var(--section-padding-x, 50px); /* 与正文左侧对齐（标准 50px） */
    width: calc(
      100% - calc(var(--section-padding-x, 50px) * 2)
    ); /* 分隔线右端对齐到内容右缘（= 页面右侧 496） */

    top: 0;
    height: 1px;
    background-color: var(--divider-color);
  }
}

/* 移动端与小屏：恢复基础分隔线（无需特殊对齐规则） */
@media (width <= 1199px) {
  .content-card > * + * {
    border-top: 1px solid var(--divider-color) !important;
  }
}

/* 超宽屏段落行长限制：提升可读性，不改变容器的 453px/496px 对齐规则 */
@media (width >= 1920px) {
  .property-detail-page .content-card .description-section p {
    max-width: var(--paragraph-measure, 68ch);
    margin-right: auto;
  }
}

/* 新增：桌面端固定正文左右边距（左 453 / 右 496），并移除 801px 上限以保证右缘对齐 */
@media (width >= 1200px) {
  .content-card {
    margin-left: calc(453px - var(--section-padding-x, 50px)) !important;
    margin-right: calc(496px - var(--section-padding-x, 50px)) !important;
    width: auto !important; /* 由左右外边距与卡片内边距共同决定可用内容宽度 */
  }

  /* 取消 801px 限宽，让标题/内容/地图充满卡片可用宽度（从而右缘能对齐到 496） */
  .content-card section > *,
  .content-card .section-title,
  .content-card .map-wrapper,
  .content-card .description-text {
    max-width: none !important;
    width: auto !important;
  }
}

/* ==== PC 端局部覆盖：隐藏指示点、移除价格下分隔线、去橙色线条、返回键白底灰箭头 ==== */
@media (width >= 1200px) {
  /* 1) 隐藏轮播指示点（仅PC，移动端保留） */
  .image-indicators {
    display: none !important;
  }

  /* 2) 价格下方分隔线去除（保持原有外边距节奏） */
  .info-card .price-wrapper {
    padding-bottom: 0 !important;
    border-bottom: none !important;
  }

  /* 3) 分隔线统一中性灰，仅影响线条，不改文字颜色 */
  .property-detail-page hr,
  .property-detail-page .el-divider,
  .content-card > * + *::before {
    background-color: var(--divider-color) !important;
    border-color: var(--divider-color) !important;
  }

  /* 4) 返回按钮：白色圆底 + 灰色箭头（与移动端对齐，PC端） */
  .back-btn {
  background: var(--color-bg-card) !important; /* 白色圆底（令牌化），适配浅/深背景 */
  color: var(--color-text-secondary) !important; /* 灰色箭头（随 currentColor） */
}

  .back-btn:hover {
    background: var(--color-bg-card) !important; /* hover 同白底，阴影由默认处理 */
  }
}

/* ==== 全端统一：隐藏指示点 + 分隔线中性化（移动端与PC同时生效） ==== */

/* 1) 移动端与PC：统一隐藏轮播指示点 */
.image-indicators {
  display: none !important;
}

/* 2) 为详情页作用域提供统一分隔线变量，并在所有断点生效 */
.property-detail-page {
  --divider-color: var(--color-border-default); /* 中性灰 */
}

/* 3) 常见分隔元素统一为中性灰（避免品牌橙渗透到“线条/边框”） */
.property-detail-page :is(hr, .el-divider, .action-divider) {
  background-color: var(--divider-color) !important;
  border-color: var(--divider-color) !important;
}

/* 4) 价格下划线彻底移除（所有断点） */
.info-card .price-wrapper {
  border-bottom: none !important;
  padding-bottom: 0 !important;
}

/* ==== 移动端(≤767px)：地图尺寸与统一左右对齐（以 24px gutter 为基准） ==== */
@media (width <= 767px) {
  /* 统一白卡内部左右边界与地图一致 */
  .content-card {
    --mobile-gutter: 8px;
  }

  .content-card .info-card,
  .content-card .location-section,
  .content-card .description-section,
  .content-card .features-section,
  .content-card .inspection-section {
    padding-left: var(--mobile-gutter) !important;
    padding-right: var(--mobile-gutter) !important;
  }

  /* 地图容器：固定高度240，1px中性灰边框，直角，溢出隐藏；宽度随父容器100% */
  .map-container {
    width: 100% !important;
    height: 240px !important;
    border: 1px solid var(--color-border-default) !important;
    border-radius: 0 !important;
    overflow: hidden !important;
    box-sizing: border-box !important; /* 边框计入宽度，确保与红线对齐 */
    background: var(--surface-2); /* 兜底底色 */
  }
}

/* ==== 精简“See your travel time”样式（PC 与移动端一致的简洁行项） ==== */

/* 基础：单行、左右分布、上下分隔线、无卡片外观 */
.see-travel-times-btn {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-start !important; /* 靠左对齐 */
  width: 100% !important;
  padding: 12px 16px 12px 0 !important; /* 右侧留 16px 缓冲 */
  margin-top: 0 !important;
  background: transparent !important;
  border: none !important; /* 去除上下横线 */
  border-radius: 0 !important;
  box-shadow: none !important;
  text-align: left !important;
  cursor: pointer;
  gap: 8px !important; /* 文案与箭头最小间距 */
}

/* 标题仅一行，副标题与图标隐藏 */
.travel-icon-wrapper {
  display: none !important;
}

.travel-btn-subtitle {
  display: none !important;
}

.travel-btn-content {
  display: inline-flex !important;
  align-items: center !important;
  flex: 0 0 auto !important; /* 不占满整行，避免视觉居中 */
  width: auto !important;
  flex-direction: row !important; /* 与标题在一行 */
}

.travel-btn-title {
  font-size: 16px !important;
  font-weight: 600 !important;
  color: var(--color-text-primary) !important;
  line-height: 1.2 !important;
}

/* 右侧折叠提示箭头（改用 Lucide 组件，去除伪元素） */

/* 不再将箭头推到最右 */
.travel-chevron {
  width: 24px;
  height: 24px;
  color: var(--color-text-secondary);
  flex-shrink: 0;
  margin-left: 8px; /* 与标题间距 */
  margin-right: 16px; /* 与右侧边缘间距 */
}

/* PC 悬浮轻微高亮 & 行高略增 */
@media (width >= 1200px) {
  .see-travel-times-btn {
    padding-block: 16px !important;
  }

  .see-travel-times-btn:hover {
    background: var(--bg-hover) !important;
  }
}
</style>
