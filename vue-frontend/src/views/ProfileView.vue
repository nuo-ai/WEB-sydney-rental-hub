<template>
  <div class="profile-container">
    <main class="main-content">
      <div class="container stack-lg">
        <!-- 标题区：与列表页一致的三段式（此页面包屑简化为单节点） -->
        <div class="title-block">
          <nav class="breadcrumbs">Home › My Center</nav>
          <h1 class="page-h1">My Center</h1>
        </div>

        <!-- 我的收藏 -->
        <section class="section-card stack-md">
          <div class="section-header" style="display:flex;align-items:center;justify-content:space-between;">
            <h2 class="h2">Favorites</h2>
            <span class="text-secondary text-sm">({{ favoriteCount }})</span>
          </div>

          <div v-if="favoriteProperties.length" class="stack-md">
            <PropertyCard
              v-for="prop in favoriteProperties"
              :key="prop.listing_id"
              :property="prop"
            />
          </div>
          <el-empty v-else description="你还没有收藏任何房源"></el-empty>
        </section>

        <!-- 浏览历史 -->
        <section class="section-card stack-md">
          <div class="section-header" style="display:flex;align-items:center;justify-content:space-between;">
            <h2 class="h2">History</h2>
            <span class="text-secondary text-sm">({{ historyCount }})</span>
          </div>

          <div v-if="historyProperties.length" class="stack-md">
            <PropertyCard
              v-for="prop in historyProperties"
              :key="prop.listing_id"
              :property="prop"
            />
          </div>
          <el-empty v-else description="你还没有浏览任何房源"></el-empty>
        </section>
      </div>
    </main>
  </div>
</template>

<script setup>
/* 为什么这样做：
   - 统一“我的中心”视觉：标题区（breadcrumbs+H1）+ 两个 section-card（收藏/历史）
   - 使用全局 utilities（stack-* / h2 / text-*）按 8pt 节奏与 type scale 对齐
   - 数据直接复用 Pinia store，避免重复数据源
*/
import { computed, onMounted } from 'vue'
import { usePropertiesStore } from '@/stores/properties'
import PropertyCard from '@/components/PropertyCard.vue'

const propertiesStore = usePropertiesStore()

// 收藏列表（优先使用 store 内聚合数据）
const favoriteProperties = computed(() => propertiesStore.favoriteProperties)
const favoriteCount = computed(() => favoriteProperties.value.length)

// 历史列表（按最近浏览顺序映射）
const historyProperties = computed(() => {
  return (propertiesStore.viewHistory || [])
    .map((id) => {
      return (
        propertiesStore.filteredProperties.find((p) => String(p.listing_id) === String(id)) ||
        propertiesStore.allProperties.find((p) => String(p.listing_id) === String(id)) ||
        null
      )
    })
    .filter(Boolean)
})
const historyCount = computed(() => historyProperties.value.length)

// 如有收藏但无详情数据时，尝试拉取（防止空白）
onMounted(async () => {
  if (favoriteCount.value > 0 && propertiesStore.favoritePropertiesData.length === 0) {
    try {
      // 有些页面首次没有 allProperties，可容错
      await propertiesStore.fetchFavoriteProperties()
    } catch {
      /* 静默容错：ESLint no-unused-vars */
    }
  }
})
</script>

<style scoped>
.profile-container {
  padding-top: 64px; /* 与全站顶部间距对齐 */
}

/* 标题区对齐 Home 规范（已在全局有 .title-block/.page-h1/.breadcrumbs 基线，这里仅兜底微调） */
.title-block {
  padding-top: 8px;
}
</style>
