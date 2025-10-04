# 设计系统组件库文档

## 概述

本设计系统基于Sydney Rental Hub区域筛选面板现代化设计的成功模式提取，提供一致的视觉风格和用户体验。

## 设计原则

- **中性灰色调**：避免过度品牌化，使用中性灰色调作为主要颜色
- **微妙的圆角**：4-6px的圆角，现代但不过分
- **一致的间距系统**：基于4px基础单位的间距系统
- **清晰的层次结构**：通过颜色、字重、间距建立清晰的视觉层次

## 设计令牌

设计令牌定义在 `src/styles/design-tokens.css` 中，包含：

### 颜色系统

- **中性灰色调**：`--color-neutral-50` 到 `--color-neutral-900`
- **语义化颜色**：`--color-bg-primary`、`--color-text-primary` 等
- **交互状态颜色**：`--color-hover-bg`、`--color-focus-ring` 等

### 间距系统

- `--space-2xs`: 4px
- `--space-xs`: 6px
- `--space-sm`: 8px
- `--space-md`: 12px
- `--space-lg`: 16px
- `--space-xl`: 20px
- `--space-2xl`: 24px
- `--space-3xl`: 32px

### 字体系统

- **字号**：`--font-size-2xs` (11px) 到 `--font-size-xl-compact` (18px)
- **字重**：`--font-weight-regular` (400) 到 `--font-weight-bold` (700)
- **行高**：`--line-height-tight` (1.2) 到 `--line-height-relaxed` (1.6)

### 圆角系统

- `--radius-compact-sm`: 2px
- `--radius-compact-md`: 4px
- `--radius-compact-lg`: 6px
- `--radius-compact-xl`: 8px

## 基础组件

### BaseChip

可复用的标签组件，用于显示选中的筛选条件。

```vue
<BaseChip @remove="handleRemove">区域名称</BaseChip>
<BaseChip variant="selected" removable>已选择</BaseChip>
<BaseChip variant="hover" :removable="false">不可移除</BaseChip>
```

**Props:**

- `variant`: 'default' | 'selected' | 'hover' - 变体类型
- `removable`: boolean - 是否可移除
- `removeLabel`: string - 移除按钮的无障碍标签

**Events:**

- `remove` - 点击移除按钮时触发

### BaseSearchInput

可复用的搜索输入框组件，提供一致的搜索体验。

```vue
<BaseSearchInput v-model="keyword" placeholder="搜索区域" @clear="handleClear" />
<BaseSearchInput v-model="query" :clearable="false" />
<BaseSearchInput v-model="search" autofocus />
```

**Props:**

- `modelValue`: string - v-model绑定值
- `placeholder`: string - 占位符文本
- `clearable`: boolean - 是否显示清除按钮
- `disabled`: boolean - 是否禁用
- `ariaLabel`: string - 无障碍标签
- `clearLabel`: string - 清除按钮的无障碍标签
- `autofocus`: boolean - 是否自动聚焦

**Events:**

- `update:modelValue` - 值变化时触发
- `input` - 输入时触发
- `focus` - 聚焦时触发
- `blur` - 失焦时触发
- `clear` - 清除时触发
- `keydown` - 键盘事件

**Methods:**

- `focus()` - 聚焦输入框
- `blur()` - 失焦输入框

### BaseButton

可复用的按钮组件，提供一致的按钮体验。

```vue
<BaseButton @click="handleClick">默认按钮</BaseButton>
<BaseButton variant="primary" :loading="isLoading">主要按钮</BaseButton>
<BaseButton variant="secondary" size="small">次要按钮</BaseButton>
<BaseButton variant="ghost">幽灵按钮</BaseButton>
<BaseButton variant="danger">危险按钮</BaseButton>
```

**Props:**

- `variant`: 'primary' | 'secondary' | 'ghost' | 'danger' - 按钮变体
- `size`: 'small' | 'medium' | 'large' - 按钮尺寸
- `type`: 'button' | 'submit' | 'reset' - 按钮类型
- `disabled`: boolean - 是否禁用
- `loading`: boolean - 是否加载中
- `block`: boolean - 是否块级按钮

**Events:**

