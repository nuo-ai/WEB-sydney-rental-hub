<template>
  <teleport to="body">
    <div v-show="modelValue" class="bs-overlay" @click.self="close">
      <div
        class="bs-container"
        :style="{ height: heightStyle }"
        role="dialog"
        aria-modal="true"
      >
        <!-- 头部/内容/底部均用插槽，按需组合，与 1.html 结构一致 -->
        <slot name="header" />
        <div class="bs-content">
          <slot />
        </div>
        <slot name="footer" />
      </div>
    </div>
  </teleport>
</template>

<script setup>
/*
  中文说明（对齐 1.html 的“底部弹层 bottom-sheet”）：
  - 全屏半透明遮罩（点击遮罩关闭）
  - 内容容器自底部滑入，圆角 12px，可配置高度百分比（默认 75%）
  - Header / Content / Footer 通过插槽自定义，匹配“标题+清除”“列表内容”“确定”按钮的布局
  - 锁定 body 滚动，Esc 关闭，关闭后恢复
*/
import { computed, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  heightPercent: { type: Number, default: 75 }, // 1.html: 位置 75%，筛选 85% 可自行配置
})
const emit = defineEmits(['update:modelValue'])

const heightStyle = computed(() => Math.min(Math.max(props.heightPercent, 50), 95) + 'dvh')

const close = () => emit('update:modelValue', false)

const lock = () => {
  document.documentElement.style.overflow = 'hidden'
  document.body.style.overflow = 'hidden'
}
const unlock = () => {
  document.documentElement.style.overflow = ''
  document.body.style.overflow = ''
}

const onKey = (e) => {
  if (e.key === 'Escape' && props.modelValue) close()
}

onMounted(() => {
  window.addEventListener('keydown', onKey)
})
onUnmounted(() => {
  window.removeEventListener('keydown', onKey)
  unlock()
})

// 打开时锁滚，关闭恢复（对齐 1.html 行为）
watch(
  () => props.modelValue,
  (val) => {
    if (val) lock()
    else unlock()
  },
  { immediate: true },
)
</script>

<style scoped>
.bs-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 1000;
  display: flex;
  align-items: flex-end;
  animation: overlay-in 0.2s ease;
}
@keyframes overlay-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

.bs-container {
  width: 100%;
  background: var(--color-bg-card);
  border-top-left-radius: var(--radius-lg, 12px);
  border-top-right-radius: var(--radius-lg, 12px);
  box-shadow: var(--shadow-md, 0 -5px 15px rgba(0,0,0,0.1));
  transform: translateY(0);
  display: flex;
  flex-direction: column;
  max-height: 95dvh;
  animation: sheet-in 0.24s ease-out;
}
@keyframes sheet-in {
  from { transform: translateY(100%); }
  to { transform: translateY(0%); }
}

.bs-content {
  flex: 1 1 auto;
  overflow: auto;
  -webkit-overflow-scrolling: touch;
  padding: 0; /* 由内部面板自己控制 */
}
</style>
