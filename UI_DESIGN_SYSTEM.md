# 🎨 Sydney Rental Hub UI设计系统

> 基于成功的PropertyDetail和PropertyCard组件提取的统一设计语言  
> 创建时间：2025-01-30  
> 参考标准：Realestate.com.au + Domain.com.au

---

## 📐 设计理念

### 核心原则
1. **清晰层级** - 信息按重要性排列，价格永远最突出
2. **最小化设计** - 去除装饰性元素，功能优先
3. **响应式优先** - 移动端体验是第一优先级
4. **一致性** - 相同功能使用相同的视觉语言

### 成功模式提取
基于PropertyDetail和PropertyCard的分析，我们的成功设计模式包括：
- **价格展示**: 大字号 + 分离的符号和单位
- **地址层级**: 主地址大字 + 次要信息小字灰色
- **图标系统**: Font Awesome统一图标
- **交互反馈**: 细腻的hover效果和过渡动画

---

## 🎨 设计令牌 (Design Tokens)

### 1. 颜色系统

```css
:root {
  /* ===== 品牌色 ===== */
  --brand-primary: #FF5824;        /* JUWO橙 - 仅用于强调 */
  --brand-primary-hover: #E64100;   /* hover状态 */
  --brand-primary-light: #FFF3F0;   /* 浅背景 */
  
  /* ===== 文字色阶 ===== */
  --text-primary: #2d2d2d;         /* 标题、重要信息 */
  --text-secondary: #666666;        /* 描述、次要信息 */
  --text-tertiary: #999999;         /* 辅助文字 */
  --text-price: #000000;            /* 价格专用黑 */
  --text-inverse: #ffffff;          /* 反色文字 */
  
  /* ===== 背景色 ===== */
  --bg-page: #f8f9fa;              /* 页面背景 */
  --bg-card: #ffffff;              /* 卡片背景 */
  --bg-hover: #f5f5f5;             /* hover背景 */
  --bg-active: #eeeeee;            /* 按下状态 */
  
  /* ===== 边框色 ===== */
  --border-light: #e5e7eb;         /* 浅边框 */
  --border-default: #d1d5db;       /* 默认边框 */
  --border-dark: #9ca3af;          /* 深边框 */
  
  /* ===== 状态色 ===== */
  --status-success: #10b981;       /* 成功、可用 */
  --status-warning: #f59e0b;       /* 警告 */
  --status-error: #ef4444;         /* 错误 */
  --status-info: #3b82f6;          /* 信息 */
}
```

### 2. 字体系统

```css
:root {
  /* ===== 字体家族 ===== */
  --font-primary: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-chinese: "PingFang SC", "Microsoft YaHei", sans-serif;
  
  /* ===== 字体大小（移动端优先） ===== */
  --text-xs: 12px;      /* 标签、辅助信息 */
  --text-sm: 14px;      /* 正文、描述 */
  --text-base: 16px;    /* 默认大小 */
  --text-lg: 18px;      /* 小标题 */
  --text-xl: 20px;      /* 标题 */
  --text-2xl: 24px;     /* 大标题 */
  --text-3xl: 28px;     /* 价格（移动端） */
  --text-4xl: 36px;     /* 价格（桌面端） */
  
  /* ===== 字重 ===== */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
  
  /* ===== 行高 ===== */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
}

/* 桌面端字体大小调整 */
@media (min-width: 768px) {
  :root {
    --text-3xl: 32px;
    --text-4xl: 40px;
  }
}
```

### 3. 间距系统（8px网格）

```css
:root {
  /* ===== 基础间距 ===== */
  --space-0: 0;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  
  /* ===== 组件内间距 ===== */
  --padding-xs: 8px 12px;
  --padding-sm: 12px 16px;
  --padding-md: 16px 20px;
  --padding-lg: 20px 24px;
  
  /* ===== 组件间间距 ===== */
  --gap-xs: 8px;
  --gap-sm: 12px;
  --gap-md: 16px;
  --gap-lg: 24px;
  --gap-xl: 32px;
}
```

### 4. 圆角系统

