# Domain标准粘性搜索实现计划

## [Overview]
实现Domain.com.au标准的粘性搜索行为，解决当前导航栏毛玻璃效果和筛选面板异常问题。

当前Vue应用需要完全重构其布局定位系统，从现有的混合定位模式（fixed导航 + sticky搜索）改为Domain标准模式（相对导航 + 正确的sticky搜索）。核心目标是实现：导航栏随滚动消失，搜索框在滚动到顶部时粘在屏幕顶部并全屏展开，同时保持内容与房源卡片580px对齐。

## [Types]
定义搜索区域的状态类型和布局模式。

```typescript
// 搜索区域状态类型
interface SearchAreaState {
  isSticky: boolean;
  scrollPosition: number;
}

// Domain标准布局模式
interface DomainLayoutMode {
  navigation: 'relative' | 'fixed';
  searchArea: 'normal' | 'sticky';
  backgroundWidth: 'container' | 'fullscreen';
  contentAlignment: '580px' | 'full';
}
```

## [Files]
需要修改的文件和具体更改内容。

### 需要修改的文件：

**1. vue-frontend/src/components/Navigation.vue**
- 将桌面端导航从 `position: fixed` 改为 `position: relative`
- 移除所有毛玻璃效果 (`backdrop-filter: blur()`)
- 统一使用纯白色背景和阴影效果

**2. vue-frontend/src/App.vue**
- 移除桌面端的 `padding-top: 64px`
- 恢复自然文档流布局

**3. vue-frontend/src/views/Home.vue**
- 重新实现搜索区域的粘性定位逻辑
- 正确实现全屏宽度背景但内容580px对齐
- 修复当前错误的负margin全屏技术

**4. vue-frontend/src/components/FilterTabs.vue**
- 移除内部状态管理冲突
- 修复"筛选"按钮文字消失问题

**5. vue-frontend/src/style.css**
- 清理重复的导航样式定义
- 移除全局的毛玻璃效果样式

## [Functions]
需要修改和创建的函数。

### 新增函数：

**Home.vue - 滚动监听函数**
```javascript
const handleScroll = () => {
  const searchElement = searchSectionRef.value;
  const scrollTop = window.pageYOffset;
  
  if (scrollTop > navigationHeight) {
    isSearchSticky.value = true;
  } else {
    isSearchSticky.value = false;
  }
}
```

### 修改函数：

**FilterTabs.vue - toggleFullPanel**
- 移除内部状态管理
- 简化为纯事件触发函数

**FilterTabs.vue - toggleDropdown**
- 移除与showFullPanel的状态冲突
- 确保下拉框和面板状态独立管理

## [Classes]
CSS类的重构和新增。

### 新增CSS类：

**搜索区域状态类**
```css
.search-area-sticky {
  position: sticky;
  top: 0;
  z-index: 50;
  width: 100vw;
  left: 50%;
  margin-left: -50vw;
  background: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.search-content-centered {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 32px 16px;
}

.search-bar-580 {
  width: 580px;
  flex-shrink: 0;
}
```

### 修改CSS类：

**Navigation相关类**
- `.top-nav`: 从 `position: fixed` 改为 `position: relative`
- 移除所有 `backdrop-filter` 属性
- 统一背景色为 `background: white`

## [Dependencies]
当前依赖保持不变。

Vue 3 + Element Plus + Vite + Pinia + Vue Router技术栈已满足所有需求，无需添加新依赖。

## [Testing]
测试方法和验证策略。

### 功能测试：
1. **导航行为测试**: 验证导航栏随滚动消失
2. **粘性搜索测试**: 验证搜索框在正确位置变为粘性
3. **全屏展开测试**: 验证粘性时背景全屏，内容580px对齐
4. **筛选功能测试**: 验证筛选按钮和面板正常工作
5. **响应式测试**: 验证移动端和桌面端行为一致性

### 浏览器兼容性测试：
- Chrome, Safari, Firefox, Edge
- 移动端Safari, Android Chrome

## [Implementation Order]
逐步实施顺序，避免引发连锁问题。

### 第1步：恢复基础布局流
1. 修改App.vue - 移除padding-top补偿
2. 修改Navigation.vue - 改为相对定位，移除毛玻璃效果

### 第2步：重构搜索区域粘性逻辑
1. 重写Home.vue中的搜索区域CSS
2. 实现正确的全屏宽度+内容对齐技术
3. 添加滚动监听逻辑（如需要）

### 第3步：修复组件状态管理
1. 清理FilterTabs.vue的状态冲突
2. 确保筛选面板状态正确管理

### 第4步：清理冗余样式
1. 移除style.css中的重复导航样式
2. 确保样式封装在各自组件内

### 第5步：验证和测试
1. 启动开发服务器
2. 使用浏览器验证所有Domain标准行为
3. 测试筛选功能是否正常工作

---

**关键成功因素**: 正确理解Domain的粘性搜索行为，实现精确的CSS定位逻辑，确保组件状态管理清晰。
