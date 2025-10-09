<template>
  <view class="container">
    <view class="header">
      <text class="title">悉尼租房小程序</text>
      <text class="subtitle">Design System Demo</text>
    </view>
    
    <!-- Property Card Demo -->
    <view class="section">
      <text class="section-title">房源卡片组件</text>
      <PropertyCard 
        :property="sampleProperty"
        @favorite="handleFavorite"
        @contact="handleContact"
      />
    </view>
    
    <!-- Button Components Demo -->
    <view class="section">
      <text class="section-title">按钮组件</text>
      <view class="button-group">
        <button class="btn btn-primary">主要按钮</button>
        <button class="btn btn-secondary">次要按钮</button>
        <button class="btn btn-ghost">幽灵按钮</button>
        <button class="btn btn-danger">危险按钮</button>
      </view>
    </view>
    
    <!-- Input Components Demo -->
    <view class="section">
      <text class="section-title">输入组件</text>
      <view class="input-group">
        <input class="input" placeholder="请输入搜索内容" />
        <textarea class="textarea" placeholder="请输入详细描述"></textarea>
        <picker class="select" mode="selector" :range="['选项1', '选项2', '选项3']">
          <view class="picker">请选择</view>
        </picker>
      </view>
    </view>
  </view>
</template>

<script>
import PropertyCard from '../../components/PropertyCard/PropertyCard.vue'

export default {
  components: {
    PropertyCard
  },
  data() {
    return {
      sampleProperty: {
        id: 1,
        title: "市中心豪华公寓",
        address: "悉尼市中心 George Street 123号",
        price: 850,
        bedrooms: 2,
        bathrooms: 1,
        parking: 1,
        area: 85,
        images: ["https://example.com/image1.jpg"],
        isFurnished: true,
        availableDate: "2025-11-01",
        features: ["洗衣机", "烘干机", "空调", "WiFi"]
      }
    }
  },
  methods: {
    handleFavorite(propertyId) {
      console.log('收藏房源:', propertyId)
      // 这里可以调用收藏功能
    },
    handleContact(propertyId) {
      console.log('联系房东:', propertyId)
      // 这里可以调用联系功能
    }
  }
}
</script>

<style scoped>
.container {
  padding: var(--space-lg);
  background-color: var(--color-semantic-bg-page);
}

.header {
  text-align: center;
  margin-bottom: var(--space-xl);
}

.title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-semantic-text-primary);
  margin-bottom: var(--space-sm);
}

.subtitle {
  font-size: var(--font-size-md);
  color: var(--color-semantic-text-secondary);
}

.section {
  margin-bottom: var(--space-xl);
}

.section-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-semantic-text-primary);
  margin-bottom: var(--space-md);
  display: block;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.btn {
  height: 80rpx;
  border-radius: var(--radius-sm);
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-medium);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-sm);
}

.btn-primary {
  background-color: var(--component-button-primary-bg);
  color: var(--component-button-primary-color);
  border: 2rpx solid var(--component-button-primary-border);
}

.btn-secondary {
  background-color: var(--component-button-secondary-bg);
  color: var(--component-button-secondary-color);
  border: 2rpx solid var(--component-button-secondary-border);
}

.btn-ghost {
  background-color: var(--component-button-ghost-bg);
  color: var(--component-button-ghost-color);
  border: none;
}

.btn-danger {
  background-color: var(--component-button-danger-bg);
  color: var(--component-button-danger-color);
  border: 2rpx solid var(--component-button-danger-border);
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.input {
  height: 80rpx;
  padding: 0 var(--space-md);
  background-color: var(--component-input-background-color);
  border: 2rpx solid var(--color-semantic-border-default);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-md);
  color: var(--component-input-color);
}

.textarea {
  min-height: 160rpx;
  padding: var(--space-md);
  background-color: var(--component-textarea-background-color);
  border: 2rpx solid var(--color-semantic-border-default);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-md);
  color: var(--component-textarea-color);
  font-family: var(--font-family-base);
}

.select {
  height: 80rpx;
  padding: 0 var(--space-md);
  background-color: var(--component-select-background-color);
  border: 2rpx solid var(--color-semantic-border-default);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-md);
  color: var(--component-select-color);
  display: flex;
  align-items: center;
}

.picker {
  flex: 1;
}
</style>
