# 🎨 前端样式指南 (Frontend Style Guide)

> 基于UI审查报告建立的统一设计规范  
> 最后更新：2025-01-30

---

## 📐 核心设计原则

1. **8px网格系统** - 所有间距必须是8的倍数
2. **5级字体系统** - 限制字体大小选择
3. **2级圆角系统** - 简化圆角使用
4. **CSS变量优先** - 禁止硬编码颜色值

---

## 🎨 设计令牌 (Design Tokens)

### 颜色系统
```css
/* 必须使用这些变量，禁止硬编码 */

/* 主色 */
--juwo-primary: #FF5824;
--juwo-primary-hover: #E64100;

/* 文字色 */
--color-text-primary: #2d2d2d;    /* 标题、重要文字 */
--color-text-secondary: #666666;   /* 次要文字、描述 */
--color-text-disabled: #999999;    /* 禁用状态 */
--color-text-price: #000000;       /* 价格专用 */

/* 背景色 */
--color-bg-page: #F4F7F9;         /* 页面背景 */
--color-bg-card: #FFFFFF;         /* 卡片背景 */
--color-bg-hover: #F5F5F5;        /* hover背景 */

/* 边框色 */
--color-border: #E5E7EB;          /* 统一边框色 */
--color-border-hover: #D1D5DB;    /* hover边框 */
```

### 间距系统 (8px Grid)
```css
/* 只能使用这些间距值 */
--space-xs: 4px;    /* 极小间距 */
--space-sm: 8px;    /* 小间距 */
--space-md: 16px;   /* 中间距 */
--space-lg: 24px;   /* 大间距 */
--space-xl: 32px;   /* 特大间距 */
--space-2xl: 48px;  /* 超大间距 */
```

### 字体系统
```css
/* 字体大小限制为5个级别 */
--font-xs: 12px;    /* 辅助文字、标签 */
--font-sm: 14px;    /* 正文、描述 */
--font-md: 16px;    /* 小标题 */
--font-lg: 20px;    /* 标题 */
--font-xl: 24px;    /* 大标题 */

/* 字重 */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### 圆角系统
```css
/* 只使用2个圆角值 */
--radius-sm: 4px;   /* 按钮、输入框 */
--radius-md: 8px;   /* 卡片、模态框 */
```

### 阴影系统
```css
/* 统一阴影效果 */
--shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
--shadow-md: 0 4px 6px rgba(0,0,0,0.1);
--shadow-lg: 0 10px 20px rgba(0,0,0,0.1);
```

---

## 🧱 组件规范

### 按钮 (Buttons)
```css
/* 主按钮 */
.btn-primary {
  height: 48px;
  padding: 0 24px;
  background: var(--juwo-primary);
  color: white;
  border-radius: var(--radius-sm);
  font-size: var(--font-sm);
  font-weight: var(--font-medium);
  transition: all 0.2s;
}

.btn-primary:hover {
  background: var(--juwo-primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

/* 次要按钮 */
.btn-secondary {
  height: 48px;
  padding: 0 24px;
  background: white;
  color: var(--juwo-primary);
  border: 1px solid var(--juwo-primary);
  border-radius: var(--radius-sm);
}
```

### 输入框 (Inputs)
```css
.input {
  height: 48px;
  padding: 0 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: var(--font-sm);
  transition: border-color 0.2s;
}

.input:focus {
  border-color: var(--juwo-primary);
  outline: none;
}
```

### 卡片 (Cards)
```css
.card {
  background: var(--color-bg-card);
  border-radius: var(--radius-md);
  padding: var(--space-md);
  box-shadow: var(--shadow-sm);
  transition: all 0.3s;
}

.card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}
```

---

## 📱 响应式断点

```css
/* 移动端优先，3个断点 */
/* Mobile: < 768px (默认) */
/* Tablet: 768px - 1024px */
@media (min-width: 768px) { }

/* Desktop: > 1024px */
@media (min-width: 1024px) { }
```

---

## ⚡ 交互规范

### Hover状态
- 所有可点击元素必须有hover反馈
- 使用 `transition: all 0.2s` 平滑过渡
- 卡片hover上移2px + 阴影加深

### Loading状态
```css
.loading {
  opacity: 0.6;
  pointer-events: none;
  position: relative;
}

.loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  border: 2px solid var(--juwo-primary);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
```

### Focus状态
- 输入框：边框变主色
- 按钮：添加outline
- 保证键盘可访问性

---

## ❌ 禁止事项

1. **禁止硬编码颜色** - 必须用CSS变量
2. **禁止随意间距** - 必须用8px倍数
3. **禁止超过5种字体大小** - 用定义好的5个级别
4. **禁止混用圆角值** - 只用4px和8px
5. **禁止无hover效果** - 可点击元素必须有反馈

---

## ✅ 检查清单

创建新组件前：
- [ ] 查看是否有类似组件可复用
- [ ] 使用CSS变量而非硬编码
- [ ] 间距是8的倍数
- [ ] 字体大小在5个级别内
- [ ] 有hover/focus/active状态
- [ ] 测试3个响应式断点
- [ ] 与现有组件风格一致

---

## 📝 示例对比

### ❌ 错误示例
```css
.bad-component {
  padding: 13px;          /* 不是8的倍数 */
  color: #333;            /* 硬编码颜色 */
  font-size: 15px;        /* 不在标准尺寸内 */
  border-radius: 6px;     /* 不是4px或8px */
}
```

### ✅ 正确示例
```css
.good-component {
  padding: var(--space-md);           /* 16px */
  color: var(--color-text-primary);   /* 使用变量 */
  font-size: var(--font-sm);          /* 14px */
  border-radius: var(--radius-md);    /* 8px */
  transition: all 0.2s;                /* 有过渡 */
}
```

---

## 🚀 实施计划

### Phase 1 - 立即执行
1. 所有新组件遵循此规范
2. 修复最明显的不一致（按钮、输入框）

### Phase 2 - 逐步改进
1. 重构现有组件
2. 统一所有间距和颜色

### Phase 3 - 长期维护
1. 添加Stylelint自动检查
2. 建立组件库文档

---

*记住：一致性 > 完美。宁可统一"不完美"，也不要各自"完美"。*