# 技术上下文 (Technical Context)

**文档状态**: 生存文档 (Living Document)
**最后更新**: 2025-09-03

---

## 1. 当前技术栈

- **前端**: Vue 3 (Composition API) + Vite + Element Plus + Pinia
- **后端**: Python FastAPI + Strawberry GraphQL + Supabase (AWS悉尼区域)
- **数据库**: PostgreSQL (Supabase) + Redis缓存 (15分钟TTL)
- **地图**: OpenStreetMap (免费) + 本地通勤计算 (Haversine算法)

---

## 2. 项目架构概览

### 项目结构
```
vue-frontend/
├── src/views/          # 页面组件 (Home.vue, PropertyDetail.vue等)
├── src/components/     # 可复用组件 (PropertyCard.vue, Sidebar.vue等)
├── src/stores/         # Pinia状态管理 (properties.js, auth.js)
├── src/services/       # API服务层 (api.js)
├── src/router/         # Vue Router配置
└── vite.config.js      # Vite配置 (CORS代理到localhost:8000)
```

### JUWO品牌设计系统
- **主色**: #FF5824 (橙色)
- **统一圆角**: 6px（组件设计令牌）
- **标准房源卡片**: 580px宽度
- **布局对齐**: 1200px最大宽度，32px间距

### API集成架构
- **代理配置**: 默认将`/api`转发到 `http://localhost:8000`；在 WSL/容器环境可通过环境变量 `VITE_API_TARGET` 切换为 `http://172.31.16.1:8000`
- **拦截器**: 自动携带JWT认证头（按需启用；已具备框架基础）
- **响应格式**: 统一`{status, data, pagination, error}`结构

---

## 3. 性能优化成果 🎯

**多项性能突破**:

1. **虚拟滚动优化**: DOM节点减少99.8% (17万+ → ~400)，列表加载提升83%
2. **API响应加速**: 服务端响应从8-10秒降至0.4-0.5秒，提升20倍
3. **数据库索引**: 筛选查询从2.2秒降至0.59秒，提升3.7倍
4. **缓存策略**: 15分钟客户端缓存 + Redis降级到内存缓存
5. **数据传输**: API字段优化减少70%响应体积

---

## 4. 开发环境

```bash
# Vue前端开发环境
cd vue-frontend
npm run dev              # localhost:5173

# 后端API服务
cd ../
python scripts/run_backend.py  # localhost:8000
```

**当前运行状态**:
- ✅ Vue前端: 正常运行 (虚拟DOM + 响应式系统)
- ✅ Python后端: 正常运行 (FastAPI + GraphQL)
- ✅ 数据库连接: 正常 (3456条示例数据；会随导入更新)
- ✅ CORS代理: 配置完成
- ✅ 地图服务: OpenStreetMap备选
- ✅ 认证系统: JWT + 邮箱验证框架
- ✅ 通勤计算: 本地算法 (无需外部API)

---

## 已解决的技术债务 ✅

**核心问题修复**:
- 用户认证体系完整 (注册/登录/邮箱验证)
- Google Places API完全替代方案 (本地存储/pre设数据)
- Redis依赖降级 (内存缓存备选)
- API响应格式统一 (description字段问题)
- 服务端分页完整迁移
- 代码注释规范建立
- PC 详情页风格一致性：统一背景/容器/内边距；替换硬编码为全局 tokens；在 src/style.css 补齐缺失变量映射

## 样式系统更新（2025-09-03）

- 在 `src/style.css` 的 `:root` 补充变量映射：`--space-1-5`, `--space-3`, `--space-3-5`, `--space-4`, `--space-6`, `--text-xs`, `--text-sm`, `--text-base`, `--text-lg`, `--font-semibold`, `--bg-base`, `--bg-hover`, `--bg-secondary`, `--radius-full`, `--shadow-xs`, `--brand-primary`, `--text-primary`, `--text-tertiary`, `--link-color`，与 JUWO 全局设计系统对齐。
- 在 `PropertyDetail.vue` 统一使用全局 tokens：如 `var(--color-bg-page)`, `var(--color-text-*)`, `var(--color-border-default)`；移除未定义变量（如 `--transition-all`）以避免回退。
- 统一 ≥1200px 与 1920px 断点的容器规范（`max-width: 1200px`, `padding: 0 32px`），与首页 Home 栅格一致，消除“另一套主题”观感。
