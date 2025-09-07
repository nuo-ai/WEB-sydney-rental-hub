<template>
  <!-- 筛选/排序图标（由提供的 SVG 转为组件） -->
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    :aria-label="ariaLabel || undefined"
    :role="ariaLabel ? 'img' : undefined"
    :aria-hidden="ariaLabel ? 'false' : 'true'"
    class="spec-icon"
  >
    <!-- 统一 stroke: currentColor，便于跟随文本色及主题令牌 -->
    <path
      d="M9.99988 20C9.9998 20.1858 10.0515 20.368 10.1492 20.5261C10.2469 20.6842 10.3867 20.8119 10.5529 20.895L12.5529 21.895C12.7054 21.9712 12.8748 22.0072 13.0451 21.9994C13.2154 21.9917 13.3809 21.9406 13.5259 21.8509C13.6709 21.7613 13.7905 21.636 13.8735 21.4871C13.9565 21.3381 14 21.1705 13.9999 21V14C14.0001 13.5044 14.1843 13.0265 14.5169 12.659L21.7399 4.67C21.8693 4.52656 21.9545 4.34868 21.985 4.15788C22.0155 3.96708 21.9901 3.77153 21.9118 3.59487C21.8335 3.41822 21.7057 3.26802 21.5439 3.16245C21.3821 3.05688 21.1931 3.00046 20.9999 3H2.99988C2.80649 3.00007 2.61727 3.05622 2.45513 3.16164C2.293 3.26706 2.16491 3.41723 2.08639 3.59396C2.00786 3.7707 1.98227 3.96641 2.01271 4.15739C2.04315 4.34837 2.12831 4.52643 2.25788 4.67L9.48288 12.659C9.81542 13.0265 9.99966 13.5044 9.99988 14V20Z"
      :stroke="color"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    />
  </svg>
</template>

<script setup>
// 中文注释（为什么）：将原生 SVG 组件化，统一 stroke: currentColor，可配置 size/color/ariaLabel，便于全站复用与主题对齐
defineProps({
  // 支持数字或字符串，数字会作为像素使用
  size: { type: [Number, String], default: 24 },
  // 颜色默认继承 currentColor，随文本色而变
  color: { type: String, default: 'currentColor' },
  // 可选无障碍标签；缺省时 aria-hidden
  ariaLabel: { type: String, default: '' },
})
</script>

<style scoped>
/* 统一规格：通过 .spec-icon 约定默认行为，可被外层覆盖尺寸与颜色 */
.spec-icon {
  display: inline-block;
  vertical-align: middle;
}
</style>
