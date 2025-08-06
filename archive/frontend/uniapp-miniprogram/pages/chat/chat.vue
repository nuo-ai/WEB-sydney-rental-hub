<template>
  <view class="chat-container">
    <!-- 聊天消息区域 -->
    <scroll-view 
      class="chat-messages" 
      scroll-y="true" 
      :scroll-top="scrollTop"
      scroll-with-animation="true"
    >
      <!-- 欢迎消息 -->
      <view class="message ai-message" v-if="messages.length === 0">
        <view class="message-content">
          <text class="welcome-text">您好！我是您的专属租房助手 🏠</text>
          <text class="help-text">我可以帮您：</text>
          <view class="help-list">
            <text>• 根据大学推荐房源</text>
            <text>• 安排$35代看房服务</text>
            <text>• 提供租房法律咨询</text>
            <text>• 合同审核服务</text>
          </view>
          <text class="question-prompt">请告诉我您在哪所大学上学？</text>
        </view>
      </view>

      <!-- 聊天消息列表 -->
      <view 
        class="message"
        :class="msg.type === 'user' ? 'user-message' : 'ai-message'"
        v-for="(msg, index) in messages" 
        :key="index"
      >
        <view class="message-content">
          <!-- 文本消息 -->
          <text v-if="msg.content_type === 'text'">{{ msg.content }}</text>
          
          <!-- 房源卡片 -->
          <view v-else-if="msg.content_type === 'property_card'" class="property-card-mini">
            <image 
              :src="msg.data.image || '/static/images/default-property.jpg'"
              class="property-image"
              mode="aspectFill"
            ></image>
            <view class="property-info">
              <view class="property-price">${{ msg.data.weekly_rent }}/周</view>
              <view class="property-title">{{ msg.data.title }}</view>
              <view class="property-address">{{ msg.data.address }}</view>
              <view class="property-commute" v-if="msg.data.commute_time">
                🚇 {{ msg.data.commute_time }}分钟
              </view>
              <view class="property-actions">
                <button 
                  class="action-btn primary"
                  @tap="bookPropertyViewing(msg.data.id)"
                >
                  代看房 $35
                </button>
                <button 
                  class="action-btn secondary"
                  @tap="viewPropertyDetail(msg.data.id)"
                >
                  查看详情
                </button>
              </view>
            </view>
          </view>
          
          <!-- 服务卡片 -->
          <view v-else-if="msg.content_type === 'service_card'" class="service-card-mini">
            <view class="service-title">{{ msg.data.title }}</view>
            <view class="service-description">{{ msg.data.description }}</view>
            <view class="service-price">${{ msg.data.price }}</view>
            <button 
              class="action-btn primary"
              @tap="bookService(msg.data.service_type)"
            >
              立即预约
            </button>
          </view>
        </view>
        
        <!-- 消息时间 -->
        <view class="message-time">{{ formatTime(msg.timestamp) }}</view>
      </view>

      <!-- 打字指示器 -->
      <view class="message ai-message" v-if="isTyping">
        <view class="message-content typing-indicator">
          <view class="typing-dot"></view>
          <view class="typing-dot"></view>
          <view class="typing-dot"></view>
        </view>
      </view>
    </scroll-view>

    <!-- 快捷建议按钮 -->
    <view class="quick-suggestions" v-if="showSuggestions">
      <view 
        class="suggestion-btn"
        v-for="suggestion in suggestions" 
        :key="suggestion"
        @tap="sendSuggestion(suggestion)"
      >
        {{ suggestion }}
      </view>
    </view>

    <!-- 输入区域 -->
    <view class="chat-input-area">
      <view class="input-container">
        <textarea
          class="chat-input"
          v-model="inputText"
          placeholder="输入您的问题..."
          :auto-height="true"
          :show-confirm-bar="false"
          maxlength="500"
          @focus="onInputFocus"
          @blur="onInputBlur"
        ></textarea>
        <button 
          class="send-btn"
          :disabled="!inputText.trim() || isSending"
          @tap="sendMessage"
        >
          发送
        </button>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  name: 'Chat',
  data() {
    return {
      messages: [],
      inputText: '',
      isTyping: false,
      isSending: false,
      scrollTop: 0,
      showSuggestions: true,
      suggestions: [
        'UTS附近房源',
        '预约代看房',
        '租房法律咨询',
        '合同审核服务'
      ]
    }
  },
  onLoad() {
    console.log('聊天页面加载')
  },
  onShow() {
    this.scrollToBottom()
  },
  methods: {
    // 发送消息
    async sendMessage() {
      if (!this.inputText.trim() || this.isSending) return
      
      const userMessage = {
        type: 'user',
        content: this.inputText.trim(),
        content_type: 'text',
        timestamp: new Date()
      }
      
      this.messages.push(userMessage)
      const messageText = this.inputText.trim()
      this.inputText = ''
      this.isSending = true
      this.isTyping = true
      this.showSuggestions = false
      
      this.scrollToBottom()
      
      try {
        const app = getApp()
        const response = await uni.request({
          url: `${app.globalData.apiBaseUrl}/api/chat`,
          method: 'POST',
          header: {
            'Content-Type': 'application/json'
          },
          data: {
            message: messageText,
            user_id: this.getUserId()
          }
        })
        
        if (response.statusCode === 200) {
          const aiResponse = response.data
          
          // 添加AI回复消息
          const aiMessage = {
            type: 'ai',
            content: aiResponse.response,
            content_type: 'text',
            timestamp: new Date()
          }
          this.messages.push(aiMessage)
          
          // 如果有房源推荐，添加房源卡片
          if (aiResponse.properties && aiResponse.properties.length > 0) {
            aiResponse.properties.forEach(property => {
              this.messages.push({
                type: 'ai',
                content_type: 'property_card',
                data: property,
                timestamp: new Date()
              })
            })
          }
          
          // 如果有服务推荐，添加服务卡片
          if (aiResponse.services && aiResponse.services.length > 0) {
            aiResponse.services.forEach(service => {
              this.messages.push({
                type: 'ai',
                content_type: 'service_card',
                data: service,
                timestamp: new Date()
              })
            })
          }
          
        } else {
          throw new Error('API请求失败')
        }
      } catch (error) {
        console.error('聊天请求失败:', error)
        
        // 模拟AI回复用于测试
        this.addMockAIResponse(messageText)
      }
      
      this.isTyping = false
      this.isSending = false
      this.scrollToBottom()
    },
    
    // 模拟AI回复（开发测试用）
    addMockAIResponse(userMessage) {
      let response = ''
      let properties = []
      
      if (userMessage.includes('UTS') || userMessage.includes('找房')) {
        response = '好的！我来为您推荐悉尼科技大学附近的房源。'
        properties = [
          {
            id: 1,
            title: 'Central Park Student Village',
            address: 'Central Park, Chippendale',
            weekly_rent: 776,
            commute_time: 8,
            image: '/static/images/property1.jpg'
          }
        ]
      } else if (userMessage.includes('代看房')) {
        response = '我来为您介绍代看房服务！这是我们最受欢迎的服务。'
      } else {
        response = '我理解您的问题。请告诉我更多具体需求，我可以为您提供更准确的帮助。'
      }
      
      // 添加AI文本回复
      this.messages.push({
        type: 'ai',
        content: response,
        content_type: 'text',
        timestamp: new Date()
      })
      
      // 添加房源卡片
      if (properties.length > 0) {
        properties.forEach(property => {
          this.messages.push({
            type: 'ai',
            content_type: 'property_card',
            data: property,
            timestamp: new Date()
          })
        })
      }
    },
    
    // 发送快捷建议
    sendSuggestion(suggestion) {
      this.inputText = suggestion
      this.sendMessage()
    },
    
    // 获取用户ID
    getUserId() {
      let userId = uni.getStorageSync('userId')
      if (!userId) {
        userId = 'user_' + Date.now()
        uni.setStorageSync('userId', userId)
      }
      return userId
    },
    
    // 格式化时间
    formatTime(timestamp) {
      const date = new Date(timestamp)
      const hours = date.getHours().toString().padStart(2, '0')
      const minutes = date.getMinutes().toString().padStart(2, '0')
      return `${hours}:${minutes}`
    },
    
    // 滚动到底部
    scrollToBottom() {
      this.$nextTick(() => {
        this.scrollTop = 999999
      })
    },
    
    // 输入框聚焦
    onInputFocus() {
      this.scrollToBottom()
    },
    
    // 输入框失焦
    onInputBlur() {
      // 处理输入框失焦
    },
    
    // 预约房源看房
    bookPropertyViewing(propertyId) {
      uni.navigateTo({
        url: `/pages/booking/booking?propertyId=${propertyId}`
      })
    },
    
    // 查看房源详情
    viewPropertyDetail(propertyId) {
      uni.navigateTo({
        url: `/pages/property/detail?id=${propertyId}`
      })
    },
    
    // 预约服务
    bookService(serviceType) {
      uni.navigateTo({
        url: `/pages/booking/booking?serviceType=${serviceType}`
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #F4F7F9;
}

.chat-messages {
  flex: 1;
  padding: 20rpx;
  overflow: hidden;
}

.message {
  margin-bottom: 30rpx;
  animation: fadeIn 0.3s ease-in;
  
  &.user-message {
    .message-content {
      background: #007BFF;
      color: white;
      margin-left: 20%;
      border-radius: 20rpx 20rpx 6rpx 20rpx;
    }
    
    .message-time {
      text-align: right;
    }
  }
  
  &.ai-message {
    .message-content {
      background: white;
      color: #333;
      margin-right: 20%;
      border-radius: 20rpx 20rpx 20rpx 6rpx;
      box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
    }
  }
}

.message-content {
  padding: 24rpx 32rpx;
  font-size: 28rpx;
  line-height: 1.5;
  word-wrap: break-word;
}

.welcome-text {
  display: block;
  font-size: 32rpx;
  font-weight: bold;
  margin-bottom: 20rpx;
}

.help-text {
  display: block;
  margin-bottom: 15rpx;
  color: #666;
}

.help-list {
  margin: 20rpx 0;
  
  text {
    display: block;
    margin-bottom: 8rpx;
    font-size: 26rpx;
    color: #666;
  }
}

.question-prompt {
  display: block;
  margin-top: 20rpx;
  color: #007BFF;
  font-weight: 500;
}

.message-time {
  font-size: 22rpx;
  color: #999;
  margin-top: 10rpx;
  padding: 0 20rpx;
}

.property-card-mini {
  background: white;
  border-radius: 16rpx;
  overflow: hidden;
  margin: 10rpx 0;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.1);
  
  .property-image {
    width: 100%;
    height: 300rpx;
  }
  
  .property-info {
    padding: 20rpx;
    
    .property-price {
      font-size: 32rpx;
      font-weight: bold;
      color: #007BFF;
      margin-bottom: 10rpx;
    }
    
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
    
    .property-commute {
      font-size: 24rpx;
      color: #007BFF;
      margin-bottom: 20rpx;
    }
    
    .property-actions {
      display: flex;
      gap: 20rpx;
    }
  }
}

.service-card-mini {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border: 2rpx solid #0ea5e9;
  border-radius: 16rpx;
  padding: 30rpx;
  margin: 10rpx 0;
  
  .service-title {
    font-size: 30rpx;
    font-weight: bold;
    margin-bottom: 15rpx;
    color: #0369a1;
  }
  
  .service-description {
    font-size: 26rpx;
    color: #666;
    margin-bottom: 20rpx;
    line-height: 1.6;
  }
  
  .service-price {
    font-size: 32rpx;
    font-weight: bold;
    color: #dc2626;
    margin-bottom: 20rpx;
  }
}

.action-btn {
  flex: 1;
  padding: 16rpx 24rpx;
  border-radius: 12rpx;
  font-size: 24rpx;
  border: none;
  
  &.primary {
    background: #28a745;
    color: white;
  }
  
  &.secondary {
    background: #6c757d;
    color: white;
  }
}

.typing-indicator {
  display: flex;
  gap: 8rpx;
  padding: 20rpx !important;
}

.typing-dot {
  width: 12rpx;
  height: 12rpx;
  background: #999;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
  
  &:nth-child(1) { animation-delay: -0.32s; }
  &:nth-child(2) { animation-delay: -0.16s; }
}

.quick-suggestions {
  padding: 20rpx;
  display: flex;
  flex-wrap: wrap;
  gap: 15rpx;
}

.suggestion-btn {
  background: white;
  padding: 15rpx 25rpx;
  border-radius: 20rpx;
  font-size: 24rpx;
  color: #007BFF;
  border: 2rpx solid #007BFF;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.chat-input-area {
  background: white;
  border-top: 2rpx solid #e3e3e3;
  padding: 20rpx;
}

.input-container {
  display: flex;
  align-items: flex-end;
  gap: 20rpx;
}

.chat-input {
  flex: 1;
  background: #f5f5f5;
  border-radius: 20rpx;
  padding: 20rpx 25rpx;
  font-size: 28rpx;
  max-height: 200rpx;
  min-height: 80rpx;
  border: none;
}

.send-btn {
  background: #007BFF;
  color: white;
  border: none;
  border-radius: 50%;
  width: 80rpx;
  height: 80rpx;
  font-size: 24rpx;
  
  &:disabled {
    background: #ccc;
  }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10rpx); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes typing {
  0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
  40% { transform: scale(1); opacity: 1; }
}
</style>
