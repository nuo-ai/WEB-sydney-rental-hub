<template>
  <div v-if="visible" class="save-search-modal-wrapper">
    <!-- 遮罩层 -->
    <div class="modal-overlay" @click="closeModal"></div>

    <!-- 保存搜索弹窗 -->
    <div ref="modalRef" class="save-search-modal" tabindex="-1">
      <!-- 头部 -->
      <div class="modal-header">
        <h3 class="modal-title">保存搜索</h3>
        <button class="close-btn" @click="closeModal" aria-label="关闭">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>

      <!-- 内容区域 -->
      <div class="modal-content">
        <!-- 搜索名称 -->
        <div class="form-group">
          <label for="searchName" class="form-label">搜索名称</label>
          <input
            id="searchName"
            v-model="searchName"
            type="text"
            class="form-input"
            placeholder="为您的搜索命名..."
            maxlength="50"
          />
          <div class="input-hint">{{ searchName.length }}/50</div>
        </div>

        <!-- 邮件通知频率 -->
        <div class="form-group">
          <label for="emailFrequency" class="form-label">邮件通知频率</label>
          <select id="emailFrequency" v-model="emailFrequency" class="form-select">
            <option value="instant">即时通知</option>
            <option value="daily">每日汇总</option>
            <option value="weekly">每周汇总</option>
            <option value="never">不接收邮件</option>
          </select>
          <div class="input-hint">当有新房源匹配您的条件时通知您</div>
        </div>

        <!-- 搜索条件预览 -->
        <div class="search-preview">
          <h4 class="preview-title">搜索条件预览</h4>
          <div class="preview-content">
            <div v-if="previewText" class="preview-description">
              {{ previewText }}
            </div>
            <div v-else class="preview-empty">
              暂无筛选条件
            </div>
          </div>
        </div>
      </div>

      <!-- 底部操作 -->
      <div class="modal-footer">
        <button class="btn-secondary" @click="closeModal">
          取消
        </button>
        <button
          class="btn-primary"
          @click="handleSave"
          :disabled="!searchName.trim() || isSaving"
        >
          <span v-if="isSaving">保存中...</span>
          <span v-else>保存搜索</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onUnmounted } from 'vue'
import { usePropertiesStore } from '@/stores/properties'

// 组件属性
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  filterConditions: {
    type: Object,
    default: () => ({})
  }
})

// 组件事件
const emit = defineEmits(['update:modelValue', 'save', 'saved'])

// 状态
const modalRef = ref(null)
const searchName = ref('')
const emailFrequency = ref('daily')
const isSaving = ref(false)

// Store
const propertiesStore = usePropertiesStore()

// 显示状态
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 生成智能搜索名称
const generateSearchName = () => {
  const conditions = props.filterConditions
  const locations = propertiesStore.selectedLocations || []

  let name = ''

  // 区域部分
  if (locations.length > 0) {
    const areaNames = locations.map(loc => loc.name || loc.suburb).filter(Boolean)
    if (areaNames.length === 1) {
      name += areaNames[0]
    } else if (areaNames.length > 1) {
      name += `${areaNames[0]} 等 ${areaNames.length} 个区域`
    }
  }

  // 房型部分
  if (conditions.bedrooms) {
    const bedroomText = conditions.bedrooms === '0' ? 'Studio'
      : conditions.bedrooms === '4+' ? '4房及以上'
      : `${conditions.bedrooms}房`
    name += name ? ` ${bedroomText}` : bedroomText
  }

  // 价格部分
  if (conditions.priceRange && Array.isArray(conditions.priceRange)) {
    const [min, max] = conditions.priceRange
    if (min > 0 || max < 5000) {
      const priceText = min > 0 && max < 5000
        ? `$${min}-${max}`
        : min > 0 ? `≥$${min}` : `≤$${max}`
      name += name ? ` ${priceText}` : priceText
    }
  }

  // 家具要求
  if (conditions.furnished) {
    name += name ? ' 有家具' : '有家具房源'
  }

  return name || '我的搜索'
}

// 搜索条件预览文本
const previewText = computed(() => {
  const conditions = props.filterConditions
  const locations = propertiesStore.selectedLocations || []

  const parts = []

  // 区域
  if (locations.length > 0) {
    const areaNames = locations.map(loc => loc.name || loc.suburb).filter(Boolean)
    if (areaNames.length === 1) {
      parts.push(`区域：${areaNames[0]}`)
    } else if (areaNames.length > 1) {
      parts.push(`区域：${areaNames[0]} 等 ${areaNames.length} 个区域`)
    }
  }

  // 房型
  if (conditions.bedrooms) {
    const bedroomText = conditions.bedrooms === '0' ? 'Studio'
      : conditions.bedrooms === '4+' ? '4房及以上'
      : `${conditions.bedrooms}房`
    parts.push(`房型：${bedroomText}`)
  }

  // 价格
  if (conditions.priceRange && Array.isArray(conditions.priceRange)) {
    const [min, max] = conditions.priceRange
    if (min > 0 || max < 5000) {
      const priceText = min > 0 && max < 5000
        ? `$${min} - $${max}`
        : min > 0 ? `≥$${min}` : `≤$${max}`
      parts.push(`价格：${priceText}`)
    }
  }

  // 浴室
  if (conditions.bathrooms) {
    const bathroomText = conditions.bathrooms === '3+' ? '3个及以上' : `${conditions.bathrooms}个`
    parts.push(`浴室：${bathroomText}`)
  }

  // 车位
  if (conditions.parking) {
    const parkingText = conditions.parking === '3+' ? '3个及以上' : `${conditions.parking}个`
    parts.push(`车位：${parkingText}`)
  }

  // 家具
  if (conditions.furnished) {
    parts.push('家具：有家具')
  }

  // 日期
  if (conditions.dateFrom || conditions.dateTo) {
    const dateText = conditions.dateFrom && conditions.dateTo
      ? `${formatDate(conditions.dateFrom)} 至 ${formatDate(conditions.dateTo)}`
      : conditions.dateFrom ? `${formatDate(conditions.dateFrom)} 之后`
      : `${formatDate(conditions.dateTo)} 之前`
    parts.push(`入住时间：${dateText}`)
  }

  return parts.join('；')
})

