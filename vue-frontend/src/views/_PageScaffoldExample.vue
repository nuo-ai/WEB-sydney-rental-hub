<!--
  新增页面统一样板（Page Scaffold Example）
  目标：保证“前端表现”统一，新增页面不再各写各的间距/配色/交互
  原则：
  - 只用全局 tokens（颜色/间距/圆角/阴影/字号），禁止散落 #hex/px
  - 统一页面骨架区块：Header / Toolbar / Content / Footer
  - 移动端固定底部导航时，根容器使用 padding-bottom: var(--bottom-nav-height) 防遮挡
  风险与回滚：
  - 本文件仅作为样板，不参与路由；复制后按需启用/删去注释即可，随时可回滚
-->

<template>
  <div class="page">
    <!-- Header：面包屑 / 标题 / 副标题 -->
    <header class="page__header stack-sm">
      <nav aria-label="Breadcrumb">
        <!-- 面包屑占位：按需替换为真实组件或简单文本 -->
        <a href="#" class="text-secondary text-sm">首页</a>
        <span class="text-secondary text-sm">/</span>
        <span class="text-secondary text-sm" aria-current="page">新页面</span>
      </nav>
      <h1 class="h1 text-primary">页面标题</h1>
      <p class="text-secondary text-sm">可选：副标题/统计信息/说明文字</p>
    </header>

    <!-- Toolbar：搜索/筛选/排序等操作区 -->
    <section class="page__toolbar stack-sm">
      <!-- 统一使用现有组件，样式走 tokens -->
      <SearchBar />
      <!-- 在这里放置 FilterTabs / 其它操作控件 -->
    </section>

    <!-- Content：主内容区（列表/网格/卡片） -->
    <main class="page__content stack-lg">
      <div class="properties-grid">
        <!-- 房源卡片示例：复用现有 PropertyCard，规格/间距自动对齐全局规范 -->
        <PropertyCard v-for="n in 3" :key="n" />
      </div>
    </main>

    <!-- Footer：分页/数据统计等 -->
    <footer class="page__footer stack-sm">
      <p class="text-secondary text-sm">这里是页脚占位（分页/统计等）</p>
    </footer>

    <!-- 移动端底部导航（如项目有统一底部导航组件，可解除注释使用）
         前端表现：固定底部导航，内容不被遮挡（依赖根容器 padding-bottom 令牌）
    -->
    <!-- <BottomNavBar /> -->
  </div>
</template>

<script setup lang="ts">
// 中文注释：示例仅引入现有、稳定组件，避免新增依赖
import SearchBar from '@/components/SearchBar.vue'
import PropertyCard from '@/components/PropertyCard.vue'
// 如已实现移动端底部导航组件，可按需启用
// import BottomNavBar from '@/components/BottomNavBar.vue'
</script>

<style scoped>
/* 页面骨架：统一左右留白与区块间距
   前端表现：
   - 移动端左右 16px，桌面 32px
   - Header/Toolbar/Content/Footer 之间使用大间距 var(--page-section-gap*)
   - 当使用固定底部导航时，内容不会被遮挡
*/
.page {
  padding-left: var(--page-x-padding-mob);
  padding-right: var(--page-x-padding-mob);
  padding-bottom: var(--bottom-nav-height); /* 如无底部导航，可按需移除 */
}

.page__header,
.page__toolbar,
.page__content,
.page__footer {
  margin-bottom: var(--page-section-gap);
}

@media (min-width: 768px) {
  .page {
    padding-left: var(--page-x-padding-desktop);
    padding-right: var(--page-x-padding-desktop);
    padding-bottom: 0; /* 桌面端通常无固定底部导航 */
  }
  .page__header,
  .page__toolbar,
  .page__content,
  .page__footer {
    margin-bottom: var(--page-section-gap-lg);
  }
}
</style>
