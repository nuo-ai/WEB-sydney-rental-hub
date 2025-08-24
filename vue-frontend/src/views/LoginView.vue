<template>
  <div class="login-container">
    <div class="login-box">
      <h2 class="title">登录</h2>
      <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" @submit.prevent="handleLogin">
        <el-form-item prop="email">
          <el-input v-model="loginForm.email" placeholder="邮箱" size="large" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="密码" size="large" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="authStore.loading" style="width: 100%;">
            登录
          </el-button>
        </el-form-item>
      </el-form>
      <div v-if="authStore.error" class="error-message">
        {{ authStore.error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()
const loginFormRef = ref(null)

const loginForm = ref({
  email: '',
  password: '',
})

const loginRules = {
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }, { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      const success = await authStore.login(loginForm.value)
      if (success) {
        ElMessage.success('登录成功')
        router.push('/')
      }
    }
  })
}
</script>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}
.login-box {
  width: 400px;
  padding: 40px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background: white;
}
.title {
  text-align: center;
  margin-bottom: 30px;
}
.error-message {
  color: red;
  text-align: center;
  margin-top: 10px;
}
</style>
