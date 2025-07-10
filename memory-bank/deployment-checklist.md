# 部署清单 (Deployment Checklist)

**第一阶段：基础设施准备 (IaaS - Infrastructure as a Service)**

*   [ ] **任务1.1: 创建云数据库 (Supabase)**
    *   说明: 我们将在 Supabase 上创建一个新的 PostgreSQL 数据库实例，并获取连接所需的所有信息（主机、端口、用户名、密码）。
*   [ ] **任务1.2: 创建后端服务 (Render)**
    *   说明: 我们将在 Render 上创建一个新的 Web Service，并将其连接到我们的 GitHub 仓库。
*   [ ] **任务1.3: 创建前端站点 (Netlify)**
    *   说明: 我们将在 Netlify 上创建一个新的站点，同样连接到 GitHub 仓库。

**第二阶段：配置与连接 (Configuration & Connection)**

*   [ ] **任务2.1: 配置后端环境变量**
    *   说明: 将 Supabase 数据库的连接信息作为环境变量添加到 Render 的后端服务中。
*   [ ] **任务2.2: 部署后端**
    *   说明: 触发 Render 的首次部署，确保后端服务可以成功启动并连接到云数据库。
*   [ ] **任务2.3: 配置前端 API 地址**
    *   说明: 修改前端代码，将其 API 请求地址指向我们刚刚部署的 Render 后端服务的 URL。
*   [ ] **任务2.4: 部署前端**
    *   说明: 触发 Netlify 的部署，发布连接到生产环境后端的新版前端。

**第三阶段：数据与自动化 (Data & Automation)**

*   [ ] **任务3.1: 迁移本地数据到云端**
    *   说明: 我们将使用 `pg_dump` 和 `psql` 工具，将您本地 PostgreSQL 数据库中的所有房源数据迁移到 Supabase 云数据库中。
*   [ ] **任务3.2: 配置自动化数据更新 (GitHub Actions)**
    *   说明: 启用并配置 `.github/workflows/update-data.yml` 工作流，使其能够安全地连接到云数据库，并设置为每天定时运行。

**第四阶段：最终验证 (Final Verification)**

*   [ ] **任务4.1: 全面线上测试**
    *   说明: 访问 Netlify 提供的生产网址，全面测试网站的所有核心功能，包括搜索、筛选和大学通勤时间查询，确保一切正常。
