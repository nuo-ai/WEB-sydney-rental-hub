# 🎨 房源卡片重设计方案

基于Realestate.com.au的最佳实践

## 📐 设计原则

### 1. 视觉层次（重要性递减）
```
1. 图片 - 最大面积，吸引注意力
2. 价格 - 最大字号，最重要信息
3. 地址 - 次大字号，位置关键
4. 房型 - 图标+数字，快速识别
5. 其他 - 最小字号，补充信息
```

### 2. 颜色策略
```css
/* 极简配色 */
--card-bg: #FFFFFF;
--text-primary: #161616;      /* 价格、标题 */
--text-secondary: #6B6B6B;    /* 地址、描述 */
--text-tertiary: #9B9B9B;     /* 辅助信息 */
--border-color: #E4E4E4;      /* 边框 */
--hover-bg: #F7F7F7;          /* hover背景 */

/* 品牌色仅用于交互 */
--action-color: #FF5824;      /* 收藏、按钮 */
```

### 3. 间距系统
```css
/* 8px网格严格执行 */
--space-xs: 4px;
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;
```

## 🎯 具体优化

### Before（现在的问题）
```vue
<!-- 问题：信息平铺，橙色太多 -->
<div class="property-price"> <!-- 22px，黑色 -->
  $850 per week
</div>
<div class="property-address"> <!-- 15px/13px，混乱 -->
  <div>123 George Street,</div>
  <div>SYDNEY NSW 2000</div>
</div>
<div class="property-features"> <!-- 图标颜色杂乱 -->
  <i class="fa-bed"></i> 2
  <i class="fa-bath"></i> 2
  <i class="fa-car"></i> 1
</div>
<div class="property-footer"> <!-- 中文显得突兀 -->
  空出日期: 立即入住
  开放时间: 周六 11:00
</div>
```

### After（优化后）
```vue
<!-- 清晰的视觉层次 -->
<div class="card-content">
  <!-- 价格：最突出 -->
  <div class="price-section">
    <span class="price">$850</span>
    <span class="price-unit">per week</span>
  </div>
  
  <!-- 地址：简洁单行 -->
  <div class="address">2C/8 Fuse Street, Zetland</div>
  
  <!-- 房型：统一灰色图标 -->
  <div class="features">
    <span class="feature">
      <svg>...</svg> <!-- 自定义图标 -->
      <span>2</span>
    </span>
    <!-- 重复其他特征 -->
  </div>
  
  <!-- 标签：仅必要信息 -->
  <div class="tags">
    <span class="tag">Unit</span>
    <span class="tag">Available Now</span>
  </div>
</div>
```

## 📏 尺寸规范

### 卡片尺寸
- **宽度**：响应式（不固定580px）
  - 桌面：3列布局，约370px
  - 平板：2列布局，约350px
  - 手机：1列布局，100%

### 图片比例
- **比例**：16:10（参考Realestate）
- **高度**：宽度 × 0.625

### 字体大小
```css
.price { font-size: 24px; font-weight: 700; }
.price-unit { font-size: 14px; font-weight: 400; }
.address { font-size: 16px; font-weight: 500; }
.features { font-size: 14px; }
.tags { font-size: 12px; }
```

## 🌏 中英文处理

### 方案A：英文为主（推荐）
- 价格、地址、房型：纯英文
- 仅在必要时使用中文（如"立即可住"）

### 方案B：分离展示
```vue
<div class="availability">
  <span class="label-cn">可入住</span>
  <span class="value-en">Now</span>
</div>
```

## 🎬 交互优化

### Hover效果
```css
.property-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transform: translateY(-2px);
  transition: all 0.2s ease;
}

/* 不改变背景色，保持清爽 */
```

### 收藏按钮
```css
.favorite-btn {
  background: rgba(255,255,255,0.9);
  color: #6B6B6B;
}
.favorite-btn:hover {
  color: #FF5824; /* 仅hover时显示品牌色 */
}
```

## 📱 响应式布局

### 网格系统
```css
.properties-grid {
  display: grid;
  gap: 24px;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
}

@media (min-width: 768px) {
  grid-template-columns: repeat(2, 1fr);
}

@media (min-width: 1200px) {
  grid-template-columns: repeat(3, 1fr);
}
```

## ✅ 实施步骤

### Phase 1：视觉清理（立即）
1. 减少颜色使用
2. 调整字体层次
3. 增加留白

### Phase 2：布局优化（明天）
1. 响应式网格
2. 图片比例调整
3. 信息重组

### Phase 3：交互提升（后天）
1. 优雅的hover效果
2. 平滑过渡动画
3. 加载状态

## 🎯 预期效果

### 专业度提升
- 从"开发原型"→"商业产品"
- 视觉干净、信息清晰
- 符合澳洲用户习惯

### 性能提升
- 移除不必要的图标字体
- 使用SVG图标
- CSS动画代替JS

### 维护性提升
- 统一的设计语言
- 可复用的组件
- 清晰的CSS变量