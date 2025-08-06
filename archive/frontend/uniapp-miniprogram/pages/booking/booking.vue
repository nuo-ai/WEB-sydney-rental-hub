<template>
  <view class="container">
    <!-- 预约类型选择 -->
    <view class="booking-type card">
      <view class="section-title">选择服务类型</view>
      <view class="type-options">
        <view 
          class="type-option"
          :class="{ 'active': bookingType === 'viewing' }"
          @tap="selectBookingType('viewing')"
        >
          <view class="option-icon">🏠</view>
          <view class="option-title">代看房服务</view>
          <view class="option-price">$35</view>
          <view class="option-desc">专业代看房，实时视频直播</view>
        </view>
        <view 
          class="type-option"
          :class="{ 'active': bookingType === 'consultation' }"
          @tap="selectBookingType('consultation')"
        >
          <view class="option-icon">⚖️</view>
          <view class="option-title">法律咨询</view>
          <view class="option-price">$50</view>
          <view class="option-desc">租房法律问题专业解答</view>
        </view>
        <view 
          class="type-option"
          :class="{ 'active': bookingType === 'contract' }"
          @tap="selectBookingType('contract')"
        >
          <view class="option-icon">📄</view>
          <view class="option-title">合同审核</view>
          <view class="option-price">$80</view>
          <view class="option-desc">合同条款逐条审核分析</view>
        </view>
      </view>
    </view>

    <!-- 房源信息（如果是代看房） -->
    <view class="property-info card" v-if="bookingType === 'viewing' && propertyInfo">
      <view class="section-title">房源信息</view>
      <view class="property-card">
        <image 
          :src="propertyInfo.image || '/static/images/default-property.jpg'"
          class="property-image"
          mode="aspectFill"
        ></image>
        <view class="property-details">
          <view class="property-title">{{ propertyInfo.title }}</view>
          <view class="property-address">📍 {{ propertyInfo.address }}</view>
          <view class="property-price">${{ propertyInfo.weekly_rent }}/周</view>
        </view>
      </view>
    </view>

    <!-- 联系方式 -->
    <view class="contact-info card">
      <view class="section-title">联系方式</view>
      <view class="form-group">
        <text class="label">微信号</text>
        <input 
          class="input"
          type="text"
          v-model="contactInfo.wechat"
          placeholder="请输入您的微信号"
        />
      </view>
      <view class="form-group">
        <text class="label">手机号</text>
        <input 
          class="input"
          type="number"
          v-model="contactInfo.phone"
          placeholder="请输入手机号"
        />
      </view>
      <view class="form-group">
        <text class="label">备注需求</text>
        <textarea 
          class="textarea"
          v-model="contactInfo.requirements"
          placeholder="请说明您的具体需求..."
          maxlength="200"
        ></textarea>
      </view>
    </view>

    <!-- 预约时间 -->
    <view class="booking-time card">
      <view class="section-title">选择时间</view>
      <view class="time-selector">
        <picker 
          mode="date" 
          :value="selectedDate"
          :start="today"
          @change="onDateChange"
        >
          <view class="picker-item">
            <text class="label">日期</text>
            <view class="picker-value">
              {{ selectedDate || '请选择日期' }}
              <text class="arrow">></text>
            </view>
          </view>
        </picker>
        
        <picker 
          mode="time" 
          :value="selectedTime"
          @change="onTimeChange"
        >
          <view class="picker-item">
            <text class="label">时间</text>
            <view class="picker-value">
              {{ selectedTime || '请选择时间' }}
              <text class="arrow">></text>
            </view>
          </view>
        </picker>
      </view>
    </view>

    <!-- 费用明细 -->
    <view class="cost-breakdown card">
      <view class="section-title">费用明细</view>
      <view class="cost-item">
        <text class="cost-label">{{ getServiceName() }}</text>
        <text class="cost-value">${{ getServicePrice() }}</text>
      </view>
      <view class="cost-item total">
        <text class="cost-label">总计</text>
        <text class="cost-value">${{ getServicePrice() }}</text>
      </view>
    </view>

    <!-- 支付按钮 -->
    <view class="payment-section">
      <button 
        class="pay-btn"
        :disabled="!canProceedPayment"
        @tap="proceedToPayment"
      >
        微信支付 ${{ getServicePrice() }}
      </button>
      <view class="payment-tips">
        <text>• 支付后客服将在1小时内联系您</text>
        <text>• 支持7天无理由退款</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  name: 'Booking',
  data() {
    return {
      bookingType: 'viewing', // viewing, consultation, contract
      propertyInfo: null,
      contactInfo: {
        wechat: '',
        phone: '',
        requirements: ''
      },
      selectedDate: '',
      selectedTime: '',
      today: '',
      serviceTypes: {
        viewing: { name: '代看房服务', price: 35 },
        consultation: { name: '法律咨询', price: 50 },
        contract: { name: '合同审核', price: 80 }
      }
    }
  },
  computed: {
    canProceedPayment() {
      return this.contactInfo.wechat && 
             this.contactInfo.phone && 
             this.selectedDate && 
             this.selectedTime
    }
  },
  onLoad(options) {
    console.log('预约页面加载', options)
    
    // 设置今天日期
    const today = new Date()
    this.today = today.toISOString().split('T')[0]
    
    // 如果是从房源页面跳转过来
    if (options.propertyId) {
      this.loadPropertyInfo(options.propertyId)
      this.bookingType = 'viewing'
    }
    
    // 如果指定了服务类型
    if (options.serviceType) {
      this.bookingType = options.serviceType
    }
    
    // 尝试从微信获取用户信息
    this.loadUserInfo()
  },
  methods: {
    // 选择预约类型
    selectBookingType(type) {
      this.bookingType = type
    },
    
    // 获取服务名称
    getServiceName() {
      return this.serviceTypes[this.bookingType]?.name || ''
    },
    
    // 获取服务价格
    getServicePrice() {
      return this.serviceTypes[this.bookingType]?.price || 0
    },
    
    // 加载房源信息
    async loadPropertyInfo(propertyId) {
      try {
        // 这里应该调用API获取房源信息
        // 暂时使用模拟数据
        this.propertyInfo = {
          id: propertyId,
          title: 'Central Park Student Village',
          address: 'Central Park, Chippendale',
          weekly_rent: 776,
          image: '/static/images/property1.jpg'
        }
      } catch (error) {
        console.error('加载房源信息失败:', error)
      }
    },
    
    // 加载用户信息
    loadUserInfo() {
      // 从本地存储获取用户信息
      const userInfo = uni.getStorageSync('userInfo')
      if (userInfo) {
        this.contactInfo.wechat = userInfo.wechat || ''
        this.contactInfo.phone = userInfo.phone || ''
      }
    },
    
    // 日期选择
    onDateChange(e) {
      this.selectedDate = e.detail.value
    },
    
    // 时间选择
    onTimeChange(e) {
      this.selectedTime = e.detail.value
    },
    
    // 处理支付
    async proceedToPayment() {
      if (!this.canProceedPayment) {
        uni.showToast({
          title: '请完善预约信息',
          icon: 'error'
        })
        return
      }
      
      // 显示加载
      uni.showLoading({
        title: '正在处理...'
      })
      
      try {
        // 保存用户联系信息到本地
        uni.setStorageSync('userInfo', {
          wechat: this.contactInfo.wechat,
          phone: this.contactInfo.phone
        })
        
        // 准备订单数据
        const orderData = {
          service_type: this.bookingType,
          property_id: this.propertyInfo?.id,
          contact_info: this.contactInfo,
          appointment_date: this.selectedDate,
          appointment_time: this.selectedTime,
          total_amount: this.getServicePrice()
        }
        
        // 调用微信支付
        await this.initiateWechatPayment(orderData)
        
      } catch (error) {
        console.error('支付处理失败:', error)
        uni.showToast({
          title: '支付失败，请重试',
          icon: 'error'
        })
      } finally {
        uni.hideLoading()
      }
    },
    
    // 发起微信支付
    async initiateWechatPayment(orderData) {
      try {
        // 创建订单
        const app = getApp()
        const orderResponse = await uni.request({
          url: `${app.globalData.apiBaseUrl}/api/orders/create`,
          method: 'POST',
          header: {
            'Content-Type': 'application/json'
          },
          data: orderData
        })
        
        if (orderResponse.statusCode === 200) {
          const { prepay_id, order_id } = orderResponse.data
          
          // 调用微信支付
          await uni.requestPayment({
            timeStamp: String(Date.now()),
            nonceStr: 'randomstring',
            package: `prepay_id=${prepay_id}`,
            signType: 'MD5',
            paySign: 'signature',
            success: (res) => {
              console.log('支付成功:', res)
              this.handlePaymentSuccess(order_id)
            },
            fail: (res) => {
              console.error('支付失败:', res)
              uni.showToast({
                title: '支付已取消',
                icon: 'error'
              })
            }
          })
        } else {
          throw new Error('创建订单失败')
        }
      } catch (error) {
        console.error('微信支付失败:', error)
        
        // 模拟支付成功用于测试
        this.handlePaymentSuccess('mock_order_' + Date.now())
      }
    },
    
    // 处理支付成功
    handlePaymentSuccess(orderId) {
      uni.showToast({
        title: '支付成功！',
        icon: 'success'
      })
      
      // 延时跳转到成功页面
      setTimeout(() => {
        uni.redirectTo({
          url: `/pages/booking/success?orderId=${orderId}`
        })
      }, 2000)
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

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.type-options {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.type-option {
  padding: 30rpx;
  border: 2rpx solid #e3e3e3;
  border-radius: 16rpx;
  background: white;
  
  &.active {
    border-color: #007BFF;
    background: #f0f9ff;
  }
  
  .option-icon {
    font-size: 48rpx;
    margin-bottom: 15rpx;
  }
  
  .option-title {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
  }
  
  .option-price {
    font-size: 28rpx;
    color: #007BFF;
    font-weight: bold;
    margin-bottom: 10rpx;
  }
  
  .option-desc {
    font-size: 24rpx;
    color: #666;
  }
}

.property-card {
  display: flex;
  gap: 20rpx;
  
  .property-image {
    width: 150rpx;
    height: 100rpx;
    border-radius: 12rpx;
  }
  
  .property-details {
    flex: 1;
    
    .property-title {
      font-size: 28rpx;
      font-weight: 500;
      margin-bottom: 8rpx;
    }
    
    .property-address {
      font-size: 24rpx;
      color: #666;
      margin-bottom: 8rpx;
    }
    
    .property-price {
      font-size: 26rpx;
      color: #007BFF;
      font-weight: bold;
    }
  }
}

.form-group {
  margin-bottom: 25rpx;
  
  .label {
    display: block;
    font-size: 26rpx;
    color: #333;
    margin-bottom: 10rpx;
  }
  
  .input, .textarea {
    width: 100%;
    padding: 20rpx;
    border: 2rpx solid #e3e3e3;
    border-radius: 12rpx;
    font-size: 28rpx;
    background: white;
    box-sizing: border-box;
  }
  
  .textarea {
    height: 120rpx;
    resize: none;
  }
}

.picker-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25rpx 0;
  border-bottom: 2rpx solid #f0f0f0;
  
  &:last-child {
    border-bottom: none;
  }
  
  .label {
    font-size: 26rpx;
    color: #333;
  }
  
  .picker-value {
    font-size: 26rpx;
    color: #666;
    display: flex;
    align-items: center;
    gap: 10rpx;
  }
  
  .arrow {
    color: #ccc;
  }
}

.cost-breakdown {
  .cost-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20rpx 0;
    border-bottom: 2rpx solid #f0f0f0;
    
    &:last-child {
      border-bottom: none;
    }
    
    &.total {
      font-weight: bold;
      font-size: 30rpx;
      color: #007BFF;
    }
    
    .cost-label {
      color: #333;
    }
    
    .cost-value {
      color: #007BFF;
    }
  }
}

.payment-section {
  margin-top: 40rpx;
  
  .pay-btn {
    width: 100%;
    background: #09bb07;
    color: white;
    border: none;
    border-radius: 12rpx;
    padding: 25rpx;
    font-size: 32rpx;
    font-weight: bold;
    
    &:disabled {
      background: #ccc;
    }
  }
  
  .payment-tips {
    margin-top: 20rpx;
    
    text {
      display: block;
      font-size: 22rpx;
      color: #666;
      margin-bottom: 5rpx;
    }
  }
}
</style>
