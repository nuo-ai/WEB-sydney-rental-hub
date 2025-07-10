<template>
  <view class="container">
    <!-- 用户信息区域 -->
    <view class="user-info card">
      <view class="user-avatar">
        <image 
          :src="userInfo.avatar || '/static/images/default-avatar.png'"
          class="avatar-img"
          mode="aspectFill"
        ></image>
      </view>
      <view class="user-details">
        <view class="user-name">{{ userInfo.nickname || '微信用户' }}</view>
        <view class="user-phone">{{ userInfo.phone || '未绑定手机号' }}</view>
        <button v-if="!isLoggedIn" class="login-btn" @tap="loginWithWechat">
          微信登录
        </button>
      </view>
    </view>

    <!-- 我的订单 -->
    <view class="my-orders card">
      <view class="section-title">我的订单</view>
      <view class="order-types">
        <view class="order-type" @tap="viewOrders('viewing')">
          <view class="type-icon">🏠</view>
          <view class="type-name">代看房</view>
          <view class="type-count">{{ orderCounts.viewing }}</view>
        </view>
        <view class="order-type" @tap="viewOrders('consultation')">
          <view class="type-icon">⚖️</view>
          <view class="type-name">法律咨询</view>
          <view class="type-count">{{ orderCounts.consultation }}</view>
        </view>
        <view class="order-type" @tap="viewOrders('contract')">
          <view class="type-icon">📄</view>
          <view class="type-name">合同审核</view>
          <view class="type-count">{{ orderCounts.contract }}</view>
        </view>
        <view class="order-type" @tap="viewOrders('all')">
          <view class="type-icon">📋</view>
          <view class="type-name">全部订单</view>
          <view class="type-count">{{ orderCounts.total }}</view>
        </view>
      </view>
    </view>

    <!-- 我的收藏 -->
    <view class="my-favorites card">
      <view class="section-title">我的收藏</view>
      <view class="favorites-preview" v-if="favoriteProperties.length > 0">
        <view 
          class="favorite-item"
          v-for="property in favoriteProperties.slice(0, 3)" 
          :key="property.id"
          @tap="viewPropertyDetail(property.id)"
        >
          <image 
            :src="property.image || '/static/images/default-property.jpg'"
            class="property-image"
            mode="aspectFill"
          ></image>
          <view class="property-info">
            <view class="property-title">{{ property.title }}</view>
            <view class="property-price">${{ property.weekly_rent }}/周</view>
          </view>
        </view>
      </view>
      <view class="no-favorites" v-else>
        <text>暂无收藏房源</text>
        <button class="browse-btn" @tap="goToIndex">去逛逛</button>
      </view>
    </view>

    <!-- 功能菜单 -->
    <view class="function-menu card">
      <view class="menu-item" @tap="contactCustomerService">
        <view class="menu-icon">💬</view>
        <view class="menu-text">联系客服</view>
        <view class="menu-arrow">></view>
      </view>
      <view class="menu-item" @tap="viewFeedback">
        <view class="menu-icon">📝</view>
        <view class="menu-text">意见反馈</view>
        <view class="menu-arrow">></view>
      </view>
      <view class="menu-item" @tap="viewAbout">
        <view class="menu-icon">ℹ️</view>
        <view class="menu-text">关于我们</view>
        <view class="menu-arrow">></view>
      </view>
      <view class="menu-item" @tap="viewSettings">
        <view class="menu-icon">⚙️</view>
        <view class="menu-text">设置</view>
        <view class="menu-arrow">></view>
      </view>
    </view>

    <!-- 退出登录 -->
    <view class="logout-section" v-if="isLoggedIn">
      <button class="logout-btn" @tap="logout">退出登录</button>
    </view>
  </view>
</template>

