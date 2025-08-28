# Sydney Rental Hub - 设计系统规则 (CLAUDE.md)

> 为 Claude 提供的设计系统集成指南，用于从 Figma 设计生成代码

**文档版本**: v2.0  
**最后更新**: 2025-08-27  
**适用框架**: Vue 3 + Element Plus

---

## 🎯 核心设计原则

### 1. JUWO 品牌主题
这是一个**房源租赁平台**，使用 **JUWO 橙色品牌主题**，专注于**移动端优先**的设计理念。

### 2. 设计语言特征
- **简洁现代**: 6px 统一圆角，1px 细边框
- **信息层次**: 清晰的视觉层次，突出价格和关键信息  
- **移动优先**: 单列布局，580px 标准宽度
- **一致性**: 所有组件遵循统一的间距和色彩系统

---

## 🎨 设计令牌 (Design Tokens)

### 颜色系统
**位置**: `vue-frontend/src/style.css`

```css
:root {
  /* JUWO 主品牌色系 */
  --juwo-primary: #FF5824;        /* 主要操作、价格高亮 */
  --juwo-primary-light: #FF7851;  /* 按钮悬停状态 */
  --juwo-primary-dark: #E64100;   /* 按钮按下状态 */
  --juwo-primary-50: #FFF3F0;     /* 淡色背景 */
  
  /* Element Plus 主题覆盖 */
  --el-color-primary: #FF5824;
  --el-color-primary-light-1: #FF7851;
  --el-color-primary-light-3: #FF9575;
  
  /* 语义化颜色 */
  --color-text-primary: #333333;    /* 主要文字 */
  --color-text-secondary: #666666;  /* 次要文字 */
  --color-text-tertiary: #999999;   /* 辅助文字 */
  --color-border: #E3E3E3;         /* 边框颜色 */
  --color-border-light: #F0F0F0;   /* 浅色边框 */
  
  /* 状态颜色 */
  --color-success: #67C23A;        /* 成功状态 */
  --color-warning: #E6A23C;        /* 警告状态 */
  --color-danger: #F56C6C;         /* 错误状态 */
  --color-info: #909399;           /* 信息状态 */
}
```

### 字体系统
```css
:root {
  /* 字体族 */
  --font-family-base: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  
  /* 字体大小 */
  --font-size-xl: 36px;      /* 大标题 (桌面端价格) */
  --font-size-lg: 32px;      /* 大标题 (平板端价格) */
  --font-size-md: 28px;      /* 中标题 (移动端价格) */
  --font-size-base: 16px;    /* 正文 */
  --font-size-sm: 14px;      /* 小字 */
  --font-size-xs: 12px;      /* 最小字 */
  
  /* 字重 */
  --font-weight-bold: 700;
  --font-weight-medium: 500;
  --font-weight-normal: 400;
  
  /* 行高 */
  --line-height-tight: 1.3;
  --line-height-base: 1.5;
  --line-height-loose: 1.7;
}
```

### 间距系统
```css
:root {
  /* 渐进式间距系统 */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 12px;   /* 组件间距 */
  --spacing-lg: 16px;   /* 容器内边距 */
  --spacing-xl: 24px;   /* 卡片间距 */
  --spacing-2xl: 32px;  /* 页面边距 */
  
  /* 布局尺寸 */
  --layout-width-card: 580px;      /* 房源卡片标准宽度 */
  --layout-width-search: 520px;    /* 搜索框宽度 */
  --layout-width-button: 48px;     /* 按钮尺寸 */
  --layout-max-width: 1200px;      /* 页面最大宽度 */
  
  /* 圆角系统 */
  --border-radius: 6px;            /* 统一圆角 */
  --border-width: 1px;             /* 统一边框宽度 */
}
```

---

## 🏗️ 组件库结构

### 位置与架构
```
vue-frontend/src/components/
├── PropertyCard.vue       # 房源卡片 (核心组件)
├── SearchBar.vue         # 搜索栏 (自动补全)
├── FilterPanel.vue       # 筛选面板 (抽屉式)
├── FilterTabs.vue        # 快速筛选标签
├── Navigation.vue        # 顶部导航
├── CommuteCalculator.vue # 通勤计算器
└── CompareToolbar.vue    # 对比工具栏
```

### 组件架构模式
**使用 Vue 3 Composition API + `<script setup>` 语法**

