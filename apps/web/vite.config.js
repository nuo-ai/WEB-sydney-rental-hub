/// <reference types="vitest/config" />
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
import path from 'node:path'
const dirname =
  typeof __dirname !== 'undefined' ? __dirname : path.dirname(fileURLToPath(import.meta.url))

// More info at: https://storybook.js.org/docs/next/writing-tests/integrations/vitest-addon
const isStorybook = process.env.STORYBOOK === 'true'

const viteInspectCompatPatch = {
  name: 'vite-plugin-inspect-compat-patch',
  enforce: 'pre',
  configureServer(server) {
    if (server && server.environments == null) {
      // Vite 7 removed the `server.environments` property that
      // `vite-plugin-inspect` expects. The plugin is bundled with
      // `vite-plugin-vue-devtools` and crashes when it tries to access
      // the missing property. Providing an empty object keeps the
      // plugin operational without altering any behaviour.
      server.environments = {}
    }
  },
}

const enableVueDevTools = process.env.ENABLE_VUE_DEVTOOLS === 'true'

export default defineConfig(async () => {
  const plugins = [vue()]
  if (!isStorybook && enableVueDevTools) {
    plugins.unshift(viteInspectCompatPatch)
    plugins.push(vueDevTools())
  }

  let testConfig
  if (isStorybook) {
    const { storybookTest } = await import('@storybook/addon-vitest/vitest-plugin')
    testConfig = {
      projects: [
        {
          extends: true,
          plugins: [
            storybookTest({
              configDir: path.join(dirname, '.storybook'),
            }),
          ],
          test: {
            name: 'storybook',
            browser: {
              enabled: true,
              headless: true,
              provider: 'playwright',
              instances: [
                {
                  browser: 'chromium',
                },
              ],
            },
            setupFiles: ['.storybook/vitest.setup.js'],
          },
        },
      ],
    }
  }

  return {
    plugins,
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    server: {
    // 固定端口，避免 Google Maps API 限制问题
    port: 5178,
    strictPort: true,
    // 如果端口被占用则报错，而不是尝试下一个端口
    host: true,
    // 监听所有地址

    // 允许通过 ngrok 访问（解决 403 Forbidden / Host 校验）
    // 也可设置为 true 完全放开（仅开发环境使用）：
    // allowedHosts: true,
    allowedHosts: ['.ngrok-free.app'],
    // 可选：若需要稳定 HMR，通过 ngrok 的 wss 连接（演示可不配置）
    // hmr: {
    //   host: 'YOUR_SUBDOMAIN.ngrok-free.app', // 替换为实际 ngrok 子域名
    //   protocol: 'wss',
    //   clientPort: 443,
    // },

    proxy: {
      '/api': {
        // 本地后端（通过 Vite 代理转发），更稳：统一指向 localhost
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
    },
    optimizeDeps: {
      include: ["@vuepic/vue-datepicker"]
    },
    // 仅在 Storybook 环境下加载测试配置
    test: testConfig,
  }
})
