<template>
  <div class="chat-container">
    <main class="main-content">
      <div class="container">
        <header class="page-header">
          <h1 class="page-title chinese-text">AI助手</h1>
          <p class="page-subtitle chinese-text">智能房源推荐和咨询服务</p>
        </header>

        <div class="chat-content">
          <div class="placeholder-content">
            <el-icon :size="64" color="#d9d9d9">
              <ChatDotRound />
            </el-icon>
            <h3 class="chinese-text">AI助手功能开发中</h3>
            <p class="chinese-text">即将提供智能房源推荐和在线咨询服务</p>
            <el-button type="primary" @click="goToHome"> 返回房源列表 </el-button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
defineOptions({ name: 'ChatView' })
import { useRouter } from 'vue-router'
import { ChatDotRound } from '@element-plus/icons-vue'

const router = useRouter()

const goToHome = () => {
  router.push('/')
}
</script>

<style scoped>
.chat-container {
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

.chat-content {
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
  margin: 16px 0 8px;
}

.placeholder-content p {
  font-size: 16px;
  color: var(--color-text-secondary);
  margin-bottom: 24px;
}
</style>
