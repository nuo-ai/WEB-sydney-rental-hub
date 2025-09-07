<template>
  <!-- 顶部筛选标签栏（仅作为统一 FilterPanel 的入口，不再弹出旧气泡面板） -->
  <div class="filter-tabs-container">
    <div class="filter-tabs">
      <!-- 区域 -->
      <div class="filter-tab-entry">
        <button class="filter-tab" @click.stop="openSection('area')">
          <span class="chinese-text">区域</span>
        </button>
      </div>

      <!-- 卧室 -->
      <div class="filter-tab-entry">
        <button class="filter-tab" @click.stop="openSection('bedrooms')">
          <span class="chinese-text">卧室</span>
        </button>
      </div>

      <!-- 价格 -->
      <div class="filter-tab-entry">
        <button class="filter-tab" @click.stop="openSection('price')">
          <span class="chinese-text">价格</span>
        </button>
      </div>

      <!-- 空出时间 -->
      <div class="filter-tab-entry">
        <button class="filter-tab" @click.stop="openSection('availability')">
          <span class="chinese-text">空出时间</span>
        </button>
      </div>

      <!-- 更多（高级筛选） -->
      <div class="filter-tab-entry">
        <button class="filter-tab" @click.stop="openSection('more')">
          <span class="chinese-text">更多</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
// 说明：本组件仅作为“锚点入口”，不再渲染任何 quick dropdown 内容。
// 点击 chip → 统一 emit 打开 FilterPanel，并传递希望聚焦的分组 section。


const emit = defineEmits(['toggleFullPanel', 'requestOpen'])

// 打开统一筛选面板，并传递分组
const openSection = (section) => {
  emit('toggleFullPanel', true)
  emit('requestOpen', { section })
}
</script>

<style scoped>
/* 顶部筛选标签栏 */
.filter-tabs-container {
  position: relative;
  width: 100%;
  margin-bottom: 0;
}

.filter-tabs {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap; /* PC端允许换行 */
  padding: 0;
  height: 48px; /* 与搜索框高度一致 */
}

/* PC端右侧布局时的样式调整 */
@media (min-width: 769px) {
  .filter-tabs-container {
    max-width: none;
  }
  .filter-tabs {
    justify-content: flex-start; /* 紧邻搜索框 */
    flex-wrap: wrap;
  }
}

/* 移动端保持原有流式排列 */
@media (max-width: 768px) {
  .filter-tabs-container {
    width: 100%;
    max-width: 100%;
    margin-bottom: 16px;
    padding: 0 16px;
    box-sizing: border-box;
  }
  .filter-tabs {
    flex-wrap: nowrap;
    overflow-x: auto;
    padding-bottom: 4px; /* 为滚动条留空间 */
  }
}

.filter-tabs::-webkit-scrollbar {
  display: none;
}

/* 单个入口 */
.filter-tab-entry {
  position: relative;
}

/* 筛选标签按钮（保持与现有 token 一致） */
.filter-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: var(--chip-bg, #f7f8fa);
  border: none;
  border-radius: 0;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: background-color 0.2s ease, color 0.2s ease;
  white-space: nowrap;
}

.filter-tab:hover {
  background: var(--chip-bg-hover, #eef1f4);
  color: var(--color-text-primary);
}

/* 移除装饰性图标，保持纯文字标签 */
</style>
