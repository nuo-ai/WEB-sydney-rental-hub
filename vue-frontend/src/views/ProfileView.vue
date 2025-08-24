<template>
  <div class="profile-container">
    <main class="main-content">
      <div class="container">
        <h1>我的账户</h1>
        <el-tabs v-model="activeTab">
          <el-tab-pane label="我的收藏" name="favorites">
            <div v-if="favoriteProperties.length">
              <PropertyCard v-for="prop in favoriteProperties" :key="prop.listing_id" :property="prop" />
            </div>
            <el-empty v-else description="你还没有收藏任何房源"></el-empty>
          </el-tab-pane>
          <el-tab-pane label="浏览历史" name="history">
            <div v-if="historyProperties.length">
              <PropertyCard v-for="prop in historyProperties" :key="prop.listing_id" :property="prop" />
            </div>
            <el-empty v-else description="你还没有浏览任何房源"></el-empty>
          </el-tab-pane>
        </el-tabs>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { usePropertiesStore } from '@/stores/properties'
import PropertyCard from '@/components/PropertyCard.vue'

const propertiesStore = usePropertiesStore()
const activeTab = ref('favorites')

const favoriteProperties = computed(() => propertiesStore.favoriteProperties)

const historyProperties = computed(() => {
  return propertiesStore.viewHistory.map(id => {
    return propertiesStore.allProperties.find(p => String(p.listing_id) === id)
  }).filter(p => p) //
})
</script>

<style scoped>
.profile-container {
  padding-top: 64px;
}
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}
</style>
