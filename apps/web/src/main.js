import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import App from './App.vue'
import router from './router'

// 导入自动化设计系统
import '@sydney-rental-hub/ui/dist/tokens.css'; // 自动生成的 Design Tokens
import './style.css' // 全局样式

import { useAuthStore } from './stores/auth'
import i18n from './i18n'

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
app.use(i18n)
app.use(router)

// Initialize auth store after Pinia is set up
const authStore = useAuthStore()
authStore.initAuth()

app.mount('#app')
