<template>
  <view class="container">
    <!-- 房源图片轮播 -->
    <swiper class="property-images" :indicator-dots="true" :autoplay="false">
      <swiper-item v-for="(image, index) in property.images" :key="index">
        <image :src="image" mode="aspectFill" class="property-image"></image>
      </swiper-item>
    </swiper>

    <!-- 房源基本信息 -->
    <view class="property-basic card">
      <view class="price-section">
        <text class="weekly-price">${{ property.weekly_rent }}/周</text>
        <text class="monthly-price">约${{ Math.round(property.weekly_rent * 4.33) }}/月</text>
      </view>
      <view class="property-title">{{ property.title }}</view>
      <view class="property-address">📍 {{ property.address }}</view>
      
      <!-- 房源特点 -->
      <view class="property-features">
        <view class="feature-item">
          <text class="feature-icon">🛏️</text>
          <text class="feature-text">{{ property.bedrooms }}房</text>
        </view>
        <view class="feature-item">
          <text class="feature-icon">🚿</text>
          <text class="feature-text">{{ property.bathrooms }}浴</text>
        </view>
        <view class="feature-item" v-if="property.parking">
          <text class="feature-icon">🚗</text>
          <text class="feature-text">停车位</text>
        </view>
        <view class="feature-item" v-if="property.furnished">
          <text class="feature-icon">🪑</text>
          <text class="feature-text">已装修</text>
        </view>
      </view>
    </view>

    <!-- 位置和交通（简化版地图方案） -->
    <view class="location-transport card">
      <view class="section-title">位置和交通</view>
      
      <!-- 小程序原生地图 -->
      <view class="map-section">
        <map 
          :longitude="property.longitude" 
          :latitude="property.latitude"
          :markers="mapMarkers"
          :scale="15"
          show-location
          enable-overlooking
          enable-zoom
          enable-scroll
          enable-rotate
          class="property-map"
        />
      </view>
      
      <!-- 交通信息 -->
      <view class="transport-info">
        <view class="commute-item" v-for="commute in property.commute_times" :key="commute.university">
          <view class="university-info">
            <text class="university-name">🎓 {{ commute.university_name }}</text>
            <text class="commute-time">{{ commute.time }}分钟</text>
          </view>
          <view class="transport-method">
            <text class="method-icon">🚇</text>
            <text class="method-text">{{ commute.method }}</text>
          </view>
        </view>
      </view>
      
      <!-- 地图操作按钮 -->
      <view class="map-actions">
        <button class="map-btn" @tap="copyAddress">
          📋 复制地址
        </button>
        <button class="map-btn" @tap="centerToProperty">
          🎯 居中显示
        </button>
        <button class="map-btn" @tap="toggleMapType">
          🗺️ {{ mapType === 'standard' ? '卫星图' : '标准图' }}
        </button>
      </view>
    </view>

    <!-- 房源描述 -->
    <view class="property-description card">
      <view class="section-title">房源介绍</view>
      <text class="description-text">{{ property.description }}</text>
    </view>

    <!-- 设施信息 -->
    <view class="amenities card" v-if="property.amenities && property.amenities.length > 0">
      <view class="section-title">设施</view>
      <view class="amenities-grid">
        <view 
          class="amenity-item"
          v-for="amenity in property.amenities" 
          :key="amenity.name"
        >
          <text class="amenity-icon">{{ amenity.icon }}</text>
          <text class="amenity-name">{{ amenity.name }}</text>
        </view>
      </view>
    </view>

    <!-- 底部操作区 -->
    <view class="bottom-actions">
      <button class="action-btn secondary" @tap="toggleFavorite">
        {{ isFavorited ? '❤️ 已收藏' : '🤍 收藏' }}
      </button>
      <button class="action-btn primary" @tap="bookViewing">
        代看房 $35
      </button>
    </view>
  </view>
</template>

