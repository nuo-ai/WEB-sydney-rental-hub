# 技术上下文 (Technical Context)

**文档状态**: 生存文档 (Living Document)
**最后更新**: 2025-09-15

---

## 当前技术栈

- **前端**: Vue 3 (Composition API) + Vite + Element Plus + Pinia + lucide-vue-next（图标）
- **后端**: Python FastAPI + Strawberry GraphQL + Supabase (AWS悉尼区域)
- **数据库**: PostgreSQL (Supabase) + Redis缓存（默认 15 分钟 TTL）
- **地图**: Google Maps JavaScript/Static Map（前端）+ Google Directions（后端，生产）；当前无 Haversine 回退

---

## 项目架构概览

### 项目结构
```
apps/web/
├── src/views/          # 页面组件
├── src/components/     # 可复用组件
├── src/stores/         # Pinia状态管理
├── src/services/       # API服务层
├── src/router/         # Vue Router配置
└── vite.config.js      # Vite配置 (CORS代理到localhost:8000)
```

### API集成架构
- **代理配置**: 默认将 `/api`转发到 `http://localhost:8000`
- **响应格式**: 统一 `{status, data, pagination, error}`结构
- **失败策略**: 快速失败并抛错，便于监控定位

---

## 筛选系统技术约定

### URL 幂等与状态同步
- **实现文件**: `apps/web/src/utils/query.js`（sanitizeQueryParams、isSameQuery）
- **落地点**: FilterPanel 统一面板、五个分面、HomeView.sort
- **前端表现**: 应用后 URL 可直链/刷新恢复，不写空键，地址栏不抖动

### 预估计数统一
- **composable**: useFilterPreviewCount 统一"应用（N）"口径
- **特性**: 并发序号守卫、300ms 防抖、组件卸载清理
- **降级**: 计数失败返回 null，按钮退回"应用/确定"

### 分组边界隔离
- **API**: `applyFilters(filters, { sections })`
- **分组**: area/price/bedrooms/availability/more
- **原则**: 仅删除指定分组旧键再合并，避免跨面板覆盖

---

## 开发环境

### 本地运行
```bash
# Web 前端开发环境
pnpm install --filter @web-sydney/web
pnpm --filter @web-sydney/web dev   # localhost:5173

# 后端API服务
cd ../
python scripts/run_backend.py  # localhost:8000
```

### E2E 测试
```bash
# 安装依赖（如首次）
npx playwright install

# 运行 URL 幂等冒烟测试
npx playwright test -g "URL 幂等与仅写非空键"
```

### 当前运行状态
- ✅ Vue前端: 正常运行 (localhost:5173)
- ✅ Python后端: 正常运行 (localhost:8000)
- ✅ 数据库连接: 正常 (Supabase PostgreSQL)
- ✅ 认证系统: JWT + 邮箱验证框架
- ✅ 通勤计算: Google Directions（生产）；无 Haversine 回退

---

## 设计系统

### JUWO品牌设计系统
- **主色**: #0057ff (纯正蓝)
- **统一圆角**: 6px（组件设计令牌）
- **布局对齐**: 1200px最大宽度，32px间距
- **响应式断点**: 768px（平板）、1200px（桌面）、1920px（超宽）

### 设计令牌约束
- **强制使用**: `var(--*)` 形式的 CSS 自定义属性
- **禁止**: 硬编码颜色、`var(--token, #hex)` 兜底形式
- **护栏**: Stylelint 规则拦截新增硬编码色

### 图标系统
- **标准**: 全站使用 `lucide-vue-next` SVG 图标库
- **导入**: `import { IconName } from 'lucide-vue-next'`
- **颜色**: `stroke: currentColor`，由外层控制

---

## 性能优化成果

1. **虚拟滚动优化**: DOM节点减少99.8%，列表加载提升83%
2. **API响应加速**: 服务端响应从8-10秒降至0.4-0.5秒，提升20倍
3. **数据库索引**: 筛选查询从2.2秒降至0.59秒，提升3.7倍
4. **缓存策略**: 15分钟客户端缓存 + Redis降级到内存缓存

---

## 部署配置

### Netlify 部署
- **配置文件**: netlify.toml
- **构建设置**: base="apps/web", command="pnpm --filter @web-sydney/web build", publish="dist"
- **SPA 重写**: `/*` → `/index.html` (status=200)

### 本地运维（PowerShell）
```powershell
# 进入项目根目录
Set-Location 'C:\Users\nuoai\Desktop\WEB-sydney-rental-hub'

# 跑 ETL
& 'C:\Python313\python.exe' 'scripts\automated_data_update_with_notifications.py' --run-once

# 清缓存
Invoke-WebRequest -UseBasicParsing -Method POST -Uri 'http://localhost:8000/api/cache/invalidate?invalidate_all=true' | Out-Null
