<template>
  <div class="sort-sheet">
    <!-- 面板头部 -->
    <div class="panel-header">
      <h3 class="panel-title chinese-text">选择排序方式</h3>
      <button class="clear-btn" type="button" @click="applySort('')">默认排序</button>
    </div>

    <!-- 面板内容：简单列表 -->
    <div class="panel-content">
      <ul class="sort-list" role="listbox" aria-label="排序方式">
        <li
          v-for="opt in options"
          :key="opt.value"
          class="sort-item"
          :class="{ selected: currentSort === opt.value }"
          role="option"
          :aria-selected="currentSort === opt.value"
          @click="applySort(opt.value)"
        >
          <span class="label">{{ opt.label }}</span>
          <svg
            v-if="currentSort === opt.value"
            class="check"
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
          >
            <path
              d="M20 6 9 17l-5-5"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
/*
  中文说明：
  - 移动端“排序”面板（列表式）
  - 选中即应用到 store.sort，并同步 URL 的 ?sort=
  - 样式完全走设计令牌（变量），不硬编码颜色
*/
import { computed, inject } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { sanitizeQueryParams, isSameQuery } from '@/utils/query'
import { usePropertiesStore } from '@/stores/properties'

const emit = defineEmits(['close'])

const t = inject('t') || ((k) => k)
const router = useRouter()
const route = useRoute()
const store = usePropertiesStore()

// 与现有 PC 端排序枚举保持一致（HomeView.vue 右上角）
const options = [
  { value: 'price_asc', label: '按最小价格' },
  { value: 'available_date_asc', label: '按空出时间' },
  { value: 'inspection_earliest', label: '按最早看房时间' },
  { value: 'suburb_az', label: '按区域（首字母）' },
]

const currentSort = computed(() => store.sort || '')

const applySort = async (val) => {
  try {
    // 1) 更新 URL（与桌面端行为一致）
    const currentQuery = { ...(route.query || {}) }
    const merged = { ...currentQuery }
    if (val) merged.sort = val
    else delete merged.sort
    const nextQuery = sanitizeQueryParams(merged)
    const currQuery = sanitizeQueryParams(currentQuery)
    if (!isSameQuery(currQuery, nextQuery)) {
      await router.replace({ query: nextQuery })
    }

    // 2) 更新 Store，并重置到第1页
    await store.setSort(val || '')

    // 3) 关闭面板
    emit('close')
  } catch (e) {
    console.error('应用排序失败:', e)
    emit('close')
  }
}
</script>

<style scoped>
.sort-sheet {
  width: 100%;
  background: var(--color-bg-card);
  border-radius: var(--radius-md);
}

/* 头部 */
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-md);
  border-bottom: 1px solid var(--color-border-default);
}
.panel-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-primary);
  margin: 0;
}
.clear-btn {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius-sm);
}
.clear-btn:hover {
  background: var(--color-surface-hover);
  color: var(--color-text-primary);
}

/* 列表 */
.panel-content {
  padding: 0 var(--space-md) var(--space-md);
}
.sort-list {
  list-style: none;
  margin: 0;
  padding: 0;
}
.sort-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-md) var(--space-xs);
  border-bottom: 1px solid var(--color-border-default);
  cursor: pointer;
  color: var(--color-text-primary);
}
.sort-item:last-child {
  border-bottom: none;
}
.sort-item:hover {
  background: var(--color-surface-hover);
}
.sort-item.selected {
  color: var(--juwo-primary); /* 项目已有品牌主色变量 */
}
.check {
  color: currentColor;
}
</style>
