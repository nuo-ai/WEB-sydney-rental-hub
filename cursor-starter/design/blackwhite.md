# LLM 指南 - 极简黑白设计系统

## 概述
本文档为大型语言模型（LLM）提供了全面的说明，以便有效地使用和扩展此极简设计系统。该系统以简洁性、一致性和可维护性为核心原则构建。

## 核心理念
在使用此设计系统进行构建时，请始终优先考虑：
1. **极简主义** - 移除不必要的元素
2. **清晰性** - 使信息层级显而易见
3. **一致性** - 使用已建立的模式
4. **留白** - 让设计有呼吸的空间
5. **功能性** - 每个元素都必须服务于一个目的

## 设计令牌（Design Tokens）用法

### 调色板
```css
/* 主要用法 */
--color-black       /* 主文本、边框、图标 */
--color-white       /* 背景、反色文本 */
--color-gray-100    /* 微妙的背景 */
--color-gray-200    /* 默认边框 */
--color-gray-400    /* 禁用状态 */
--color-gray-600    /* 次要文本 */
```

**规则：**
- 主内容使用纯黑色 (#000)
- 谨慎使用灰色以区分层级
- 除非明确要求，否则绝不使用彩色
- 边框默认为 1px 宽的 gray-200

### 排版层级
```css
/* 使用语义化尺寸 */
--text-base   /* 正文文本 - 16px */
--text-lg     /* 强调正文 - 20px */
--text-xl     /* 小标题 - 25px */
--text-2xl    /* 区块标题 - 31px */
--text-3xl    /* 页面标题 - 39px */
--text-4xl    /* 英雄区域标题 - 49px */
```

**规则：**
- 正文文本：使用 `--text-base` 搭配 `--leading-relaxed` 行高
- 标题：使用 `--font-bold` 搭配 `--leading-tight` 行高
- 始终包含正确的标题层级 (h1 → h6)
- 每个组件限制使用 2-3 种字号

### 间距系统
```css
/* 4px 基础单位 */
--space-2   /* 8px - 紧凑间距 */
--space-4   /* 16px - 默认间距 */
--space-6   /* 24px - 舒适间距 */
--space-8   /* 32px - 区块间距 */
--space-12  /* 48px - 大间隙 */
```

**规则：**
- 在组件内部使用一致的间距
- 默认内边距：`--space-4`
- 区块外边距：`--space-8` 或 `--space-12`
- 切勿使用任意的间距值

## 组件模式

### 按钮组件
```tsx
/* 主按钮 */
className="px-6 py-3 bg-black text-white font-medium 
          hover:bg-gray-800 transition-colors duration-200
          focus:outline focus:outline-2 focus:outline-black"

/* 次按钮 */
className="px-6 py-3 bg-white text-black font-medium 
          border border-black hover:bg-gray-100 
          transition-colors duration-200"

/* 幽灵按钮 */
className="px-6 py-3 text-black font-medium 
          hover:bg-gray-100 transition-colors duration-200"
```

### 卡片组件
```tsx
className="bg-white border border-gray-200 
          p-6 space-y-4"

/* 带悬停效果 */
className="bg-white border border-gray-200 
          p-6 space-y-4 transition-all duration-200
          hover:border-black hover:shadow-md"
```

### 输入框组件
```tsx
className="w-full px-4 py-2 border border-gray-200 
          focus:border-black focus:outline-none
          transition-colors duration-200
          placeholder:text-gray-400"
```

### 布局容器
```tsx
/* 带内边距的全宽容器 */
className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"

/* 内容容器 */
className="max-w-4xl mx-auto"

/* 用于表单的窄容器 */
className="max-w-md mx-auto"
```

## 通用布局

### 英雄区域（Hero Section）
```tsx
<section className="min-h-screen flex items-center justify-center px-4">
  <div className="max-w-4xl mx-auto text-center space-y-8">
    <h1 className="text-4xl md:text-5xl font-bold leading-tight">
      {title}
    </h1>
    <p className="text-lg md:text-xl text-gray-600 max-w-2xl mx-auto">
      {description}
    </p>
    <div className="flex gap-4 justify-center">
      {/* 按钮 */}
    </div>
  </div>
</section>
```

### 仪表盘布局
```tsx
<div className="min-h-screen flex">
  {/* 侧边栏 */}
  <aside className="w-64 border-r border-gray-200 p-6">
    {/* 导航 */}
  </aside>
  
  {/* 主内容 */}
  <main className="flex-1 p-8">
    <div className="max-w-6xl mx-auto space-y-8">
      {/* 内容 */}
    </div>
  </main>
</div>
```

### 网格布局
```tsx
/* 2 列 */
className="grid grid-cols-1 md:grid-cols-2 gap-6"

/* 3 列 */
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"

/* 4 列 */
className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6"
```

## 状态模式

### 悬停状态（Hover States）
- 按钮：背景轻微变暗或添加边框
- 卡片：添加黑色边框或微妙的阴影
- 链接：不透明度降至 0.7
- 始终包含过渡效果以实现平滑动画

### 焦点状态（Focus States）
- 始终包含可见的焦点指示器
- 使用 2px 黑色轮廓，偏移 2px
- 切勿移除焦点状态

### 禁用状态（Disabled States）
```tsx
className="opacity-50 cursor-not-allowed pointer-events-none"
```

### 加载状态（Loading States）
```tsx
/* 加载中旋转图标 */
<div className="animate-spin h-5 w-5 border-2 
              border-gray-300 border-t-black rounded-full" />

/* 骨架屏 */
<div className="animate-pulse bg-gray-200 h-4 w-full rounded" />
```

## 响应式设计规则

### 断点
- 始终采用移动优先的方法
- sm: 640px
- md: 768px  
- lg: 1024px
- xl: 1280px
- 2xl: 1536px

### 通用响应式模式
```tsx
/* 文本大小 */
className="text-base md:text-lg lg:text-xl"

/* 内边距 */
className="p-4 md:p-6 lg:p-8"

/* 网格列数 */
className="grid-cols-1 md:grid-cols-2 lg:grid-cols-3"

/* 显示/隐藏 */
className="hidden md:block"  /* 在移动端隐藏 */
className="md:hidden"        /* 仅在移动端显示 */
```

## 动画指南

### 允许的动画
```css
/* 过渡 */
transition-all duration-200
transition-colors duration-150
transition-opacity duration-300

/* 变换 */
hover:scale-105
hover:-translate-y-1

/* 关键帧 (谨慎使用) */
animate-pulse  /* 加载状态 */
animate-spin   /* 旋转图标 */
```

**规则：**
- 保持动画微妙且功能化
- 持续时间：微交互为 150-300ms
- 使用 ease 或 ease-in-out 缓动函数
- 避免弹跳或俏皮的动画

## 组件组合

### 构建新组件时
1. 从语义化 HTML 开始
2. 应用设计令牌中的基础样式
3. 添加交互状态（悬停、焦点、激活）
4. 确保响应式行为
5. 测试可访问性

### 组件结构示例
```tsx
// Component.tsx
import React from 'react';
import styles from './Component.module.css';

interface ComponentProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
  className?: string;
}

export const Component: React.FC<ComponentProps> = ({ 
  children, 
  variant = 'primary',
  className = '' 
}) => {
  const baseStyles = 'base-styles-here';
  const variantStyles = {
    primary: 'primary-styles',
    secondary: 'secondary-styles'
  };
  
  return (
    <div className={`${baseStyles} ${variantStyles[variant]} ${className}`}>
      {children}
    </div>
  );
};
```

## 文件命名约定

### 组件
- PascalCase: `Button.tsx`, `Card.tsx`
- 索引导出: `components/ui/index.ts`

### 样式
- 小写: `globals.css`, `typography.css`
- CSS 模块: `Button.module.css`

### 工具函数
- camelCase: `formatDate.ts`, `parseData.ts`

### 页面/示例
- kebab-case: `landing-page.tsx`, `dashboard-view.tsx`

## 需要避免的常见陷阱

### 禁止：
- 添加黑/白/灰以外的颜色
- 过度使用阴影
- 创建过于复杂的布局
- 添加没有目的的装饰性元素
- 使用不一致的间距
- 忘记悬停/焦点状态
- 忽略响应式设计
- 过度动画化界面

### 务必：
- 通过大小和字重维持视觉层级
- 全局使用一致的间距
- 确保所有交互元素都有状态
- 在多种屏幕尺寸上测试
- 保持组件简单且可复用
- 记录组件用法
- 遵循已建立的模式

## 扩展系统

### 添加新组件
1. 检查是否可以用现有组件组合而成
2. 遵循已建立的视觉语言
3. 仅使用现有的设计令牌
4. 记录组件的用途和用法
5. 包含所有必要的状态

### 修改现有组件
1. 保持向后兼容
2. 更新文档
3. 在所有使用实例中进行测试
4. 保留可访问性功能

## 可访问性清单
- [ ] 使用了语义化的 HTML 元素
- [ ] 在需要的地方使用了 ARIA 标签
- [ ] 键盘导航功能正常
- [ ] 焦点指示器可见
- [ ] 颜色对比度符合 WCAG AA 标准
- [ ] 交互元素有悬停/焦点状态
- [ ] 表单输入框有关联的标签
- [ ] 错误信息清晰明了

## 快速参考

### 核心类名 (Tailwind)
```css
/* 布局 */
flex items-center justify-center
grid grid-cols-{n} gap-{n}
max-w-{size} mx-auto

/* 间距 */
p-{n} m-{n} space-y-{n} gap-{n}

/* 排版 */
text-{size} font-{weight} leading-{height}

/* 边框 */
border border-gray-200 rounded-{size}

/* 状态 */
hover: focus: active: disabled:

/* 响应式 */
sm: md: lg: xl: 2xl:
```

## 测试你的实现

在认为一个组件完成之前：
1. 对照设计原则进行审查
2. 检查响应式行为
3. 测试所有交互状态
4. 验证可访问性
5. 确保间距一致
6. 验证语义化 HTML 的使用

请记住：如有疑问，选择简洁。最好的界面往往是元素最少但仍能有效实现用户目标的界面。

---

# LLM Instructions - Minimalist Black & White Design System

## Overview
This document provides comprehensive instructions for Large Language Models (LLMs) to effectively use and extend this minimalist design system. The system is built with simplicity, consistency, and maintainability as core principles.

## Core Philosophy
When building with this design system, always prioritize:
1. **Minimalism** - Remove unnecessary elements
2. **Clarity** - Make information hierarchy obvious
3. **Consistency** - Use established patterns
4. **White Space** - Let the design breathe
5. **Functionality** - Every element must serve a purpose

## Design Tokens Usage

### Color Palette
```css
/* Primary Usage */
--color-black       /* Primary text, borders, icons */
--color-white       /* Backgrounds, inverted text */
--color-gray-100    /* Subtle backgrounds */
--color-gray-200    /* Default borders */
--color-gray-400    /* Disabled states */
--color-gray-600    /* Secondary text */
```

**Rules:**
- Use pure black (#000) for primary content
- Use grays sparingly for hierarchy
- Never use colors unless explicitly requested
- Borders should be 1px and gray-200 by default

### Typography Scale
```css
/* Use semantic sizing */
--text-base   /* Body text - 16px */
--text-lg     /* Emphasized body - 20px */
--text-xl     /* Small headings - 25px */
--text-2xl    /* Section headings - 31px */
--text-3xl    /* Page headings - 39px */
--text-4xl    /* Hero headings - 49px */
```

**Rules:**
- Body text: Use `--text-base` with `--leading-relaxed`
- Headings: Use `--font-bold` with `--leading-tight`
- Always include proper heading hierarchy (h1 → h6)
- Limit to 2-3 font sizes per component

### Spacing System
```css
/* 4px base unit */
--space-2   /* 8px - Tight spacing */
--space-4   /* 16px - Default spacing */
--space-6   /* 24px - Comfortable spacing */
--space-8   /* 32px - Section spacing */
--space-12  /* 48px - Large gaps */
```

**Rules:**
- Use consistent spacing within components
- Default padding: `--space-4`
- Section margins: `--space-8` or `--space-12`
- Never use arbitrary spacing values

## Component Patterns

### Button Component
```tsx
/* Primary Button */
className="px-6 py-3 bg-black text-white font-medium 
          hover:bg-gray-800 transition-colors duration-200
          focus:outline focus:outline-2 focus:outline-black"

/* Secondary Button */
className="px-6 py-3 bg-white text-black font-medium 
          border border-black hover:bg-gray-100 
          transition-colors duration-200"

/* Ghost Button */
className="px-6 py-3 text-black font-medium 
          hover:bg-gray-100 transition-colors duration-200"
```

### Card Component
```tsx
className="bg-white border border-gray-200 
          p-6 space-y-4"

/* With hover effect */
className="bg-white border border-gray-200 
          p-6 space-y-4 transition-all duration-200
          hover:border-black hover:shadow-md"
```

### Input Component
```tsx
className="w-full px-4 py-2 border border-gray-200 
          focus:border-black focus:outline-none
          transition-colors duration-200
          placeholder:text-gray-400"
```

### Layout Containers
```tsx
/* Full-width container with padding */
className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"

/* Content container */
className="max-w-4xl mx-auto"

/* Narrow container for forms */
className="max-w-md mx-auto"
```

## Common Layouts

### Hero Section
```tsx
<section className="min-h-screen flex items-center justify-center px-4">
  <div className="max-w-4xl mx-auto text-center space-y-8">
    <h1 className="text-4xl md:text-5xl font-bold leading-tight">
      {title}
    </h1>
    <p className="text-lg md:text-xl text-gray-600 max-w-2xl mx-auto">
      {description}
    </p>
    <div className="flex gap-4 justify-center">
      {/* Buttons */}
    </div>
  </div>
</section>
```

### Dashboard Layout
```tsx
<div className="min-h-screen flex">
  {/* Sidebar */}
  <aside className="w-64 border-r border-gray-200 p-6">
    {/* Navigation */}
  </aside>
  
  {/* Main Content */}
  <main className="flex-1 p-8">
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Content */}
    </div>
  </main>
</div>
```

### Grid Layout
```tsx
/* 2 Column */
className="grid grid-cols-1 md:grid-cols-2 gap-6"

/* 3 Column */
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"

/* 4 Column */
className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6"
```

## State Patterns

### Hover States
- Buttons: Darken background slightly or add border
- Cards: Add black border or subtle shadow
- Links: Reduce opacity to 0.7
- Always include transition for smooth effect

### Focus States
- Always include visible focus indicators
- Use 2px black outline with 2px offset
- Never remove focus states

### Disabled States
```tsx
className="opacity-50 cursor-not-allowed pointer-events-none"
```

### Loading States
```tsx
/* Spinner */
<div className="animate-spin h-5 w-5 border-2 
              border-gray-300 border-t-black rounded-full" />

/* Skeleton */
<div className="animate-pulse bg-gray-200 h-4 w-full rounded" />
```

## Responsive Design Rules

### Breakpoints
- Mobile First approach always
- sm: 640px
- md: 768px  
- lg: 1024px
- xl: 1280px
- 2xl: 1536px

### Common Responsive Patterns
```tsx
/* Text sizing */
className="text-base md:text-lg lg:text-xl"

/* Padding */
className="p-4 md:p-6 lg:p-8"

/* Grid columns */
className="grid-cols-1 md:grid-cols-2 lg:grid-cols-3"

/* Hide/Show */
className="hidden md:block"  /* Hide on mobile */
className="md:hidden"        /* Show only on mobile */
```

## Animation Guidelines

### Allowed Animations
```css
/* Transitions */
transition-all duration-200
transition-colors duration-150
transition-opacity duration-300

/* Transforms */
hover:scale-105
hover:-translate-y-1

/* Keyframes (use sparingly) */
animate-pulse  /* Loading states */
animate-spin   /* Spinners */
```

**Rules:**
- Keep animations subtle and functional
- Duration: 150-300ms for micro-interactions
- Use ease or ease-in-out timing functions
- Avoid bouncy or playful animations

## Component Composition

### When Building New Components
1. Start with semantic HTML
2. Apply base styles from design tokens
3. Add interactive states (hover, focus, active)
4. Ensure responsive behavior
5. Test accessibility

### Example Component Structure
```tsx
// Component.tsx
import React from 'react';
import styles from './Component.module.css';

interface ComponentProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
  className?: string;
}

export const Component: React.FC<ComponentProps> = ({ 
  children, 
  variant = 'primary',
  className = '' 
}) => {
  const baseStyles = 'base-styles-here';
  const variantStyles = {
    primary: 'primary-styles',
    secondary: 'secondary-styles'
  };
  
  return (
    <div className={`${baseStyles} ${variantStyles[variant]} ${className}`}>
      {children}
    </div>
  );
};
```

## File Naming Conventions

### Components
- PascalCase: `Button.tsx`, `Card.tsx`
- Index exports: `components/ui/index.ts`

### Styles
- Lowercase: `globals.css`, `typography.css`
- CSS Modules: `Button.module.css`

### Utilities
- camelCase: `formatDate.ts`, `parseData.ts`

### Pages/Examples
- kebab-case: `landing-page.tsx`, `dashboard-view.tsx`

## Common Pitfalls to Avoid

### DON'T:
- Add colors beyond black/white/gray
- Use shadows excessively
- Create overly complex layouts
- Add decorative elements without purpose
- Use inconsistent spacing
- Forget hover/focus states
- Ignore responsive design
- Over-animate interfaces

### DO:
- Maintain visual hierarchy through size and weight
- Use consistent spacing throughout
- Ensure all interactive elements have states
- Test on multiple screen sizes
- Keep components simple and reusable
- Document component usage
- Follow established patterns

## Extending the System

### Adding New Components
1. Check if existing components can be composed
2. Follow the established visual language
3. Use only existing design tokens
4. Document the component purpose and usage
5. Include all necessary states

### Modifying Existing Components
1. Maintain backward compatibility
2. Update documentation
3. Test across all usage instances
4. Preserve accessibility features

## Accessibility Checklist
- [ ] Semantic HTML elements used
- [ ] ARIA labels where needed
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] Color contrast meets WCAG AA
- [ ] Interactive elements have hover/focus states
- [ ] Form inputs have labels
- [ ] Error messages are clear

## Quick Reference

### Essential Classes (Tailwind)
```css
/* Layout */
flex items-center justify-center
grid grid-cols-{n} gap-{n}
max-w-{size} mx-auto

/* Spacing */
p-{n} m-{n} space-y-{n} gap-{n}

/* Typography */
text-{size} font-{weight} leading-{height}

/* Borders */
border border-gray-200 rounded-{size}

/* States */
hover: focus: active: disabled:

/* Responsive */
sm: md: lg: xl: 2xl:
```

## Testing Your Implementation

Before considering a component complete:
1. Review against the design principles
2. Check responsive behavior
3. Test all interactive states
4. Verify accessibility
5. Ensure consistent spacing
6. Validate semantic HTML usage

Remember: When in doubt, choose simplicity. The best interface is often the one with the least elements that still accomplishes the user's goal effectively.
