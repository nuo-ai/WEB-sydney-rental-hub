# 项目计划与进展 (progress.md)

**最后更新**: 2025年7月11日

## 核心目标: 构建智能、自动化的数据管道

我们当前的核心任务是构建一个健壮、智能、自动化的数据更新系统，为Taro小程序和未来的市场运营提供强大的数据支持。

---

### **自动化更新策略**

*   **执行方式**: 使用 GitHub Actions 在云端执行自动化脚本。
*   **触发机制**: 调用 `python scripts/automated_data_update.py --run-once` 命令。
*   **更新频率**: 每日三次，以最高效地捕捉新房源信息。
*   **最终确定的更新时间 (悉尼时间 AEST)**:
    *   **11:00** (捕捉上午的房源更新)
    *   **15:00** (捕捉下午的房源更新)
    *   **18:00** (捕捉临近下班及傍晚的最后更新)

---

### **TODO 列表**

**Phase 1: 智能数据管道基础建设**

*   [x] **任务 1.1: 升级数据库 Schema** (完成于 2025年7月11日)
    *   **动作**: ✅ 为 `properties` 表增加 `status` (TEXT) 和 `status_changed_at` (TIMESTAMP WITH TIME ZONE) 两个新字段。
    *   **测试**: ✅ 确认新字段已成功添加到 Supabase 数据库表中。
    *   **交付**:
        *   ✅ 更新后的 `database/setup_database.sql` 文件。
        *   ✅ `git commit -m "feat(db): add status and status_changed_at to properties"`
        *   ✅ 更新 `memory-bank`。

*   [x] **任务 1.2: 升级 ETL 脚本** (完成于 2025年7月11日)
    *   **动作**: ✅ 修改 `database/process_csv.py`，实现对 `status` 字段的智能判断和更新逻辑。
    *   **测试**: ✅ 本地运行脚本，并验证数据库中的 `status` 和 `status_changed_at` 字段已按预期更新。
    *   **交付**:
        *   ✅ 更新后的 `database/process_csv.py` 文件。
        *   [ ] `git commit -m "feat(etl): implement intelligent status tracking"`
        *   [ ] 更新 `memory-bank`。

**Phase 2: 自动化与监控**

*   [ ] **任务 2.1: 完善一键执行脚本**
    *   **动作**: 为 `scripts/automated_data_update.py` 正式添加并测试 `--run-once` 参数。
    *   **测试**: 运行 `python scripts/automated_data_update.py --run-once`，确认脚本在完成一次更新后能自动退出。
    *   **交付**:
        *   更新后的 `scripts/automated_data_update.py` 文件。
        *   `git commit -m "feat(scripts): add --run-once flag for manual trigger"`
        *   更新 `memory-bank`。

*   [ ] **任务 2.2: 配置 GitHub Actions 自动化**
    *   **动作**: 编写并测试 `.github/workflows/update-data.yml`，使其能按照 `11:00, 15:00, 18:00` 的策略每日定时调用更新脚本。
    *   **测试**: 手动触发一次 GitHub Actions workflow，检查其是否在云端成功运行并更新了数据库。
    *   **交付**:
        *   最终的 `.github/workflows/update-data.yml` 文件。
        *   `git commit -m "ci(automation): configure daily data update workflow"`
        *   更新 `memory-bank`。

**Phase 3: 数据应用**

*   [ ] **任务 3.1: 创建“最新房源”API**
    *   **动作**: 在 `backend/main.py` 中增加一个新的 GraphQL 查询或 RESTful API 接口，用于获取指定时间范围内 `status` 为 'new' 或 'updated' 的房源。
    *   **测试**: 本地启动后端服务，并使用工具成功调用新接口，验证返回数据是否正确。
    *   **交付**:
        *   更新后的 `backend/main.py` 文件。
        *   `git commit -m "feat(api): add endpoint for latest listings"`
        *   更新 `memory-bank`。