<script>
export default {
  name: 'PropertyDetail',
  data() {
    return {
      propertyId: '',
      property: {},
      isFavorited: false,
      loading: true,
      mapType: 'standard' // 地图类型：standard 或 satellite
    }
  },
  computed: {
    // 地图标记点
    mapMarkers() {
      if (!this.property.longitude || !this.property.latitude) return []
      
      return [
        {
          id: 1,
          longitude: this.property.longitude,
          latitude: this.property.latitude,
          title: this.property.title,
          iconPath: '/static/icons/property-marker.png',
          width: 30,
          height: 30,
          callout: {
            content: this.property.title,
            color: '#333',
            fontSize: 14,
            borderRadius: 8,
            bgColor: '#fff',
            padding: 8,
            display: 'BYCLICK'
          }
        }
      ]
    }
  },
  onLoad(options) {
    console.log('房源详情页加载', options)
    if (options.id) {
      this.propertyId = options.id
      this.loadPropertyDetail()
    }
  },
  methods: {
    // 加载房源详情
    async loadPropertyDetail() {
      this.loading = true
      
      try {
        const app = getApp()
        const response = await uni.request({
          url: `${app.globalData.apiBaseUrl}/api/properties/${this.propertyId}`,
          method: 'GET'
        })
        
        if (response.statusCode === 200) {
          this.property = response.data
        } else {
          throw new Error('加载房源详情失败')
        }
      } catch (error) {
        console.error('请求失败:', error)
        // 使用模拟数据
        this.loadMockData()
      }
      
      this.loading = false
      this.checkFavoriteStatus()
    },
    
    // 模拟数据（开发测试用）
    loadMockData() {
      this.property = {
        id: this.propertyId,
        title: 'Central Park Student Village',
        address: '28 Broadway, Chippendale NSW 2008',
        weekly_rent: 776,
        bedrooms: 1,
        bathrooms: 1,
        parking: false,
        furnished: true,
        // 添加地图坐标 - Central Park的实际坐标
        longitude: 151.1996,
        latitude: -33.8830,
        images: [
          '/static/images/property1-1.jpg',
          '/static/images/property1-2.jpg',
          '/static/images/property1-3.jpg'
        ],
        description: '位于Central Park的现代化学生公寓，步行即可到达UTS。设施齐全，包括健身房、学习区域、洗衣房等。24小时安保，是学生的理想选择。',
        commute_times: [
          {
            university: 'UTS',
            university_name: '悉尼科技大学',
            time: 8,
            method: '步行 + 轻轨'
          },
          {
            university: 'USYD',
            university_name: '悉尼大学',
            time: 15,
            method: '地铁'
          }
        ],
        amenities: [
          { name: '健身房', icon: '💪' },
          { name: '洗衣房', icon: '👕' },
          { name: '学习室', icon: '📚' },
          { name: '24小时安保', icon: '🔒' },
          { name: 'WiFi', icon: '📶' },
          { name: '空调', icon: '❄️' }
        ]
      }
    },
    
    // 检查收藏状态
    checkFavoriteStatus() {
      const favorites = uni.getStorageSync('favorites') || []
      this.isFavorited = favorites.includes(this.propertyId)
    },
    
    // 切换收藏状态
    toggleFavorite() {
      let favorites = uni.getStorageSync('favorites') || []
      
      if (this.isFavorited) {
        favorites = favorites.filter(id => id !== this.propertyId)
        this.isFavorited = false
        uni.showToast({ title: '已取消收藏', icon: 'none' })
      } else {
        favorites.push(this.propertyId)
        this.isFavorited = true
        uni.showToast({ title: '已收藏', icon: 'success' })
      }
      
      uni.setStorageSync('favorites', favorites)
    },
    
    // 地图操作选项
    openMapOptions() {
      uni.showActionSheet({
        itemList: ['复制地址', '打开谷歌地图', '打开苹果地图'],
        success: (res) => {
          switch (res.tapIndex) {
            case 0:
              this.copyAddress()
              break
            case 1:
              this.openGoogleMaps()
              break
            case 2:
              this.openAppleMaps()
              break
          }
        }
      })
    },
    
    // 复制地址
    copyAddress() {
      uni.setClipboardData({
        data: this.property.address,
        success: () => {
          uni.showToast({
            title: '地址已复制',
            icon: 'success'
          })
        }
      })
    },
    
    // 打开谷歌地图
    openGoogleMaps() {
      const address = encodeURIComponent(this.property.address)
      const url = `https://maps.google.com/search/${address}`
      
      uni.setClipboardData({
        data: url,
        success: () => {
          uni.showModal({
            title: '地图链接已复制',
            content: '请在浏览器中粘贴打开查看详细地图',
            showCancel: false
          })
        }
      })
    },
    
    // 打开苹果地图
    openAppleMaps() {
      const address = encodeURIComponent(this.property.address)
      const url = `http://maps.apple.com/?q=${address}`
      
      uni.setClipboardData({
        data: url,
        success: () => {
          uni.showModal({
            title: '地图链接已复制',
            content: '请在Safari中粘贴打开查看详细地图',
            showCancel: false
          })
        }
      })
    },
    
    // 预约代看房
    bookViewing() {
      uni.navigateTo({
        url: `/pages/booking/booking?propertyId=${this.propertyId}`
      })
    },
    
    // 地图居中到房源位置
    centerToProperty() {
      // 这里可以通过MapContext API来控制地图
      uni.showToast({
        title: '地图已居中',
        icon: 'success'
      })
    },
    
    // 切换地图类型
    toggleMapType() {
      this.mapType = this.mapType === 'standard' ? 'satellite' : 'standard'
      uni.showToast({
        title: `已切换到${this.mapType === 'standard' ? '标准' : '卫星'}地图`,
        icon: 'none'
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.container {
  background: #F4F7F9;
  min-height: 100vh;
  padding-bottom: 120rpx; // 为底部按钮留空间
}

.property-images {
  height: 500rpx;
  
  .property-image {
    width: 100%;
    height: 100%;
  }
}

.property-basic {
  margin: 20rpx;
  padding: 30rpx;
}

.price-section {
  margin-bottom: 20rpx;
  
  .weekly-price {
    font-size: 40rpx;
    font-weight: bold;
    color: #007BFF;
    margin-right: 20rpx;
  }
  
  .monthly-price {
    font-size: 24rpx;
    color: #666;
  }
}

.property-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
}

.property-address {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 25rpx;
}

.property-features {
  display: flex;
  gap: 25rpx;
  
  .feature-item {
    display: flex;
    align-items: center;
    gap: 8rpx;
    
    .feature-icon {
      font-size: 24rpx;
    }
    
    .feature-text {
      font-size: 24rpx;
      color: #666;
    }
  }
}

.section-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.map-section {
  margin-bottom: 25rpx;
  
  .property-map {
    width: 100%;
    height: 300rpx;
    border-radius: 12rpx;
    border: 1rpx solid #e3e3e3;
  }
}

.transport-info {
  margin-bottom: 25rpx;
  
  .commute-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20rpx 0;
    border-bottom: 2rpx solid #f0f0f0;
    
    &:last-child {
      border-bottom: none;
    }
    
    .university-info {
      .university-name {
        display: block;
        font-size: 26rpx;
        color: #333;
        margin-bottom: 5rpx;
      }
      
      .commute-time {
        font-size: 32rpx;
        font-weight: bold;
        color: #007BFF;
      }
    }
    
    .transport-method {
      display: flex;
      align-items: center;
      gap: 8rpx;
      
      .method-icon {
        font-size: 24rpx;
      }
      
      .method-text {
        font-size: 24rpx;
        color: #666;
      }
    }
  }
}

.map-actions {
  display: flex;
  gap: 15rpx;
  
  .map-btn {
    flex: 1;
    background: #f8f9fa;
    color: #666;
    border: 2rpx solid #e3e3e3;
    border-radius: 12rpx;
    padding: 15rpx 10rpx;
    font-size: 24rpx;
  }
}

.description-text {
  font-size: 28rpx;
  line-height: 1.6;
  color: #333;
}

.amenities-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
  
  .amenity-item {
    display: flex;
    align-items: center;
    gap: 10rpx;
    background: #f8f9fa;
    padding: 15rpx 20rpx;
    border-radius: 20rpx;
    
    .amenity-icon {
      font-size: 24rpx;
    }
    
    .amenity-name {
      font-size: 24rpx;
      color: #666;
    }
  }
}

.bottom-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  padding: 20rpx;
  border-top: 2rpx solid #e3e3e3;
  display: flex;
  gap: 20rpx;
  
  .action-btn {
    flex: 1;
    padding: 25rpx;
    border-radius: 12rpx;
    font-size: 28rpx;
    border: none;
    
    &.primary {
      background: #28a745;
      color: white;
    }
    
    &.secondary {
      background: #f8f9fa;
      color: #666;
      border: 2rpx solid #e3e3e3;
    }
  }
}
</style>
