<template>
  <div class="compare-toolbar" v-if="compareItems.length > 0">
    <div class="compare-items">
      <div v-for="item in compareItems" :key="item.listing_id" class="compare-item">
        <span>{{ item.address }}</span>
        <el-button size="small" circle :icon="Close" @click="removeFromCompare(item.listing_id)" />
      </div>
    </div>
    <el-button type="primary" @click="goToCompare" :disabled="compareItems.length < 2">
      对比 ({{ compareItems.length }})
    </el-button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'
import { Close } from '@element-plus/icons-vue'

const propertiesStore = usePropertiesStore()
const router = useRouter()

const compareItems = computed(() => {
  return propertiesStore.allProperties.filter((p) =>
    propertiesStore.compareIds.includes(p.listing_id),
  )
})

const removeFromCompare = (id) => {
  propertiesStore.toggleCompare(id)
}

const goToCompare = () => {
  router.push('/compare')
}
</script>

<style scoped>
.compare-toolbar {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: #333;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  z-index: 1001;
}
.compare-items {
  display: flex;
  gap: 10px;
}
.compare-item {
  background: #555;
  padding: 5px 10px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 5px;
}
</style>
