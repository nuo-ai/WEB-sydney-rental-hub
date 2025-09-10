<template>
  <div class="google-map-container">
    <!-- 如果地图加载失败，显示静态地图作为备用 -->
    <div v-if="mapError" class="map-fallback">
      <img
        :src="staticMapUrl"
        :alt="markerTitle"
        class="static-map"
        @error="handleStaticMapError"
      />
      <div class="map-error-info">
        <el-icon><Location /></el-icon>
        <span>{{ markerTitle }}</span>
      </div>
    </div>

    <!-- 正常的Google地图 -->
    <div v-else ref="mapRef" class="google-map" :id="mapId">
      <!-- 加载占位符 -->
      <div v-if="!mapLoaded && !mapError" class="map-loading">
        <el-icon class="is-loading" :size="24"><Loading /></el-icon>
        <span>Loading map...</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick, computed } from 'vue'
import { Loading, Location } from '@element-plus/icons-vue'

const props = defineProps({
  latitude: {
    type: Number,
    required: true,
  },
  longitude: {
    type: Number,
    required: true,
  },
  zoom: {
    type: Number,
    default: 14,
  },
  height: {
    type: String,
    default: '200px',
  },
  showMarker: {
    type: Boolean,
    default: true,
  },
  markerTitle: {
    type: String,
    default: 'Property Location',
  },
  // 新增：是否锁定地图中心（锁定后缩放/拖拽都会回到锁定中心）
  lockCenter: {
    type: Boolean,
    default: false,
  },
  // 新增：锁定的中心点（不传则默认使用 latitude/longitude）
  focusCenter: {
    type: Object,
    default: null,
  },
  // 新增：路线数据（[{lat,lng}, ...] 或 { encodedPolyline: '...' } 或 { path: [{lat,lng}] }）
  route: {
    type: [Array, Object],
    default: null,
  },
  // 新增：路线样式
  routeOptions: {
    type: Object,
    default: () => ({
      strokeColor: '#4285F4',
      strokeOpacity: 0.9,
      strokeWeight: 5,
      zIndex: 999,
    }),
  },
  // 新增：在有路线时是否自动缩放以完整展示路径（默认开启，移动端体验更好）
  autoFit: {
    type: Boolean,
    default: true,
  },
  // 新增：fitBounds 的像素内边距（移动端建议 24）
  fitPadding: {
    type: Number,
    default: 24,
  },
  // 新增：可选的起终点，用于绘制端点标记或参与 fitBounds
  routeEndpoints: {
    type: Object,
    default: null,
  },
  // 新增：路线标签文本（显示在路径附近的气泡）
  routeLabelText: {
    type: String,
    default: '',
  },
})

const mapRef = ref(null)
const mapId = `map-${Math.random().toString(36).substr(2, 9)}`
const mapLoaded = ref(false)
const mapError = ref(null)
let map = null
let marker = null
let googleMapsLoaded = false
let isInitializing = false
let isDestroyed = false // 跟踪组件是否已销毁
let polyline = null // 路径 Polyline 实例
let listeners = [] // 已注册的地图事件监听器
let lastRoutePath = null // 记录最近一次路线点列，便于 resize 重新自适应
let isFitting = false // 正在执行 fitBounds，避免与锁定中心冲突
let resizeTimer = null // 节流 resize
let routeLabelInfoWindow = null // 路线标签 InfoWindow 实例

// 数值校验与经纬度规范化：兼容字符串输入并过滤 NaN/Infinity
const isFiniteNumber = (n) => typeof n === 'number' && Number.isFinite(n)
const toNumber = (v) => (typeof v === 'string' ? Number(v) : v)
const normalizeLatLng = (lat, lng) => {
  const nLat = toNumber(lat)
  const nLng = toNumber(lng)
  if (isFiniteNumber(nLat) && isFiniteNumber(nLng)) {
    return { lat: nLat, lng: nLng }
  }
  return null
}

// 计算当前应当锁定的中心点
const getLockCenter = () => {
  // 优先使用 focusCenter（若提供），否则使用 props 的经纬度；均做数值规范化
  if (props.focusCenter) {
    const c = normalizeLatLng(props.focusCenter.lat, props.focusCenter.lng)
    if (c) return c
  }
  return normalizeLatLng(props.latitude, props.longitude)
}

// 应用中心锁定：将地图中心回到目标点
const applyCenterLock = () => {
  // 说明：仅在用户显式开启锁定时生效；且在自动适配期间不回弹中心，避免与 fitBounds 抢焦点
  if (map && googleMapsLoaded && !isDestroyed && props.lockCenter && !isFitting) {
    const c = getLockCenter()
    if (c) {
      map.setCenter(c)
    }
  }
}

