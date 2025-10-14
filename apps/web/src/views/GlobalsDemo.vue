<template>
  <div class="container globals-scope" style="padding: var(--space-6) 0; margin-top: 80px;">
    <div class="demo-toolbar" style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
      <button class="btn" @click="enableDark">启用暗色主题</button>
      <button class="btn" @click="disableDark">关闭暗色主题</button>
      <span class="state">当前：{{ isDark ? '暗色' : '亮色' }}</span>
    </div>
    <h1>Globals Demo · 基础排版与重置</h1>
    <p>本页用于验证 cursor-starter/design/globals.css（清理版）是否生效。应可见：标题加粗/紧凑行高、段落间距、链接带下划线、代码样式、引用左边框、表格行高与分割线、滚动条样式等。</p>

    <h2>链接与强调</h2>
    <p>
      这是一个
      <a href="https://example.com" target="_blank" rel="noreferrer">带下划线的链接</a>，
      <strong>strong 半粗</strong>，
      <em>em 斜体</em>，
      <small>small 小号</small>
    </p>

    <h2>代码与预格式化</h2>
    <p>行内 <code>code</code> 示例。</p>
    <pre><code>// 代码块
function greet(name) {
  console.log('Hello, ' + name)
}
greet('Sydney')</code></pre>

    <h2>引用与分隔线</h2>
    <blockquote>这是一段引用（blockquote），左侧应有 2px 黑色边框。</blockquote>
    <hr />

    <h2>列表与表格</h2>
    <ul>
      <li>无序列表项 A</li>
      <li>无序列表项 B</li>
    </ul>
    <table>
      <thead>
        <tr>
          <th>列1</th>
          <th>列2</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>单元格 A1</td>
          <td>单元格 A2</td>
        </tr>
        <tr>
          <td>单元格 B1</td>
          <td>单元格 B2</td>
        </tr>
      </tbody>
    </table>

    <h2>滚动条示例（Webkit）</h2>
    <div style="height: 120px; overflow: auto; border: 1px solid var(--color-border); padding: var(--space-3); border-radius: var(--radius-base); background: var(--color-gray-50);">
      <p v-for="i in 12" :key="i">滚动内容行 {{ i }}</p>
    </div>

    <h2>Tailwind + Element Plus 统一主题验证</h2>
    <div class="p-4 bg-background text-foreground border border-border rounded-md flex items-center gap-3">
      <input class="px-3 py-2 border border-border rounded-md bg-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2" placeholder="Tailwind 输入" />
      <button class="px-3 py-2 rounded-md bg-primary text-white hover:opacity-90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">Tailwind 按钮</button>
      <el-input style="width: 220px" placeholder="Element Plus 输入" />
      <el-button type="primary">Element Plus 按钮</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isDark = ref(false)

function apply(val) {
  const el = document.documentElement
  if (val) el.classList.add('dark')
  else el.classList.remove('dark')
  isDark.value = el.classList.contains('dark')
}

function enableDark() {
  apply(true)
}

function disableDark() {
  apply(false)
}

onMounted(() => {
  isDark.value = document.documentElement.classList.contains('dark')
})
</script>

<style src="../styles/cursor-globals-scope.css"></style>

<style scoped>
/* 局部微调，确保 demo 更明显 */
.container > h2 {
  margin-top: var(--space-6);
}

/* 暗色演示工具条样式（使用语义令牌，亮/暗均优雅） */
.demo-toolbar .btn {
  padding: 6px 10px;
  border: 1px solid var(--color-border-default);
  border-radius: 6px;
  background: var(--bg-base);
  color: var(--text-primary);
  cursor: pointer;
  transition: background-color 0.15s ease;
}
.demo-toolbar .btn:hover {
  background: var(--bg-hover);
}
.demo-toolbar .state {
  color: var(--text-secondary);
  font-size: 0.9rem;
}
</style>
