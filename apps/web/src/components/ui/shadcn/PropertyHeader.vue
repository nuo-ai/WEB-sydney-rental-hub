<script setup lang="ts">
import { BedDouble, Bath, Car } from 'lucide-vue-next';

defineProps({
  address: String,
  price: String,
  bedrooms: Number,
  bathrooms: Number,
  parking: Number,
});
</script>

<template>
  <div>
    <h1 class="text-3xl font-bold tracking-tight">{{ address }}</h1>
    <div class="mt-2 flex items-center justify-between">
      <p class="text-2xl font-semibold">{{ price }}</p>
      <div class="flex items-center space-x-4 text-muted-foreground">
        <div class="flex items-center">
          <BedDouble class="mr-2 h-5 w-5" />
          <span>{{ bedrooms }}</span>
        </div>
        <div class="flex items-center">
          <Bath class="mr-2 h-5 w-5" />
          <span>{{ bathrooms }}</span>
        </div>
        <div class="flex items-center">
          <Car class="mr-2 h-5 w-5" />
          <span>{{ parking }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
