<template>
  <div class="container mx-auto py-8">
    <button @click="$router.back()" class="mb-4 text-blue-600 hover:text-blue-800">
      ← 返回
    </button>
    <h1 class="text-3xl font-bold mb-6">Tabs 组件测试</h1>

    <div class="space-y-8">
      <!-- 非受控：defaultValue -->
      <section class="border rounded-lg p-6">
        <h2 class="text-xl font-semibold mb-4">非受控（defaultValue）</h2>
        <Tabs defaultValue="account" class="w-full">
          <TabsList class="mb-4">
            <TabsTrigger value="account">账户</TabsTrigger>
            <TabsTrigger value="password">密码</TabsTrigger>
            <TabsTrigger value="profile">资料</TabsTrigger>
          </TabsList>
          <div class="rounded-md border p-4">
            <TabsContent value="account">
              <p>账户内容：展示账户相关设置。</p>
            </TabsContent>
            <TabsContent value="password">
              <p>密码内容：展示密码修改表单。</p>
            </TabsContent>
            <TabsContent value="profile">
              <p>资料内容：展示用户基础资料。</p>
            </TabsContent>
          </div>
        </Tabs>
      </section>

      <!-- 受控：v-model -->
      <section class="border rounded-lg p-6">
        <h2 class="text-xl font-semibold mb-4">受控（v-model）</h2>
        <div class="mb-3 text-sm text-muted-foreground">
          当前值：<span class="font-mono">{{ value }}</span>
        </div>
        <Tabs v-model="value" class="w-full">
          <TabsList class="mb-4">
            <TabsTrigger value="one">One</TabsTrigger>
            <TabsTrigger value="two">Two</TabsTrigger>
          </TabsList>
          <div class="rounded-md border p-4">
            <TabsContent value="one">
              <p>面板 One：这里是第一个面板内容。</p>
            </TabsContent>
            <TabsContent value="two" :forceMount="true">
              <p>面板 Two：forceMount 测试，切换时不卸载节点。</p>
            </TabsContent>
          </div>
        </Tabs>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@sydney-rental-hub/ui/tabs'

const value = ref('one')
</script>
