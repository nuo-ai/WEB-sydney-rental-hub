<script setup lang="ts">
// 为什么：App 作为路由承载容器，统一用 router-view 渲染页面
</script>

<template>
  <router-view />
</template>

<style>
/* 业务规则：页面样式在各自组件内 scoped 管理；此处保持全局容器最简 */
</style>
