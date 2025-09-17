<template>
  <!-- 通知铃铛图标（由提供的 SVG 转为组件） -->
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
      d="M10.268 21C10.4435 21.304 10.696 21.5565 11 21.732C11.3041 21.9075 11.6489 21.9999 12 21.9999C12.3511 21.9999 12.6959 21.9075 13 21.732C13.304 21.5565 13.5565 21.304 13.732 21M3.262 15.326C3.13137 15.4692 3.04516 15.6472 3.01386 15.8385C2.98256 16.0298 3.00752 16.226 3.08571 16.4034C3.1639 16.5807 3.29194 16.7316 3.45426 16.8375C3.61658 16.9434 3.80618 16.9999 4 17H20C20.1938 17.0001 20.3834 16.9438 20.5459 16.8381C20.7083 16.7324 20.8365 16.5817 20.9149 16.4045C20.9933 16.2273 21.0185 16.0311 20.9874 15.8398C20.9564 15.6485 20.8704 15.4703 20.74 15.327C19.41 13.956 18 12.499 18 8C18 6.4087 17.3679 4.88258 16.2426 3.75736C15.1174 2.63214 13.5913 2 12 2C10.4087 2 8.88258 2.63214 7.75736 3.75736C6.63214 4.88258 6 6.4087 6 8C6 12.499 4.589 13.956 3.262 15.326Z"
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
