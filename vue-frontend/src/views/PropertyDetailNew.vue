<template>
  <div class="figma-container">
    <!-- 根容器 1920x2597 -->
    <div class="root-container">
      <!-- 图片区域 687px高度 -->
      <div class="image-section">
        <el-image
          v-if="images.length > 0"
          :src="images[currentImageIndex]"
          class="main-image"
          fit="cover"
        />

        <!-- 返回按钮 -->
        <button @click="goBack" class="back-btn">
          <el-icon :size="20"><ArrowLeft /></el-icon>
        </button>
      </div>

      <!-- 主内容区 1683x1909 位于 left:117px top:687px -->
      <div class="main-content-wrapper">
        <div class="main-content">

          <!-- 第一部分：基本信息 -->
          <div class="info-section">
            <!-- 价格和可用日期 -->
            <div class="availability-bond">
              <span>Available from Monday, 1st September 2025</span>
              <span class="divider">|</span>
              <span>Bond ${{ getBondAmount() }}</span>
            </div>

            <!-- 价格 -->
            <div class="price">${{ property?.rent_pw || 0 }} per week</div>

            <!-- 地址 -->
            <div class="address">
              <h1>{{ property?.address }}</h1>
              <p>{{ property?.suburb }}, NSW {{ property?.postcode }}</p>
            </div>

            <!-- 房屋特征 -->
            <div class="features">
              <div class="feature">
                <el-icon><House /></el-icon>
                <span>{{ property?.bedrooms || 0 }}</span>
              </div>
              <div class="feature">
                <el-icon><Van /></el-icon>
                <span>{{ property?.bathrooms || 0 }}</span>
              </div>
              <div class="feature">
                <el-icon><Ticket /></el-icon>
                <span>{{ property?.parking_spaces || 0 }}</span>
              </div>
              <div class="property-type">Apartment / Unit / Flat</div>
            </div>
          </div>

          <!-- 地图区域 975x681 位于 left:315px -->
          <div class="map-section">
            <h2>Location</h2>
            <div class="map-container">
              <SimpleMap
                v-if="property?.latitude && property?.longitude"
                :latitude="property.latitude"
                :longitude="property.longitude"
                :zoom="15"
                height="360px"
                :marker-title="property.address"
              />
            </div>

            <!-- See travel times 按钮 - 保留原功能 -->
            <button class="see-travel-times-btn" @click="handleSeeTravelTimes">
              <div class="travel-icon-wrapper">
                <i class="fas fa-location-dot"></i>
              </div>
              <div class="travel-btn-content">
                <span class="travel-btn-title">See travel times</span>
                <span class="travel-btn-subtitle">Find out travel times from this property to your destinations</span>
              </div>
            </button>
          </div>

          <!-- Property Description 975x439 位于 left:337px -->
          <div class="description-section">
            <h2 class="section-title">Property Description</h2>
            <div class="description-content">
              <p class="headline">Fully Furnished-2B2B! WeChat: KRL103,BoeyANTmover,KRL106,ATR102,KRL_111,KRL104</p>
              <p>?? Fully Furnished 2 Bed 2 Bath in Maroubra |Big Balcony I Quiet Location | Direct Bus to UNSW</p>
              <p>??Address: 7/264 Maroubra Road, Maroubra</p>
            </div>
            <button class="read-more-btn" @click="isDescriptionExpanded = !isDescriptionExpanded">
              {{ isDescriptionExpanded ? 'Read less' : 'Read more' }}
            </button>
          </div>

          <!-- Property Features -->
          <div class="features-section">
            <h2 class="section-title">Property Features</h2>
            <div class="features-grid">
              <div class="feature-column">
                <div class="feature-item">Dishwasher</div>
                <div class="feature-item">Fireplace(s)</div>
                <div class="feature-item">Separate Dining Room</div>
                <div class="feature-item">Heating</div>
                <div class="feature-item">Study</div>
                <div class="feature-item">Double glazed windows</div>
                <div class="feature-item">Energy efficient appliances</div>
                <div class="feature-item">Water efficient appliances</div>
                <div class="feature-item">Wall / ceiling insulation</div>
              </div>
              <div class="feature-column">
                <div class="feature-item">Rainwater storage tank</div>
                <div class="feature-item">Greywater system</div>
                <div class="feature-item">Water efficient fixtures</div>
                <div class="feature-item">Shed</div>
                <div class="feature-item">Fully fenced</div>
                <div class="feature-item">Balcony / Deck</div>
                <div class="feature-item">Garden / Courtyard</div>
              </div>
            </div>
            <button class="view-less-btn">View less</button>
          </div>

          <!-- Inspection Times 975x439 -->
          <div class="inspection-section">
            <h2 class="inspection-title">Inspection times</h2>
            <span class="inspection-label">INSPECTIONS</span>

            <div class="inspection-grid">
              <!-- 左列 -->
              <div class="inspection-column">
                <div class="inspection-item">
                  <div class="inspection-date">
                    <div class="day">Monday, 1 Sep</div>
                    <div class="time">6:00am - 6:10am</div>
                  </div>
                  <button class="calendar-btn">
                    <el-icon><Calendar /></el-icon>
                  </button>
                </div>
                <div class="inspection-item">
                  <div class="inspection-date">
                    <div class="day">Wednesday, 3 Sep</div>
                    <div class="time">6:00am - 6:10am</div>
                  </div>
                  <button class="calendar-btn">
                    <el-icon><Calendar /></el-icon>
                  </button>
                </div>
                <div class="inspection-item">
                  <div class="inspection-date">
                    <div class="day">Friday, 5 Sep</div>
                    <div class="time">6:00am - 6:10am</div>
                  </div>
                  <button class="calendar-btn">
                    <el-icon><Calendar /></el-icon>
                  </button>
                </div>
                <div class="inspection-item">
                  <div class="inspection-date">
                    <div class="day">Sunday, 7 Sep</div>
                    <div class="time">6:00am - 6:10am</div>
                  </div>
                  <button class="calendar-btn">
                    <el-icon><Calendar /></el-icon>
                  </button>
                </div>
              </div>

              <!-- 右列 -->
              <div class="inspection-column">
                <div class="inspection-item">
                  <div class="inspection-date">
                    <div class="day">Tuesday, 2 Sep</div>
                    <div class="time">6:00am - 6:10am</div>
                  </div>
                  <button class="calendar-btn">
                    <el-icon><Calendar /></el-icon>
                  </button>
                </div>
                <div class="inspection-item">
                  <div class="inspection-date">
                    <div class="day">Thursday, 4 Sep</div>
                    <div class="time">6:00am - 6:10am</div>
                  </div>
                  <button class="calendar-btn">
                    <el-icon><Calendar /></el-icon>
                  </button>
                </div>
                <div class="inspection-item">
                  <div class="inspection-date">
                    <div class="day">Saturday, 6 Sep</div>
                    <div class="time">6:00am - 6:10am</div>
                  </div>
                  <button class="calendar-btn">
                    <el-icon><Calendar /></el-icon>
                  </button>
                </div>

                <!-- Add all to planner 按钮 -->
                <div class="planner-btn-wrapper">
                  <button class="add-to-planner">
                    <el-icon><Plus /></el-icon>
                    <span>Add all to planner</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- Auth Modal -->
    <AuthModal
      v-if="showAuthModal"
      v-model="showAuthModal"
      @success="handleAuthSuccess"
    />
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'
import { useAuthStore } from '@/stores/auth'
import {
  ArrowLeft, House, Ticket, Van, Calendar, Plus
} from '@element-plus/icons-vue'
import SimpleMap from '@/components/SimpleMap.vue'
import AuthModal from '@/components/modals/AuthModal.vue'

