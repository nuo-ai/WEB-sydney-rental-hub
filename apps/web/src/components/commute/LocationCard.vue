<template>
  <div class="location-card">
    <div class="location-info">
      <span class="location-label" :class="labelClass">{{ location.label }}</span>
      <span class="location-address typo-body-sm">{{ truncatedAddress }}</span>
    </div>

    <div class="commute-info">
      <div v-if="isLoading" class="loading">
        <Loader2 class="spec-icon spinner" />
      </div>
      <div v-else-if="commuteData">
        <div class="time">{{ commuteData.duration }}</div>
        <div class="distance typo-body-sm">{{ commuteData.distance }}</div>
      </div>
      <div v-else class="no-data">
        <div class="time">--</div>
      </div>
    </div>

    <button class="remove-btn" @click="handleRemove" :title="$t('locationCard.remove')">
      <X class="spec-icon" />
    </button>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, inject } from 'vue'
import { useCommuteStore } from '@/stores/commute'
import { transportAPI } from '@/services/api'
import { Loader2, X } from 'lucide-vue-next'

const props = defineProps({
  location: {
    type: Object,
    required: true,
  },
  mode: {
    type: String,
    default: 'DRIVING',
  },
  from: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['remove'])

const commuteStore = useCommuteStore()
const t = inject('t')

// 响应式状态
const isLoading = ref(false)
const commuteData = ref(null)
const error = ref(null)

// 计算属性
const truncatedAddress = computed(() => {
  const address = props.location.address
  if (address.length > 40) {
    return address.substring(0, 37) + '...'
  }
  return address
})

const labelClass = computed(() => {
  const label = props.location.label?.toLowerCase()
  return `label-${label || 'other'}`
})

// 计算通勤时间
const calculateCommute = async () => {
  if (!props.from || !props.location) return

  isLoading.value = true
  error.value = null

  try {
    // 检查缓存
    const cacheKey = `${props.from.lat},${props.from.lng}-${props.location.id}-${props.mode}`
    const cached = commuteStore.getFromCache(cacheKey)

    if (cached) {
      commuteData.value = cached
    } else {
      // 准备API调用参数
      const origin = `${props.from.lat},${props.from.lng}`
      const destination = props.location.address

      // 确保location有坐标信息（用于本地估算）
      if (!props.location.latitude || !props.location.longitude) {
        console.warn('Location missing coordinates:', props.location)
      }

      const result = await transportAPI.getDirections(origin, destination, props.mode)

      if (result.error) {
        throw new Error(result.error)
      }

      commuteData.value = {
        duration: result.duration || (t ? t('locationCard.na') : 'N/A'),
        distance: result.distance || '',
      }

      // 缓存结果
      commuteStore.setCache(cacheKey, commuteData.value)
    }
  } catch (err) {
    console.error('Failed to calculate commute:', err)
    error.value = err.message
    commuteData.value = {
      duration: t ? t('locationCard.na') : 'N/A',
      distance: '',
    }
  } finally {
    isLoading.value = false
  }
}

// 监听交通方式变化
watch(
  () => props.mode,
  () => {
    calculateCommute()
  },
)

// 监听起点变化
watch(
  () => props.from,
  () => {
    calculateCommute()
  },
  { deep: true },
)

const handleRemove = () => {
  emit('remove', props.location.id)
}

// 生命周期
onMounted(() => {
  calculateCommute()
})
</script>

<style scoped>
.location-card {
  display: flex;
  align-items: center;
  padding: 12px;
  background: var(--surface-2);
  border-radius: 8px;
  margin-bottom: 12px;
  transition: all 0.2s;
}

.location-card:hover {
  background: var(--bg-hover);
}

/* 地址信息 */
.location-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.location-label {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  align-self: flex-start;
}

.label-work {
  background: var(--surface-2);
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border-default);
}

.label-school {
  background: var(--surface-2);
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border-default);
}

.label-home {
  background: var(--surface-2);
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border-default);
}

.label-other {
  background: var(--surface-2);
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border-default);
}

.location-address {
  font-size: 14px;
  color: var(--color-text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 通勤信息 */
.commute-info {
  flex-shrink: 0;
  min-width: 80px;
  text-align: right;
  margin: 0 12px;
}

.loading {
  color: var(--text-muted);
}

.time {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: 1.2;
}

.distance {
  font-size: 12px;
  color: var(--color-text-secondary);
  margin-top: 2px;
}

.no-data .time {
  color: var(--text-muted);
}

/* 删除按钮 */
.remove-btn {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  border: none;
  background: none;
  color: var(--text-muted);
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s;
}

.remove-btn:hover {
  background: var(--color-bg-card);
  color: var(--color-danger);
}

/* 加载动画 */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

.spinner {
  animation: spin 1s linear infinite;
}

/* 移动端优化 */
@media (width <= 768px) {
  .location-card {
    padding: 10px;
  }

  .commute-info {
    min-width: 70px;
    margin: 0 8px;
  }
}
</style>