// 清空已绘制的路线
const clearRoute = () => {
  // 说明：避免重复绘制或内存泄漏
  if (polyline) {
    polyline.setMap(null)
    polyline = null
  }
  // 同步清理路线标签
  if (routeLabelInfoWindow) {
    try {
      routeLabelInfoWindow.close()
    } catch {
      // 忽略关闭异常
    }
    routeLabelInfoWindow = null
  }
}

// 解码 Google Encoded Polyline 字符串
function decodePolyline(str) {
  // 说明：采用标准 Google Polyline 解码算法，兼容服务端返回的压缩路径
  let index = 0,
    lat = 0,
    lng = 0
  const coordinates = []
  while (index < str.length) {
    let b,
      shift = 0,
      result = 0
    do {
      b = str.charCodeAt(index++) - 63
      result |= (b & 0x1f) << shift
      shift += 5
    } while (b >= 0x20)
    const dlat = result & 1 ? ~(result >> 1) : result >> 1
    lat += dlat

    shift = 0
    result = 0
    do {
      b = str.charCodeAt(index++) - 63
      result |= (b & 0x1f) << shift
      shift += 5
    } while (b >= 0x20)
    const dlng = result & 1 ? ~(result >> 1) : result >> 1
    lng += dlng

    coordinates.push({ lat: lat / 1e5, lng: lng / 1e5 })
  }
  return coordinates
}

const fitRouteBounds = (path) => {
  // 说明：将整条路线纳入视野，含起终点（若提供），并留出安全内边距
  if (!map || !path || path.length < 2) return
  const bounds = new google.maps.LatLngBounds()
  path.forEach((p) => bounds.extend(new google.maps.LatLng(p.lat, p.lng)))
  if (
    props.routeEndpoints &&
    props.routeEndpoints.origin &&
    typeof props.routeEndpoints.origin.lat === 'number' &&
    typeof props.routeEndpoints.origin.lng === 'number'
  ) {
    bounds.extend(
      new google.maps.LatLng(props.routeEndpoints.origin.lat, props.routeEndpoints.origin.lng),
    )
  }
  if (
    props.routeEndpoints &&
    props.routeEndpoints.destination &&
    typeof props.routeEndpoints.destination.lat === 'number' &&
    typeof props.routeEndpoints.destination.lng === 'number'
  ) {
    bounds.extend(
      new google.maps.LatLng(
        props.routeEndpoints.destination.lat,
        props.routeEndpoints.destination.lng,
      ),
    )
  }
  try {
    isFitting = true
    map.fitBounds(bounds, {
      top: props.fitPadding,
      right: props.fitPadding,
      bottom: props.fitPadding,
      left: props.fitPadding,
    })
  } finally {
    // 小延迟后恢复，以便地图 idle 后不会被锁定中心立刻拉回
    setTimeout(() => {
      isFitting = false
    }, 300)
  }
}

// 在路径中点放置/更新路线标签 InfoWindow
const updateRouteLabel = (path) => {
  // 说明：仅当提供了标签文本且路径有效时才展示；定位到路径中点
  if (!map || !googleMapsLoaded || isDestroyed) return
  if (!path || path.length < 2) return

  const text = props.routeLabelText
  if (!text) {
    // 若文本为空则移除已有标签
    if (routeLabelInfoWindow) {
      try {
        routeLabelInfoWindow.close()
      } catch {
        // 忽略关闭异常
      }
      routeLabelInfoWindow = null
    }
    return
  }

  const mid = path[Math.floor(path.length / 2)]
  if (!routeLabelInfoWindow) {
    routeLabelInfoWindow = new google.maps.InfoWindow({
      content: text,
      position: mid,
      disableAutoPan: true, // 说明：不触发自动平移，避免影响用户交互
    })
    // 兼容旧版 open(map) 签名
    try {
      routeLabelInfoWindow.open(map)
    } catch {
      routeLabelInfoWindow.open({ map })
    }
  } else {
    try {
      routeLabelInfoWindow.setContent(text)
      routeLabelInfoWindow.setPosition(mid)
      // 确保已打开
      routeLabelInfoWindow.open({ map })
    } catch {
      // 忽略异常
    }
  }
}

