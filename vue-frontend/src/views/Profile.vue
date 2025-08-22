<template>
  <div class="profile-container">
    <main class="main-content">
      <div class="container">
        <header class="page-header">
          <h1 class="page-title chinese-text">我的</h1>
          <p class="page-subtitle chinese-text">个人中心和账户设置</p>
        </header>

        <div class="profile-content">
          <div class="placeholder-content">
            <el-icon :size="64" color="#d9d9d9">
              <User />
            </el-icon>
            <h3 class="chinese-text">用户系统开发中</h3>
            <p class="chinese-text">即将提供用户登录、个人设置等功能</p>
            
            <!-- 临时收藏统计 -->
            <div class="stats-card">
              <h4 class="chinese-text">当前收藏</h4>
              <p class="stats-number">{{ favoriteCount }}</p>
              <p class="chinese-text">套房源</p>
              <el-button type="primary" @click="goToFavorites">
                查看收藏
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'
import { User } from '@element-plus/icons-vue'

const router = useRouter()
const propertiesStore = usePropertiesStore()

const favoriteCount = computed(() => {
  return propertiesStore.favoriteProperties.length
})

const goToFavorites = () => {
  router.push('/favorites')
}
</script>

<style scoped>
.profile-container {
  min-height: 100vh;
  background-color: var(--color-bg-page);
}

.main-content {
  width: 100%;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px 16px;
}

.page-header {
  margin-bottom: 32px;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 8px;
}

.page-subtitle {
  font-size: 18px;
  color: var(--color-text-secondary);
}

.profile-content {
  background: white;
  padding: 40px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-content {
  text-align: center;
  max-width: 400px;
}

.placeholder-content h3 {
  font-size: 20px;
  color: var(--color-text-primary);
  margin: 16px 0 8px 0;
}

.placeholder-content p {
  font-size: 16px;
  color: var(--color-text-secondary);
  margin-bottom: 24px;
}

.stats-card {
  background: var(--juwo-primary-50);
  border: 2px solid var(--juwo-primary-100);
  border-radius: var(--radius-lg);
  padding: 24px;
  margin-top: 32px;
}

.stats-card h4 {
  font-size: 16px;
  color: var(--color-text-primary);
  margin: 0 0 8px 0;
}

.stats-number {
  font-size: 36px;
  font-weight: 700;
  color: var(--juwo-primary);
  margin: 8px 0;
}

.stats-card p {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0 0 16px 0;
}
</style>