// 格式化日期
const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
}

// 保存搜索
const handleSave = async () => {
  if (!searchName.value.trim()) return

  isSaving.value = true

  try {
    // 构建保存的搜索对象
    const savedSearch = {
      id: Date.now().toString(),
      name: searchName.value.trim(),
      emailFrequency: emailFrequency.value,
      conditions: props.filterConditions,
      locations: propertiesStore.selectedLocations || [],
      createdAt: new Date().toISOString(),
      lastNotified: null
    }

    // 保存到本地存储
    const existingSaves = JSON.parse(localStorage.getItem('savedSearches') || '[]')
    existingSaves.push(savedSearch)
    localStorage.setItem('savedSearches', JSON.stringify(existingSaves))

    // 发送保存事件
    emit('save', savedSearch)
    emit('saved', savedSearch)

    // 关闭弹窗
    closeModal()

    // 显示成功提示（这里可以用 ElMessage 或其他通知组件）
    console.log('搜索已保存！', savedSearch)

  } catch (error) {
    console.error('保存搜索失败:', error)
  } finally {
    isSaving.value = false
  }
}

// 关闭弹窗
const closeModal = () => {
  visible.value = false
  // 重置表单
  searchName.value = ''
  emailFrequency.value = 'daily'
}

// 键盘事件处理
const handleKeyDown = (event) => {
  if (event.key === 'Escape') {
    closeModal()
  }
}

// 监听显示状态变化
watch(visible, (newValue) => {
  if (newValue) {
    // 打开时生成默认搜索名称
    searchName.value = generateSearchName()

    // 聚焦到弹窗
    nextTick(() => {
      modalRef.value?.focus()
    })

    // 添加键盘监听
    document.addEventListener('keydown', handleKeyDown)
  } else {
    // 关闭时移除监听
    document.removeEventListener('keydown', handleKeyDown)
  }
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
})
</script>

<style scoped>
/* 弹窗容器 */
.save-search-modal-wrapper {
  position: fixed;
  inset: 0;
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
}

.save-search-modal {
  position: relative;
  width: 100%;
  max-width: 480px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  max-height: 90vh;
  overflow: hidden;
}

/* 头部 */
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 24px 0;
}

.modal-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
}

/* 内容区域 */
.modal-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 24px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--color-border-default);
  border-radius: 8px;
  font-size: 14px;
  color: var(--color-text-primary);
  background: white;
  transition: border-color 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: var(--juwo-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-select {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--color-border-default);
  border-radius: 8px;
  font-size: 14px;
  color: var(--color-text-primary);
  background: white;
  cursor: pointer;
  transition: border-color 0.2s ease;
  box-sizing: border-box;
}

.form-select:focus {
  outline: none;
  border-color: var(--juwo-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.input-hint {
  font-size: 12px;
  color: var(--color-text-secondary);
  margin-top: 4px;
}

/* 搜索条件预览 */
.search-preview {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-default);
  border-radius: 8px;
  padding: 16px;
}

.preview-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 12px;
}

.preview-content {
  font-size: 14px;
  line-height: 1.5;
}

.preview-description {
  color: var(--color-text-primary);
}

.preview-empty {
  color: var(--color-text-secondary);
  font-style: italic;
}

/* 底部操作 */
.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  padding: 0 24px 24px;
  border-top: 1px solid var(--color-border-default);
  margin-top: 16px;
  padding-top: 16px;
}

.btn-secondary {
  padding: 10px 20px;
  border: 1px solid var(--color-border-default);
  border-radius: 6px;
  background: white;
  color: var(--color-text-primary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  border-color: var(--color-border-strong);
  background: var(--color-bg-hover);
}

.btn-primary {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  background: var(--juwo-primary);
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover:not(:disabled) {
  background: var(--juwo-primary-light);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .save-search-modal {
    max-width: 95vw;
    margin: 10px;
  }

  .modal-header {
    padding: 20px 20px 0;
  }

  .modal-content {
    padding: 20px;
  }

  .modal-footer {
    padding: 0 20px 20px;
    flex-direction: column-reverse;
    gap: 8px;
  }

  .btn-secondary,
  .btn-primary {
    width: 100%;
    justify-content: center;
  }
}
</style>
