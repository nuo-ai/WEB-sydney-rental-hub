<script setup lang="ts">
import { inject, computed } from 'vue'

const props = defineProps<{
  value: string
}>()

// 从 Tabs 根组件注入当前值
const current = inject<any>('tabs.value', null)
const active = computed(() => (current?.value ?? undefined) === props.value)
</script>

<template>
  <div
    v-show="active"
    role="tabpanel"
    :data-state="active ? 'active' : 'inactive'"
    class="outline-none"
  >
    <slot />
  </div>
</template>
