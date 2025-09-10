<template>
  <teleport to="body">
    <transition name="dropdown-fade">
      <div v-if="isOpen" class="filter-dropdown-overlay" @click.self="closeDropdown">
        <div
          ref="dropdownRef"
          class="filter-dropdown-container"
          :style="positionStyle"
          role="dialog"
          aria-modal="true"
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
  // 显式传入定位（优先使用），格式：{ top: number|string, left: number|string, width?: number|string }
  explicitPosition: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['update:modelValue', 'close'])

const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
})

const dropdownRef = ref(null)
const positionStyle = ref({})

// 中文注释：记录关闭后要恢复的焦点来源（优先使用触发器，其次使用关闭前的活动元素）
const previousActiveElement = ref(null)
const restoreFocus = () => {
  // 优先将焦点还给触发器，其次是关闭前记录的活动元素
  const triggerEl = props.trigger?.value
  const target =
    triggerEl && typeof triggerEl.focus === 'function'
      ? triggerEl
      : previousActiveElement.value && typeof previousActiveElement.value.focus === 'function'
        ? previousActiveElement.value
        : null
  if (target) {
    // 使用 rAF 确保在 DOM 更新与过渡后再聚焦
    requestAnimationFrame(() => target.focus())
  }
}

// 中文注释：计算下拉面板的位置，确保正确对齐在触发元素下方
const calculatePosition = () => {
  // 中文注释：若提供了显式坐标，则优先使用，避免任何时序问题
  if (
    props.explicitPosition &&
    props.explicitPosition.top != null &&
    props.explicitPosition.left != null
  ) {
    const top =
      typeof props.explicitPosition.top === 'number'
        ? `${props.explicitPosition.top}px`
        : `${props.explicitPosition.top}`
    const left =
      typeof props.explicitPosition.left === 'number'
        ? `${props.explicitPosition.left}px`
        : `${props.explicitPosition.left}`
    const width =
      props.explicitPosition.width != null
        ? typeof props.explicitPosition.width === 'number'
          ? `${props.explicitPosition.width}px`
          : `${props.explicitPosition.width}`
        : props.width ||
          `${Math.max(props.trigger?.value?.getBoundingClientRect?.().width || 0, 280)}px`
    return { top, left, width }
  }
  // 中文注释：触发元素尚未就绪时，保持上一次定位（或空），避免写入 0,0 导致出现在左上角
  if (!props.trigger?.value) return positionStyle.value || {}

  const rect = props.trigger.value.getBoundingClientRect()
  const viewportHeight = window.innerHeight
  const viewportWidth = window.innerWidth

  let left = rect.left + (props.offset?.x || 0)
  let width = props.width || `${Math.max(rect.width, 280)}px` // 至少280px或与触发元素同宽

  // 中文注释：根据position属性计算水平位置
  if (props.position === 'bottom-center') {
    left = rect.left + rect.width / 2 - parseInt(width) / 2
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
    // 中文注释：若提供了显式坐标（explicitPosition），即使 trigger 未就绪也必须计算定位
    const hasExplicit =
      props.explicitPosition &&
      props.explicitPosition.top != null &&
      props.explicitPosition.left != null
    if (!hasExplicit && !props.trigger?.value) return
    positionStyle.value = calculatePosition()
  })
}

// 中文注释：关闭下拉面板
const closeDropdown = () => {
  isOpen.value = false
  emit('close')
  // 中文注释：关闭后还原焦点到触发器（或先前聚焦元素），提升可达性
  restoreFocus()
}

// 中文注释：处理ESC键关闭
const handleKeyDown = (e) => {
  if (!isOpen.value) return
  // 中文注释：ESC 关闭
  if (props.closeOnEsc && e.key === 'Escape') {
    e.stopPropagation()
    closeDropdown()
    return
  }
  // 中文注释：Tab 焦点陷阱，焦点在面板内部循环，不逃逸到页面
  if (e.key === 'Tab') {
    const focusables = getFocusableElements()
    if (focusables.length === 0) {
      // 中文注释：无可聚焦子元素时将焦点停留在容器
      e.preventDefault()
      dropdownRef.value?.focus?.()
      return
    }
    const first = focusables[0]
    const last = focusables[focusables.length - 1]
    const active = document.activeElement
    if (e.shiftKey) {
      if (active === first || active === dropdownRef.value) {
        e.preventDefault()
        last.focus()
      }
    } else {
      if (active === last) {
        e.preventDefault()
        first.focus()
      }
    }
  }
}