```css
:root {
  --radius-none: 0;
  --radius-sm: 4px;     /* 按钮、输入框 */
  --radius-md: 8px;     /* 卡片 */
  --radius-lg: 12px;    /* 模态框 */
  --radius-full: 9999px; /* 圆形 */
}
```

### 5. 阴影系统

```css
:root {
  --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-sm: 0 2px 4px 0 rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 8px 0 rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 8px 16px 0 rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 16px 32px 0 rgba(0, 0, 0, 0.12);
  
  /* 专用阴影 */
  --shadow-card: 0 2px 8px rgba(0, 0, 0, 0.08);
  --shadow-card-hover: 0 4px 16px rgba(0, 0, 0, 0.12);
  --shadow-button: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

### 6. 动画系统

```css
:root {
  /* ===== 持续时间 ===== */
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 350ms;
  
  /* ===== 缓动函数 ===== */
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  
  /* ===== 标准过渡 ===== */
  --transition-all: all var(--duration-normal) var(--ease-in-out);
  --transition-colors: color, background-color, border-color var(--duration-fast) var(--ease-in-out);
  --transition-transform: transform var(--duration-normal) var(--ease-out);
}
```

---

## 🧱 组件规范

### 1. 按钮组件

```css
/* 主按钮 */
.btn-primary {
  height: 48px;
  padding: 0 24px;
  background: var(--brand-primary);
  color: var(--text-inverse);
  border: none;
  border-radius: var(--radius-sm);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  cursor: pointer;
  transition: var(--transition-all);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--gap-xs);
}

.btn-primary:hover {
  background: var(--brand-primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-button);
}

.btn-primary:active {
  transform: translateY(0);
}

/* 次要按钮 */
.btn-secondary {
  height: 48px;
  padding: 0 24px;
  background: var(--bg-card);
  color: var(--text-primary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  font-size: var(--text-sm);
  font-weight: var(--font-normal);
  cursor: pointer;
  transition: var(--transition-all);
}

.btn-secondary:hover {
  background: var(--bg-hover);
  border-color: var(--border-dark);
}

/* 图标按钮 */
.btn-icon {
  width: 40px;
  height: 40px;
  padding: 0;
  background: transparent;
  color: var(--text-secondary);
  border: none;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: var(--transition-all);
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-icon:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}
```

### 2. 卡片组件

```css
.card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  overflow: hidden;
  transition: var(--transition-all);
}

.card:hover {
  box-shadow: var(--shadow-card-hover);
  transform: translateY(-2px);
}

.card-body {
  padding: var(--space-4);
}

.card-footer {
  padding: var(--space-3) var(--space-4);
  border-top: 1px solid var(--border-light);
}
```

### 3. 价格显示组件

```css
.price-display {
  display: flex;
  align-items: baseline;
  gap: 4px;
  font-weight: var(--font-bold);
  color: var(--text-price);
}

.price-symbol {
  font-size: 0.75em;
  font-weight: var(--font-normal);
}

.price-value {
  font-size: var(--text-3xl);
  line-height: 1;
}

.price-unit {
  font-size: var(--text-sm);
  font-weight: var(--font-normal);
  color: var(--text-secondary);
  margin-left: 4px;
}

/* 示例：$650 per week */
```

### 4. 地址显示组件

```css
.address-display {
  display: flex;
  flex-direction: column;
  gap: var(--gap-xs);
}

.address-primary {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  line-height: var(--leading-tight);
}

.address-secondary {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: var(--leading-normal);
}
```

### 5. 房型规格组件

```css
.property-specs {
  display: flex;
  gap: var(--gap-lg);
}

.spec-item {
  display: flex;
  align-items: center;
  gap: var(--gap-xs);
  color: var(--text-secondary);
}

.spec-icon {
  font-size: var(--text-base);
  color: var(--text-tertiary);
}

.spec-value {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--text-primary);
}

.spec-label {
  font-size: var(--text-xs);
  color: var(--text-tertiary);
}
```

### 6. 状态标签组件

```css
.status-tag {
  display: inline-flex;
  align-items: center;
  gap: var(--gap-xs);
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  text-transform: uppercase;
}

.status-tag.available {
  background: var(--status-success);
  color: white;
}

