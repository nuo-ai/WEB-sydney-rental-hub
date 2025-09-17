<template>
  <div class="compare-container">
    <h1>房源对比</h1>
    <div class="compare-grid">
      <div v-for="item in compareItems" :key="item.listing_id" class="compare-column">
        <PropertyCard :property="item" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { usePropertiesStore } from '@/stores/properties'
import PropertyCard from '@/components/PropertyCard.vue'

const propertiesStore = usePropertiesStore()

const compareItems = computed(() => {
  return propertiesStore.allProperties.filter((p) =>
    propertiesStore.compareIds.includes(p.listing_id),
  )
})
</script>

<style scoped>
.compare-container {
  padding-top: 64px;
  padding-left: 24px;
  padding-right: 24px;
}

.compare-grid {
  display: flex;
  gap: 20px;
  justify-content: center;
}
</style>