```vue
<template>
  <!-- 模板结构 -->
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { usePropertiesStore } from '@/stores/properties'

// 响应式状态
const isVisible = ref(false)
const store = usePropertiesStore()

// 计算属性
const filteredData = computed(() => store.filteredProperties)

// 方法定义
const handleClick = () => {
  // 处理逻辑
}

// 生命周期
onMounted(() => {
  // 初始化逻辑
})
</script>

<style scoped>
/* 组件样式 */
</style>
```

---

## 🛠️ 技术栈与工具

### 核心框架
- **前端框架**: Vue 3 (Composition API)
- **UI 组件库**: Element Plus
- **构建工具**: Vite
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP 客户端**: Axios

### 样式系统
- **方法**: CSS3 + CSS Variables (不使用 CSS-in-JS)
- **预处理器**: 原生 CSS (不使用 Sass/Less)
- **响应式**: CSS Media Queries
- **图标**: Font Awesome + Element Plus Icons

### 开发工具
```json
{
  "devDependencies": {
    "eslint": "^8.x",
    "prettier": "^3.x",
    "@vitejs/plugin-vue": "^4.x"
  }
}
```

---

## 📱 响应式设计规范

### 断点系统
```css
/* 移动端优先设计 */
.component {
  /* 移动端样式 (默认) */
  width: 100%;
  padding: var(--spacing-lg);
}

/* 平板端 */
@media (min-width: 768px) {
  .component {
    width: var(--layout-width-card);
    padding: var(--spacing-xl);
  }
}

/* 桌面端 */
@media (min-width: 1200px) {
  .component {
    max-width: var(--layout-max-width);
    padding: var(--spacing-2xl);
  }
}
```

### 移动端布局模式
```css
/* 单列布局 */
.properties-grid {
  display: flex;
  flex-direction: column;
  align-items: flex-start;  /* 强制左对齐 */
  gap: var(--spacing-xl);
  max-width: var(--layout-width-card);
}

/* 渐进式间距 */
.mobile-spacing {
  padding: var(--spacing-sm) 0 var(--spacing-md) 0;
}
```

---

## 🖼️ 资源管理

### 图片处理
```javascript
// 房源图片数组处理
const processImages = (images) => {
  if (!images || !Array.isArray(images) || images.length === 0) {
    return ['/default-property.jpg']
  }
  
  return images.map(img => 
    typeof img === 'string' ? img : img.url
  )
}
```

### 图标系统
```vue
<template>
  <!-- Font Awesome 图标 -->
  <i class="fas fa-heart" :class="{ active: isFavorite }"></i>
  
  <!-- Element Plus 图标 -->
  <el-icon><Search /></el-icon>
</template>

<script setup>
import { Search } from '@element-plus/icons-vue'
</script>

<style>
/* 图标样式统一 */
.icon {
  color: var(--juwo-primary);
  font-size: 16px;
}

.icon.active {
  color: var(--juwo-primary-dark);
}
</style>
```

---

## 🎯 核心组件模式

### PropertyCard.vue (580px 标准)
```vue
<template>
  <div class="property-card" @click="$router.push(`/properties/${property.listing_id}`)">
    <!-- 图片轮播 -->
    <div class="property-images">
      <el-carousel height="240px" indicator-position="none">
        <el-carousel-item v-for="(image, index) in processedImages" :key="index">
          <img :src="image" :alt="`房源图片 ${index + 1}`" />
        </el-carousel-item>
      </el-carousel>
      
      <!-- 收藏按钮 -->
      <button class="favorite-btn" @click.stop="toggleFavorite">
        <i class="fas fa-heart" :class="{ active: isFavorite }"></i>
      </button>
    </div>
    
    <!-- 房源信息 -->
    <div class="property-info">
      <!-- 价格 (使用 JUWO 主色) -->
      <div class="property-price">
        <span class="currency">$</span>
        <span class="amount">{{ property.rent_pw }}</span>
        <span class="period">per week</span>
      </div>
      
      <!-- 地址 -->
      <div class="property-address">
        {{ property.address }}, {{ property.suburb }}
      </div>
      
      <!-- 房型信息 -->
      <div class="property-specs">
        <span class="spec-item">
          <i class="fas fa-bed"></i>
          {{ property.bedrooms }}
        </span>
        <span class="spec-item">
          <i class="fas fa-bath"></i>
          {{ property.bathrooms }}
        </span>
        <span class="spec-item">
          <i class="fas fa-car"></i>
          {{ property.parking_spaces }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.property-card {
  width: var(--layout-width-card);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--border-radius);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s ease;
}

.property-card:hover {
  border-color: var(--juwo-primary);
  box-shadow: 0 4px 12px rgba(255, 88, 36, 0.1);
}

.property-price .amount {
  color: var(--juwo-primary);
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-bold);
}

@media (min-width: 768px) {
  .property-price .amount {
    font-size: var(--font-size-lg);
  }
}

@media (min-width: 1200px) {
  .property-price .amount {
    font-size: var(--font-size-xl);
  }
}
</style>
```

