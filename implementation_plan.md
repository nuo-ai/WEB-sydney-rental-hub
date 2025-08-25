# Implementation Plan: 通勤时间计算器集成到PropertyDetail.vue

## [Overview]
将frontend/details.html中完整的通勤时间计算器功能集成到vue-frontend/src/views/PropertyDetail.vue中，提供四种交通方式的通勤时间计算，预设大学目的地，以及自定义目的地添加功能。

这个实施计划将现有的600+行功能完备的PropertyDetail.vue组件增强通勤计算功能，而不是重新创建组件。计划严格遵循sydney-rental-hub.rules.md中的所有规则，特别是Memory Bank原则、Standard Task Execution、Technical Standards和边界管理原则。

该功能将使用Vue 3 Composition API、Element Plus UI库、Pinia状态管理，并通过Netlify Function调用Google Directions API，为用户提供准确的通勤时间信息。

## [Types]
定义通勤计算器相关的TypeScript类型和接口。

```typescript
// 交通方式枚举
type CommuteMode = 'DRIVING' | 'TRANSIT' | 'WALKING' | 'BICYCLING'

// 通勤结果接口
interface CommuteResult {
  duration: string    // "15 分钟"
  distance: string    // "8.2 km" 
  error?: string      // 错误信息
}

// 目的地接口
interface CommuteDestination {
  id: string                              // 唯一标识符
  name: string                           // 显示名称
  address: string                        // 完整地址
  results: Record<CommuteMode, CommuteResult | null>  // 各交通方式结果缓存
  isLoading: boolean                     // 加载状态
}

// 预设目的地接口
interface PresetDestination {
  name: string        // "UTS"
  address: string     // "15 Broadway, Ultimo NSW 2007, Australia"
}

// 通勤状态接口
interface CommuteState {
  destinations: CommuteDestination[]     // 用户添加的目的地列表
  activeMode: CommuteMode               // 当前选中的交通方式
  isCalculating: boolean                // 全局计算状态
  presetDestinations: PresetDestination[] // 预设目的地列表
}
```

## [Files]
详细的文件修改计划。

### 新建文件：
- `vue-frontend/src/components/CommuteCalculator.vue` - 独立的通勤计算器组件
- `vue-frontend/src/services/commuteService.js` - 通勤计算API服务
- `vue-frontend/src/composables/useCommute.js` - 通勤计算逻辑组合式函数

### 修改文件：
- `vue-frontend/src/views/PropertyDetail.vue` - 集成CommuteCalculator组件
- `vue-frontend/src/stores/properties.js` - 添加通勤状态管理
- `vue-frontend/src/services/api.js` - 添加通勤API调用方法

### 配置文件：
- 无需修改package.json（已有所需依赖：Element Plus、Pinia、Vue 3）

## [Functions]
详细的函数规划。

### 新建函数：

#### vue-frontend/src/services/commuteService.js
- `fetchCommuteTime(origin: string, destination: string, mode: CommuteMode)` - 调用Netlify Function获取通勤时间
- `getPresetDestinations()` - 获取预设目的地列表

#### vue-frontend/src/composables/useCommute.js
- `useCommute()` - 主要组合式函数，返回通勤状态和方法
- `addDestination(name: string, address: string)` - 添加目的地
- `removeDestination(id: string)` - 删除目的地
- `switchMode(mode: CommuteMode)` - 切换交通方式
- `calculateCommuteTime(destination: CommuteDestination, mode: CommuteMode)` - 计算单个目的地的通勤时间

#### vue-frontend/src/components/CommuteCalculator.vue
- `handlePresetClick(preset: PresetDestination)` - 处理预设目的地点击
- `handleAddCustomDestination()` - 处理自定义目的地添加
- `handleModeSwitch(mode: CommuteMode)` - 处理交通方式切换
- `handleRemoveDestination(id: string)` - 处理目的地移除

### 修改函数：

#### vue-frontend/src/stores/properties.js
- 新增 `addCommuteDestination(propertyId, destination)` - 添加通勤目的地
- 新增 `removeCommuteDestination(propertyId, destinationId)` - 移除通勤目的地
- 新增 `setCommuteMode(mode)` - 设置活动交通方式
- 新增 `updateCommuteResult(destinationId, mode, result)` - 更新通勤结果

