<template>
  <div class="container mx-auto p-8">
    <h1 class="text-3xl font-bold mb-6">BaseInput 组件测试</h1>
    <div class="max-w-md space-y-6">
      <div>
        <label for="default-input" class="block text-sm font-medium text-gray-700 mb-1">
          默认输入框
        </label>
        <BaseInput id="default-input" v-model="textValue" placeholder="请输入文本..." />
        <p class="mt-2 text-sm text-gray-500">当前值: {{ textValue }}</p>
      </div>

      <div>
        <label for="password-input" class="block text-sm font-medium text-gray-700 mb-1">
          密码输入框
        </label>
        <BaseInput id="password-input" v-model="passwordValue" type="password" placeholder="请输入密码..." />
      </div>

      <div>
        <label for="disabled-input" class="block text-sm font-medium text-gray-700 mb-1">
          禁用输入框
        </label>
        <BaseInput id="disabled-input" placeholder="已被禁用" :disabled="true" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { BaseInput } from '@sydney-rental-hub/ui';

const textValue = ref('');
const passwordValue = ref('');
</script>
