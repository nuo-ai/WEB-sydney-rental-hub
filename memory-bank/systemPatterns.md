# 系统模式 (System Patterns)

**文档状态**: 生存文档 (Living Document)
**最后更新**: 2025-08-22

---

## 1. 新架构设计模式 (Vue 3 生态系统)

### 1.1 前端架构演进

**从巨型单文件到现代组件化架构**:

**Legacy架构问题 (已识别)**:
```
问题架构:
├── 单一HTML文件 (1000+行)
│   ├── 内联样式 (800行CSS混乱)
│   ├── 多套重复样式系统
│   └── 维护性极差
├── 单一JS文件 (600行)
│   ├── 全局状态管理
│   ├── 复杂事件处理
│   └── 缺少模块化
└── 技术债务严重
    ├── 样式冲突和重复
    ├── 代码复用困难
    └── 扩展性限制
```

**新Vue 3架构 (现代化)**:
```
Vue 3生态架构:
├── 组件化架构
│   ├── 单文件组件 (.vue)
│   ├── Composition API
│   └── 响应式状态管理
├── 设计系统
│   ├── Element Plus组件库
│   ├── APP UI Kit设计规范
│   └── 统一的样式系统
├── 模块化开发
│   ├── 组件复用
│   ├── 状态管理 (Pinia)
│   └── 路由管理 (Vue Router)
└── 现代工具链
    ├── Vite构建系统
    ├── TypeScript支持
    └── 热更新开发体验
```

### 1.2 组件化设计模式

**核心组件架构**:
```vue
<!-- 标准Vue组件结构 -->
<template>
  <!-- UI模板 -->
</template>

<script setup>
// 逻辑层 - Composition API
import { ref, computed, onMounted } from 'vue'
import { useStore } from '@/stores'

// 响应式状态
const state = ref(initialValue)

// 计算属性
const computed = computed(() => derivedValue)

// 生命周期
onMounted(() => {
  // 初始化逻辑
})
</script>

<style scoped>
/* 样式层 - 作用域隔离 */
</style>
```

**组件层次结构**:
```
组件架构:
├── 页面级组件 (Views)
│   ├── Home.vue (首页)
│   ├── PropertyDetail.vue (详情页)
│   ├── Favorites.vue (收藏页)
│   └── Profile.vue (个人中心)
├── 业务组件 (Business Components)
│   ├── PropertyCard.vue (房源卡片)
│   ├── FilterPanel.vue (筛选面板)
│   ├── SearchBar.vue (搜索栏)
│   └── ImageCarousel.vue (图片轮播)
├── 通用组件 (Common Components)
│   ├── Layout.vue (布局组件)
│   ├── Navigation.vue (导航组件)
│   └── LoadingState.vue (加载状态)
└── Element Plus组件
    ├── el-card (卡片)
    ├── el-drawer (抽屉)
    ├── el-slider (滑块)
    └── ... (其他UI组件)
```

---

## 2. 状态管理模式 (Pinia)

### 2.1 Store架构设计

**模块化状态管理**:
```javascript
// stores/properties.js - 房源数据管理
export const usePropertiesStore = defineStore('properties', {
  state: () => ({
    properties: [],
    filteredProperties: [],
    loading: false,
    currentProperty: null
  }),
  
  getters: {
    totalCount: (state) => state.properties.length,
    hasProperties: (state) => state.properties.length > 0
  },
  
  actions: {
    async fetchProperties() {
      this.loading = true
      try {
        const data = await propertyAPI.getList()
        this.properties = data
        this.filteredProperties = data
      } finally {
        this.loading = false
      }
    }
  }
})
```

**Store模块划分**:
```
状态管理架构:
├── properties.js (房源数据)
│   ├── 房源列表
│   ├── 筛选状态
│   └── 详情缓存
├── filters.js (筛选状态)
│   ├── 价格范围
│   ├── 房型选择
│   └── 地区选择
├── user.js (用户状态)
│   ├── 登录状态
│   ├── 收藏列表
│   └── 用户偏好
└── app.js (应用状态)
    ├── 加载状态
    ├── 错误处理
    └── 全局配置
```