// 中文注释：处理窗口大小变化
const handleResize = () => {
  if (isOpen.value) {
    updatePosition()
  }
}

// 中文注释：锁定/恢复 body 滚动，避免出现页面滚动条与面板滚动条并列
const lockBodyScroll = () => {
  document.documentElement.style.overflow = 'hidden'
  document.body.style.overflow = 'hidden'
}
const unlockBodyScroll = () => {
  document.documentElement.style.overflow = ''
  document.body.style.overflow = ''
}

// 中文注释：将焦点移动到面板内首个可交互控件，提升键盘可达性
const focusFirstInteractive = () => {
  const root = dropdownRef.value
  if (!root) return
  // 中文注释：排除 tabindex="-1"（如右上角关闭按钮），避免首焦点落在“关闭”
  const first = root.querySelector(
    'button:not([tabindex="-1"]), [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
  )
  if (first && typeof first.focus === 'function') {
    first.focus()
  } else {
    root.focus?.()
  }
}

// 中文注释：获取面板内可聚焦元素集合（用于焦点陷阱）
const getFocusableElements = () => {
  const root = dropdownRef.value
  if (!root) return []
  // 中文注释：与 focusFirstInteractive 一致，排除 tabindex="-1" 的按钮（如右上角关闭按钮）
  const selector =
    'button:not([tabindex="-1"]), [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  const nodes = Array.from(root.querySelectorAll(selector)).filter(
    (el) => !el.hasAttribute('disabled') && el.getAttribute('aria-hidden') !== 'true',
  )
  return nodes
}

// 中文注释：监听面板打开状态（锁滚 + 焦点首控件 + 定位确认）
watch(
  () => isOpen.value,
  (newVal) => {
    if (newVal) {
      // 中文注释：记录打开前的活动元素，关闭时用于还原焦点
      previousActiveElement.value = document.activeElement
      // 中文注释：首次打开立即计算一次，并锁定 body 滚动
      lockBodyScroll()
      updatePosition()
      nextTick(() => {
        // 中文注释：优先将焦点移至首个交互控件；如果不存在则聚焦容器
        focusFirstInteractive()
        // 中文注释：在布局/赋值可能慢一拍的场景下，追加 1–2 帧 rAF 进行轻量确认重算
        const ensurePosition = (attempt = 0) => {
          if (!positionStyle.value?.top || !positionStyle.value?.left) {
            updatePosition()
          }
          if (attempt < 2) {
            requestAnimationFrame(() => ensurePosition(attempt + 1))
          }
        }
        requestAnimationFrame(() => ensurePosition(0))
      })
    } else {
      // 中文注释：关闭时恢复 body 滚动
      unlockBodyScroll()
    }
  },
)

// 中文注释：监听触发元素变化或窗口滚动，更新位置
watch(
  () => props.trigger?.value,
  (el) => {
    // 中文注释：触发元素一旦就绪即尝试定位，不再依赖 isOpen，先准备好位置
    if (el) {
      updatePosition()
    }
  },
  { immediate: true },
)

// 中文注释：当外部显式坐标变化时，若面板已打开则立即更新
watch(
  () => props.explicitPosition,
  (pos) => {
    if (isOpen.value && pos && pos.top != null && pos.left != null) {
      updatePosition()
    }
  },
  { deep: true },
)

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

onUnmounted(() => {
  // 中文注释：组件卸载时确保恢复页面滚动，并尝试将焦点还原到触发器
  unlockBodyScroll()
  restoreFocus()
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
  transition:
    opacity 0.2s,
    transform 0.2s;
}

.dropdown-fade-enter-from,
.dropdown-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
