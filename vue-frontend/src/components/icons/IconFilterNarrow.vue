<template>
  <!-- 使用用户提供的更窄筛选图标；颜色随父元素 currentColor；不会撑开布局 -->
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    aria-hidden="true"
  >
    <path
      d="M14 17H5M14 17C14 18.6569 15.3431 20 17 20C18.6569 20 20 18.6569 20 17C20 15.3431 18.6569 14 17 14C15.3431 14 14 15.3431 14 17ZM19 7H10M10 7C10 8.65685 8.65685 10 7 10C5.34315 10 4 8.65685 4 7C4 5.34315 5.34315 4 7 4C8.65685 4 10 5.34315 10 7Z"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    />
  </svg>
</template>

<script setup>
// 中文注释：采用提供的 SVG，尺寸通过 props 控制；默认 18，更利于与文字并排
const { size } = defineProps({
  size: {
    type: [Number, String],
    default: 18,
  },
})
</script>
