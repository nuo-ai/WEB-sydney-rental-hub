import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import App from './App.vue'
import router from './router'

// 导入设计系统样式（按顺序）
import './styles/design-tokens.css' // 设计令牌
import './styles/base-components.css' // 基础组件
import './style.css' // 全局样式

import { useAuthStore } from './stores/auth'

const app = createApp(App)

// Configure Element Plus with JUWO brand colors
app.use(ElementPlus, {
  // Global configuration for JUWO brand
})

// Register all Element Plus icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(createPinia())
app.use(router)

// Initialize auth store after Pinia is set up
const authStore = useAuthStore()
authStore.initAuth()

app.mount('#app')
