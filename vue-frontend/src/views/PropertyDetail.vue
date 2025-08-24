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
          <div v-if="loading" class="loading-spinner">加载中...</div>
          <div v-else-if="error" class="error-message">{{ error }}</div>
          <div v-else-if="property">
            <h1>{{ property.address }}</h1>
            <p>{{ property.suburb }}, {{ property.postcode }}</p>
            <h2>${{ property.rent_pw }} / week</h2>
            
            <h3>房源特色</h3>
            <ul>
              <li>卧室: {{ property.bedrooms }}</li>
              <li>浴室: {{ property.bathrooms }}</li>
              <li>车位: {{ property.parking_spaces }}</li>
              <li>家具: {{ property.is_furnished ? '是' : '否' }}</li>
              <li>入住日期: {{ property.available_date }}</li>
            </ul>

            <h3>房源描述</h3>
            <p>{{ property.description }}</p>

             <el-button type="primary" @click="handleContactProperty(property)">
              联系我们
            </el-button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'
import { ArrowLeft } from '@element-plus/icons-vue'
import { userAPI } from '@/services/api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const propertiesStore = usePropertiesStore()

const propertyId = route.params.id

const property = computed(() => propertiesStore.currentProperty)
const loading = computed(() => propertiesStore.loading)
const error = computed(() => propertiesStore.error)

const goBack = () => {
  router.go(-1)
}

onMounted(() => {
  propertiesStore.fetchPropertyDetail(propertyId)
  propertiesStore.logHistory(propertyId)
})

const handleContactProperty = async (property) => {
  try {
    const payload = {
      propertyId: property.listing_id,
      address: property.address,
      // a more detailed implementation would include a form for user details
    }
    const response = await userAPI.contactUs(payload)
    if (response.success) {
      ElMessage.success(response.message)
    }
  } catch {
    ElMessage.error('请求失败，请稍后再试')
  }
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
