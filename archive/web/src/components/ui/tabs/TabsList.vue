<script setup lang="ts">
import { useSlots } from 'vue'
</script>

<template>
  <div
    role="tablist"
    class="inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground"
  >
    <slot />
  </div>
</template>