const route = useRoute()
const router = useRouter()
const propertiesStore = usePropertiesStore()
const authStore = useAuthStore()

const propertyId = route.params.id
const currentImageIndex = ref(0)
const isDescriptionExpanded = ref(false)
const showAuthModal = ref(false)

const property = computed(() => propertiesStore.currentProperty)
const images = computed(() => {
  if (!property.value?.images) return []
  return property.value.images.filter(url => url && url.trim())
})

const goBack = () => router.go(-1)

const getBondAmount = () => {
  if (!property.value) return '0'
  return (property.value.rent_pw * 4).toString()
}

// 保留原有的 handleSeeTravelTimes 功能
const handleSeeTravelTimes = () => {
  const isTest = authStore.testMode

  if (isTest || authStore.isAuthenticated) {
    router.push({
      name: 'CommuteTimes',
      query: {
        propertyId: propertyId,
        address: property.value.address,
        suburb: property.value.suburb,
        lat: property.value.latitude,
        lng: property.value.longitude
      }
    })
  } else {
    showAuthModal.value = true
  }
}

const handleAuthSuccess = () => {
  showAuthModal.value = false
  handleSeeTravelTimes()
}

onMounted(async () => {
  await propertiesStore.fetchPropertyDetail(propertyId)
})
</script>

