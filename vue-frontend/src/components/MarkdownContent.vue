<template>
  <div class="markdown-content" v-html="sanitizedHtml"></div>
</template>

<script setup>
import { computed } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const props = defineProps({
  content: {
    type: String,
    default: '',
  },
  // 是否将普通换行转换为 <br>
  preserveLineBreaks: {
    type: Boolean,
    default: true,
  },
})

// 配置 marked
marked.setOptions({
  breaks: true, // 将换行符转换为 <br>
  gfm: true, // 启用 GitHub Flavored Markdown
  headerIds: false, // 不生成标题ID
  mangle: false, // 不转义邮箱
})

const sanitizedHtml = computed(() => {
  if (!props.content) return ''

  let processedContent = props.content

  // 预处理文本，将列表标记转换为Markdown格式
  processedContent = processedContent
    // 将 "- " 开头的行确保被识别为列表
    .replace(/^- /gm, '- ')
    // 将 "• " 转换为 "- "
    .replace(/^• /gm, '- ')
    // 将 "Feature:" 或 "THE FEATURES" 等标题加粗
    .replace(/^(Features?:|THE FEATURES?|FEATURES?:?)\s*$/gim, '**$1**')
    .replace(/^(THE PROPERTY|PROPERTY:?)\s*$/gim, '**$1**')
    // 确保列表项之间有适当的间距
    .replace(/\n-\s/g, '\n- ')

  // 使用marked解析Markdown
  const html = marked(processedContent)

  // 使用DOMPurify清理HTML，防止XSS攻击
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: [
      'p',
      'br',
      'strong',
      'b',
      'em',
      'i',
      'u',
      'h1',
      'h2',
      'h3',
      'h4',
      'h5',
      'h6',
      'ul',
      'ol',
      'li',
      'blockquote',
      'pre',
      'code',
      'a',
      'hr',
      'span',
    ],
    ALLOWED_ATTR: ['href', 'target', 'rel', 'class'],
  })
})
</script>

<style scoped>
.markdown-content {
  font-size: 14px;
  line-height: 1.8;
  color: #333;
}

.markdown-content :deep(p) {
  margin: 0 0 12px;
}

.markdown-content :deep(p:last-child) {
  margin-bottom: 0;
}

.markdown-content :deep(strong),
.markdown-content :deep(b) {
  font-weight: 600;
  color: #111;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  margin: 12px 0;
  padding-left: 20px;
}

.markdown-content :deep(li) {
  margin: 6px 0;
  line-height: 1.6;
}

.markdown-content :deep(ul li) {
  list-style-type: disc;
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3),
.markdown-content :deep(h4),
.markdown-content :deep(h5),
.markdown-content :deep(h6) {
  font-weight: 600;
  color: #111;
  margin: 16px 0 8px;
  line-height: 1.3;
}

.markdown-content :deep(h1) {
  font-size: 24px;
}

.markdown-content :deep(h2) {
  font-size: 20px;
}

.markdown-content :deep(h3) {
  font-size: 18px;
}

.markdown-content :deep(h4) {
  font-size: 16px;
}

.markdown-content :deep(h5) {
  font-size: 14px;
}

.markdown-content :deep(h6) {
  font-size: 14px;
}

.markdown-content :deep(blockquote) {
  margin: 12px 0;
  padding: 8px 16px;
  border-left: 3px solid #007bff;
  background-color: #f8f9fa;
  color: #555;
}

.markdown-content :deep(pre) {
  background-color: #f5f5f5;
  padding: 12px;
  border-radius: 4px;
  overflow-x: auto;
  margin: 12px 0;
}

.markdown-content :deep(code) {
  background-color: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: Consolas, Monaco, monospace;
  font-size: 13px;
}

.markdown-content :deep(hr) {
  margin: 16px 0;
  border: none;
  border-top: 1px solid #e5e5e5;
}

.markdown-content :deep(a) {
  color: #007bff;
  text-decoration: none;
}

.markdown-content :deep(a:hover) {
  text-decoration: underline;
}
</style>