// 渲染路线 Polyline
const renderRoute = () => {
  // 说明：允许传入多种数据格式；空值直接跳过以避免误绘制
  if (!map || !googleMapsLoaded || isDestroyed) return
  clearRoute()
  if (!props.route) return

  let path = []
  if (Array.isArray(props.route)) {
    path = props.route
  } else if (props.route && typeof props.route === 'object') {
    if (props.route.encodedPolyline) {
      path = decodePolyline(props.route.encodedPolyline)
    } else if (Array.isArray(props.route.path)) {
      path = props.route.path
    }
  }

  if (!path || path.length < 2) return
  polyline = new google.maps.Polyline({
    path,
    ...props.routeOptions,
    map,
  })
  // 记录并自动自适应视野
  lastRoutePath = path
  if (props.autoFit) {
    fitRouteBounds(path)
  }
  // 更新路线标签展示
  updateRouteLabel(path)
}

// 静态地图URL（作为备用）
const staticMapUrl = computed(() => {
  const size = '600x300'
  const zoom = props.zoom
  const c = getLockCenter()
  // 从环境变量获取 API 密钥（安全实践）
  const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || ''

  if (!c || !apiKey || apiKey === 'YOUR_NEW_API_KEY_HERE_REPLACE_ME') {
    // 坐标或密钥无效时不返回 URL，交由组件显示兜底占位
    return ''
  }

  const center = `${c.lat},${c.lng}`
  const marker = `markers=color:red%7C${center}`
  return `https://maps.googleapis.com/maps/api/staticmap?center=${center}&zoom=${zoom}&size=${size}&${marker}&key=${apiKey}`
})

// 处理静态地图加载失败
const handleStaticMapError = () => {
  // 静态地图加载失败，使用占位图
}

// Check if Google Maps is already loaded
const isGoogleMapsLoaded = () => {
  return typeof google !== 'undefined' && google.maps
}

