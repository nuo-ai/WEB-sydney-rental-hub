<template>
  <view class="page">
    <view class="controls">
      <view class="control">
        <text class="label">space-md(px)</text>
        <input class="input" type="number" :value="numValue(vars['--srh-space-md'])" @input="onPx('--srh-space-md', $event.detail.value)" />
      </view>
      <view class="control">
        <text class="label">price font-size(px)</text>
        <input class="input" type="number" :value="numValue(vars['--srh-font-size-price'])" @input="onPx('--srh-font-size-price', $event.detail.value)" />
      </view>
      <view class="control">
        <text class="label">price line-height(px)</text>
        <input class="input" type="number" :value="numValue(vars['--srh-line-height-price'])" @input="onPx('--srh-line-height-price', $event.detail.value)" />
      </view>
      <view class="control">
        <text class="label">address font-size(px)</text>
        <input class="input" type="number" :value="numValue(vars['--srh-font-size-address'])" @input="onPx('--srh-font-size-address', $event.detail.value)" />
      </view>
      <view class="control">
        <text class="label">address line-height(px)</text>
        <input class="input" type="number" :value="numValue(vars['--srh-line-height-address'])" @input="onPx('--srh-line-height-address', $event.detail.value)" />
      </view>
      <view class="control">
        <text class="label">inspection font-size(px)</text>
        <input class="input" type="number" :value="numValue(vars['--srh-font-size-inspection'])" @input="onPx('--srh-font-size-inspection', $event.detail.value)" />
      </view>
      <view class="control">
        <text class="label">inspection line-height(px)</text>
        <input class="input" type="number" :value="numValue(vars['--srh-line-height-inspection'])" @input="onPx('--srh-line-height-inspection', $event.detail.value)" />
      </view>
      <view class="control">
        <text class="label">radius-md(px)</text>
        <input class="input" type="number" :value="numValue(vars['--srh-radius-md'])" @input="onPx('--srh-radius-md', $event.detail.value)" />
      </view>
      <view class="control --wide">
        <text class="label">shadow(文本)</text>
        <input class="input" type="text" :value="vars['--srh-shadow-card']" @input="onShadow($event.detail.value)" placeholder="如: 0 1px 4px 0 rgba(0,0,0,.16)" />
      </view>

      <view class="actions">
        <button class="btn" type="default" @click="reset">重置</button>
        <button class="btn primary" type="primary" @click="exportVars">导出 JSON</button>
        <text class="tips">说明：H5 下可实时调参；小程序端展示静态效果。</text>
      </view>
    </view>

    <view class="preview">
      <view class="card">
        <view class="image"></view>
        <view class="content">
          <view class="header">
            <text class="price">$800 pw</text>
            <view class="fav-btn">♥</view>
          </view>
          <text class="address">12 Example St, Zetland NSW 2017</text>
          <view class="meta">
            <text class="meta-item">2 Bed</text>
            <text class="meta-item">2 Bath</text>
            <text class="meta-item">1 Car</text>
          </view>
          <text class="inspection">Inspection today 2:15pm</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
/**
 * 预览页说明：
 * - 目的：把 SRH Token 可视化，H5 端支持运行时微调（通过 CSS Variables）
 * - 小程序端：运行时 CSS 变量不支持动态 setProperty，此页仅作静态展示
 * - 导出：将当前 CSS 变量导出为 JSON，方便回填到 SCSS token（apps/uni-app/src/uni.scss）
 */
import { reactive, onMounted } from 'vue'

const VAR_NAMES = [
  '--srh-space-md',
  '--srh-font-size-price',
  '--srh-line-height-price',
  '--srh-font-size-address',
  '--srh-line-height-address',
  '--srh-font-size-inspection',
  '--srh-line-height-inspection',
  '--srh-radius-md',
  '--srh-shadow-card'
]

const vars = reactive({})
const initialVars = {}

function isH5() {
  // 条件编译优先；运行时兜底
  let flag = false
  // #ifdef H5
  flag = true
  // #endif
  return flag
}

