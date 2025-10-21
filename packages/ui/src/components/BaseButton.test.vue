<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">BaseButton 组件测试</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- 基础变体测试 -->
      <div class="border p-4 rounded-lg">
        <h2 class="text-lg font-semibold mb-4">基础变体</h2>
        <div class="flex flex-wrap gap-2">
          <BaseButton variant="primary">Primary</BaseButton>
          <BaseButton variant="secondary">Secondary</BaseButton>
          <BaseButton variant="ghost">Ghost</BaseButton>
          <BaseButton variant="link">Link</BaseButton>
        </div>
      </div>

      <!-- 尺寸测试 -->
      <div class="border p-4 rounded-lg">
        <h2 class="text-lg font-semibold mb-4">尺寸</h2>
        <div class="flex flex-wrap items-center gap-2">
          <BaseButton size="small">Small</BaseButton>
          <BaseButton size="medium">Medium</BaseButton>
          <BaseButton size="large">Large</BaseButton>
        </div>
      </div>

      <!-- 状态测试 -->
      <div class="border p-4 rounded-lg">
        <h2 class="text-lg font-semibold mb-4">状态</h2>
        <div class="flex flex-wrap gap-2">
          <BaseButton :loading="true">Loading</BaseButton>
          <BaseButton :disabled="true">Disabled</BaseButton>
          <BaseButton :block="true">Block Button</BaseButton>
        </div>
      </div>

      <!-- 图标测试 -->
      <div class="border p-4 rounded-lg">
        <h2 class="text-lg font-semibold mb-4">图标</h2>
        <div class="flex flex-wrap gap-2">
          <BaseButton>
            <template #icon>
              <Plus class="w-4 h-4" />
            </template>
            前置图标
          </BaseButton>
          <BaseButton>
            后置图标
            <template #iconRight>
              <ArrowRight class="w-4 h-4" />
            </template>
          </BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Plus, ArrowRight } from 'lucide-vue-next'
import BaseButton from './BaseButton.vue'
</script>
