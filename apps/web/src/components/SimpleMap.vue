<template>
  <div class="simple-map-container">
    <!-- 使用OpenStreetMap的iframe嵌入 -->
    <iframe
      v-if="!useStaticImage"
      :src="openStreetMapUrl"
      class="map-iframe"
      frameborder="0"
      scrolling="no"
      marginheight="0"
      marginwidth="0"
      :title="markerTitle"
    ></iframe>

    <!-- 备用：显示静态地址信息 -->
    <div v-else class="map-static">
      <div class="map-icon">
        <el-icon :size="48" class="map-icon-symbol"><Location /></el-icon>
      </div>
      <div class="map-info">
        <h4>{{ markerTitle }}</h4>
        <p>{{ formattedCoordinates }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { Location } from '@element-plus/icons-vue'

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
  markerTitle: {
    type: String,
    default: 'Property Location',
  },
})

// 是否使用静态图片模式
const useStaticImage = ref(false)

// OpenStreetMap嵌入URL
const openStreetMapUrl = computed(() => {
  const bbox = calculateBoundingBox(props.latitude, props.longitude, props.zoom)
  return `https://www.openstreetmap.org/export/embed.html?bbox=${bbox}&layer=mapnik&marker=${props.latitude},${props.longitude}`
})

// 计算边界框
function calculateBoundingBox(lat, lng, zoom) {
  const n = Math.pow(2, zoom)
  const latDelta = 180 / n
  const lngDelta = 360 / n

  const minLat = lat - latDelta / 2
  const maxLat = lat + latDelta / 2
  const minLng = lng - lngDelta / 2
  const maxLng = lng + lngDelta / 2

  return `${minLng},${minLat},${maxLng},${maxLat}`
}

// 格式化坐标显示
const formattedCoordinates = computed(() => {
  const lat = props.latitude.toFixed(6)
  const lng = props.longitude.toFixed(6)
  return `纬度: ${lat}, 经度: ${lng}`
})
</script>

<style scoped>
.simple-map-container {
  width: 100%;
  height: v-bind(height);
  border-radius: 8px;
  overflow: hidden;
  background-color: var(--surface-2);
}

.map-iframe {
  width: 100%;
  height: 100%;
  border: none;
}

.map-static {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  text-align: center;
  background: linear-gradient(135deg, var(--surface-2) 0%, var(--surface-4) 100%);
}

.map-icon {
  margin-bottom: 16px;
}

.map-icon :deep(.el-icon),
.map-icon :deep(svg) {
  color: var(--juwo-primary);
}

.map-info h4 {
  margin: 0 0 8px;
  font-size: 16px;
  color: var(--color-text-primary);
}

.map-info p {
  margin: 0;
  font-size: 14px;
  color: var(--color-text-secondary);
}
</style>