### 搜索栏组件模式
```vue
<template>
  <div class="search-filter-container">
    <!-- 搜索框 (520px) -->
    <div class="search-bar">
      <el-autocomplete
        v-model="searchQuery"
        :fetch-suggestions="querySearch"
        placeholder="输入区域名称或邮编"
        @select="handleSelect"
      />
    </div>
    
    <!-- 筛选按钮 (48px) -->
    <el-button class="filter-trigger-btn" @click="showFilter = true">
      <i class="fas fa-filter"></i>
    </el-button>
  </div>
</template>

<style scoped>
.search-filter-container {
  display: flex;
  gap: var(--spacing-md);
  max-width: calc(var(--layout-width-search) + var(--layout-width-button) + var(--spacing-md));
}

.search-bar {
  width: var(--layout-width-search);
}

.filter-trigger-btn {
  width: var(--layout-width-button);
  height: var(--layout-width-button);
  border-radius: var(--border-radius);
}
</style>
```

---

## 🔗 API 集成模式

### 服务层结构
```javascript
// services/api.js
import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api',  // 使用 Vite 代理
  timeout: 10000
})

// 统一响应处理
const handleResponse = (response) => {
  if (response.data.status === 'success') {
    return response.data.data
  }
  throw new Error(response.data.error || 'API 请求失败')
}

export const propertyAPI = {
  // 获取房源列表 (支持分页)
  getList: (params = {}) => 
    apiClient.get('/properties', { params }).then(handleResponse),
    
  // 获取房源详情
  getDetail: (id) => 
    apiClient.get(`/properties/${id}`).then(handleResponse),
    
  // 搜索房源
  search: (query) => 
    apiClient.get('/properties/search', { params: { q: query } }).then(handleResponse)
}
```

### Pinia 状态管理模式
```javascript
// stores/properties.js
import { defineStore } from 'pinia'
import { propertyAPI } from '@/services/api'

export const usePropertiesStore = defineStore('properties', {
  state: () => ({
    allProperties: [],
    filteredProperties: [],
    favoriteIds: JSON.parse(localStorage.getItem('favorites') || '[]'),
    loading: false,
    searchQuery: '',
    filters: {
      priceRange: [0, 5000],
      bedrooms: null,
      suburb: null
    }
  }),
  
  getters: {
    favoriteProperties: (state) => 
      state.allProperties.filter(p => 
        state.favoriteIds.includes(p.listing_id)
      )
  },
  
  actions: {
    // 获取房源数据
    async fetchProperties(params = {}) {
      this.loading = true
      try {
        this.allProperties = await propertyAPI.getList(params)
        this.applyFilters(this.filters)
      } catch (error) {
        console.error('获取房源失败:', error)
      } finally {
        this.loading = false
      }
    },
    
    // 应用筛选
    applyFilters(newFilters) {
      // 先更新筛选条件
      Object.assign(this.filters, newFilters)
      
      // 基于更新后的条件筛选
      this.filteredProperties = this.allProperties.filter(property => {
        const { priceRange, bedrooms, suburb } = this.filters
        
        // 价格筛选
        if (property.rent_pw < priceRange[0] || property.rent_pw > priceRange[1]) {
          return false
        }
        
        // 卧室数筛选
        if (bedrooms && property.bedrooms !== bedrooms) {
          return false
        }
        
        // 区域筛选
        if (suburb && !property.suburb.toLowerCase().includes(suburb.toLowerCase())) {
          return false
        }
        
        return true
      })
    },
    
    // 切换收藏状态
    toggleFavorite(propertyId) {
      const index = this.favoriteIds.indexOf(propertyId)
      if (index > -1) {
        this.favoriteIds.splice(index, 1)
      } else {
        this.favoriteIds.push(propertyId)
      }
      localStorage.setItem('favorites', JSON.stringify(this.favoriteIds))
    }
  }
})
```

