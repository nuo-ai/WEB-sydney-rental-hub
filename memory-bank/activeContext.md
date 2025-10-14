# 当前工作快照（apps/web-shadcn · PropertyDetail 重建）

更新时间：2025-10-15 04:08 AEST

一、已完成（核心里程碑）
- 新建并初始化纯净前端应用 apps/web-shadcn（Vite + Vue3 + TS + Tailwind v4 + shadcn-vue init，基色 Zinc）
- 配置要点：
  - @tailwindcss/vite 插件启用；tsconfig 路径别名 @/*；src/style.css 使用 @import "tailwindcss"
- 通过 CLI 添加基础 UI 组件（路径：src/components/ui/*）：
  - Button / Card（含 Header/Content/Footer/Title/Description/Action）
  - Avatar（含 Image/Fallback）/ Badge / Separator / Input / Textarea
  - Alert / Skeleton / Dialog / Carousel / Sonner（Toast）
- 安装通用依赖：
  - lucide-vue-next（统一图标库）
  - markdown-it（Markdown 渲染）
- 页面落地：
  - 新建并挂载 PropertyDetail.vue（apps/web-shadcn/src/views/PropertyDetail.vue）
  - 替换 Hero 区为 Carousel 轮播（多图可轮播，空图占位保留）

二、与 legacy 详情页（apps/web/src/views/PropertyDetail.vue）功能对照差异
- Loading/小提示（ElMessage/小条提示）→ Sonner（Toast）/ Spinner（轻量加载）
- 错误态（el-alert）→ Alert
- 骨架屏（el-skeleton）→ Skeleton
- 图片预览（el-image 预览层）→ Dialog（结合 Carousel 大图预览）
- 描述 Markdown → markdown-it 渲染 + 样式
- 地图与“See travel times” → 第三方地图（@fawmi/vue-google-maps/Mapbox）+ Button + Icon
- Add-to-calendar → 第三方/自研逻辑（非 shadcn）

三、下一步（P0 优先事项，按小补丁推进）
1) 接入 Sonner 容器，替换「Enquire/Inspect」等动作用 toast（替代 ElMessage）
2) 预留加载/错误分支，接入 Skeleton 与 Alert（为未来数据/路由接入做占位）
3) 为 Carousel 的每张图片挂载 Dialog 打开逻辑，支持大图预览
4) Spinner：若 CLI 继续不稳定，先用 Button 的 loading 状态替代，后续补齐组件

四、重要文件/目录
- apps/web-shadcn/vite.config.ts（plugins: vue(), tailwindcss()；alias @）
- apps/web-shadcn/src/views/PropertyDetail.vue（新页面主体，已落地 Carousel）
- apps/web-shadcn/src/components/ui/*（shadcn 组件存放目录）
- apps/web-shadcn/src/App.vue（直接挂载 PropertyDetail 便于预览）

五、工作方式与约束（保留）
- 小步快跑，replace_in_file 细粒度补丁；避免一次性重构
- 与 legacy 完全解耦，新应用内逐项实现（Tailwind v4 + shadcn）
- P0 完成后再接路由与真实数据，再处理地图/Add-to-calendar
