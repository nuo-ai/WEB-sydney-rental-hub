<template>
  <div id="app" class="app-container">
    <!-- 导航组件 -->
    <Navigation :isHidden="isNavHidden" />

    <!-- 主要内容区域 -->
    <router-view class="main-view" @updateNavVisibility="handleNavVisibility" />

    <!-- 对比工具栏 -->
    <CompareToolbar />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Navigation from '@/components/Navigation.vue'
import CompareToolbar from '@/components/CompareToolbar.vue'

// 导航栏显示状态
const isNavHidden = ref(false)

// 处理导航栏显示状态变化
const handleNavVisibility = (hidden) => {
  // 只在桌面端处理导航状态更新，移动端忽略
  if (window.innerWidth > 768) {
    isNavHidden.value = hidden
  }
}
</script>

<style>
/* JUWO桔屋找房 - 全局应用样式 */

/* 引入Font Awesome图标库 */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css');

/* 应用容器 */
.app-container {
  min-height: 100vh;
  background-color: var(--color-bg-page);
  position: relative;
}

/* 主视图区域 */
.main-view {
  min-height: 100vh;
  width: 100%;
}

/* 移动端适配 - 为底部导航留空间 */
@media (max-width: 768px) {
  .main-view {
    padding-bottom: 80px;
  }
}

/* 桌面端适配 - 为固定导航栏留出空间 */
@media (min-width: 769px) {
  .main-view {
    padding-top: 64px; /* 为固定导航栏预留空间 */
  }
}

/* 全局滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: var(--neutral-scrollbar-color);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--neutral-scrollbar-hover-color);
}


/* 全局选择样式 */
::selection {
  background-color: var(--juwo-primary-50);
  color: var(--juwo-primary);
}

/* 全局链接样式 */
a {
  color: var(--link-color);
  text-decoration: none;
  transition: all 0.2s ease;
}

a:hover {
  color: var(--link-hover-color);
}

/* 全局按钮样式增强 */
.el-button {
  font-weight: 600;
  transition: all 0.2s ease;
}

.el-button:hover {
  transform: translateY(-1px);
}

.el-button:active {
  transform: translateY(0);
}

/* 全局输入框样式增强 */
.el-input__wrapper {
  transition: all 0.2s ease;
}

.el-input__wrapper:hover {
  border-color: var(--color-border-strong);
}

/* 全局加载动画 */
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.is-loading {
  animation: spin 1s linear infinite;
}

/* 响应式字体大小 */
@media (max-width: 767px) {
  html {
    font-size: 14px;
  }
}

@media (min-width: 768px) {
  html {
    font-size: 16px;
  }
}

/* 性能优化 */
* {
  box-sizing: border-box;
}

img {
  max-width: 100%;
  height: auto;
}

/* 无障碍增强 */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* 打印样式 */
@media print {
  .app-container {
    background: white;
  }

  .main-view {
    padding: 0;
  }

  nav {
    display: none;
  }
}
</style>
