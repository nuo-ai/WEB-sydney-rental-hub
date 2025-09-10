<template>
  <el-dialog
    v-model="visible"
    fullscreen
    :show-close="false"
    class="name-location-modal"
    :append-to-body="true"
  >
    <template #header>
      <div class="modal-header">
        <button class="back-btn" @click="handleBack">
          <ArrowLeft class="spec-icon" />
        </button>
        <h2 class="modal-title typo-heading-card">{{ $t('nameLocation.title') }}</h2>
        <button class="skip-btn typo-button" @click="handleSkip">
          {{ $t('nameLocation.skip') }}
        </button>
      </div>
    </template>

    <div class="modal-content">
      <!-- 选中的地址 -->
      <div class="selected-address">
        <MapPin class="selected-icon spec-icon" />
        <p class="typo-body">{{ displayAddress }}</p>
      </div>

      <!-- 标签选择 -->
      <div class="label-options">
        <label v-for="option in labelOptions" :key="option.value" class="label-option">
          <input type="radio" v-model="selectedLabel" :value="option.value" name="location-label" />
          <span class="radio-circle"></span>
          <span class="label-text">{{ option.label }}</span>
          <GraduationCap v-if="option.value === '学校'" class="label-icon spec-icon" />
          <MapPin v-else class="label-icon spec-icon" />
        </label>
      </div>

      <!-- 确认按钮 -->
      <div class="action-section">
        <el-button
          type="danger"
          size="large"
          @click="handleConfirm"
          :disabled="!selectedLabel"
          class="confirm-btn typo-button"
        >
          {{ $t('nameLocation.confirm') }}
        </el-button>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ArrowLeft, MapPin, GraduationCap } from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  address: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['update:modelValue', 'confirm', 'skip', 'back'])

// 响应式状态
const visible = ref(props.modelValue)
const selectedLabel = ref('学校')

// 标签选项
const labelOptions = [
  {
    value: '学校',
    label: '学校',
    icon: 'fas fa-graduation-cap',
  },
  {
    value: '其他',
    label: '其他',
    icon: 'fas fa-map-pin',
  },
]

// 计算属性
const displayAddress = computed(() => {
  if (!props.address) return ''
  return props.address.formatted_address || props.address.name || ''
})

// 监听props变化
watch(
  () => props.modelValue,
  (newVal) => {
    visible.value = newVal
    if (newVal) {
      // 重置选择（默认选“学校”）
      selectedLabel.value = '学校'
    }
  },
)

// 监听visible变化
watch(visible, (newVal) => {
  emit('update:modelValue', newVal)
})

// 方法
const handleBack = () => {
  // 返回按钮被点击
  visible.value = false
  emit('update:modelValue', false)
  // 触发back事件，让父组件决定如何处理
  emit('back')
}

const handleSkip = () => {
  // 跳过按钮被点击
  // Skip时默认使用“其他”标签
  const data = {
    address: props.address,
    label: '其他',
  }
  emit('skip', data)
  emit('confirm', data) // 也触发confirm事件
  visible.value = false
  emit('update:modelValue', false)
}

const handleConfirm = () => {
  if (!selectedLabel.value) return

  // 确认按钮被点击
  emit('confirm', {
    address: props.address,
    label: selectedLabel.value,
  })

  visible.value = false
  emit('update:modelValue', false)
}
</script>

<style scoped>
.name-location-modal :deep(.el-dialog__header) {
  padding: 0;
  margin: 0;
}

.name-location-modal :deep(.el-dialog__body) {
  padding: 0;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 顶部导航 */
.modal-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--color-bg-card);
  padding: 20px;
  border-bottom: 1px solid var(--color-border-default);
  display: flex;
  align-items: center;
  position: relative;
}

.back-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: none;
  color: var(--color-text-primary);
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s;
}

.back-btn:hover {
  background: var(--bg-hover);
}

.modal-title {
  flex: 1;
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
  text-align: center;
  padding: 0 60px;
}

.skip-btn {
  position: absolute;
  right: 20px;
  background: none;
  border: none;
  color: var(--juwo-primary);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  padding: 8px;
}

.skip-btn:hover {
  text-decoration: underline;
}

/* 内容区域 */
.modal-content {
  flex: 1;
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
}

/* 选中的地址 */
.selected-address {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: var(--surface-2);
  border-radius: 8px;
  margin-bottom: 32px;
}

.selected-address .selected-icon {
  flex-shrink: 0;
  color: var(--color-text-secondary);
  width: 16px;
  height: 16px;
  margin-top: 2px;
}

.selected-address p {
  flex: 1;
  margin: 0;
  font-size: 15px;
  color: var(--color-text-primary);
  line-height: 1.5;
}

/* 标签选项 */
.label-options {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.label-option {
  display: flex;
  align-items: center;
  padding: 16px;
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-default);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.label-option:hover {
  border-color: var(--color-border-strong);
  background: var(--bg-hover);
}

.label-option input[type='radio'] {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.radio-circle {
  width: 20px;
  height: 20px;
  border: 2px solid var(--color-border-default);
  border-radius: 50%;
  margin-right: 12px;
  position: relative;
  transition: all 0.2s;
}

.radio-circle::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--juwo-primary);
  transform: translate(-50%, -50%) scale(0);
  transition: transform 0.2s;
}

.label-option input:checked ~ .radio-circle {
  border-color: var(--juwo-primary);
}

.label-option input:checked ~ .radio-circle::after {
  transform: translate(-50%, -50%) scale(1);
}

.label-option input:checked ~ .label-text {
  font-weight: 600;
  color: var(--juwo-primary);
}

.label-text {
  flex: 1;
  font-size: 16px;
  color: var(--color-text-primary);
  transition: all 0.2s;
}

.label-icon {
  color: var(--text-muted);
  font-size: 18px;
  transition: color 0.2s;
}

.label-option input:checked ~ .label-icon {
  color: var(--juwo-primary);
}

/* 操作区域 */
.action-section {
  margin-top: auto;
  padding-top: 24px;
}

.confirm-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  background: var(--juwo-primary) !important;
  border-color: var(--juwo-primary) !important;
}

.confirm-btn:hover:not(:disabled) {
  background: var(--juwo-primary-dark) !important;
  border-color: var(--juwo-primary-dark) !important;
}

.confirm-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .modal-content {
    padding: 20px 16px;
  }

  .modal-header {
    padding: 16px;
  }

  .modal-title {
    font-size: 18px;
  }
}
</style>
