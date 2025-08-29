# 代码注释规则

## ⚠️ Claude必须严格遵守
**Claude在编写代码时必须100%遵循这些规则，不得违反**

## 核心原则
**代码应该自文档化，注释只在代码无法自我解释时补充上下文**

## 必须写注释的场景

### 1. 解释"为什么"而非"什么"
```javascript
// 防止重复提交造成数据不一致
if (isSubmitting) return;

// 澳洲租房市场周租金转月租金使用4.33倍率（52周/12月）
const monthlyRent = weeklyRent * 4.33;
```

### 2. 复杂的业务逻辑
```javascript
// 悉尼房源"Available now"表示立即可入住
// 未来时间段筛选时需要排除这些房源
if (!property.available_date && dateRange.isInFuture()) {
  return false;
}
```

### 3. 技术决策和权衡
```javascript
// 使用内存缓存替代Redis：数据量小，避免外部依赖
// 缺点：重启后丢失，但15分钟TTL使影响可控
const cache = new Map();
```

### 4. 待办事项和已知问题
```javascript
// TODO: 用户量超过1000时改为虚拟滚动
// FIXME: iOS Safari日期选择器兼容性问题
// HACK: 临时方案，等API v2上线后重构
```

### 5. API参数和返回值的特殊说明
```javascript
/**
 * @param suburbs - 逗号分隔的区域列表，支持大小写不敏感匹配
 * @returns 包含分页信息的房源数组，已按租金升序排列
 */
```

## 禁止的做法

### ❌ 重复显而易见的代码
```javascript
// 错误示例
// 设置加载状态为true
loading = true;

// 递增计数器
counter++;
```

### ❌ 过时的注释
维护不当的注释比没有注释更危险

### ❌ 注释掉的代码
使用Git管理版本历史，不要留存注释代码

### ❌ 用注释弥补糟糕的命名
```javascript
// 错误：用注释解释变量
let d; // 租金差额

// 正确：使用清晰的命名
let rentDifference;
```

## 注释格式规范

- 单行注释：`//` 后加一个空格
- 多行注释：用于函数/类的文档说明
- 中文注释：确保说明清晰的业务逻辑
- 英文注释：仅用于通用技术说明

## Claude的自查清单
在提交代码前，Claude必须自查：
- [ ] 是否有解释"什么"的废话注释？删除！
- [ ] 是否有步骤编号注释（1、2、3）？删除！
- [ ] 是否解释了"为什么"做技术决策？保留！
- [ ] 是否说明了业务逻辑和特殊规则？保留！
- [ ] 变量命名是否清晰到不需要注释？

## 记住
**如果需要大量注释才能解释代码，首先考虑重构代码使其更清晰**

## 违规示例（Claude不应该写的）
```javascript
// ❌ 错误：步骤编号
// 1. 导入组件
import Component from './Component.vue'

// ❌ 错误：解释显而易见的代码
// 设置loading为true
loading = true

// ❌ 错误：用注释代替好的命名
let d; // 租金差额
```

## 正确示例（Claude应该写的）
```javascript
// 虚拟滚动阈值50条：低于此数量性能影响可忽略
const VIRTUAL_SCROLL_THRESHOLD = 50

// localStorage开关：便于A/B测试和问题快速回滚
const enableVirtual = localStorage.getItem('enableVirtualScroll') !== 'false'

// 澳洲租房周租转月租使用4.33倍率（52周/12月）
const monthlyRent = weeklyRent * 4.33
```