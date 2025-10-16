<script setup lang="ts">
/*
  页面职责：“我的”页占位（头像/昵称/积分 + 菜单项）
  为什么：与底部导航联动，用于拼装演示与后续扩展（收藏/历史/搜索等）
  技术权衡：
  - 仅静态占位，不接路由与数据；后续可替换为真实用户信息与跳转
*/
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 个人信息 -->
    <section class="bg-white">
      <div class="mx-auto w-full max-w-[420px] flex items-center gap-4 px-4 py-6">
        <img
          class="h-16 w-16 rounded-full object-cover"
          src="https://images.unsplash.com/photo-1570295999918-56ceb5ecca61?q=80&w=2080&auto=format&fit=crop"
          alt="用户头像"
          loading="lazy"
        />
        <div class="flex-1">
          <p class="text-lg font-semibold text-gray-900">Michael</p>
          <p class="text-sm text-gray-500">积分 55</p>
        </div>
      </div>
    </section>

    <!-- 菜单列表 1 -->
    <section class="mt-3 bg-white">
      <ul class="mx-auto w-full max-w-[420px] divide-y divide-gray-100">
        <li>
          <button type="button" class="w-full px-4 py-4 flex items-center justify-between text-gray-900">
            <span>我的收藏</span>
            <span aria-hidden="true" class="text-gray-400">›</span>
          </button>
        </li>
        <li>
          <button type="button" class="w-full px-4 py-4 flex items-center justify-between text-gray-900">
            <span>历史浏览</span>
            <span aria-hidden="true" class="text-gray-400">›</span>
          </button>
        </li>
        <li>
          <button type="button" class="w-full px-4 py-4 flex items-center justify-between text-gray-900">
            <span>搜索历史</span>
            <span aria-hidden="true" class="text-gray-400">›</span>
          </button>
        </li>
      </ul>
    </section>

    <!-- 菜单列表 2 -->
    <section class="mt-3 bg-white">
      <ul class="mx-auto w-full max-w-[420px] divide-y divide-gray-100">
        <li>
          <button type="button" class="w-full px-4 py-4 flex items-center justify-between text-gray-900">
            <span>我的动态</span>
            <span aria-hidden="true" class="text-gray-400">›</span>
          </button>
        </li>
        <li>
          <button type="button" class="w-full px-4 py-4 flex items-center justify-between text-gray-900">
            <span>我的房源</span>
            <span aria-hidden="true" class="text-gray-400">›</span>
          </button>
        </li>
        <li>
          <button type="button" class="w-full px-4 py-4 flex items-center justify-between text-gray-900">
            <span>访客记录</span>
            <span aria-hidden="true" class="text-gray-400">›</span>
          </button>
        </li>
      </ul>
    </section>

    <!-- 底部留白，避免与底部导航遮挡 -->
    <div class="h-24"></div>
  </div>
</template>