function readComputedVar(name) {
  if (!isH5()) return ''
  const v = getComputedStyle(document.documentElement).getPropertyValue(name) || ''
  return v.trim()
}

function setCssVar(name, value) {
  if (!isH5()) return
  document.documentElement.style.setProperty(name, value)
}

function numValue(px) {
  if (!px) return ''
  const n = String(px).trim().replace('px', '')
  return n
}

function onPx(name, val) {
  const v = String(val || '').trim()
  if (!v) return
  const px = `${parseFloat(v)}px`
  vars[name] = px
  setCssVar(name, px)
}

function onShadow(val) {
  const v = String(val || '').trim()
  vars['--srh-shadow-card'] = v
  setCssVar('--srh-shadow-card', v)
}

function reset() {
  VAR_NAMES.forEach(n => {
    const v = initialVars[n]
    if (v !== undefined) {
      vars[n] = v
      setCssVar(n, v)
    }
  })
  uni.showToast({ title: '已重置', icon: 'none' })
}

function exportVars() {
  const obj = {}
  VAR_NAMES.forEach(n => { obj[n] = vars[n] })
  const json = JSON.stringify(obj, null, 2)
  // 复制到剪贴板（H5/小程序通用 API）
  uni.setClipboardData({
    data: json,
    success: () => { uni.showToast({ title: '已复制 JSON', icon: 'none' }) }
  })
}

onMounted(() => {
  // 初始化读取
  VAR_NAMES.forEach(n => {
    const v = readComputedVar(n)
    const val = v || vars[n] || ''
    vars[n] = val
    initialVars[n] = val
  })
})
</script>

<style lang="scss" scoped>
.page {
  padding: var(--srh-space-md);
  box-sizing: border-box;
}

.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
  background: #fafafa;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 12px;
}

.control {
  width: calc(50% - 6px);
  display: flex;
  align-items: center;
  gap: 8px;

  &.--wide {
    width: 100%;
  }

  .label {
    width: 180px;
    color: #666;
  }

  .input {
    flex: 1;
    height: 34px;
    padding: 6px 8px;
    border: 1px solid #ddd;
    border-radius: 6px;
    background: #fff;
    box-sizing: border-box;
  }
}

.actions {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  margin-top: 4px;

  .btn {
    padding: 0 14px;
    height: 36px;
    line-height: 36px;
    border-radius: 6px;
  }
  .primary {
    background: #007aff;
    color: #fff;
  }
  .tips {
    color: #999;
    font-size: 12px;
  }
}

.preview {
  .card {
    background: var(--srh-card-bg);
    padding: var(--srh-card-padding);
    box-shadow: var(--srh-shadow-card);
    border-radius: var(--srh-radius-md);
  }

  .image {
    width: 100%;
    height: 0;
    padding-top: calc(var(--srh-image-aspect) * 100%); // 基于比例的占位
    background: #eee;
    border-radius: 6px;
    margin-bottom: 12px;
  }

  .content {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .price {
    font-size: var(--srh-font-size-price);
    line-height: var(--srh-line-height-price);
    color: var(--srh-text-primary);
    font-weight: 600;
  }

  .fav-btn {
    width: var(--srh-button-size);
    height: var(--srh-button-size);
    border-radius: var(--srh-radius-md);
    background: #f5f5f5;
    color: #333;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .address {
    font-size: var(--srh-font-size-address);
    line-height: var(--srh-line-height-address);
    color: var(--srh-text-primary);
  }

  .meta {
    display: flex;
    flex-direction: row;

    .meta-item {
      color: var(--srh-text-secondary);
      margin-right: var(--srh-meta-gap);

      &:last-child {
        margin-right: 0;
      }
    }
  }

  .inspection {
    font-size: var(--srh-font-size-inspection);
    line-height: var(--srh-line-height-inspection);
    color: var(--srh-text-secondary);
  }
}
</style>
