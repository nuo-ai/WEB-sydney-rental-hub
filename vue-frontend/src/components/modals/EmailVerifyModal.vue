<template>
  <el-dialog
    v-model="visible"
    fullscreen
    :show-close="false"
    class="verify-modal"
    :append-to-body="true"
  >
    <template #header>
      <div class="modal-header">
        <button class="back-btn" @click="handleBack">
          <i class="fas fa-arrow-left"></i>
        </button>
        <h2 class="modal-title">Check your email</h2>
      </div>
    </template>
    
    <div class="verify-content">
      <div class="verify-icon">
        <i class="fas fa-envelope-open-text"></i>
      </div>
      
      <h3 class="verify-title">Verify your email address</h3>
      
      <p class="verify-description">
        We've sent a verification email to:
      </p>
      
      <div class="email-display">{{ email }}</div>
      
      <p class="verify-instructions">
        Please check your inbox and click the verification link to activate your account.
      </p>
      
      <div class="verify-actions">
        <el-button 
          type="primary" 
          size="large"
          :loading="checking"
          @click="checkVerification"
          class="check-btn"
        >
          {{ checking ? 'Checking...' : 'I\'ve verified my email' }}
        </el-button>
        
        <button 
          class="resend-link" 
          @click="resendEmail"
          :disabled="resendCountdown > 0"
        >
          {{ resendCountdown > 0 ? `Resend in ${resendCountdown}s` : 'Resend verification email' }}
        </button>
      </div>
      
      <div class="divider"></div>
      
      <div class="help-section">
        <h4>Didn't receive the email?</h4>
        <ul class="help-list">
          <li>Check your spam or junk folder</li>
          <li>Make sure {{ email }} is correct</li>
          <li>Wait a few minutes and try again</li>
        </ul>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  email: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'verified'])

const authStore = useAuthStore()

// 响应式状态
const visible = ref(props.modelValue)
const checking = ref(false)
const resendCountdown = ref(0)
let countdownInterval = null
let verificationInterval = null

// 监听props变化
watch(() => props.modelValue, (newVal) => {
  visible.value = newVal
  if (newVal) {
    startAutoCheck()
  } else {
    stopAutoCheck()
  }
})

// 监听visible变化
watch(visible, (newVal) => {
  emit('update:modelValue', newVal)
})

// 自动检查邮箱验证状态
const startAutoCheck = () => {
  verificationInterval = setInterval(async () => {
    const verified = await authStore.checkEmailVerification()
    if (verified) {
      stopAutoCheck()
      handleVerified()
    }
  }, 3000) // 每3秒检查一次
  
  // 5分钟后停止自动检查
  setTimeout(() => {
    stopAutoCheck()
  }, 300000)
}

const stopAutoCheck = () => {
  if (verificationInterval) {
    clearInterval(verificationInterval)
    verificationInterval = null
  }
}

const handleBack = () => {
  visible.value = false
  stopAutoCheck()
}

const checkVerification = async () => {
  checking.value = true
  
  try {
    const verified = await authStore.checkEmailVerification()
    
    if (verified) {
      handleVerified()
    } else {
      ElMessage.warning('Email not verified yet. Please check your inbox.')
    }
  } catch (error) {
    ElMessage.error('Failed to check verification status')
  } finally {
    checking.value = false
  }
}

const handleVerified = () => {
  stopAutoCheck()
  emit('verified')
  visible.value = false
}

const resendEmail = async () => {
  if (resendCountdown.value > 0) return
  
  try {
    await authStore.resendVerificationEmail(props.email)
    ElMessage.success('Verification email sent!')
    
    // 开始倒计时
    resendCountdown.value = 60
    countdownInterval = setInterval(() => {
      resendCountdown.value--
      if (resendCountdown.value <= 0) {
        clearInterval(countdownInterval)
      }
    }, 1000)
  } catch (error) {
    ElMessage.error('Failed to resend email. Please try again.')
  }
}

onMounted(() => {
  if (visible.value) {
    startAutoCheck()
  }
})

onUnmounted(() => {
  stopAutoCheck()
  if (countdownInterval) {
    clearInterval(countdownInterval)
  }
})
</script>

<style scoped>
.verify-modal :deep(.el-dialog__header) {
  padding: 0;
  margin: 0;
}

.verify-modal :deep(.el-dialog__body) {
  padding: 0;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: white;
  padding: 20px;
  border-bottom: 1px solid #e3e3e3;
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: none;
  color: #666;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s;
}

.back-btn:hover {
  background: #f5f5f5;
}

.modal-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.verify-content {
  flex: 1;
  padding: 32px 20px;
  overflow-y: auto;
  max-width: 440px;
  width: 100%;
  margin: 0 auto;
  text-align: center;
}

.verify-icon {
  width: 80px;
  height: 80px;
  background: #fef3c7;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
}

.verify-icon i {
  font-size: 40px;
  color: #f59e0b;
}

.verify-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
}

.verify-description {
  font-size: 16px;
  color: #666;
  margin-bottom: 12px;
}

.email-display {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  padding: 12px 16px;
  background: #f5f5f5;
  border-radius: 8px;
  margin-bottom: 16px;
}

.verify-instructions {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  margin-bottom: 32px;
}

.verify-actions {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
}

.check-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
}

.resend-link {
  background: none;
  border: none;
  color: #dc2626;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  padding: 8px;
}

.resend-link:hover:not(:disabled) {
  text-decoration: underline;
}

.resend-link:disabled {
  color: #999;
  cursor: not-allowed;
}

.divider {
  height: 1px;
  background: #e3e3e3;
  margin: 32px 0;
}

.help-section {
  text-align: left;
}

.help-section h4 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}

.help-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.help-list li {
  font-size: 14px;
  color: #666;
  padding: 8px 0;
  padding-left: 20px;
  position: relative;
}

.help-list li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #999;
}

/* Mobile optimization */
@media (max-width: 768px) {
  .verify-content {
    padding: 24px 16px;
  }
  
  .modal-header {
    padding: 16px;
  }
}
</style>