# Sydney Rental Hub - 悉尼租房平台

## 项目愿景
为悉尼租客打造最高效的找房平台，通过智能筛选和通勤分析帮用户找到理想住所。

## 当前 Sprint（2025-01-30 ~ 02-05）
1. ✅ 文档瘦身计划（进行中）
2. ⏳ 完成个人中心页面
3. ⏳ 实现排序功能
4. ⏳ 清理导航系统

## 核心命令
```bash
# 前端开发
cd vue-frontend && npm run dev    # http://localhost:5173

# 后端API
python scripts/run_backend.py     # http://localhost:8000

# 数据库
# Supabase云数据库，无需本地启动
```

## 关键文件
```
/vue-frontend/src/
├── views/HomeView.vue         # 房源列表页（虚拟滚动）
├── views/PropertyDetail.vue   # 房源详情页
├── views/Profile.vue          # 个人中心（待完成）
├── components/PropertyCard.vue # 核心卡片组件
└── stores/properties.js       # 状态管理

/backend/
├── main.py                    # FastAPI入口
└── crud/properties_crud.py    # 数据库操作
```

## 技术栈
- **前端**: Vue 3 + Element Plus + Pinia
- **后端**: FastAPI + PostgreSQL (Supabase)
- **部署**: 本地开发环境

## 开发规范
1. **代码注释用中文**，解释"为什么"而非"什么"
2. 每次改动保持简单，避免大规模重构
3. 开始任务前先制定计划并获得批准
4. 完成后提供 commit message

## 性能指标
- 房源总数: 3,456 条
- 列表渲染: < 0.5秒（虚拟滚动）
- API响应: < 500ms
- 内存占用: < 50MB

## 相关文档
- `VISION.md` - 项目目标和成功标准
- `CURRENT_TASK.md` - 当前任务和阻塞
- `TODO.md` - 完整任务列表

---
*保持简洁，专注当下，每日 /clear*