<style scoped>
/* 精确复制 PC.txt 的布局 */
.figma-container {
  width: 100%;
  min-height: 100vh;
  background: #f5f5f5;
}

/* 根容器 1920x2597 */
.root-container {
  width: 1920px;
  margin: 0 auto;
  position: relative;
  background: white;
}

/* 图片区域 - 前687px */
.image-section {
  width: 1920px;
  height: 687px;
  position: relative;
  background: #000;
}

.main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.back-btn {
  position: absolute;
  top: 20px;
  left: 20px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

/* 主内容包装器 - 精确定位 */
.main-content-wrapper {
  position: absolute;
  left: 117px;
  top: 687px;
  width: 1683px;
  background: rgba(254, 254, 254, 1);
}

.main-content {
  position: relative;
  width: 100%;
}

/* 基本信息部分 */
.info-section {
  padding: 40px;
  background: white;
  margin-bottom: 20px;
}

.availability-bond {
  font-size: 14px;
  color: #6e7881;
  margin-bottom: 16px;
  font-family: Inter, sans-serif;
}

.divider {
  margin: 0 10px;
  color: #d0d3d9;
}

.price {
  font-size: 36px;
  font-weight: 700;
  color: #2e3a4b;
  margin-bottom: 20px;
  font-family: Inter, sans-serif;
}

.address h1 {
  font-size: 22px;
  font-weight: 600;
  color: #2e3a4b;
  margin: 0 0 8px 0;
  font-family: Inter, sans-serif;
}

.address p {
  font-size: 16px;
  color: #6e7881;
  margin: 0;
  font-family: Inter, sans-serif;
}

.features {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-top: 20px;
}

.feature {
  display: flex;
  align-items: center;
  gap: 6px;
}

.feature span {
  font-size: 18px;
  font-weight: 600;
  color: #2e3a4b;
  font-family: Inter, sans-serif;
}

.property-type {
  padding-left: 24px;
  border-left: 1px solid #d0d3d9;
  font-size: 18px;
  font-weight: 600;
  color: #6e7881;
  font-family: Inter, sans-serif;
}

/* 地图部分 - 精确位置 left:315px */
.map-section {
  position: relative;
  left: 198px; /* 315px - 117px = 198px 相对偏移 */
  width: 975px;
  padding: 32px;
  background: white;
  margin-bottom: 32px;
}

.map-section h2 {
  font-size: 24px;
  font-weight: 700;
  color: #2e3a4b;
  margin: 0 0 24px 0;
  font-family: Inter, sans-serif;
}

.map-container {
  width: 958px;
  height: 360px;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
}

/* See travel times 按钮 - 保留原样式和功能 */
.see-travel-times-btn {
  width: 100%;
  max-width: 600px;
  padding: 14px 16px;
  margin-top: 16px;
  background: white;
  border: 1px solid #d0d3d9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.see-travel-times-btn:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12);
  background: #f8f9fa;
}

.travel-icon-wrapper {
  width: 40px;
  height: 40px;
  background: #f0f2f5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.travel-icon-wrapper i {
  font-size: 18px;
  color: #017188;
}

.travel-btn-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.travel-btn-title {
  font-size: 15px;
  font-weight: 600;
  color: #2e3a4b;
  font-family: Inter, sans-serif;
}

.travel-btn-subtitle {
  font-size: 13px;
  color: #6e7881;
  line-height: 1.4;
  font-family: Inter, sans-serif;
}

/* Description部分 - 975x439 位于 left:337px */
.description-section {
  position: relative;
  left: 220px; /* 337px - 117px = 220px */
  width: 975px;
  padding: 32px;
  background: white;
  margin-bottom: 32px;
}

.section-title {
  font-size: 23px;
  font-weight: 700;
  color: #60606D;
  margin: 0 0 24px 0;
  font-family: Inter, sans-serif;
}

.description-content {
  margin-bottom: 20px;
}

.headline {
  font-size: 15px;
  font-weight: 700;
  color: #757D8B;
  margin-bottom: 12px;
  font-family: Inter, sans-serif;
}

.description-content p {
  font-size: 14px;
  color: #757D8B;
  line-height: 1.6;
  margin-bottom: 8px;
  font-family: Inter, sans-serif;
}

.read-more-btn {
  padding: 6px 14px;
  border: 1px solid #6F6997;
  border-radius: 4px;
  background: white;
  font-size: 13px;
  font-weight: 700;
  color: #4F6181;
  cursor: pointer;
  font-family: Inter, sans-serif;
}

/* Features部分 */
.features-section {
  position: relative;
  left: 220px;
  width: 975px;
  padding: 32px;
  background: white;
  margin-bottom: 32px;
}

.features-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 100px;
  margin-bottom: 24px;
}

