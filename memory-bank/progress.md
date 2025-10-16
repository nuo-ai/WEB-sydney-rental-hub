# 项目进展 (Progress)

**文档状态**: 生存文档 (Living Document)
**最后更新**: 2025-10-16

---

## 当前阶段

**阶段 2: 前端组件系统搭建**

我们正处于 MVP 冲刺计划的第 2 阶段。

## 已完成的里程碑

- **Monorepo 架构建立**:
  - 成功搭建了基于 pnpm 和 Turborepo 的 Monorepo。
  - 清理了项目结构，移除了冲突和冗余的配置。

- **核心技术决策完成**:
  - 决定废弃旧版前端，保留并重构后端。
  - 确定在新前端 `apps/vue-juwo` 中使用 `shadcn-vue` 和 `tailwindcss`。

- **MVP 计划制定**:
  - 制定了详细的、分阶段的 MVP 冲刺计划，并记录在 `PROJECT_PLAN.md`。

- **Nextra 文档站初始化**:
  - 完成 Nextra 文档站基础配置
  - 实现 LivePreview iframe 实时预览功能
  - 建立基础文档结构和页面

- **前端基础环境搭建**:
  - 解决 Vue 项目 Tailwind CSS PostCSS 插件迁移问题
  - 验证 shadcn-vue 核心组件(Button/Card/Sheet)可用性

## 下一阶段目标

- **阶段 2: 前端组件系统搭建** ✅ 已完成:
  - 使用 shadcn-vue 手动安装核心组件(Button/Card/Sheet)
  - 在 Vue 项目中实现基础页面结构（SplashView、ListingsView）
  - 完善 Nextra 文档中的组件说明

- **阶段 3: 功能扩展与 MVP 闭环**:
  - 实现用户认证流程
  - 实现房源收藏功能
  - 实现基础的筛选功能