// Load Google Maps script
const loadGoogleMaps = () => {
  return new Promise((resolve, reject) => {
    if (isGoogleMapsLoaded()) {
      googleMapsLoaded = true
      resolve()
      return
    }

    // Check if script is already being loaded
    if (window.googleMapsLoadPromise) {
      window.googleMapsLoadPromise.then(resolve).catch(reject)
      return
    }

    // Create a new promise for loading
    window.googleMapsLoadPromise = new Promise((resolveLoad, rejectLoad) => {
      const script = document.createElement('script')
      // 从环境变量获取 API 密钥（不再使用硬编码的后备密钥）
      const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || ''

      if (!apiKey || apiKey === 'YOUR_NEW_API_KEY_HERE_REPLACE_ME') {
        console.error(
          'Google Maps API key not configured. Please set VITE_GOOGLE_MAPS_API_KEY in .env file',
        )
        rejectLoad(new Error('API key not configured'))
        return
      }

      script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`
      script.async = true
      script.defer = true

      script.onload = () => {
        googleMapsLoaded = true
        resolveLoad()
      }

      script.onerror = () => {
        const error = new Error('Failed to load Google Maps')
        rejectLoad(error)
      }

      document.head.appendChild(script)
    })

    window.googleMapsLoadPromise.then(resolve).catch(reject)
  })
}

// Initialize the map
const initMap = async () => {
  // Prevent multiple initializations
  if (isInitializing || mapLoaded.value || isDestroyed) {
    return
  }

  isInitializing = true

  try {
    // 初始化地图
    await loadGoogleMaps()

    // Wait for DOM to be ready
    await nextTick()

    if (!mapRef.value) {
      console.error('Map ref not found')
      isInitializing = false
      return
    }

    const safeInitialCenter = getLockCenter() || { lat: 0, lng: 0 }
    const mapOptions = {
      center: safeInitialCenter,
      zoom: props.zoom,
      mapTypeControl: false,
      streetViewControl: false,
      fullscreenControl: false,
      styles: [
        {
          featureType: 'poi',
          elementType: 'labels',
          stylers: [{ visibility: 'off' }],
        },
      ],
    }

    // 创建地图
    map = new google.maps.Map(mapRef.value, mapOptions)

    // 若开启中心锁定则立即应用一次，并注册事件监听在缩放/拖拽/空闲后回到锁定中心
    if (props.lockCenter) {
      applyCenterLock()
    }
    listeners.push(
      map.addListener('zoom_changed', () => {
        applyCenterLock()
      }),
      map.addListener('dragend', () => {
        applyCenterLock()
      }),
      map.addListener('idle', () => {
        if (props.lockCenter) applyCenterLock()
      }),
    )

    // 若提供路线则渲染 Polyline
    renderRoute()

    if (props.showMarker) {
      const c = getLockCenter()
      if (c) {
        marker = new google.maps.Marker({
          position: c,
          map: map,
          title: props.markerTitle,
          animation: google.maps.Animation.DROP,
        })
      }
      // 添加标记到地图
    }

    // 检查组件是否还存在
    if (!isDestroyed) {
      mapLoaded.value = true
      // 初始化完成后触发一次 resize，修复首次渲染时 canvas 未填满容器的情况
      setTimeout(() => {
        try {
          triggerMapResize()
        } catch (err) {
          // ignore
          void err
        }
      }, 0)
    }
  } catch (error) {
    console.error('Error initializing Google Map:', error)
    mapError.value = '地图暂时无法加载'
  } finally {
    if (!isDestroyed) {
      isInitializing = false
    }
  }
}

// Update map center when coordinates change
watch(
  () => [props.latitude, props.longitude],
  ([newLat, newLng]) => {
    if (map && googleMapsLoaded && !isDestroyed) {
      // 说明：当开启中心锁定时，以锁定中心为准；否则跟随传入经纬度（规范化并校验）
      if (props.lockCenter) {
        applyCenterLock()
      } else {
        const c = normalizeLatLng(newLat, newLng)
        if (c) {
          map.setCenter(c)
          if (marker) {
            marker.setPosition(c)
          }
        }
      }
    }
  },
)

// 当锁定开关或锁定中心变化时，重新应用中心锁定
watch(
  () => [props.lockCenter, props.focusCenter],
  () => {
    applyCenterLock()
  },
  { deep: true },
)

// 当路线或样式变更时，重新渲染路线
watch(
  () => props.route,
  () => {
    renderRoute()
  },
  { deep: true },
)

watch(
  () => props.routeOptions,
  () => {
    renderRoute()
  },
  { deep: true },
)

// 当路线标签文本变化时，刷新 InfoWindow
watch(
  () => props.routeLabelText,
  () => {
    if (lastRoutePath && lastRoutePath.length > 1) {
      updateRouteLabel(lastRoutePath)
    } else if (routeLabelInfoWindow) {
      try {
        routeLabelInfoWindow.close()
      } catch {
        // 忽略
      }
      routeLabelInfoWindow = null
    }
  },
)

// 高度变更时触发地图 resize，修复容器高度变化后的灰条
watch(
  () => props.height,
  async () => {
    await nextTick()
    triggerMapResize()
  },
)

/* 中文注释：统一触发地图 resize 并根据策略恢复视图，避免容器高度变化后出现灰条 */
const triggerMapResize = () => {
  if (!map || !googleMapsLoaded || isDestroyed) return
  try {
    if (google && google.maps && google.maps.event) {
      google.maps.event.trigger(map, 'resize')
    }
  } catch {
    // 忽略触发异常
  }

  if (props.autoFit && lastRoutePath && lastRoutePath.length > 1) {
    // 有路线时优先自适应并更新标签
    fitRouteBounds(lastRoutePath)
    updateRouteLabel(lastRoutePath)
  } else {
    // 无路线时按中心策略恢复视图
    if (props.lockCenter) {
      applyCenterLock()
    } else {
      const c = getLockCenter()
      if (c) map.setCenter(c)
    }
  }
}

const onResize = () => {
  clearTimeout(resizeTimer)
  resizeTimer = setTimeout(() => {
    triggerMapResize()
  }, 150)
}

onMounted(() => {
  initMap()
  if (typeof window !== 'undefined') {
    window.addEventListener('resize', onResize)
  }
})

onUnmounted(() => {
  isDestroyed = true
  // 清理标记
  if (marker) {
    marker.setMap(null)
    marker = null
  }
  // 清理路线
  if (polyline) {
    polyline.setMap(null)
    polyline = null
  }
  // 清理路线标签
  if (routeLabelInfoWindow) {
    try {
      routeLabelInfoWindow.close()
    } catch {
      // 忽略
    }
    routeLabelInfoWindow = null
  }
  // 移除事件监听，避免内存泄漏
  try {
    if (listeners && listeners.length && google && google.maps && google.maps.event) {
      listeners.forEach((l) => google.maps.event.removeListener(l))
    }
  } catch {
    // 忽略清理异常
  }
  listeners = []
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', onResize)
  }
  map = null
  mapLoaded.value = false
})
</script>

<style scoped>
.google-map-container {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
}

.google-map {
  width: 100%;
  height: v-bind(height);
  background-color: #f5f5f5;
  position: relative;
}

.map-loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #999;
}

.map-loading span {
  font-size: 14px;
}

/* 备用地图样式 */
.map-fallback {
  width: 100%;
  height: v-bind(height);
  background-color: #f5f5f5;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  overflow: hidden;
}

.static-map {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.map-error-info {
  position: absolute;
  bottom: 10px;
  left: 10px;
  background: rgba(255, 255, 255, 0.9);
  padding: 8px 12px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #666;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