- `click` - 点击时触发

**Slots:**

- `default` - 按钮文本
- `icon` - 前置图标
- `iconRight` - 后置图标

### BaseListItem

可复用的列表项组件，提供一致的列表项体验。

```vue
<BaseListItem @click="handleClick">基础列表项</BaseListItem>
<BaseListItem selected>已选择的项</BaseListItem>
<BaseListItem disabled>禁用的项</BaseListItem>
<BaseListItem :clickable="false" :bordered="false">静态项</BaseListItem>
```

**Props:**

- `selected`: boolean - 是否选中
- `disabled`: boolean - 是否禁用
- `clickable`: boolean - 是否可点击
- `bordered`: boolean - 是否显示边框
- `role`: string - ARIA角色

**Events:**

- `click` - 点击时触发
- `select` - 选择状态变化时触发

**Slots:**

- `default` - 主要内容
- `prefix` - 前置内容
- `suffix` - 后置内容
- `description` - 描述内容

## 使用指南

### 1. 导入组件

```javascript
import BaseChip from '@/components/base/BaseChip.vue'
import BaseSearchInput from '@/components/base/BaseSearchInput.vue'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseListItem from '@/components/base/BaseListItem.vue'
```

### 2. 使用设计令牌

在组件样式中使用设计令牌：

```css
.my-component {
  padding: var(--space-md);
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-compact-md);
  color: var(--color-text-primary);
  font-size: var(--font-size-sm);
  transition: var(--transition-normal);
}

.my-component:hover {
  background: var(--color-hover-bg);
  border-color: var(--color-hover-border);
}
```

### 3. 工具类

可以使用预定义的工具类：

```html
<div class="filter-text-primary filter-bg-secondary filter-radius-md">使用工具类的内容</div>
```

### 4. 响应式设计

所有组件都包含响应式设计，在移动端会自动调整：

- 字体大小增加（iOS防缩放）
- 触摸目标增大
- 间距适当调整

## 最佳实践

### 1. 颜色使用

- **主要文本**：使用 `--color-text-primary`
- **次要文本**：使用 `--color-text-secondary`
- **边框**：使用 `--color-border-default`
- **背景**：使用 `--color-bg-primary` 或 `--color-bg-secondary`

### 2. 间距使用

- **组件内部间距**：使用 `--space-sm` (8px)
- **组件之间间距**：使用 `--space-md` (12px) 或 `--space-lg` (16px)
- **区块间距**：使用 `--space-xl` (20px) 或 `--space-2xl` (24px)

### 3. 交互状态

- **悬浮状态**：使用 `--color-hover-bg` 和 `--color-hover-border`
- **选中状态**：使用 `--color-selected-bg` 和 `--color-selected-border`
- **焦点状态**：使用 `--color-focus-ring`

### 4. 过渡动画

- **快速交互**：使用 `--transition-fast` (0.15s)
- **常规交互**：使用 `--transition-normal` (0.2s)
- **慢速交互**：使用 `--transition-slow` (0.3s)

## 扩展指南

### 添加新的设计令牌

1. 在 `src/styles/design-tokens.css` 中添加新令牌
2. 遵循命名约定：语义层使用 `--[category]-[property]`，组件层继续以 `--filter-[component]-*` 聚合
3. 提供语义化的名称而非具体值

### 创建新的基础组件

1. 在 `src/components/base/` 目录下创建新组件
2. 使用设计令牌而非硬编码值
3. 提供完整的Props、Events、Slots文档
4. 包含响应式设计
5. 添加无障碍支持

### 应用到现有组件

1. 导入所需的基础组件
2. 替换硬编码样式为设计令牌
3. 使用基础组件替换重复的UI元素
4. 保持现有功能不变

## 维护指南

### 版本控制

- 设计令牌的变更需要谨慎评估影响范围
- 基础组件的API变更需要更新所有使用方
- 保持向后兼容性

### 测试

- 在不同屏幕尺寸下测试组件
- 验证无障碍功能
- 确保与现有组件的兼容性

### 文档更新

- 新增组件时更新此文档
- 记录重要的设计决策
- 提供使用示例和最佳实践