.feature-item {
  font-size: 15px;
  color: #7F8194;
  padding: 10px 0;
  font-family: Inter, sans-serif;
}

.view-less-btn {
  font-size: 15px;
  color: #6FC168;
  background: none;
  border: none;
  cursor: pointer;
  font-family: Inter, sans-serif;
}

/* Inspection部分 - 975x439 */
.inspection-section {
  position: relative;
  left: 220px;
  width: 975px;
  height: 439px;
  padding: 32px;
  background: white;
  margin-bottom: 60px;
}

.inspection-title {
  font-size: 23px;
  font-weight: 700;
  color: #4C5267;
  margin: 0 0 8px 0;
  font-family: Inter, sans-serif;
}

.inspection-label {
  font-size: 14px;
  font-weight: 700;
  color: #6F7386;
  text-transform: uppercase;
  font-family: Inter, sans-serif;
}

.inspection-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 32px;
}

.inspection-item {
  width: 305px;
  height: 72px;
  border: 1px solid #D0D3D9;
  background: white;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 4px;
}

.inspection-date .day {
  font-size: 15px;
  font-weight: 700;
  color: #6E7385;
  margin-bottom: 4px;
  font-family: Inter, sans-serif;
}

.inspection-date .time {
  font-size: 15px;
  color: #7F8194;
  font-family: Inter, sans-serif;
}

.calendar-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.planner-btn-wrapper {
  grid-column: 2;
  margin-top: 20px;
}

.add-to-planner {
  width: 305px;
  height: 72px;
  border: 1px solid #D0D3D9;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 700;
  color: #6E7285;
  cursor: pointer;
  border-radius: 4px;
  font-family: Inter, sans-serif;
}

/* 响应式 - 移动端降级 */
@media (max-width: 1920px) {
  .root-container {
    width: 100%;
    max-width: 1920px;
  }

  .image-section {
    width: 100%;
  }

  .main-content-wrapper {
    position: relative;
    left: 0;
    top: 0;
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }

  .map-section,
  .description-section,
  .features-section,
  .inspection-section {
    left: 0;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .image-section {
    height: 300px;
  }

  .inspection-grid {
    grid-template-columns: 1fr;
  }

  .features-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}
</style>
