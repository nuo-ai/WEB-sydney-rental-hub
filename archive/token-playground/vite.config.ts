/// <reference path="./src/env.d.ts" />
// @ts-nocheck
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'node:path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    fs: {
      allow: [
        // 允许访问上层工作区根目录
        path.resolve(__dirname, '..', '..'),
        // 明确允许访问 vue-frontend（共享样式与生成 tokens）
        path.resolve(__dirname, '..', '..', 'vue-frontend'),
      ],
    },
  },
})
