<template>
  <div class="virtual-list-container" ref="containerRef" @scroll="handleScroll">
    <!-- 虚拟滚动容器 -->
    <div
      class="virtual-list-scroller"
      :style="{
        height: `${totalHeight}px`,
        width: '100%',
        position: 'relative'
      }"
    >
      <!-- 虚拟化的房源卡片 -->
      <div
        v-for="(item, index) in visibleItems"
        :key="`row-${item.index}`"
        class="virtual-row-wrapper"
        :style="{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: `${item.height}px`,
          transform: `translateY(${item.offset}px)`
        }"
      >
        <div class="virtual-row">
          <PropertyCard
            v-for="property in item.properties"
            :key="property.listing_id"
            :property="property"
            @click="$emit('property-click', property)"
            @contact="$emit('contact-property', property)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import PropertyCard from './PropertyCard.vue'

const props = defineProps({
  properties: {
    type: Array,
    required: true,
    default: () => []
  }
})

const emit = defineEmits(['property-click', 'contact-property'])

// 响应式引用
const containerRef = ref(null)
const scrollTop = ref(0)
const containerHeight = ref(800) // 默认高度

// 配置参数
const CARD_HEIGHT = 430 // PropertyCard 的估算高度
const GAP = 24 // 卡片间距
const OVERSCAN = 3 // 预渲染的行数

// 根据屏幕宽度动态调整列数
const getColumns = () => {
  const width = window.innerWidth
  if (width < 768) {
    return 1  // 移动端单列
  } else if (width < 1024) {
    return 2  // 平板双列
  } else {
    return 2  // 桌面端双列
  }
}

const columns = ref(getColumns())
const rowHeight = computed(() => CARD_HEIGHT + GAP)

// 计算总行数
const totalRows = computed(() => {
  return Math.ceil(props.properties.length / columns.value)
})

// 计算总高度
const totalHeight = computed(() => {
  return totalRows.value * rowHeight.value
})

// 计算可见行范围
const visibleRange = computed(() => {
  const start = Math.floor(scrollTop.value / rowHeight.value)
  const end = Math.ceil((scrollTop.value + containerHeight.value) / rowHeight.value)
  
  return {
    start: Math.max(0, start - OVERSCAN),
    end: Math.min(totalRows.value, end + OVERSCAN)
  }
})

// 计算可见项
const visibleItems = computed(() => {
  const items = []
  const { start, end } = visibleRange.value
  
  for (let i = start; i < end; i++) {
    const startIdx = i * columns.value
    const endIdx = Math.min(startIdx + columns.value, props.properties.length)
    const rowProperties = props.properties.slice(startIdx, endIdx)
    
    if (rowProperties.length > 0) {
      items.push({
        index: i,
        offset: i * rowHeight.value,
        height: rowHeight.value,
        properties: rowProperties
      })
    }
  }
  
  return items
})

// 处理滚动
const handleScroll = (e) => {
  scrollTop.value = e.target.scrollTop
}

// 处理窗口大小变化
const handleResize = () => {
  columns.value = getColumns()
  if (containerRef.value) {
    containerHeight.value = containerRef.value.clientHeight
  }
}

// 生命周期
onMounted(() => {
  window.addEventListener('resize', handleResize)
  handleResize() // 初始化容器高度
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

</script>

<style scoped>
.virtual-list-container {
  width: 100%;
  height: 600px; /* 固定高度，确保虚拟滚动正常工作 */
  overflow-y: auto;
  overflow-x: hidden;
  position: relative;
}

@media (max-width: 768px) {
  .virtual-list-container {
    height: calc(100vh - 280px); /* 移动端调整高度 */
  }
}

@media (min-width: 769px) {
  .virtual-list-container {
    height: calc(100vh - 200px); /* 桌面端动态高度 */
  }
}

.virtual-list-scroller {
  position: relative;
}

.virtual-row {
  display: grid;
  gap: 24px;
  padding: 0;
  width: 100%;
}

/* 响应式网格布局 */
@media (max-width: 767px) {
  .virtual-row {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}

@media (min-width: 768px) and (max-width: 1023px) {
  .virtual-row {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
}

@media (min-width: 1024px) {
  .virtual-row {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
}

/* 滚动条样式优化 */
.virtual-list-container::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.virtual-list-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.virtual-list-container::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.virtual-list-container::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>