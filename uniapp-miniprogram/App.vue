<template>
  <view id="app">
    <!-- 全局样式应用 -->
  </view>
</template>

<script>
export default {
  name: 'App',
  onLaunch: function() {
    console.log('悉尼租房助手小程序启动')
    
    // 检查微信登录状态
    this.checkLoginStatus()
    
    // 初始化全局配置
    this.initGlobalConfig()
  },
  onShow: function() {
    console.log('应用显示')
  },
  onHide: function() {
    console.log('应用隐藏')
  },
  methods: {
    // 检查登录状态
    checkLoginStatus() {
      const token = uni.getStorageSync('userToken')
      if (!token) {
        console.log('用户未登录')
      } else {
        console.log('用户已登录')
      }
    },
    
    // 初始化全局配置
    initGlobalConfig() {
      // 设置API基础URL
      getApp().globalData = {
        apiBaseUrl: 'http://localhost:8000',  // 开发环境
        // apiBaseUrl: 'https://your-api-domain.com',  // 生产环境
        userInfo: null,
        isLoggedIn: false
      }
    }
  }
}
</script>

<style lang="scss">
/* 全局样式 */
@import '@/static/styles/common.scss';

/* 重置默认样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

page {
  background-color: #F4F7F9;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* 通用类 */
.container {
  padding: 20rpx;
}

.card {
  background: #fff;
  border-radius: 16rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
  margin-bottom: 20rpx;
}

.btn-primary {
  background: #007BFF;
  color: #fff;
  border: none;
  border-radius: 12rpx;
  padding: 16rpx 32rpx;
  font-size: 28rpx;
}

.btn-secondary {
  background: #6c757d;
  color: #fff;
  border: none;
  border-radius: 12rpx;
  padding: 16rpx 32rpx;
  font-size: 28rpx;
}

.text-primary {
  color: #007BFF;
}

.text-secondary {
  color: #6c757d;
}

.text-center {
  text-align: center;
}

.flex {
  display: flex;
}

.flex-column {
  flex-direction: column;
}

.justify-center {
  justify-content: center;
}

.align-center {
  align-items: center;
}

.space-between {
  justify-content: space-between;
}

.mt-10 { margin-top: 20rpx; }
.mt-15 { margin-top: 30rpx; }
.mt-20 { margin-top: 40rpx; }
.mb-10 { margin-bottom: 20rpx; }
.mb-15 { margin-bottom: 30rpx; }
.mb-20 { margin-bottom: 40rpx; }
.p-10 { padding: 20rpx; }
.p-15 { padding: 30rpx; }
.p-20 { padding: 40rpx; }
</style>
