<template>
  <div class="property-detail-container">
    <main class="main-content">
      <div class="container">
        <!-- 返回按钮 -->
        <div class="back-navigation">
          <el-button 
            @click="goBack"
            class="back-btn"
            :icon="ArrowLeft"
          >
            返回
          </el-button>
        </div>

        <!-- 房源详情内容 -->
        <div class="property-detail-content">
          <div class="chinese-text">
            <h1>房源详情页</h1>
            <p>房源ID: {{ propertyId }}</p>
            <p>详情页功能开发中...</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const propertyId = route.params.id

const goBack = () => {
  router.go(-1)
}
</script>

<style scoped>
.property-detail-container {
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

.back-navigation {
  margin-bottom: 24px;
}

.property-detail-content {
  background: white;
  padding: 32px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}
</style>
