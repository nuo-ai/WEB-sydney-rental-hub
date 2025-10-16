<script setup lang="ts">
/*
  文件职责：渲染位置筛选的“热门区域 + 按字母分组”的左侧列表内容
  为什么：将纯展示与选中态切换与右侧索引/弹层容器解耦，便于复用与测试
  技术权衡：
  - 无滚动副作用：不直接操作滚动，仅负责渲染与触发选中
  - 选中态通过 v-model (update:modelValue) 与父级同步，保持单一数据源
*/

const props = withDefaults(defineProps<{
  // A-Z 分组（key 为大写字母或 '#'）
  groups: Record<string, string[]>
  // 热门区域列表
  hot: string[]
  // 已选区域（v-model）
  modelValue: string[]
}>(), {
  groups: () => ({}),
  hot: () => [],
  modelValue: () => [],
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string[]): void
}>()

function isSelected(name: string) {
  return props.modelValue?.includes(name)
}

function toggle(name: string) {
  const set = new Set(props.modelValue || [])
  if (set.has(name)) set.delete(name)
  else set.add(name)
  emit('update:modelValue', Array.from(set))
}

// 分组标题 id，用于右侧 AlphabetIndex 的锚点跳转（与 demo.html 对齐：district-group-A）
function groupAnchorId(letter: string) {
  return `district-group-${letter}`
}
</script>

<template>
  <div class="space-y-4">
    <!-- 热门区域 -->
    <section v-if="hot.length" class="pt-2">
      <h3 class="px-4 pb-2 text-sm text-gray-500">热门区域</h3>
      <div class="px-4 flex flex-wrap gap-2">
        <button
          v-for="name in hot"
          :key="name"
          type="button"
          :data-district-name="name"
          @click="toggle(name)"
          class="rounded-md border px-3 py-1.5 text-sm transition-colors"
          :class="isSelected(name)
            ? 'bg-teal-50 text-teal-600 border-teal-200'
            : 'bg-gray-50 text-gray-700 border-gray-200 hover:bg-gray-100'"
        >
          {{ name }}
        </button>
      </div>
    </section>

    <!-- 按字母分组列表 -->
    <section v-for="letter in Object.keys(groups).sort()" :key="letter">
      <h4
        class="px-4 py-2 text-base font-medium text-gray-900 bg-white sticky top-0"
        :id="groupAnchorId(letter)"
      >
        {{ letter }}
      </h4>
      <ul class="divide-y divide-gray-100">
        <li
          v-for="name in groups[letter]"
          :key="name"
          class="flex items-center justify-between px-4 py-3 cursor-pointer"
          :data-district-name="name"
          @click="toggle(name)"
        >
          <span class="text-gray-900">{{ name }}</span>
          <!-- 选中勾选：不用图标库，使用文本符号，保持轻依赖 -->
          <span
            class="ml-2 inline-flex h-5 w-5 items-center justify-center rounded text-sm"
            :class="isSelected(name) ? 'text-teal-600' : 'text-transparent'"
            aria-hidden="true"
          >
            ✓
          </span>
        </li>
      </ul>
    </section>
  </div>
</template>