.status-tag.new {
  background: var(--brand-primary);
  color: white;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: var(--radius-full);
  background: currentColor;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
```

---

## 📱 响应式设计

### 断点系统

```css
/* 移动优先的断点 */
/* Mobile: 默认 (< 768px) */
/* Tablet: >= 768px */
/* Desktop: >= 1024px */
/* Wide: >= 1280px */

@media (min-width: 768px) {
  /* Tablet styles */
}

@media (min-width: 1024px) {
  /* Desktop styles */
}

@media (min-width: 1280px) {
  /* Wide screen styles */
}
```

### 网格系统

```css
.container {
  width: 100%;
  padding: 0 var(--space-4);
  margin: 0 auto;
}

@media (min-width: 768px) {
  .container {
    padding: 0 var(--space-6);
  }
}

@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    padding: 0 var(--space-8);
  }
}

.grid {
  display: grid;
  gap: var(--gap-md);
}

.grid-cols-1 { grid-template-columns: repeat(1, 1fr); }
.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
.grid-cols-4 { grid-template-columns: repeat(4, 1fr); }
```

---

## ⚡ 交互规范

### 1. Hover状态
- 所有可交互元素必须有hover反馈
- 卡片：上移2px + 阴影加深
- 按钮：颜色变深 + 轻微上移
- 链接：下划线或颜色变化

### 2. Focus状态
```css
:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 2px;
}
```

### 3. Loading状态
```css
.skeleton {
  background: linear-gradient(90deg, 
    var(--bg-hover) 25%, 
    #f0f0f0 50%, 
    var(--bg-hover) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### 4. 过渡动画原则
- 入场：fade + slide up
- 出场：fade + slide down
- 切换：crossfade
- 展开/收起：height + opacity

---

## 🎯 设计模式库

### 1. 列表页模式
- 顶部：搜索栏 + 筛选按钮
- 主体：网格卡片布局
- 底部：分页或加载更多

### 2. 详情页模式
- 顶部：图片轮播
- 信息区：价格 > 地址 > 规格 > 描述
- 操作区：固定底部或侧边

### 3. 表单页模式
- 分步骤：进度指示器
- 分组：卡片分隔
- 验证：即时反馈

### 4. 空状态模式
- 图标/插图
- 主要文字
- 次要说明
- 行动按钮

---

## ✅ 实施指南

### Phase 1：建立基础（第1周）
1. 创建CSS变量文件
2. 建立基础组件（按钮、卡片、表单）
3. 统一现有页面的间距和颜色

### Phase 2：组件化（第2周）
1. 提取可复用组件
2. 建立组件文档
3. 重构关键页面

### Phase 3：优化完善（第3周）
1. 响应式优化
2. 动画和过渡
3. 性能优化

### Phase 4：维护机制（持续）
1. 代码审查标准
2. 新组件审批流程
3. 定期设计评审

---

## 📋 检查清单

开发新功能前：
- [ ] 是否有现成组件可用？
- [ ] 是否遵循8px网格？
- [ ] 是否使用设计令牌？
- [ ] 是否有合适的hover/focus状态？
- [ ] 是否在三个断点下测试？
- [ ] 是否与现有页面风格一致？

---

## 🚫 常见错误

1. **硬编码值**
   ```css
   /* ❌ 错误 */
   color: #666;
   padding: 13px;
   
   /* ✅ 正确 */
   color: var(--text-secondary);
   padding: var(--space-3);
   ```

2. **不一致的间距**
   ```css
   /* ❌ 错误 */
   margin: 10px 15px 12px 18px;
   
   /* ✅ 正确 */
   margin: var(--space-2) var(--space-4);
   ```

3. **缺少过渡**
   ```css
   /* ❌ 错误 */
   :hover {
     background: red;
   }
   
   /* ✅ 正确 */
   transition: var(--transition-all);
   :hover {
     background: var(--brand-primary);
   }
   ```

---

## 📚 参考资源

- [Realestate.com.au](https://www.realestate.com.au) - 视觉参考
- [Domain.com.au](https://www.domain.com.au) - 交互参考
- [Material Design](https://material.io) - 设计原则
- [Tailwind CSS](https://tailwindcss.com) - 工具类命名

---

*记住：一致性是关键。宁可统一使用"不完美"的设计，也不要各自为政。*