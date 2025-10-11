<template>
  <view class="content">
    <image class="logo" src="/static/logo.png"></image>
    <view class="text-area">
      <text class="title">{{ title }}</text>
      <view style="margin-top: 16rpx;">
        <uni-badge text="uni-ui" type="primary" :inverted="true"></uni-badge>
      </view>
      <view style="margin-top: 24rpx;">
        <button type="primary" @click="gotoPreview">打开 Token 预览页</button>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      title: 'Hello uni-ui',
    }
  },
  onLoad() {},
  methods: {
    // 跳转到设计 Token 预览页（H5 可动态微调；小程序端静态展示）
    gotoPreview() {
      uni.navigateTo({ url: '/pages/tokens/preview' })
    }
  },
}
</script>

<style>
.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.logo {
  height: 200rpx;
  width: 200rpx;
  margin-top: 200rpx;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 50rpx;
}

.text-area {
  display: flex;
  justify-content: center;
}

.title {
  font-size: 36rpx;
  color: #8f8f94;
}
</style>
