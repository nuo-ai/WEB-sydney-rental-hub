<script setup lang="ts">
/*
  文件职责：提供“底部弹层”通用容器（BottomSheet），统一移动端弹层交互与样式
  为什么：demo.html 多处使用底部弹层（位置/排序/筛选），先做通用外壳，后续各业务弹层在其上组合
  技术权衡：
  - 采用 Headless UI Dialog 保证可访问性与焦点管理
  - 使用 Transition 实现“自底向上”过渡动画
  - 固定 max-width: 420px 与最大高度 vh，匹配移动端容器与 demo 行为
  - 内部采用 flex-col + flex-1 让内容可滚动（不影响头/脚区域）
*/

import {
  Dialog,
  DialogPanel,
  DialogTitle,
  DialogDescription,
  TransitionChild,
  TransitionRoot,
} from '@headlessui/vue'
import type { HTMLAttributes } from 'vue'
import { computed, withDefaults } from 'vue'
import { cn } from '@/lib/utils'

const props = withDefaults(defineProps<{
  open?: boolean
  class?: HTMLAttributes['class']
  // 显示在标题区域的简易文案；若传入 slot[name=title] 则覆盖此文案
  title?: string
  // 弹层最大高度（占视口比例 0.3~0.95），默认 0.85
  height?: number
  // 是否显示头部；默认 true
  showHeader?: boolean
  // 是否显示底部区域；默认 false（由业务组件决定是否启用）
  showFooter?: boolean
}>(), {
  open: false,
  height: 0.85,
  showHeader: true,
  showFooter: false,
})

const emit = defineEmits<{
  (e: 'update:open', value: boolean): void
  // 子组件内部不直接控制外部状态，仅通过该事件通知父层
  (e: 'close'): void
}>()

// 计算最大高度（vh），限制在 30%~95% 之间，保证小屏也可操作
const maxVH = computed(() => {
  const h = typeof props.height === 'number' ? props.height : 0.85
  const clamped = Math.min(0.95, Math.max(0.3, h))
  return `${Math.round(clamped * 100)}vh`
})

function close() {
  emit('update:open', false)
  emit('close')
}
</script>

<template>
  <TransitionRoot :show="!!open" as="template">
    <Dialog as="div" class="relative z-50" @close="close">
      <!-- 遮罩层：加深 60% 透明黑，提高与页面的层次分离 -->
      <TransitionChild
        as="template"
        enter="ease-out duration-200"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="ease-in duration-150"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black/60" aria-hidden="true" />
      </TransitionChild>

      <!-- 底部对齐容器 -->
      <div class="fixed inset-0 flex items-end justify-center">
        <TransitionChild
          as="template"
          enter="ease-out duration-200"
          enter-from="translate-y-full"
          enter-to="translate-y-0"
          leave="ease-in duration-150"
          leave-from="translate-y-0"
          leave-to="translate-y-full"
        >
          <DialogPanel
            :class="cn(
              // 布局与容器
              'w-full max-w-[420px] bg-white shadow-xl outline-none',
              // 视觉：顶部圆角，内部纵向布局
              'rounded-t-2xl flex flex-col',
              props.class,
            )"
            :style="{ maxHeight: maxVH }"
          >
            <!-- Drag handle（视觉提示，非交互） -->
            <div class="mx-auto mt-2 h-1.5 w-12 rounded-full bg-gray-300" aria-hidden="true" />

            <!-- 头部（可选） -->
            <div v-if="showHeader">
              <div class="px-4 pt-3 pb-2">
                <DialogTitle v-if="title || $slots.title" class="text-base font-medium text-gray-900">
                  <slot name="title">{{ title }}</slot>
                </DialogTitle>
                <DialogDescription v-if="$slots.description" class="mt-1 text-sm text-gray-500">
                  <slot name="description" />
                </DialogDescription>
              </div>
              <div class="h-px w-full bg-gray-100" />
            </div>

            <!-- 可滚动内容区：flex-1 确保在限定高度内滚动 -->
            <div class="flex-1 overflow-y-auto px-4 py-3">
              <slot />
            </div>

            <!-- 底部（可选）：常用于“清除/确定”等操作按钮 -->
            <div v-if="showFooter" class="border-t border-gray-100 px-4 py-3">
              <slot name="footer" />
              <!-- iOS 安全区兜底 -->
              <div class="pb-[env(safe-area-inset-bottom)]"></div>
            </div>
          </DialogPanel>
        </TransitionChild>
      </div>
    </Dialog>
  </TransitionRoot>
</template>
