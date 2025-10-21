<script setup lang="ts">
import { inject, computed } from "vue"
import type { HTMLAttributes } from "vue"
import { cn } from "../../../lib/utils"

/**
 * 纯 Vue TabsContent，实现展示/隐藏逻辑，避免引入 reka-ui。
 * - 属性：
 *   - value：当前面板对应的值（与 TabsTrigger 的 value 一致）
 *   - forceMount：是否强制挂载（true 时使用 v-show，仅隐藏不卸载；默认 false 使用 v-if）
 *   - class：自定义类名（通过 cn 合并）
 * - 可视状态：
 *   - data-state="active|inactive" 用于 Tailwind data 选择器样式控制
 *   - role="tabpanel" 语义化，配合 a11y
 */
const props = withDefaults(defineProps<{
  value: string
  forceMount?: boolean
  class?: HTMLAttributes["class"]
}>(), {
  forceMount: false,
})

const ctx = inject<{
  valueRef: { value: string | null }
}>("srh-tabs-ctx")

if (!ctx) {
  throw new Error("[TabsContent] must be used inside <Tabs> root")
}

const isActive = computed(() => ctx.valueRef.value === props.value)
</script>

<template>
  <!-- 强制挂载：不卸载，只切换可见性 -->
  <template v-if="props.forceMount">
    <div
      role="tabpanel"
      :data-state="isActive ? 'active' : 'inactive'"
      :hidden="!isActive"
      v-show="isActive"
      :class="cn(props.class)"
    >
      <slot />
    </div>
  </template>

  <!-- 默认：未激活时直接卸载节点 -->
  <template v-else>
    <div
      v-if="isActive"
      role="tabpanel"
      data-state="active"
      :class="cn(props.class)"
    >
      <slot />
    </div>
  </template>
</template>
