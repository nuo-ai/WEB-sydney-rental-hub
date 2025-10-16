<script setup lang="ts">
/*
  文件职责：位置筛选右侧 A-Z 索引条，点击字母后向父级发出 jump 事件
  为什么：与左侧分组面板解耦，父级掌控滚动容器与锚点，组件保持“无滚动副作用”
  技术权衡：
  - 使用 button 元素保证可访问性（可通过键盘聚焦/激活）
  - 体积小、无状态，仅接收 letters 并 emit('jump', letter)
*/

const props = withDefaults(defineProps<{
  letters: string[]
}>(), {
  // 默认 A-Z
  letters: () => Array.from({ length: 26 }, (_, i) => String.fromCharCode(65 + i)),
})

const emit = defineEmits<{
  (e: 'jump', letter: string): void
}>()

function onJump(letter: string) {
  emit('jump', letter)
}
</script>

<template>
  <nav
    aria-label="Alphabetical index"
    class="select-none"
  >
    <ul class="flex flex-col items-center gap-1 py-2 px-1">
      <li v-for="letter in letters" :key="letter">
        <button
          type="button"
          class="h-5 w-5 text-[11px] leading-5 text-gray-500 hover:text-gray-800 active:text-teal-600
                 rounded focus:outline-none focus-visible:ring-2 focus-visible:ring-teal-500"
          @click="onJump(letter)"
          :aria-label="`跳转到 ${letter} 区`"
        >
          {{ letter }}
        </button>
      </li>
    </ul>
  </nav>
</template>