<script>
export default {
  name: 'Profile',
  data() {
    return {
      isLoggedIn: false,
      userInfo: {
        nickname: '',
        avatar: '',
        phone: ''
      },
      orderCounts: {
        viewing: 0,
        consultation: 0,
        contract: 0,
        total: 0
      },
      favoriteProperties: []
    }
  },
  onShow() {
    this.loadUserData()
    this.loadOrderCounts()
    this.loadFavoriteProperties()
  },
  methods: {
    // 微信登录
    async loginWithWechat() {
      try {
        // 获取微信登录授权
        const loginRes = await uni.login({
          provider: 'weixin'
        })
        
        if (loginRes.errMsg === 'login:ok') {
          // 获取用户信息授权
          const userInfoRes = await uni.getUserInfo({
            provider: 'weixin'
          })
          
          if (userInfoRes.errMsg === 'getUserInfo:ok') {
            const { nickName, avatarUrl } = userInfoRes.userInfo
            
            this.userInfo = {
              nickname: nickName,
              avatar: avatarUrl,
              phone: this.userInfo.phone
            }
            
            this.isLoggedIn = true
            
            // 保存到本地存储
            uni.setStorageSync('userInfo', this.userInfo)
            uni.setStorageSync('isLoggedIn', true)
            
            uni.showToast({
              title: '登录成功',
              icon: 'success'
            })
          }
        }
      } catch (error) {
        console.error('微信登录失败:', error)
        uni.showToast({
          title: '登录失败',
          icon: 'error'
        })
      }
    },
    
    // 加载用户数据
    loadUserData() {
      const savedUserInfo = uni.getStorageSync('userInfo')
      const savedLoginStatus = uni.getStorageSync('isLoggedIn')
      
      if (savedUserInfo) {
        this.userInfo = savedUserInfo
      }
      
      if (savedLoginStatus) {
        this.isLoggedIn = savedLoginStatus
      }
    },
    
    // 加载订单数量
    async loadOrderCounts() {
      try {
        const app = getApp()
        const response = await uni.request({
          url: `${app.globalData.apiBaseUrl}/api/orders/count`,
          method: 'GET',
          header: {
            'Authorization': `Bearer ${uni.getStorageSync('userToken')}`
          }
        })
        
        if (response.statusCode === 200) {
          this.orderCounts = response.data
        }
      } catch (error) {
        console.error('加载订单数量失败:', error)
        // 使用模拟数据
        this.orderCounts = {
          viewing: 2,
          consultation: 1,
          contract: 0,
          total: 3
        }
      }
    },
    
    // 加载收藏房源
    async loadFavoriteProperties() {
      try {
        const app = getApp()
        const response = await uni.request({
          url: `${app.globalData.apiBaseUrl}/api/favorites`,
          method: 'GET',
          header: {
            'Authorization': `Bearer ${uni.getStorageSync('userToken')}`
          }
        })
        
        if (response.statusCode === 200) {
          this.favoriteProperties = response.data.properties || []
        }
      } catch (error) {
        console.error('加载收藏房源失败:', error)
        // 使用模拟数据
        this.favoriteProperties = [
          {
            id: 1,
            title: 'Central Park Student Village',
            weekly_rent: 776,
            image: '/static/images/property1.jpg'
          }
        ]
      }
    },
    
    // 查看订单
    viewOrders(type) {
      uni.navigateTo({
        url: `/pages/orders/list?type=${type}`
      })
    },
    
    // 查看房源详情
    viewPropertyDetail(propertyId) {
      uni.navigateTo({
        url: `/pages/property/detail?id=${propertyId}`
      })
    },
    
    // 去首页逛逛
    goToIndex() {
      uni.switchTab({
        url: '/pages/index/index'
      })
    },
    
    // 联系客服
    contactCustomerService() {
      uni.switchTab({
        url: '/pages/chat/chat'
      })
    },
    
    // 意见反馈
    viewFeedback() {
      uni.showModal({
        title: '意见反馈',
        content: '请通过AI助手联系我们，我们会及时处理您的反馈',
        showCancel: false
      })
    },
    
    // 关于我们
    viewAbout() {
      uni.showModal({
        title: '关于我们',
        content: '悉尼租房助手 - 专为中国学生打造的租房平台\n版本：1.0.0',
        showCancel: false
      })
    },
    
    // 设置
    viewSettings() {
      uni.showModal({
        title: '设置',
        content: '设置功能正在开发中，敬请期待',
        showCancel: false
      })
    },
    
    // 退出登录
    logout() {
      uni.showModal({
        title: '确认退出',
        content: '确定要退出登录吗？',
        success: (res) => {
          if (res.confirm) {
            this.isLoggedIn = false
            this.userInfo = {
              nickname: '',
              avatar: '',
              phone: ''
            }
            
            uni.removeStorageSync('userInfo')
            uni.removeStorageSync('isLoggedIn')
            uni.removeStorageSync('userToken')
            
            uni.showToast({
              title: '已退出登录',
              icon: 'success'
            })
          }
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.container {
  padding: 20rpx;
  background: #F4F7F9;
  min-height: 100vh;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 30rpx;
  padding: 30rpx;
  
  .user-avatar {
    .avatar-img {
      width: 120rpx;
      height: 120rpx;
      border-radius: 50%;
    }
  }
  
  .user-details {
    flex: 1;
    
    .user-name {
      font-size: 32rpx;
      font-weight: bold;
      color: #333;
      margin-bottom: 10rpx;
    }
    
    .user-phone {
      font-size: 26rpx;
      color: #666;
      margin-bottom: 20rpx;
    }
    
    .login-btn {
      background: #007BFF;
      color: white;
      border: none;
      border-radius: 20rpx;
      padding: 15rpx 30rpx;
      font-size: 26rpx;
    }
  }
}

.section-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.order-types {
  display: flex;
  justify-content: space-between;
  
  .order-type {
    flex: 1;
    text-align: center;
    padding: 20rpx 10rpx;
    
    .type-icon {
      font-size: 40rpx;
      margin-bottom: 10rpx;
    }
    
    .type-name {
      font-size: 24rpx;
      color: #666;
      margin-bottom: 8rpx;
    }
    
    .type-count {
      font-size: 28rpx;
      font-weight: bold;
      color: #007BFF;
    }
  }
}

.favorites-preview {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
  
  .favorite-item {
    display: flex;
    gap: 20rpx;
    padding: 20rpx;
    background: #f8f9fa;
    border-radius: 12rpx;
    
    .property-image {
      width: 120rpx;
      height: 80rpx;
      border-radius: 8rpx;
    }
    
    .property-info {
      flex: 1;
      
      .property-title {
        font-size: 26rpx;
        color: #333;
        margin-bottom: 8rpx;
      }
      
      .property-price {
        font-size: 24rpx;
        color: #007BFF;
        font-weight: bold;
      }
    }
  }
}

.no-favorites {
  text-align: center;
  padding: 60rpx 20rpx;
  
  text {
    display: block;
    color: #666;
    margin-bottom: 30rpx;
  }
  
  .browse-btn {
    background: #007BFF;
    color: white;
    border: none;
    border-radius: 20rpx;
    padding: 15rpx 30rpx;
    font-size: 26rpx;
  }
}

.function-menu {
  .menu-item {
    display: flex;
    align-items: center;
    padding: 25rpx 0;
    border-bottom: 2rpx solid #f0f0f0;
    
    &:last-child {
      border-bottom: none;
    }
    
    .menu-icon {
      font-size: 36rpx;
      margin-right: 20rpx;
    }
    
    .menu-text {
      flex: 1;
      font-size: 28rpx;
      color: #333;
    }
    
    .menu-arrow {
      color: #ccc;
      font-size: 24rpx;
    }
  }
}

.logout-section {
  margin-top: 40rpx;
  
  .logout-btn {
    width: 100%;
    background: #dc3545;
    color: white;
    border: none;
    border-radius: 12rpx;
    padding: 25rpx;
    font-size: 28rpx;
  }
}
</style>
