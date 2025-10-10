import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import App from './App.vue'
import router from './router'

// 导入自动化设计系统（通过 UI 包暴露的设计令牌）
import '@sydney-rental-hub/ui/dist/tokens.css'
import './styles/design-tokens.css' // 项目语义令牌（确保与 UI 包 tokens 对齐）
import './styles/theme-dark.css' // 暗色主题（.dark 作用域语义令牌覆盖）
import './style.css' // 全局样式（先加载本项目现有全局）
import './styles/cursor-globals.css' // 经清理的 cursor globals（置于 style.css 之后以提高可见度）
import './styles/cursor-globals-override.css' // 变量映射兜底（保持品牌语义）
import './styles/cursor-globals-debug.css' // 调试：右下角徽标，确认 globals 生效

/* 调试：始终注入调试类，显示右下角徽标（确认全局样式链路生效）。确认后可改回仅 DEV。 */
if (typeof document !== 'undefined') {
  document.documentElement.classList.add('__globals-debug')
}

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