---

## 3. UI Kit集成模式

### 3.1 设计系统集成

**APP UI Kit → Vue组件转换模式**:
```vue
<!-- 基于UI Kit的房源卡片组件 -->
<template>
  <div class="property-card" :class="uiKitClasses">
    <!-- 图片区域 - UI Kit设计 -->
    <div class="image-container">
      <el-carousel :height="imageHeight" indicator-position="none">
        <el-carousel-item v-for="image in property.images" :key="image">
          <img :src="image" :alt="property.title" class="property-image" />
        </el-carousel-item>
      </el-carousel>
      
      <!-- 价格标签 - UI Kit样式 -->
      <div class="price-tag">{{ formatPrice(property.rent_pw) }}</div>
      
      <!-- 收藏按钮 - Element Plus + UI Kit样式 -->
      <el-button 
        :icon="favoriteIcon" 
        circle 
        class="favorite-button"
        @click="toggleFavorite"
      />
    </div>
    
    <!-- 内容区域 - UI Kit排版 -->
    <div class="content-area">
      <h3 class="property-title">{{ property.address }}</h3>
      <div class="property-features">
        <span class="feature-item">
          <i class="icon-bed"></i>
          {{ property.bedrooms }}
        </span>
        <span class="feature-item">
          <i class="icon-bath"></i>
          {{ property.bathrooms }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* UI Kit样式适配 */
.property-card {
  /* 基于UI Kit的设计规范 */
  background: var(--ui-kit-card-bg);
  border-radius: var(--ui-kit-border-radius);
  box-shadow: var(--ui-kit-shadow);
  overflow: hidden;
  transition: var(--ui-kit-transition);
}

/* 响应式适配 - APP到PC */
@media (min-width: 768px) {
  .property-card {
    width: 320px; /* 从APP全宽适配到PC固定宽度 */
  }
}
</style>
```

### 3.2 样式系统模式

**CSS变量系统 (基于UI Kit)**:
```css
:root {
  /* 从UI Kit提取的设计令牌 */
  --ui-kit-primary: #007AFF;
  --ui-kit-secondary: #34C759;
  --ui-kit-text-primary: #000000;
  --ui-kit-text-secondary: #8E8E93;
  --ui-kit-background: #F2F2F7;
  
  /* 间距系统 */
  --ui-kit-spacing-xs: 4px;
  --ui-kit-spacing-sm: 8px;
  --ui-kit-spacing-md: 16px;
  --ui-kit-spacing-lg: 24px;
  --ui-kit-spacing-xl: 32px;
  
  /* 字体系统 */
  --ui-kit-font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --ui-kit-font-size-sm: 14px;
  --ui-kit-font-size-md: 16px;
  --ui-kit-font-size-lg: 18px;
  
  /* 圆角系统 */
  --ui-kit-border-radius-sm: 8px;
  --ui-kit-border-radius-md: 12px;
  --ui-kit-border-radius-lg: 16px;
  
  /* 阴影系统 */
  --ui-kit-shadow-sm: 0 2px 4px rgba(0,0,0,0.1);
  --ui-kit-shadow-md: 0 4px 8px rgba(0,0,0,0.12);
  --ui-kit-shadow-lg: 0 8px 16px rgba(0,0,0,0.15);
}
```

---

## 4. API集成模式

### 4.1 服务层设计

**API服务封装**:
```javascript
// services/api.js - 统一API接口
import axios from 'axios'

const apiClient = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const propertyAPI = {
  // 获取房源列表
  async getList(params = {}) {
    const response = await apiClient.get('/properties', { params })
    return response.data.data
  },
  
  // 获取房源详情
  async getDetail(id) {
    const response = await apiClient.get(`/properties/${id}`)
    return response.data
  },
  
  // 搜索房源
  async search(query) {
    const response = await apiClient.get('/properties', {
      params: { search: query }
    })
    return response.data.data
  }
}
```

