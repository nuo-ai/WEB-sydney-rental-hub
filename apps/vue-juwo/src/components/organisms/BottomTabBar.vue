<script setup lang="ts">
/*
  文件职责：底部导航栏（首页/发现/找房/消息/我的）
  为什么：跨页面统一底部导航交互与样式
  技术权衡：
  - 不引入图标库，使用 emoji/字符占位；后续可替换为统一图标组件
  - 仅通过 active 与 change 事件控制，保持无状态
*/

import type { TabKey } from '@/types/ui'

const props = defineProps<{
  active: TabKey
}>()

const emit = defineEmits<{
  (e: 'change', tab: TabKey): void
}>()

function go(tab: TabKey) {
  emit('change', tab)
}
</script>

<template>
  <nav class="sticky bottom-0 inset-x-0 bg-white border-t border-gray-200">
    <ul class="mx-auto grid max-w-[420px] grid-cols-5 py-2 text-xs text-gray-500">
      <li class="flex flex-col items-center" :class="props.active === 'home' ? 'text-teal-600' : ''">
        <button type="button" @click="go('home')" class="flex flex-col items-center">
          <span class="text-xl leading-none">🏠</span>
          <span>首页</span>
        </button>
      </li>
      <li class="flex flex-col items-center" :class="props.active === 'discover' ? 'text-teal-600' : ''">
        <button type="button" @click="go('discover')" class="flex flex-col items-center">
          <span class="text-xl leading-none">🧭</span>
          <span>发现</span>
        </button>
      </li>
      <li class="flex flex-col items-center" :class="props.active === 'find' ? 'text-teal-600' : ''">
        <button type="button" @click="go('find')" class="flex flex-col items-center">
          <span class="text-xl leading-none">🔎</span>
          <span>找房</span>
        </button>
      </li>
      <li class="flex flex-col items-center" :class="props.active === 'messages' ? 'text-teal-600' : ''">
        <button type="button" @click="go('messages')" class="flex flex-col items-center">
          <span class="text-xl leading-none">💬</span>
          <span>消息</span>
        </button>
      </li>
      <li class="flex flex-col items-center" :class="props.active === 'account' ? 'text-teal-600' : ''">
        <button type="button" @click="go('account')" class="flex flex-col items-center">
          <span class="text-xl leading-none">👤</span>
          <span>我的</span>
        </button>
      </li>
    </ul>
  </nav>
</template>
