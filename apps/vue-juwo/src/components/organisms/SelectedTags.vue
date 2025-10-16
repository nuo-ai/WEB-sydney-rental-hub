<script setup lang="ts">
/*
  文件职责：展示“已选区域”的标签列表，支持单个移除
  为什么：位置筛选需直观展示所选条目，并允许快速撤销单个选择
  技术权衡：
  - 组件本身不持久化状态，仅通过事件让父组件更新 v-model
  - 无图标库强依赖，移除符号使用纯文本“×”，保证最小依赖与一致性
*/

const props = withDefaults(defineProps<{
  // 已选条目（地区名称）
  selected: string[]
  // 当没有选择时是否隐藏组件（默认隐藏以节省空间）
  hideWhenEmpty?: boolean
}>(), {
  selected: () => [],
  hideWhenEmpty: true,
})

const emit = defineEmits<{
  (e: 'remove', name: string): void
}>()

function onRemove(name: string) {
  emit('remove', name)
}
</script>

<template>
  <div
    v-if="!hideWhenEmpty || (selected && selected.length > 0)"
    class="px-4 py-2 border-b border-gray-100"
  >
    <div class="flex flex-wrap gap-2">
      <span
        v-for="name in selected"
        :key="name"
        class="inline-flex items-center rounded-md bg-teal-50 text-teal-700 border border-teal-200 px-2 py-1 text-sm"
      >
        <span class="truncate max-w-[10rem]">{{ name }}</span>
        <button
          type="button"
          class="ml-1 -mr-0.5 inline-flex h-5 w-5 items-center justify-center rounded hover:bg-teal-100 text-teal-700"
          aria-label="移除已选项"
          @click="onRemove(name)"
        >
          ×
        </button>
      </span>
    </div>
  </div>
</template>