### 4.2 错误处理模式

**统一错误处理**:
```javascript
// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 添加loading状态
    const appStore = useAppStore()
    appStore.setLoading(true)
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    const appStore = useAppStore()
    appStore.setLoading(false)
    return response
  },
  (error) => {
    const appStore = useAppStore()
    appStore.setLoading(false)
    appStore.setError(error.message)
    return Promise.reject(error)
  }
)
```

---

## 5. 响应式设计模式

### 5.1 移动优先策略

**断点系统**:
```css
/* 移动优先的响应式设计 */
.container {
  /* 基础样式 - 移动端 */
  padding: var(--ui-kit-spacing-md);
}

/* 平板适配 */
@media (min-width: 768px) {
  .container {
    padding: var(--ui-kit-spacing-lg);
    max-width: 768px;
    margin: 0 auto;
  }
}

/* 桌面适配 */
@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    padding: var(--ui-kit-spacing-xl);
  }
}
```

### 5.2 组件响应式模式

**自适应组件**:
```vue
<template>
  <div class="responsive-grid" :class="gridClasses">
    <PropertyCard 
      v-for="property in properties" 
      :key="property.id"
      :property="property"
      :size="cardSize"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useBreakpoints } from '@/composables/useBreakpoints'

const { isMobile, isTablet, isDesktop } = useBreakpoints()

const gridClasses = computed(() => ({
  'grid-mobile': isMobile.value,
  'grid-tablet': isTablet.value, 
  'grid-desktop': isDesktop.value
}))

const cardSize = computed(() => {
  if (isMobile.value) return 'small'
  if (isTablet.value) return 'medium'
  return 'large'
})
</script>
```

---

## 6. 多端扩展模式

### 6.1 Vue到uni-app迁移模式

**组件兼容性设计**:
```vue
<!-- Vue Web版本 -->
<template>
  <el-card class="property-card">
    <template #header>
      <div class="card-header">{{ title }}</div>
    </template>
    <div class="card-content">{{ content }}</div>
  </el-card>
</template>

<!-- uni-app版本 (未来) -->
<template>
  <view class="property-card">
    <view class="card-header">{{ title }}</view>
    <view class="card-content">{{ content }}</view>
  </view>
</template>
```

### 6.2 代码复用策略

**共享业务逻辑**:
```javascript
// composables/useProperty.js - 跨平台业务逻辑
export function useProperty() {
  const property = ref(null)
  const loading = ref(false)
  
  const fetchProperty = async (id) => {
    loading.value = true
    try {
      property.value = await propertyAPI.getDetail(id)
    } finally {
      loading.value = false
    }
  }
  
  return {
    property: readonly(property),
    loading: readonly(loading),
    fetchProperty
  }
}
```

---

## 7. 学习与调试模式

### 7.1 开发调试策略

**Vue DevTools集成**:
- 组件层次结构可视化
- 状态变化实时监控
- 事件追踪和调试
- 性能分析工具

**错误边界处理**:
```vue
<!-- ErrorBoundary.vue -->
<template>
  <div v-if="hasError" class="error-boundary">
    <h2>出现了一个错误</h2>
    <p>{{ errorMessage }}</p>
    <el-button @click="retry">重试</el-button>
  </div>
  <slot v-else />
</template>

<script setup>
import { ref } from 'vue'

const hasError = ref(false)
const errorMessage = ref('')

const handleError = (error) => {
  hasError.value = true
  errorMessage.value = error.message
}

const retry = () => {
  hasError.value = false
  errorMessage.value = ''
}
</script>
```

---

**总结**: Vue 3生态系统为我们提供了现代化、可维护、可扩展的前端架构。通过组件化设计、状态管理、UI Kit集成和响应式设计的系统性模式，我们能够构建出高质量的用户界面，同时为未来的多端扩展奠定坚实基础。