#### vue-frontend/src/services/api.js
- 新增 `getDirections(origin, destination, mode)` - 调用通勤计算API

## [Classes]
类结构规划（主要是Vue组件类）。

### 新建组件类：

#### CommuteCalculator.vue
- 使用 `<script setup>` Composition API语法
- 集成Element Plus组件：el-tabs、el-tab-pane、el-button、el-input、el-loading、el-message
- 响应式设计：移动端友好的标签页和按钮布局
- 状态管理：使用Pinia store管理通勤数据
- 错误处理：优雅处理API调用失败和网络错误

#### 主要方法：
- `setup()` - 组合式API设置函数
- 响应式数据：destinations、activeMode、isLoading
- 计算属性：filteredResults、hasDestinations
- 监听器：activeMode变化时重新计算
- 生命周期：onMounted时加载预设目的地

### 修改组件类：

#### PropertyDetail.vue
- 在现有组件中添加CommuteCalculator组件引用
- 在适当位置插入通勤计算器section（地图section之后）
- 传递必要的props：property信息用于起始地址

## [Dependencies]
依赖项管理。

### 现有依赖（无需新增）：
- Vue 3 (^3.4.0) - 核心框架
- Element Plus (^2.4.0) - UI库
- Pinia (^2.1.0) - 状态管理
- @element-plus/icons-vue (^2.3.0) - 图标库

### API依赖：
- Google Maps Directions API - 通过现有Netlify Function调用
- Google Places API - 地址自动完成功能

### 第三方库考虑：
- 无需新增第三方库，使用现有Element Plus和Vue生态

## [Testing]
测试策略。

### 单元测试（Vitest）：
- `tests/unit/composables/useCommute.spec.js` - useCommute组合式函数测试
- `tests/unit/services/commuteService.spec.js` - 通勤服务API测试
- `tests/unit/components/CommuteCalculator.spec.js` - CommuteCalculator组件测试
- `tests/unit/stores/properties.spec.js` - properties store通勤相关方法测试

### 测试用例覆盖：
1. 预设目的地加载和点击
2. 自定义目的地添加和验证
3. 交通方式切换功能
4. API调用成功和失败场景
5. 加载状态和错误状态处理
6. 目的地删除功能
7. 结果缓存机制

### E2E测试（Playwright）：
- `tests/e2e/property-detail-commute.spec.js` - 完整通勤计算器用户流程测试

### 测试数据：
- Mock API responses for different commute scenarios
- Test property data with valid latitude/longitude
- Preset destination test data

## [Implementation Order]
实施顺序（严格按顺序执行）。

### Phase 1: 基础服务和API集成
1. **创建commuteService.js** - 实现API调用逻辑，集成Netlify Function
2. **更新api.js** - 添加通勤相关API方法
3. **测试API集成** - 验证Netlify Function调用正常

### Phase 2: 状态管理和数据层
4. **更新properties.js store** - 添加通勤状态管理和方法
5. **创建useCommute.js** - 实现通勤逻辑组合式函数
6. **单元测试数据层** - 测试store和composable功能

### Phase 3: UI组件开发
7. **创建CommuteCalculator.vue** - 实现完整通勤计算器组件
8. **样式和响应式设计** - 使用Element Plus确保移动端友好
9. **组件单元测试** - 测试用户交互和状态管理

### Phase 4: 集成和优化
10. **集成到PropertyDetail.vue** - 在现有详情页中添加通勤功能
11. **端到端测试** - 验证完整用户流程
12. **性能优化** - 优化API调用和缓存机制

### Phase 5: 验证和文档
13. **浏览器测试** - 在实际浏览器中验证功能
14. **更新memory-bank** - 记录功能完成状态
15. **代码审查和清理** - 确保代码质量和规范

---

## 关键实施注意事项：

### 遵循Clinerules：
- 严格使用Element Plus UI库，不自定义样式
- 使用replace_in_file而非write_to_file修改现有文件
- 每个阶段等待用户确认后再继续
- 遵循Vue 3 Composition API和PascalCase命名

### 技术考虑：
- API调用错误处理和重试机制
- 移动端响应式设计优化
- 无障碍性支持（ARIA标签）
- SEO友好的结构化数据

### 用户体验：
- 加载状态的优雅显示
- 错误信息的用户友好提示
- 预设目的地的快速选择
- 结果的清晰可读展示
