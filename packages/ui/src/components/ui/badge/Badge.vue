<script setup lang="ts">
import type { HTMLAttributes } from "vue"
import type { BadgeVariants } from "./index"
import { cn } from "../../../lib/utils"
import { badgeVariants } from "."

/**
 * 说明：
 * - 去除对 reka-ui Primitive 与类型依赖，避免跨框架/外部原语绑定
 * - 保留 variant/class API 与外观一致性
 * - 使用原生元素并透传 $attrs，兼容现有用法
 */
interface Props {
  variant?: BadgeVariants["variant"]
  class?: HTMLAttributes["class"]
}

const props = defineProps<Props>()
</script>

<template>
  <span
    data-slot="badge"
    :class="cn(badgeVariants({ variant }), props.class)"
    v-bind="$attrs"
  >
    <slot />
  </span>
</template>
