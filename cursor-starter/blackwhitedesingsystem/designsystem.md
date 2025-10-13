# 高端暗色设计系统

## 目录
1. [概述](#概述)
2. [品牌哲学](#品牌哲学)
3. [视觉识别](#视觉识别)
4. [色彩系统](#色彩系统)
5. [排版](#排版)
6. [组件架构](#组件架构)
7. [布局原则](#布局原则)
8. [UI 组件](#ui-组件)
9. [设计模式](#设计模式)
10. [动画与动效](#动画与动效)
11. [实施指南](#实施指南)

## 概述

这个高端暗色设计系统旨在创造一种极致奢华的数字体验，体现了曼哈顿私人俱乐部的专属感和高端金融机构的精致感。它采用暗黑模式优先的方法构建，提供了一个面向那些重视实质、隐私和卓越品质的挑剔专业人士的界面。

### 核心原则
- **暗黑模式优先**：主要体验针对暗色环境进行优化
- **框架无关**：可适应任何前端技术
- **奢华材质**：数字世界中的铂金、黑曜石和水晶
- **极简复杂性**：通过克制实现最大影响力
- **专属感觉**：私人会员俱乐部的审美

## 品牌哲学

### 愿景
创造一个数字圣殿，让优质内容与无可挑剔的设计相遇——一个感觉像是数字领域中的私人会员俱乐部空间，每一次互动都散发着品质和专属感。

### 品牌个性
- **奢华**：高级材质，卓越工艺
- **专属**：会员制感觉，精心策划的体验
- **精致**：优雅的品味，有教养的视角
- **审慎**：低调的优雅，安静的自信
- **创新**：前沿而永恒

## 视觉识别

### Logo 处理
- **概念**：极简执行，搭配高级间距
- **字重**：仅使用极细到细的字重
- **间距**：宽裕的字母间距（最小 0.1em）
- **饰面**：
  - 特殊应用场景下的铂金箔效果
  - 数字环境下的微妙发光处理
  - 适用时的浮雕/凹雕效果

### 设计原则
- 极致简约，最大化影响力
- 以宽裕的负空间作为奢华元素
- 完美的对称性和数学般的精确性
- 高级饰面和微妙的纹理
- 对微交互的执着

## 色彩系统

### 主色板 - “午夜曼哈顿”
```css
/* 核心颜色 */
--obsidian-black: #0A0A0A;     /* rgb(10, 10, 10) - 主背景 */
--deep-charcoal: #1A1A1A;      /* rgb(26, 26, 26) - 上层表面 */
--platinum: #E5E5E5;           /* rgb(229, 229, 229) - 主文本 */
--pure-white: #FFFFFF;         /* rgb(255, 255, 255) - 最大对比度 */
--smoke: #2A2A2A;              /* rgb(42, 42, 42) - 次级表面 */
```

### 强调色 - “顶层公寓系列”
```css
/* 奢华强调色 */
--champagne-gold: #D4AF37;     /* rgb(212, 175, 55) - 高级高光 */
--manhattan-blue: #1E3A5F;     /* rgb(30, 58, 95) - 信任，深度 */
--burgundy: #722F37;           /* rgb(114, 47, 55) - 浓郁的强调色 */
--pearl-gray: #B8B8B8;        /* rgb(184, 184, 184) - 柔和的元素 */
--midnight-navy: #0F1419;      /* rgb(15, 20, 25) - 最深的背景 */
```

### 功能性颜色
```css
/* 系统状态 */
--success: #22C55E;            /* rgb(34, 197, 94) - 成功状态 */
--warning: #F59E0B;            /* rgb(245, 158, 11) - 警告状态 */
--error: #EF4444;              /* rgb(239, 68, 68) - 错误状态 */
--info: #3B82F6;               /* rgb(59, 130, 246) - 信息 */
```

### 不透明度等级
```css
/* 精致的透明度 */
--opacity-ghost: 0.05;         /* 几乎不可见的叠加层 */
--opacity-whisper: 0.10;       /* 微妙的背景 */
--opacity-breath: 0.15;        /* 轻触感 */
--opacity-presence: 0.25;      /* 可察觉但柔和 */
--opacity-statement: 0.40;     /* 清晰而精致 */
--opacity-bold: 0.60;          /* 强烈的存在感 */
```

## 排版

### 字体选择
**主字体**：为奢华感优化的系统字体
```css
font-family: 
  "SF Pro Display",           /* macOS */
  "Segoe UI Variable",        /* Windows 11 */
  "Inter",                    /* 备用 */
  system-ui,
  -apple-system,
  sans-serif;
```

**次字体**：用于技术内容的等宽字体
```css
font-family:
  "SF Mono",                  /* macOS */
  "Consolas",                 /* Windows */
  "Monaco",                   /* 备用 */
  monospace;
```

### 字号层级 - “铂金层级”
```css
/* 展示型排版 */
.display-xl { font-size: 4.5rem; font-weight: 100; letter-spacing: -0.02em; }
.display-lg { font-size: 3.75rem; font-weight: 100; letter-spacing: -0.02em; }
.display-md { font-size: 3rem; font-weight: 200; letter-spacing: -0.01em; }
.display-sm { font-size: 2.25rem; font-weight: 200; letter-spacing: -0.01em; }

/* 标题排版 */
.heading-xl { font-size: 1.875rem; font-weight: 300; letter-spacing: -0.01em; }
.heading-lg { font-size: 1.5rem; font-weight: 300; letter-spacing: -0.005em; }
.heading-md { font-size: 1.25rem; font-weight: 400; letter-spacing: 0; }
.heading-sm { font-size: 1.125rem; font-weight: 400; letter-spacing: 0; }
.heading-xs { font-size: 1rem; font-weight: 500; letter-spacing: 0.01em; }

/* 正文排版 */
.body-xl { font-size: 1.25rem; font-weight: 300; line-height: 1.6; }
.body-lg { font-size: 1.125rem; font-weight: 300; line-height: 1.6; }
.body-md { font-size: 1rem; font-weight: 400; line-height: 1.5; }
.body-sm { font-size: 0.875rem; font-weight: 400; line-height: 1.4; }
.body-xs { font-size: 0.75rem; font-weight: 400; line-height: 1.3; }

/* 特殊排版 */
.label { font-size: 0.75rem; font-weight: 500; letter-spacing: 0.05em; text-transform: uppercase; }
.caption { font-size: 0.6875rem; font-weight: 400; letter-spacing: 0.02em; }
.overline { font-size: 0.625rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; }
```

## 组件架构

### 海拔系统（Elevation System）
```css
/* 阴影层 - 高级深度感 */
--shadow-whisper: 0 1px 2px rgba(0, 0, 0, 0.3);
--shadow-subtle: 0 2px 4px rgba(0, 0, 0, 0.4);
--shadow-gentle: 0 4px 8px rgba(0, 0, 0, 0.5);
--shadow-moderate: 0 8px 16px rgba(0, 0, 0, 0.6);
--shadow-pronounced: 0 16px 32px rgba(0, 0, 0, 0.7);
--shadow-dramatic: 0 24px 48px rgba(0, 0, 0, 0.8);
```

### 表面层级
```css
/* 背景层 */
--surface-base: var(--obsidian-black);      /* 主背景 */
--surface-raised: var(--deep-charcoal);     /* 卡片、模态框 */
--surface-elevated: var(--smoke);           /* 下拉菜单、工具提示 */
--surface-overlay: rgba(26, 26, 26, 0.95);  /* 模态框背景 */
```

### 边框系统
```css
/* 精致的边框 */
--border-ghost: rgba(229, 229, 229, 0.05);  /* 几乎不可见 */
--border-subtle: rgba(229, 229, 229, 0.10); /* 卡片轮廓 */
--border-gentle: rgba(229, 229, 229, 0.15); /* 表单元素 */
--border-defined: rgba(229, 229, 229, 0.25); /* 激活状态 */
--border-prominent: rgba(229, 229, 229, 0.40); /* 焦点状态 */
```

## 布局原则

### 间距等级 - “黄金比例”
```css
/* 高级间距系统 */
--space-1: 0.25rem;   /* 4px - 微调 */
--space-2: 0.5rem;    /* 8px - 小间隙 */
--space-3: 0.75rem;   /* 12px - 组件内边距 */
--space-4: 1rem;      /* 16px - 标准间距 */
--space-5: 1.25rem;   /* 20px - 区块间距 */
--space-6: 1.5rem;    /* 24px - 大间距 */
--space-8: 2rem;      /* 32px - 主要区块 */
--space-10: 2.5rem;   /* 40px - 页面区块 */
--space-12: 3rem;     /* 48px - 英雄区域间距 */
--space-16: 4rem;     /* 64px - 布局间距 */
--space-20: 5rem;     /* 80px - 主要布局 */
--space-24: 6rem;     /* 96px - 建筑级间距 */
```

### 网格系统
```css
/* 奢华网格 - 12 列系统 */
.container {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 var(--space-6);
}

/* 响应式容器 */
.container-xs { max-width: 480px; }   /* 移动设备 */
.container-sm { max-width: 640px; }   /* 小型平板 */
.container-md { max-width: 768px; }   /* 平板 */
.container-lg { max-width: 1024px; }  /* 桌面 */
.container-xl { max-width: 1280px; }  /* 大型桌面 */
.container-2xl { max-width: 1440px; } /* 超大桌面 */
```

## UI 组件

### 按钮 - “行政操作”
```css
/* 主按钮 - 香槟金 */
.btn-primary {
  background: var(--champagne-gold);
  color: var(--obsidian-black);
  border: 1px solid var(--champagne-gold);
  font-weight: 500;
  letter-spacing: 0.01em;
}

/* 次按钮 - 铂金描边 */
.btn-secondary {
  background: transparent;
  color: var(--platinum);
  border: 1px solid var(--border-defined);
  font-weight: 400;
}

/* 第三级按钮 - 极简 */
.btn-tertiary {
  background: transparent;
  color: var(--pearl-gray);
  border: none;
  font-weight: 400;
}

/* 幽灵按钮 - 微妙的存在感 */
.btn-ghost {
  background: rgba(229, 229, 229, 0.05);
  color: var(--platinum);
  border: 1px solid var(--border-ghost);
}
```

### 卡片 - “高级表面”
```css
.card {
  background: var(--surface-raised);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  box-shadow: var(--shadow-gentle);
  overflow: hidden;
}

.card-elevated {
  background: var(--surface-elevated);
  box-shadow: var(--shadow-moderate);
}

.card-floating {
  background: var(--surface-elevated);
  box-shadow: var(--shadow-pronounced);
  transform: translateY(-2px);
}
```

### 表单 - “精致输入”
```css
.input {
  background: var(--surface-raised);
  border: 1px solid var(--border-gentle);
  color: var(--platinum);
  border-radius: 6px;
  padding: var(--space-3) var(--space-4);
  font-weight: 300;
}

.input:focus {
  border-color: var(--champagne-gold);
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
  outline: none;
}

.input::placeholder {
  color: var(--pearl-gray);
  font-weight: 300;
}
```

## 设计模式

### 导航 - “私人俱乐部导引”
```css
/* 顶部导航 */
.nav-primary {
  background: rgba(10, 10, 10, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-ghost);
}

/* 侧边栏导航 */
.nav-sidebar {
  background: var(--surface-raised);
  border-right: 1px solid var(--border-subtle);
  width: 280px;
}

/* 导航项 */
.nav-item {
  color: var(--pearl-gray);
  font-weight: 300;
  letter-spacing: 0.01em;
  transition: all 200ms ease;
}

.nav-item:hover {
  color: var(--platinum);
  background: rgba(229, 229, 229, 0.05);
}

.nav-item.active {
  color: var(--champagne-gold);
  background: rgba(212, 175, 55, 0.1);
}
```

### 数据展示 - “信息层级”
```css
/* 表格 */
.table {
  background: var(--surface-base);
  border: 1px solid var(--border-subtle);
}

.table-header {
  background: var(--surface-raised);
  color: var(--pearl-gray);
  font-weight: 500;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  font-size: 0.75rem;
}

.table-row:hover {
  background: rgba(229, 229, 229, 0.03);
}

.table-row:nth-child(even) {
  background: rgba(229, 229, 229, 0.01);
}
```

## 动画与动效

### 过渡系统
```css
/* 高级缓动函数 */
--ease-luxury: cubic-bezier(0.25, 0.1, 0.25, 1);     /* 平滑的奢华感 */
--ease-elegant: cubic-bezier(0.4, 0, 0.2, 1);        /* 材质般的优雅 */
--ease-refined: cubic-bezier(0.65, 0, 0.35, 1);      /* 精致的动效 */

/* 持续时间等级 */
--duration-instant: 100ms;   /* 微交互 */
--duration-quick: 200ms;     /* 标准过渡 */
--duration-smooth: 300ms;    /* 组件动画 */
--duration-gentle: 500ms;    /* 布局变化 */
--duration-luxurious: 800ms; /* 英雄区域动画 */
```

### 微交互
```css
/* 悬停提升效果 */
.hover-lift {
  transition: transform var(--duration-quick) var(--ease-elegant),
              box-shadow var(--duration-quick) var(--ease-elegant);
}

.hover-lift:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-moderate);
}

/* 焦点状态 */
.focus-ring:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.15);
}

/* 加载状态 */
.loading-shimmer {
  background: linear-gradient(
    90deg,
    var(--surface-raised) 0%,
    var(--surface-elevated) 50%,
    var(--surface-raised) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite var(--ease-luxury);
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
```

## 实施指南

### 框架无关原则

#### CSS 自定义属性
所有设计令牌都应实现为 CSS 自定义属性，以便任何框架都能使用它们：
```css
:root {
  /* 颜色 */
  --obsidian-black: #0A0A0A;
  --platinum: #E5E5E5;
  
  /* 排版 */
  --font-display: "SF Pro Display", system-ui, sans-serif;
  --font-body: "SF Pro Text", system-ui, sans-serif;
  
  /* 间距 */
  --space-4: 1rem;
  --space-8: 2rem;
  
  /* 阴影 */
  --shadow-gentle: 0 4px 8px rgba(0, 0, 0, 0.5);
}
```

#### 组件结构
设计具有清晰层级的组件，以便可以在任何框架中实现：
```html
<!-- 按钮组件结构 -->
<button class="btn btn-primary btn-lg">
  <span class="btn-icon"><!-- 图标 --></span>
  <span class="btn-text">按钮文本</span>
</button>
```

#### 工具类
为常用模式提供原子化的工具类：
```css
/* 间距工具类 */
.p-4 { padding: var(--space-4); }
.m-8 { margin: var(--space-8); }

/* 排版工具类 */
.text-platinum { color: var(--platinum); }
.text-champagne { color: var(--champagne-gold); }

/* 表面工具类 */
.surface-raised { background: var(--surface-raised); }
.surface-elevated { background: var(--surface-elevated); }
```

### 暗黑模式优化

#### 对比度要求
- 正常文本最小对比度：4.5:1
- 大号文本最小对比度：3:1
- 高级体验：尽可能达到 7:1+

#### 减轻眼部疲劳
```css
/* 减少蓝光 */
.reduced-blue {
  filter: hue-rotate(15deg) saturate(0.9);
}

/* 夜间模式下的暖色温 */
@media (prefers-color-scheme: dark) and (max-height: 800px) {
  :root {
    filter: sepia(0.1) hue-rotate(15deg);
  }
}
```

### 可访问性标准

#### 焦点管理
```css
/* 增强的焦点指示器 */
.focus-visible:focus-visible {
  outline: 2px solid var(--champagne-gold);
  outline-offset: 2px;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.2);
}
```

#### 屏幕阅读器支持
```css
/* 仅屏幕阅读器可见内容 */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}
```

该设计系统为创建高端暗黑模式体验提供了全面的基础，可以在任何技术栈中实施，同时保持奢华的美学和卓越的用户体验标准。

---

# Premium Dark Design System

## Table of Contents
1. [Overview](#overview)
2. [Brand Philosophy](#brand-philosophy)
3. [Visual Identity](#visual-identity)
4. [Color System](#color-system)
5. [Typography](#typography)
6. [Component Architecture](#component-architecture)
7. [Layout Principles](#layout-principles)
8. [UI Components](#ui-components)
9. [Design Patterns](#design-patterns)
10. [Animation & Motion](#animation--motion)
11. [Implementation Guidelines](#implementation-guidelines)

## Overview

This premium dark design system creates an ultra-luxury digital experience that embodies the exclusivity of Manhattan's private clubs and the sophistication of high-end financial institutions. Built with a dark-mode-first approach, it delivers an interface that speaks to discerning professionals who value substance, privacy, and exceptional quality.

### Core Principles
- **Dark-mode first**: Primary experience optimized for dark environments
- **Framework agnostic**: Adaptable to any frontend technology
- **Luxury materials**: Digital equivalent of platinum, obsidian, and crystal
- **Minimal complexity**: Maximum impact through restraint
- **Exclusive feel**: Private members' club aesthetic

## Brand Philosophy

### Vision
Create a digital sanctuary where premium content meets impeccable design - a space that feels like a private members' club in the digital realm, where every interaction exudes quality and exclusivity.

### Brand Personality
- **Luxurious**: Premium materials, exceptional craftsmanship
- **Exclusive**: Members-only feel, curated experiences  
- **Sophisticated**: Refined taste, cultured perspective
- **Discreet**: Understated elegance, quiet confidence
- **Innovative**: Cutting-edge while timeless

## Visual Identity

### Logo Treatment
- **Concept**: Minimalist execution with premium spacing
- **Weight**: Ultra-thin to light weights only
- **Spacing**: Generous letter-spacing (0.1em minimum)
- **Finishes**:
  - Platinum foil effect for special applications
  - Subtle glow treatments for digital
  - Embossed/debossed when applicable

### Design Principles
- Extreme minimalism with maximum impact
- Generous negative space as luxury element
- Perfect symmetry and mathematical precision
- Premium finishes and subtle textures
- Obsession with micro-interactions

## Color System

### Primary Palette - "Midnight Manhattan"
```css
/* Core Colors */
--obsidian-black: #0A0A0A;     /* rgb(10, 10, 10) - Primary background */
--deep-charcoal: #1A1A1A;      /* rgb(26, 26, 26) - Elevated surfaces */
--platinum: #E5E5E5;           /* rgb(229, 229, 229) - Primary text */
--pure-white: #FFFFFF;         /* rgb(255, 255, 255) - Maximum contrast */
--smoke: #2A2A2A;              /* rgb(42, 42, 42) - Secondary surfaces */
```

### Accent Colors - "Penthouse Collection"
```css
/* Luxury Accents */
--champagne-gold: #D4AF37;     /* rgb(212, 175, 55) - Premium highlights */
--manhattan-blue: #1E3A5F;     /* rgb(30, 58, 95) - Trust, depth */
--burgundy: #722F37;           /* rgb(114, 47, 55) - Rich accent */
--pearl-gray: #B8B8B8;        /* rgb(184, 184, 184) - Muted elements */
--midnight-navy: #0F1419;      /* rgb(15, 20, 25) - Deepest backgrounds */
```

### Functional Colors
```css
/* System States */
--success: #22C55E;            /* rgb(34, 197, 94) - Success states */
--warning: #F59E0B;            /* rgb(245, 158, 11) - Warning states */
--error: #EF4444;              /* rgb(239, 68, 68) - Error states */
--info: #3B82F6;               /* rgb(59, 130, 246) - Information */
```

### Opacity Scale
```css
/* Refined Transparency */
--opacity-ghost: 0.05;         /* Barely visible overlays */
--opacity-whisper: 0.10;       /* Subtle backgrounds */
--opacity-breath: 0.15;        /* Light touches */
--opacity-presence: 0.25;      /* Noticeable but gentle */
--opacity-statement: 0.40;     /* Clear but refined */
--opacity-bold: 0.60;          /* Strong presence */
```

## Typography

### Font Selection
**Primary**: System fonts optimized for luxury
```css
font-family: 
  "SF Pro Display",           /* macOS */
  "Segoe UI Variable",        /* Windows 11 */
  "Inter",                    /* Fallback */
  system-ui,
  -apple-system,
  sans-serif;
```

**Secondary**: Monospace for technical content
```css
font-family:
  "SF Mono",                  /* macOS */
  "Consolas",                 /* Windows */
  "Monaco",                   /* Fallback */
  monospace;
```

### Type Scale - "Platinum Hierarchy"
```css
/* Display Typography */
.display-xl { font-size: 4.5rem; font-weight: 100; letter-spacing: -0.02em; }
.display-lg { font-size: 3.75rem; font-weight: 100; letter-spacing: -0.02em; }
.display-md { font-size: 3rem; font-weight: 200; letter-spacing: -0.01em; }
.display-sm { font-size: 2.25rem; font-weight: 200; letter-spacing: -0.01em; }

/* Heading Typography */
.heading-xl { font-size: 1.875rem; font-weight: 300; letter-spacing: -0.01em; }
.heading-lg { font-size: 1.5rem; font-weight: 300; letter-spacing: -0.005em; }
.heading-md { font-size: 1.25rem; font-weight: 400; letter-spacing: 0; }
.heading-sm { font-size: 1.125rem; font-weight: 400; letter-spacing: 0; }
.heading-xs { font-size: 1rem; font-weight: 500; letter-spacing: 0.01em; }

/* Body Typography */
.body-xl { font-size: 1.25rem; font-weight: 300; line-height: 1.6; }
.body-lg { font-size: 1.125rem; font-weight: 300; line-height: 1.6; }
.body-md { font-size: 1rem; font-weight: 400; line-height: 1.5; }
.body-sm { font-size: 0.875rem; font-weight: 400; line-height: 1.4; }
.body-xs { font-size: 0.75rem; font-weight: 400; line-height: 1.3; }

/* Specialized Typography */
.label { font-size: 0.75rem; font-weight: 500; letter-spacing: 0.05em; text-transform: uppercase; }
.caption { font-size: 0.6875rem; font-weight: 400; letter-spacing: 0.02em; }
.overline { font-size: 0.625rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; }
```

## Component Architecture

### Elevation System
```css
/* Shadow Layers - Premium Depth */
--shadow-whisper: 0 1px 2px rgba(0, 0, 0, 0.3);
--shadow-subtle: 0 2px 4px rgba(0, 0, 0, 0.4);
--shadow-gentle: 0 4px 8px rgba(0, 0, 0, 0.5);
--shadow-moderate: 0 8px 16px rgba(0, 0, 0, 0.6);
--shadow-pronounced: 0 16px 32px rgba(0, 0, 0, 0.7);
--shadow-dramatic: 0 24px 48px rgba(0, 0, 0, 0.8);
```

### Surface Hierarchy
```css
/* Background Layers */
--surface-base: var(--obsidian-black);      /* Primary background */
--surface-raised: var(--deep-charcoal);     /* Cards, modals */
--surface-elevated: var(--smoke);           /* Dropdowns, tooltips */
--surface-overlay: rgba(26, 26, 26, 0.95);  /* Modal backgrounds */
```

### Border System
```css
/* Refined Borders */
--border-ghost: rgba(229, 229, 229, 0.05);  /* Barely visible */
--border-subtle: rgba(229, 229, 229, 0.10); /* Card outlines */
--border-gentle: rgba(229, 229, 229, 0.15); /* Form elements */
--border-defined: rgba(229, 229, 229, 0.25); /* Active states */
--border-prominent: rgba(229, 229, 229, 0.40); /* Focus states */
```

## Layout Principles

### Spacing Scale - "Golden Proportions"
```css
/* Premium Spacing System */
--space-1: 0.25rem;   /* 4px - Micro adjustments */
--space-2: 0.5rem;    /* 8px - Small gaps */
--space-3: 0.75rem;   /* 12px - Component padding */
--space-4: 1rem;      /* 16px - Standard spacing */
--space-5: 1.25rem;   /* 20px - Section spacing */
--space-6: 1.5rem;    /* 24px - Large spacing */
--space-8: 2rem;      /* 32px - Major sections */
--space-10: 2.5rem;   /* 40px - Page sections */
--space-12: 3rem;     /* 48px - Hero spacing */
--space-16: 4rem;     /* 64px - Layout spacing */
--space-20: 5rem;     /* 80px - Major layout */
--space-24: 6rem;     /* 96px - Architectural spacing */
```

### Grid System
```css
/* Luxury Grid - 12 Column System */
.container {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 var(--space-6);
}

/* Responsive Containers */
.container-xs { max-width: 480px; }   /* Mobile */
.container-sm { max-width: 640px; }   /* Small tablet */
.container-md { max-width: 768px; }   /* Tablet */
.container-lg { max-width: 1024px; }  /* Desktop */
.container-xl { max-width: 1280px; }  /* Large desktop */
.container-2xl { max-width: 1440px; } /* Extra large */
```

## UI Components

### Buttons - "Executive Actions"
```css
/* Primary Button - Champagne Gold */
.btn-primary {
  background: var(--champagne-gold);
  color: var(--obsidian-black);
  border: 1px solid var(--champagne-gold);
  font-weight: 500;
  letter-spacing: 0.01em;
}

/* Secondary Button - Platinum Outline */
.btn-secondary {
  background: transparent;
  color: var(--platinum);
  border: 1px solid var(--border-defined);
  font-weight: 400;
}

/* Tertiary Button - Minimal */
.btn-tertiary {
  background: transparent;
  color: var(--pearl-gray);
  border: none;
  font-weight: 400;
}

/* Ghost Button - Subtle Presence */
.btn-ghost {
  background: rgba(229, 229, 229, 0.05);
  color: var(--platinum);
  border: 1px solid var(--border-ghost);
}
```

### Cards - "Premium Surfaces"
```css
.card {
  background: var(--surface-raised);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  box-shadow: var(--shadow-gentle);
  overflow: hidden;
}

.card-elevated {
  background: var(--surface-elevated);
  box-shadow: var(--shadow-moderate);
}

.card-floating {
  background: var(--surface-elevated);
  box-shadow: var(--shadow-pronounced);
  transform: translateY(-2px);
}
```

### Forms - "Refined Inputs"
```css
.input {
  background: var(--surface-raised);
  border: 1px solid var(--border-gentle);
  color: var(--platinum);
  border-radius: 6px;
  padding: var(--space-3) var(--space-4);
  font-weight: 300;
}

.input:focus {
  border-color: var(--champagne-gold);
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
  outline: none;
}

.input::placeholder {
  color: var(--pearl-gray);
  font-weight: 300;
}
```

## Design Patterns

### Navigation - "Private Club Wayfinding"
```css
/* Top Navigation */
.nav-primary {
  background: rgba(10, 10, 10, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-ghost);
}

/* Sidebar Navigation */
.nav-sidebar {
  background: var(--surface-raised);
  border-right: 1px solid var(--border-subtle);
  width: 280px;
}

/* Navigation Items */
.nav-item {
  color: var(--pearl-gray);
  font-weight: 300;
  letter-spacing: 0.01em;
  transition: all 200ms ease;
}

.nav-item:hover {
  color: var(--platinum);
  background: rgba(229, 229, 229, 0.05);
}

.nav-item.active {
  color: var(--champagne-gold);
  background: rgba(212, 175, 55, 0.1);
}
```

### Data Display - "Information Hierarchy"
```css
/* Tables */
.table {
  background: var(--surface-base);
  border: 1px solid var(--border-subtle);
}

.table-header {
  background: var(--surface-raised);
  color: var(--pearl-gray);
  font-weight: 500;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  font-size: 0.75rem;
}

.table-row:hover {
  background: rgba(229, 229, 229, 0.03);
}

.table-row:nth-child(even) {
  background: rgba(229, 229, 229, 0.01);
}
```

## Animation & Motion

### Transition System
```css
/* Premium Easing Functions */
--ease-luxury: cubic-bezier(0.25, 0.1, 0.25, 1);     /* Smooth luxury feel */
--ease-elegant: cubic-bezier(0.4, 0, 0.2, 1);        /* Material elegance */
--ease-refined: cubic-bezier(0.65, 0, 0.35, 1);      /* Sophisticated motion */

/* Duration Scale */
--duration-instant: 100ms;   /* Micro-interactions */
--duration-quick: 200ms;     /* Standard transitions */
--duration-smooth: 300ms;    /* Component animations */
--duration-gentle: 500ms;    /* Layout changes */
--duration-luxurious: 800ms; /* Hero animations */
```

### Micro-Interactions
```css
/* Hover Elevations */
.hover-lift {
  transition: transform var(--duration-quick) var(--ease-elegant),
              box-shadow var(--duration-quick) var(--ease-elegant);
}

.hover-lift:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-moderate);
}

/* Focus States */
.focus-ring:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.15);
}

/* Loading States */
.loading-shimmer {
  background: linear-gradient(
    90deg,
    var(--surface-raised) 0%,
    var(--surface-elevated) 50%,
    var(--surface-raised) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite var(--ease-luxury);
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
```

## Implementation Guidelines

### Framework Agnostic Principles

#### CSS Custom Properties
All design tokens should be implemented as CSS custom properties, allowing any framework to consume them:
```css
:root {
  /* Colors */
  --obsidian-black: #0A0A0A;
  --platinum: #E5E5E5;
  
  /* Typography */
  --font-display: "SF Pro Display", system-ui, sans-serif;
  --font-body: "SF Pro Text", system-ui, sans-serif;
  
  /* Spacing */
  --space-4: 1rem;
  --space-8: 2rem;
  
  /* Shadows */
  --shadow-gentle: 0 4px 8px rgba(0, 0, 0, 0.5);
}
```

#### Component Structure
Design components with clear hierarchies that can be implemented in any framework:
```html
<!-- Button Component Structure -->
<button class="btn btn-primary btn-lg">
  <span class="btn-icon"><!-- Icon --></span>
  <span class="btn-text">Button Text</span>
</button>
```

#### Utility Classes
Provide atomic utility classes for common patterns:
```css
/* Spacing Utilities */
.p-4 { padding: var(--space-4); }
.m-8 { margin: var(--space-8); }

/* Typography Utilities */
.text-platinum { color: var(--platinum); }
.text-champagne { color: var(--champagne-gold); }

/* Surface Utilities */
.surface-raised { background: var(--surface-raised); }
.surface-elevated { background: var(--surface-elevated); }
```

### Dark Mode Optimization

#### Contrast Requirements
- Minimum contrast ratio: 4.5:1 for normal text
- Minimum contrast ratio: 3:1 for large text
- Premium experience: Target 7:1+ wherever possible

#### Eye Strain Reduction
```css
/* Reduced Blue Light */
.reduced-blue {
  filter: hue-rotate(15deg) saturate(0.9);
}

/* Warm Temperature for Late Hours */
@media (prefers-color-scheme: dark) and (max-height: 800px) {
  :root {
    filter: sepia(0.1) hue-rotate(15deg);
  }
}
```

### Accessibility Standards

#### Focus Management
```css
/* Enhanced Focus Indicators */
.focus-visible:focus-visible {
  outline: 2px solid var(--champagne-gold);
  outline-offset: 2px;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.2);
}
```

#### Screen Reader Support
```css
/* Screen Reader Only Content */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}
```

This design system provides a comprehensive foundation for creating premium dark-mode experiences that can be implemented across any technology stack while maintaining the luxury aesthetic and exceptional user experience standards.
