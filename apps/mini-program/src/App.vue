<script>
import { createSSRApp } from 'vue'

export function createApp() {
  const app = createSSRApp({
    onShow(options) {
      // 应用显示时的逻辑
      console.log('小程序启动')
    },
    onHide() {
      // 应用隐藏时的逻辑
      console.log('小程序进入后台')
    }
  })
  
  return {
    app
  }
}
</script>

<style>
/* 导入生成的主题样式 */
@import './styles/generated/light.wxss';
@import './styles/generated/dark.wxss';

/* 全局样式 */
.container {
  background-color: var(--color-semantic-bg-page);
}

/* 主题相关样式 */
.theme-light {
  /* Light theme is default, variables are already defined */
}

.theme-dark {
  /* Dark theme variables are already defined */
}

/* 响应式断点 */
@media (min-width: 768px) {
  .container {
    max-width: 750px;
    margin: 0 auto;
  }
}

/* 无障碍支持 */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
</style>
