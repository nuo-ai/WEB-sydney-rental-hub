import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import i18n from '../src/i18n'

import '../src/styles/design-tokens.css'
import '../src/styles/base-components.css'
import '../src/styles/page-tokens.css'
import '../src/styles/typography.css'
import '../src/style.css'

const createMemoryStorage = () => {
  let store = {}

  return {
    getItem(key) {
      return Object.prototype.hasOwnProperty.call(store, key) ? store[key] : null
    },
    setItem(key, value) {
      store[key] = String(value)
    },
    removeItem(key) {
      delete store[key]
    },
    clear() {
      store = {}
    },
    key(index) {
      const keys = Object.keys(store)
      return keys[index] || null
    },
    get length() {
      return Object.keys(store).length
    },
  }
}

if (typeof globalThis.localStorage === 'undefined') {
  globalThis.localStorage = createMemoryStorage()
}

if (typeof globalThis.sessionStorage === 'undefined') {
  globalThis.sessionStorage = createMemoryStorage()
}

const setupApp = (app) => {
  if (app.config.globalProperties.__storybook_global_setup__) {
    return
  }

  app.use(createPinia())
  app.use(i18n)
  app.use(ElementPlus)

  Object.entries(ElementPlusIconsVue).forEach(([key, component]) => {
    app.component(key, component)
  })

  app.config.globalProperties.__storybook_global_setup__ = true
}

/** @type { import('@storybook/vue3-vite').Preview } */
const preview = {
  setup(app) {
    setupApp(app)
  },
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },

    a11y: {
      // 'todo' - show a11y violations in the test UI only
      // 'error' - fail CI on a11y violations
      // 'off' - skip a11y checks entirely
      test: 'todo',
    },
  },
}

export default preview
