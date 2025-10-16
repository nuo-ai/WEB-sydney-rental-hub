<script setup lang="ts">
/*
  文件职责：单个筛选入口按钮（“位置/排序/筛选”），统一外观与交互
  为什么：三处按钮风格与交互一致，抽象出最小可复用单元，便于后续扩展（如角标/高亮）
  技术权衡：
  - 不直接依赖 shadcn Button，避免样式/尺寸受限；使用原生 button + Tailwind
  - 图标通过插槽传入，避免强绑定图标库（lucide/FontAwesome 可自由对接）
*/

const props = withDefaults(defineProps<{
  label: string
  active?: boolean // 高亮态，用于有选中条件时的视觉提示
}>(), {
  active: false,
})

const emit = defineEmits<{
  (e: 'click'): void
}>()

function onClick() {
  emit('click')
}
</script>

<template>
  <button
    type="button"
    @click="onClick"
    class="inline-flex items-center gap-1.5 rounded-md px-3 py-1.5 text-sm font-medium transition-colors
           border border-transparent
           hover:bg-gray-100 active:bg-gray-200
           data-[active=true]:bg-teal-50 data-[active=true]:text-teal-600 data-[active=true]:border-teal-200"
    :data-active="active ? 'true' : 'false'"
  >
    <!-- 图标插槽（可选） -->
    <slot name="icon" />
    <span>{{ label }}</span>
  </button>
</template>
