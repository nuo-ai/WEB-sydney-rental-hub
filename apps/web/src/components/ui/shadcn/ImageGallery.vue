<script setup lang="ts">
defineProps({
  images: {
    type: Array as () => string[],
    default: () => [],
  },
});
</script>

<template>
  <div class="grid grid-cols-3 grid-rows-2 gap-2 h-[400px]">
    <div class="col-span-2 row-span-2">
      <img
        v-if="images.length > 0"
        :src="images[0]"
        alt="Main property image"
        class="w-full h-full object-cover rounded-lg"
      />
    </div>
    <div v-if="images.length > 1">
      <img
        :src="images[1]"
        alt="Property image thumbnail 1"
        class="w-full h-full object-cover rounded-lg"
      />
    </div>
    <div v-if="images.length > 2">
      <img
        :src="images[2]"
        alt="Property image thumbnail 2"
        class="w-full h-full object-cover rounded-lg"
      />
    </div>
  </div>
</template>
