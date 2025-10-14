<template>
  <div class="token-controls">
    <div v-for="(items, groupName) in grouped" :key="groupName">
      <h4>{{ groupName }}</h4>
      <div class="token-item" v-for="item in items" :key="item.cssVar">
        <label :for="item.cssVar">{{ item.label }}</label>
        <input
          v-if="isColor(item.value)"
          type="color"
          :id="item.cssVar"
          :value="item.value"
          @input="onInput(item, $event.target.value)"
        >
        <input
          v-else
          type="text"
          :id="item.cssVar"
          :value="item.value"
          @input="onInput(item, $event.target.value)"
        >
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import tokenData from '../../../../vue-frontend/src/generated-tokens/json/tokens.json';

/**
 * 扁平化 color 令牌，输出形如：
 * { label: 'gray / 500', cssVar: '--color-gray-500', value: '#6b7280', group: 'gray' }
 */
function flatten(obj, pathParts = [], out = []) {
  Object.entries(obj || {}).forEach(([k, v]) => {
    const next = [...pathParts, k];
    if (typeof v === 'string') {
      const cssVar = `--${next.join('-')}`; // e.g. --color-gray-500
      out.push({
        label: next.slice(1).join(' / '), // 去掉 color 前缀，仅用于展示
        cssVar,
        value: v,
        group: pathParts[1] || k // 第一层分类：white/black/gray/brand/semantic
      });
    } else if (v && typeof v === 'object') {
      flatten(v, next, out);
    }
  });
  return out;
}

const entries = ref(flatten({ color: tokenData.color }));

// 分组后用于界面展示
const grouped = computed(() => {
  const map = {};
  for (const item of entries.value) {
    if (!map[item.group]) map[item.group] = [];
    map[item.group].push(item);
  }
  return map;
});

function isColor(val) {
  return typeof val === 'string' && /^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/.test(val);
}

function setCssVar(cssVar, value) {
  document.documentElement.style.setProperty(cssVar, value);
}

function onInput(item, value) {
  item.value = value;
  setCssVar(item.cssVar, value);
}

// 初始同步 tokens 到 CSS 变量，确保预览初始值一致
onMounted(() => {
  for (const item of entries.value) {
    setCssVar(item.cssVar, item.value);
  }
});
</script>

<style scoped>
.token-controls {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.token-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
label {
  font-size: 0.9rem;
}
input {
  width: 100px;
}
</style>