---

## 📋 Figma 到代码的转换规则

### 1. 设计令牌映射
```javascript
// Figma 设计值 → CSS 变量映射
const tokenMapping = {
  // 颜色
  'Primary/Orange': 'var(--juwo-primary)',
  'Text/Primary': 'var(--color-text-primary)',
  'Border/Light': 'var(--color-border-light)',
  
  // 间距
  'Spacing/Small': 'var(--spacing-sm)',
  'Spacing/Medium': 'var(--spacing-md)',
  'Spacing/Large': 'var(--spacing-lg)',
  
  // 字体
  'Typography/H1': 'var(--font-size-xl)',
  'Typography/Body': 'var(--font-size-base)',
  'Typography/Caption': 'var(--font-size-sm)'
}
```

### 2. 组件生成模板
```vue
<!-- 从 Figma 组件生成 Vue 组件的标准模板 -->
<template>
  <div class="figma-component" :class="componentClass">
    <!-- 基于 Figma 层级结构生成 DOM -->
    <div class="content-area">
      <!-- 动态内容 -->
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// Props 定义 (基于 Figma 组件属性)
const props = defineProps({
  variant: {
    type: String,
    default: 'default'
  },
  size: {
    type: String, 
    default: 'medium'
  }
})

// 动态样式类
const componentClass = computed(() => {
  return [
    `variant-${props.variant}`,
    `size-${props.size}`
  ]
})
</script>

<style scoped>
.figma-component {
  /* 使用设计令牌 */
  border-radius: var(--border-radius);
  border: var(--border-width) solid var(--color-border);
  
  /* 响应式处理 */
  width: 100%;
}

/* 变体样式 */
.variant-primary {
  background-color: var(--juwo-primary);
  color: white;
}

.variant-secondary {
  background-color: var(--color-border-light);
  color: var(--color-text-primary);
}
</style>
```

### 3. 布局转换规则
```css
/* Figma Auto Layout → CSS Flexbox */
.auto-layout-horizontal {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: var(--spacing-md);
}

.auto-layout-vertical {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--spacing-md);
}

/* Figma Constraints → CSS 定位 */
.constraint-left-right {
  width: 100%;
}

.constraint-top-bottom {
  height: 100%;
}

.constraint-center {
  margin: 0 auto;
}
```

---

## ⚡ 性能优化规范

### 图片优化
```vue
<template>
  <!-- 懒加载 + 响应式图片 -->
  <el-image
    :src="imageUrl"
    :lazy="true"
    fit="cover"
    :preview-src-list="allImages"
    placeholder="加载中..."
  >
    <template #error>
      <div class="image-error">
        <i class="fas fa-image"></i>
        <span>暂无图片</span>
      </div>
    </template>
  </el-image>
</template>
```

### 组件懒加载
```javascript
// router/index.js
const routes = [
  {
    path: '/properties/:id',
    name: 'PropertyDetail',
    component: () => import('@/views/PropertyDetail.vue') // 懒加载
  }
]
```

---

## 🚨 重要注意事项

### 1. 必须遵循的模式
- ✅ **统一设计令牌**: 所有颜色、间距、字体必须使用 CSS 变量
- ✅ **移动端优先**: 始终从移动端样式开始，再适配大屏
- ✅ **580px 标准**: 房源卡片和搜索区域宽度标准
- ✅ **JUWO 品牌色**: 所有主要操作使用 `var(--juwo-primary)`

### 2. 避免的反模式  
- ❌ **硬编码样式值**: 不要使用固定的 `#FF5824` 等颜色值
- ❌ **不一致的间距**: 不要使用任意的 margin/padding 值
- ❌ **破坏响应式**: 不要使用固定宽度破坏移动端布局
- ❌ **忽略无障碍**: 必须包含 alt 文本和语义化标签

### 3. Element Plus 集成
```javascript
// 正确的 Element Plus 主题定制
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
app.use(ElementPlus)

// CSS 变量会自动覆盖 Element Plus 默认主题
```

---

## 📚 参考资源

- **Vue 3 官方文档**: https://vuejs.org/
- **Element Plus 组件库**: https://element-plus.org/
- **Font Awesome 图标**: https://fontawesome.com/
- **项目 Memory Bank**: 查看 `memory-bank/` 文件夹获取最新进展

---

**维护说明**: 此文档随项目演进持续更新，任何设计系统变更都应反映在这里。