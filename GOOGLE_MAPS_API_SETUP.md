# 🗺️ Google Maps API 开通指南

## 📋 需要开通的 API

根据代码分析，你的项目需要以下 4 个 Google Maps API：

| API 名称 | 用途 | 使用位置 |
|---------|------|---------|
| **Maps JavaScript API** | 交互式地图显示 | GoogleMap.vue 组件 |
| **Maps Static API** | 静态地图图片（备用） | PropertyDetail.vue |
| **Places API** | 地点搜索和自动完成 | CommuteCalculator.vue, places.js |
| **Directions API** | 通勤路线计算 | backend/main.py, mcp-server |

## 🚀 开通步骤

### 步骤 1：访问 Google Cloud Console

1. 打开 [Google Cloud Console](https://console.cloud.google.com/)
2. 登录你的 Google 账号
3. 如果是第一次使用，需要同意服务条款

### 步骤 2：创建或选择项目

1. 点击顶部的项目选择器
2. 选择现有项目 `principal-media-427420-a9` 
   或点击"新建项目"创建新项目（推荐创建新项目以便重新开始）

### 步骤 3：启用 APIs

1. 在左侧菜单选择 **"API 和服务" > "库"**
2. 逐个搜索并启用以下 API：

#### 3.1 启用 Maps JavaScript API
- 搜索 "Maps JavaScript API"
- 点击进入
- 点击 **"启用"** 按钮

#### 3.2 启用 Maps Static API  
- 搜索 "Maps Static API"
- 点击进入
- 点击 **"启用"** 按钮

#### 3.3 启用 Places API
- 搜索 "Places API"
- 点击进入
- 点击 **"启用"** 按钮

#### 3.4 启用 Directions API
- 搜索 "Directions API"
- 点击进入
- 点击 **"启用"** 按钮

### 步骤 4：创建 API 密钥

1. 在左侧菜单选择 **"API 和服务" > "凭据"**
2. 点击顶部的 **"+ 创建凭据"**
3. 选择 **"API 密钥"**
4. 密钥创建成功后，立即复制保存

### 步骤 5：设置 API 密钥限制（重要！）

点击刚创建的 API 密钥进行配置：

#### 5.1 应用程序限制

选择 **"HTTP 引荐来源网址（网站）"**

添加以下网址（根据实际情况调整）：
```
http://localhost:5173/*
http://localhost:5174/*
http://localhost:8000/*
http://127.0.0.1:5173/*
https://your-domain.com/*
https://www.your-domain.com/*
```

#### 5.2 API 限制

选择 **"限制密钥"**

勾选以下 API：
- ✅ Maps JavaScript API
- ✅ Maps Static API
- ✅ Places API
- ✅ Directions API

点击 **"保存"**

### 步骤 6：配置计费（必需）

⚠️ **注意**：Google Maps API 需要启用计费账户才能使用

1. 在左侧菜单选择 **"结算"**
2. 点击 **"链接结算账户"**
3. 创建新的结算账户或选择现有账户
4. 添加信用卡信息

**免费额度**：
- 每月 $200 美元的免费额度
- 足够个人项目和开发使用
- 约等于：
  - 28,000 次地图加载
  - 40,000 次路线请求
  - 100,000 次静态地图请求

### 步骤 7：设置配额和预算警报（推荐）

保护自己免受意外高额账单：

1. **设置配额限制**：
   - 进入 "API 和服务" > "配额"
   - 为每个 API 设置每日请求限制
   - 建议：每日 1,000-5,000 次请求

2. **设置预算警报**：
   - 进入 "结算" > "预算和提醒"
   - 创建预算（如 $50/月）
   - 设置 50%、90%、100% 的提醒

### 步骤 8：在项目中配置密钥

1. 编辑 `vue-frontend/.env` 文件：
```env
VITE_GOOGLE_MAPS_API_KEY=你复制的API密钥
```

2. 重启开发服务器：
```bash
cd vue-frontend
npm run dev
```

## ✅ 验证配置

### 测试前端地图功能
1. 访问 http://localhost:5173
2. 打开任意房源详情页
3. 检查地图是否正常显示
4. 测试 "See travel times" 功能

### 检查 API 使用情况
1. 访问 [API 控制台](https://console.cloud.google.com/apis/dashboard)
2. 查看 API 使用量图表
3. 确认没有错误

## 🔍 常见问题

### Q: 提示 "此 API 密钥未获授权使用此服务"
**A:** 检查是否启用了所有必需的 API，并且密钥限制中包含了这些 API

### Q: 提示 "RefererNotAllowedMapError"
**A:** 在密钥的 HTTP 引荐来源网址中添加你的域名

### Q: 地图显示 "仅供开发使用"水印
**A:** 需要启用计费账户

### Q: 如何查看 API 调用日志？
**A:** 访问 "日志记录" > "日志浏览器"，筛选 Maps API 相关日志

## 💰 费用估算

基于典型使用场景（每日 100 个用户）：

| 功能 | 每日调用 | 月度费用 |
|-----|---------|---------|
| 地图显示 | 500 次 | $3.50 |
| 路线计算 | 200 次 | $1.00 |
| 地点搜索 | 300 次 | $2.55 |
| **总计** | - | **$7.05** |

💡 完全在 $200 免费额度内！

## 📚 相关文档

- [Google Maps Platform 文档](https://developers.google.com/maps/documentation)
- [API 定价](https://developers.google.com/maps/billing-and-pricing/pricing)
- [最佳实践](https://developers.google.com/maps/optimization-guide)
- [错误代码参考](https://developers.google.com/maps/documentation/javascript/error-messages)

---

**最后更新：** 2025-01-31
**文档版本：** 1.0