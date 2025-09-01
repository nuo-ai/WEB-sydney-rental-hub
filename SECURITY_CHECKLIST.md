# 🔒 Google Maps API 密钥安全修复清单

## ⚠️ 紧急情况说明
您的 Google Maps API 密钥已在 GitHub 上公开泄露。Google 已发送安全警告。

## ✅ 已完成的修复步骤

1. **[✓] 移除硬编码密钥**
   - 更新 `PropertyDetail.vue` 使用环境变量
   - 更新 `GoogleMap.vue` 移除硬编码密钥
   - 删除包含密钥的备份文件

2. **[✓] 配置环境变量**
   - 更新 `.env` 文件（密钥已替换为占位符）
   - 更新 `.env.example` 添加安全警告
   - 更新 `.gitignore` 排除敏感文件

3. **[✓] 创建清理脚本**
   - `clean_api_keys.sh` - 用于清理 Git 历史

## 🚨 立即需要执行的步骤

### 1. 重新生成 API 密钥（最紧急！）

1. 访问 [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. 找到项目 "principal-media-427420-a9"
3. 删除或限制泄露的密钥：`AIzaSyDR-IqWUXtp64-Pfp09FwGvFHnbKjMNuqU`
4. 创建新的 API 密钥

### 2. 配置新密钥的安全限制

在 Google Cloud Console 中为新密钥设置：

**应用程序限制：**
- 选择 "HTTP referrers (网站)"
- 添加允许的网址：
  ```
  http://localhost:5173/*
  http://localhost:5174/*
  https://your-domain.com/*
  ```

**API 限制：**
- 选择 "限制密钥"
- 仅勾选：
  - Maps JavaScript API
  - Maps Static API
  - Places API（如需要）

**配额限制：**
- 设置每日请求上限（如 1000 次）
- 启用配额警报

### 3. 更新本地配置

编辑 `vue-frontend/.env`：
```env
VITE_GOOGLE_MAPS_API_KEY=你的新密钥
```

### 4. 清理 Git 历史（可选但推荐）

**⚠️ 警告：这会重写历史，需要所有协作者重新克隆仓库**

```bash
# 备份仓库
cp -r . ../WEB-sydney-rental-hub-backup

# 运行清理脚本
bash clean_api_keys.sh

# 强制推送
git push origin --force --all
git push origin --force --tags
```

## 📋 安全最佳实践

### 环境变量管理
- ✅ 使用 `.env` 文件存储敏感信息
- ✅ `.env` 文件加入 `.gitignore`
- ✅ 提供 `.env.example` 示例文件
- ✅ 生产环境使用环境变量而非文件

### API 密钥安全
- ✅ 为不同环境使用不同密钥
- ✅ 设置 HTTP referrer 限制
- ✅ 限制 API 使用范围
- ✅ 设置配额和监控
- ✅ 定期轮换密钥

### 代码审查
- ✅ 提交前检查敏感信息
- ✅ 使用 git-secrets 等工具自动检测
- ✅ Code Review 时特别注意配置文件

## 🔍 验证修复

运行以下命令确认密钥已移除：

```bash
# 在当前代码中搜索
grep -r "AIzaSyDR-IqWUXtp64" .

# 在 Git 历史中搜索
git log -p -S "AIzaSyDR-IqWUXtp64"
```

## 📞 需要帮助？

- [Google Cloud 支持](https://cloud.google.com/support)
- [Google Maps API 文档](https://developers.google.com/maps/documentation)
- [GitHub 安全指南](https://docs.github.com/en/code-security)

---

**最后更新：** 2025-01-31
**状态：** ⚠️ 等待新密钥配置