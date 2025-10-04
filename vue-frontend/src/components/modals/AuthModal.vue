<template>
  <el-dialog
    v-model="visible"
    fullscreen
    :show-close="false"
    class="auth-modal"
    :append-to-body="true"
  >
    <template #header>
      <div class="modal-header">
        <button class="close-btn" @click="handleClose">
          <i class="fas fa-times"></i>
        </button>
        <h2 class="modal-title">{{ isLogin ? 'Sign in' : 'Create an account' }}</h2>
      </div>
    </template>

    <div class="auth-content">
      <el-form
        ref="authFormRef"
        :model="authForm"
        :rules="authRules"
        label-position="top"
        class="auth-form"
      >
        <el-form-item label="Email address" prop="email">
          <el-input
            v-model="authForm.email"
            placeholder="Enter your email"
            size="large"
            @keyup.enter="handleSubmit"
          />
        </el-form-item>

        <el-form-item label="Password" prop="password">
          <el-input
            v-model="authForm.password"
            type="password"
            placeholder="Enter password"
            size="large"
            show-password
            @keyup.enter="handleSubmit"
          />
        </el-form-item>

        <el-button
          type="danger"
          size="large"
          :loading="loading"
          @click="handleSubmit"
          class="submit-btn"
        >
          {{ isLogin ? 'Sign in' : 'Create account' }}
        </el-button>
      </el-form>

      <div class="switch-mode">
        <span>{{ isLogin ? "Don't have an account?" : 'Already have an account?' }}</span>
        <a @click="toggleMode" class="switch-link">
          {{ isLogin ? 'Create account' : 'Sign in' }}
        </a>
      </div>

      <div class="divider">
        <span>or continue with</span>
      </div>

      <div class="social-buttons">
        <button class="social-btn google-btn" @click="handleGoogleAuth">
          <i class="fab fa-google"></i>
          <span>Google</span>
        </button>
        <button class="social-btn facebook-btn" @click="handleFacebookAuth">
          <i class="fab fa-facebook-f"></i>
          <span>Facebook</span>
        </button>
      </div>
    </div>
  </el-dialog>

  <!-- Email Verification Modal -->
  <EmailVerifyModal
    v-if="showVerifyModal"
    v-model="showVerifyModal"
    :email="authForm.email"
    @verified="handleVerified"
  />
</template>

<script setup>
import { ref, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import EmailVerifyModal from './EmailVerifyModal.vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue', 'success'])

const authStore = useAuthStore()

// 响应式状态
const visible = ref(props.modelValue)
const isLogin = ref(false)
const loading = ref(false)
const showVerifyModal = ref(false)
const authFormRef = ref()

const authForm = ref({
  email: '',
  password: '',
})

// 表单验证规则
const authRules = {
  email: [
    { required: true, message: 'Please enter email address', trigger: 'blur' },
    { type: 'email', message: 'Please enter a valid email address', trigger: 'blur' },
  ],
  password: [
    { required: true, message: 'Please enter password', trigger: 'blur' },
    { min: 6, message: 'Password must be at least 6 characters', trigger: 'blur' },
  ],
}

// 监听props变化
watch(
  () => props.modelValue,
  (newVal) => {
    visible.value = newVal
  },
)

// 监听visible变化
watch(visible, (newVal) => {
  emit('update:modelValue', newVal)
})

const handleClose = () => {
  visible.value = false
  // 重置表单
  authForm.value = {
    email: '',
    password: '',
  }
  if (authFormRef.value) {
    authFormRef.value.clearValidate()
  }
}

const toggleMode = () => {
  isLogin.value = !isLogin.value
  // 清除验证状态
  if (authFormRef.value) {
    authFormRef.value.clearValidate()
  }
}

const handleSubmit = async () => {
  // 验证表单
  const valid = await authFormRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true

  try {
    if (isLogin.value) {
      // 登录逻辑
      const success = await authStore.login(authForm.value.email, authForm.value.password)
      if (success) {
        ElMessage.success('Login successful!')
        handleClose()
        emit('success')
      }
    } else {
      // 注册逻辑
      const result = await authStore.register(authForm.value.email, authForm.value.password)
      if (result) {
        // 显示邮箱验证模态框
        showVerifyModal.value = true
      }
    }
  } catch (error) {
    ElMessage.error(error.message || (isLogin.value ? 'Login failed' : 'Registration failed'))
  } finally {
    loading.value = false
  }
}

const handleVerified = () => {
  showVerifyModal.value = false
  handleClose()
  emit('success')
  ElMessage.success('Email verified successfully!')
}

const handleGoogleAuth = () => {
  ElMessage.info('Google authentication coming soon')
}

const handleFacebookAuth = () => {
  ElMessage.info('Facebook authentication coming soon')
}
</script>

<style scoped>
.auth-modal :deep(.el-dialog__header) {
  padding: 0;
  margin: 0;
}

.auth-modal :deep(.el-dialog__body) {
  padding: 0;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--color-bg-card);
  padding: 20px;
  border-bottom: 1px solid var(--color-border-default);
  display: flex;
  align-items: center;
  gap: 16px;
}

.close-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: none;
  color: var(--color-text-secondary);
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s;
}

.close-btn:hover {
  background: var(--surface-2);
}

.modal-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.auth-content {
  flex: 1;
  padding: 32px 20px;
  overflow-y: auto;
  max-width: 440px;
  width: 100%;
  margin: 0 auto;
}

.auth-form {
  margin-bottom: 24px;
}

.auth-form :deep(.el-form-item__label) {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 8px;
}

.auth-form :deep(.el-input__wrapper) {
  border-radius: 8px;
  height: 48px;
}

.submit-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  margin-top: 24px;
  background: var(--color-danger) !important;
  border-color: var(--color-danger) !important;
}

.submit-btn:hover {
  background: var(--color-danger-hover) !important;
  border-color: var(--color-danger-hover) !important;
}

.switch-mode {
  text-align: center;
  margin: 24px 0;
  font-size: 14px;
  color: var(--color-text-secondary);
}

.switch-link {
  color: var(--color-danger);
  cursor: pointer;
  font-weight: 600;
  margin-left: 4px;
  text-decoration: none;
}

.switch-link:hover {
  text-decoration: underline;
}

.divider {
  text-align: center;
  margin: 32px 0 24px;
  position: relative;
}

.divider span {
  background: var(--color-bg-card);
  padding: 0 16px;
  color: var(--text-muted);
  font-size: 14px;
  position: relative;
  z-index: 1;
}

.divider::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  width: 100%;
  height: 1px;
  background: var(--color-border-default);
}

.social-buttons {
  display: flex;
  gap: 12px;
}

.social-btn {
  flex: 1;
  height: 48px;
  border: 1px solid var(--color-border-default);
  border-radius: 8px;
  background: var(--color-bg-card);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  transition: all 0.2s;
}

.social-btn:hover {
  background: var(--surface-2);
  border-color: var(--color-border-strong);
}

.social-btn i {
  font-size: 18px;
}

.google-btn i {
  color: var(--brand-google);
}

.facebook-btn i {
  color: var(--brand-facebook);
}

/* Mobile optimization */
@media (width <= 768px) {
  .auth-content {
    padding: 24px 16px;
  }

  .modal-header {
    padding: 16px;
  }
}
</style>
