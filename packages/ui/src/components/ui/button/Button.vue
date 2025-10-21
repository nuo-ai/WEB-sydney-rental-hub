<script setup lang="ts">
import type { HTMLAttributes } from "vue"
import { cn } from "../../../lib/utils"
import { buttonVariants } from "."

/**
 * 说明：
 * - 移除对 reka-ui Primitive 的依赖，避免跨框架/外部原语绑定
 * - 保留 variant/size/class API 与外观一致性
 * - 提供 `as` 支持以兼容自定义根元素（默认 button）
 * - `asChild` 作为兼容字段保留但不生效（目前项目未使用）
 */
interface Props {
  variant?: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link"
  size?: "default" | "sm" | "lg" | "icon" | "icon-sm" | "icon-lg"
  as?: string | object
  asChild?: boolean
  class?: HTMLAttributes["class"]
}

const props = withDefaults(defineProps<Props>(), {
  variant: "default",
  size: "default",
  as: "button",
  asChild: false,
})
</script>

<template>
  <component
    :is="as"
    data-slot="button"
    :class="cn(buttonVariants({ variant, size }), props.class)"
    v-bind="$attrs"
  >
    <slot />
  </component>
</template>
