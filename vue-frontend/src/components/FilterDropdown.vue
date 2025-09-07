<template>
  <teleport to="body">
    <transition name="dropdown-fade">
      <div v-if="isOpen" class="filter-dropdown-overlay" @click.self="closeDropdown">
        <div
          ref="dropdownRef"
          class="filter-dropdown-container"
          :style="positionStyle"
          @click.stop
          tabindex="-1"
        >
          <div class="filter-dropdown-content">
            <slot></slot>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'

// 中文注释：下拉面板通用容器，支持定位计算、遮罩层和动画过渡
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  trigger: {
    type: Object,
    default: null,
  },
  offset: {
    type: Object,
    default: () => ({ x: 0, y: 8 }),
  },
  width: {
    type: String,
    default: null, // 如果不设置，则至少与触发元素同宽
  },
  position: {
    type: String,
    default: 'bottom-start', // bottom-start, bottom-center, bottom-end
  },
  closeOnEsc: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['update:modelValue', 'close'])

const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
})

const dropdownRef = ref(null)
const positionStyle = ref({})

// 中文注释：计算下拉面板的位置，确保正确对齐在触发元素下方
const calculatePosition = () => {
  if (!props.trigger?.value) return { top: '0px', left: '0px' }

  const rect = props.trigger.value.getBoundingClientRect()
  const viewportHeight = window.innerHeight
  const viewportWidth = window.innerWidth

  let left = rect.left + (props.offset?.x || 0)
  let width = props.width || `${Math.max(rect.width, 280)}px` // 至少280px或与触发元素同宽

  // 中文注释：根据position属性计算水平位置
  if (props.position === 'bottom-center') {
    left = rect.left + (rect.width / 2) - (parseInt(width) / 2)
  } else if (props.position === 'bottom-end') {
    left = rect.right - parseInt(width) - (props.offset?.x || 0)
  }

  // 中文注释：确保不超出视口左右边界
  if (left + parseInt(width) > viewportWidth) {
    left = viewportWidth - parseInt(width) - 10 // 右边留10px边距
  }
  if (left < 10) {
    left = 10 // 左边留10px边距
  }

  let top = rect.bottom + (props.offset?.y || 8)
  const dropdownHeight = dropdownRef.value?.offsetHeight || 300 // 预估高度

  // 中文注释：如果下拉面板底部超出视口，尝试向上显示
  if (top + dropdownHeight > viewportHeight) {
    // 向上显示的空间是否足够
    if (rect.top > dropdownHeight) {
      top = rect.top - dropdownHeight - (props.offset?.y || 8)
    } else {
      // 如果上下都不够，就固定在底部并允许内部滚动
      top = viewportHeight - dropdownHeight - 10 // 底部留10px边距
    }
  }

  return {
    top: `${top}px`,
    left: `${left}px`,
    width: width,
  }
}

// 中文注释：更新下拉面板位置
const updatePosition = () => {
  nextTick(() => {
    positionStyle.value = calculatePosition()
  })
}

// 中文注释：关闭下拉面板
const closeDropdown = () => {
  isOpen.value = false
  emit('close')
}

// 中文注释：处理ESC键关闭
const handleKeyDown = (e) => {
  if (props.closeOnEsc && e.key === 'Escape' && isOpen.value) {
    closeDropdown()
  }
}

// 中文注释：处理窗口大小变化
const handleResize = () => {
  if (isOpen.value) {
    updatePosition()
  }
}

// 监听面板打开状态
watch(() => isOpen.value, (newVal) => {
  if (newVal) {
    updatePosition()
    nextTick(() => {
      // 中文注释：面板打开时，将焦点移至面板以支持键盘访问
      dropdownRef.value?.focus?.()
    })
  }
})

// 中文注释：监听触发元素变化或窗口滚动，更新位置
watch(() => props.trigger, () => {
  if (isOpen.value) {
    updatePosition()
  }
}, { deep: true })

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown)
  window.addEventListener('resize', handleResize)
  window.addEventListener('scroll', handleResize, true)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
  window.removeEventListener('resize', handleResize)
  window.removeEventListener('scroll', handleResize, true)
})
</script>

<style scoped>
.filter-dropdown-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  background: transparent;
  pointer-events: auto;
}

.filter-dropdown-container {
  position: fixed;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1001;
  max-height: calc(100vh - 40px);
  max-width: calc(100vw - 20px);
  overflow: hidden;
  outline: none; /* 移除焦点轮廓 */
}

.filter-dropdown-content {
  max-height: inherit;
  overflow-y: auto;
  overscroll-behavior: contain; /* 防止滚动穿透 */
}

/* 中文注释：过渡动画 */
.dropdown-fade-enter-active,
.dropdown-fade-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}

.dropdown-fade-enter-from,
.dropdown-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
