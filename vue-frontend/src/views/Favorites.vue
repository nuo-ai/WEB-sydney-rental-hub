<template>
  <div class="favorites-container">
    <main class="main-content">
      <div class="container">
        <!-- 页面标题 -->
        <header class="page-header">
          <h1 class="page-title chinese-text">我的收藏</h1>
          <p class="page-subtitle chinese-text">您收藏的房源列表</p>
        </header>

        <!-- 收藏房源列表 -->
        <div class="favorites-section">
          <!-- 空状态 -->
          <div v-if="favoriteProperties.length === 0" class="empty-state">
            <el-icon :size="64" color="#d9d9d9">
              <Star />
            </el-icon>
            <h3 class="chinese-text">还没有收藏的房源</h3>
            <p class="chinese-text">浏览房源时点击收藏按钮，将喜欢的房源保存在这里</p>
            <el-button type="primary" @click="goToHome"> 去看房源 </el-button>
          </div>

          <!-- 收藏房源网格 -->
          <div v-else class="properties-grid">
            <PropertyCard
              v-for="property in favoriteProperties"
              :key="property.listing_id"
              :property="property"
              @click="goToPropertyDetail"
              @contact="handleContactProperty"
            />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
defineOptions({ name: 'FavoritesView' })
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { usePropertiesStore } from '@/stores/properties'
import PropertyCard from '@/components/PropertyCard.vue'
import { Star } from '@element-plus/icons-vue'

// 路由
const router = useRouter()

// 状态管理
const propertiesStore = usePropertiesStore()

// 页面加载时获取收藏的房源数据
onMounted(async () => {
  await propertiesStore.fetchFavoriteProperties()
})

// 计算属性
const favoriteProperties = computed(() => {
  return propertiesStore.favoriteProperties
})

// 方法
const goToHome = () => {
  router.push('/')
}

const goToPropertyDetail = (property) => {
  router.push({ name: 'PropertyDetail', params: { id: property.listing_id } })
}

const handleContactProperty = (property) => {
  ElMessage.success(`正在为您联系关于 ${property.address} 的房源信息`)
}
</script>

<style scoped>
/* 收藏页面容器 */
.favorites-container {
  min-height: 100vh;
  background-color: var(--color-bg-page);
}

/* 主内容区域 */
.main-content {
  width: 100%;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px 16px;
}

@media (width >= 768px) {
  .container {
    padding: 32px 24px;
  }
}

@media (width >= 1024px) {
  .container {
    padding: 40px 32px;
  }
}

/* 页面标题 */
.page-header {
  margin-bottom: 32px;
  text-align: left;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 8px;
  line-height: 1.2;
}

.page-subtitle {
  font-size: 18px;
  color: var(--color-text-secondary);
  line-height: 1.4;
}

/* 收藏列表区域 */
.favorites-section {
  min-height: 400px;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  gap: 16px;
  text-align: center;
}

.empty-state h3 {
  font-size: 20px;
  color: var(--color-text-primary);
  margin: 0;
}

.empty-state p {
  font-size: 16px;
  color: var(--color-text-secondary);
  margin: 0;
  max-width: 400px;
}

/* 房源网格 */
.properties-grid {
  display: grid;
  gap: 24px;
  justify-items: center;
}

/* 移动端 - 单列布局 */
@media (width <= 767px) {
  .properties-grid {
    grid-template-columns: 1fr;
  }
}

/* 平板端 - 双列布局 */
@media (width >= 768px) and (width <= 1199px) {
  .properties-grid {
    grid-template-columns: repeat(2, 1fr);
    max-width: 1200px;
    margin: 0 auto;
  }
}

/* 桌面端 - 灵活布局 */
@media (width >= 1200px) {
  .properties-grid {
    grid-template-columns: repeat(auto-fit, minmax(580px, 1fr));
    max-width: 1800px;
    margin: 0 auto;
  }
}
</style>
