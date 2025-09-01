# 📋 Sydney Rental Hub - TODO管理清单

> 最后更新：2025-01-30
> 使用 Todo Tree 插件可在侧边栏查看所有 TODO/FIXME/HACK 标记

---

## 待办事项 (Todo)

### 高优先级 (P0) - 第一期核心功能

- [ ] **个人中心页面开发** #feature @2d

  - [ ] 我的收藏
  - [ ] 浏览历史
  - [ ] 搜索订阅管理
  - [ ] 通知设置
- [ ] **排序功能实现** #feature @4h

  - [ ] 价格排序（高到低/低到高）
  - [ ] 时间排序（最新/最旧）
  - [ ] 面积排序
- [ ] **搜索条件保存** #feature @1d

  - [ ] 保存当前搜索条件
  - [ ] 命名搜索条件
  - [ ] 快速应用已保存条件

### 中优先级 (P1) - 第一期增强功能

- [ ] **地图视图实现**（参考Zillow） #feature @1w

  - [ ] 集成地图组件
  - [ ] 房源位置标记
  - [ ] 框选区域搜索
  - [ ] 地图与列表切换
- [ ] **新房源自动提醒** #feature @3d

  - [ ] 后台任务扫描新房源
  - [ ] 匹配用户订阅条件
  - [ ] 邮件通知系统
  - [ ] 通知历史记录
- [ ] **收藏功能后端API** #feature @2d

  ```python
  # TODO [P1]: 实现 /api/favorites CRUD端点
  # 文件：backend/crud/favorites_crud.py
  # 需求：用户收藏列表持久化
  ```
- [ ] **通勤功能CRUD完善** #feature @3d

  ```python
  # TODO [P1]: 完成通勤地址的增删改查
  # 文件：backend/crud/commute_crud.py
  # 当前：框架已搭建，核心逻辑待实现
  ```
- [ ] **图片懒加载** #performance @4h

  ```javascript
  // TODO [P1]: 实现 v-lazy 指令或使用 vue-lazyload
  // 影响：首屏加载时间减少60%
  ```

### 低优先级 (P2) - 第二期规划

- [ ] **AI助手功能** #feature @2w

  - [ ] 自然语言搜索
  - [ ] 房源对比功能
  - [ ] 个性化推荐
  - [ ] 智能问答
- [ ] **GraphQL集成** #feature @2d

  ```javascript
  // TODO [P2]: 集成 Apollo Client 替代部分 REST API
  // 好处：减少过度获取，提升性能
  ```
- [ ] **PWA离线支持** #feature @1w

  ```javascript
  // TODO [P2]: 添加 Service Worker 实现离线浏览
  ```
- [ ] **单元测试** #quality @1w

  ```javascript
  // TODO [P2]: 使用 Vitest 添加组件测试
  // 目标覆盖率：80%
  ```

## 💡 优化想法 (Ideas/Backlog)

> 💭 讨论中产生的建议，需要评估后才决定是否实施

TODO管理决策流程

```
1. 讨论阶段 → Ideas/Backlog（不设优先级）
2. 评估决策 → 确定是否实施
3. 计划排期 → 分配优先级（P0/P1/P2）
4. 开始执行 → 移到"正在进行"
5. 完成验证 → 移到"已完成"
```

### 优先级分配原则

- **P0**: 仅限阻塞性问题（系统崩溃、无法使用核心功能）
- **P1**: 已承诺的功能、影响用户体验的bug
- **P2**: 性能优化、代码质量改进
- **Ideas**: 所有讨论中的建议，未经决策不分配优先级

### 代码中的TODO标记规范

```javascript
// TODO [优先级] [负责人] [日期]: 描述
// FIXME: 需要修复的bug
// HACK: 临时解决方案
// NOTE: 重要说明
// OPTIMIZE: 性能优化点
// REVIEW: 需要代码审查
```

### 优先级定义

- **P0**: 阻塞性问题，立即处理
- **P1**: 重要功能，本周/本月完成
- **P2**: 改进项，有时间再做
- **P3**: 想法阶段，待评估

*使用 Todo Tree 插件可以在 VSCode 侧边栏实时查看所有 TODO 标记*
