# 悉尼租房助手 - 微信小程序

基于uni-app框架开发的微信小程序，专为中国学生在悉尼租房提供服务。

## 🚀 项目特点

- **微信小程序原生体验** - 流畅的微信生态集成
- **AI智能助手** - 复用现有的FastAPI后端AI服务
- **微信支付集成** - $35代看房服务，$50法律咨询，$80合同审核
- **大学通勤优先** - 以大学为中心的房源推荐
- **中文界面** - 完全中文化的用户体验

## 📱 核心功能

### 1. 房源搜索 (`pages/index/index.vue`)
- 按大学筛选房源（UTS、悉尼大学、UNSW等）
- 显示通勤时间和房源基本信息
- 一键预约代看房服务

### 2. AI租房助手 (`pages/chat/chat.vue`)
- 智能房源推荐
- 租房法律咨询
- 合同审核预约
- 实时聊天体验

### 3. 预约服务 (`pages/booking/booking.vue`)
- 代看房服务预约（$35）
- 法律咨询预约（$50）
- 合同审核预约（$80）
- 微信支付集成

### 4. 个人中心 (`pages/profile/profile.vue`)
- 微信登录
- 订单管理
- 收藏房源
- 客服联系

## 🛠️ 技术架构

```
uniapp-miniprogram/
├── App.vue                 # 主应用文件
├── main.js                 # 入口文件
├── manifest.json           # uni-app配置
├── pages.json             # 页面路由配置
├── package.json           # 项目依赖
├── pages/                 # 页面文件
│   ├── index/index.vue    # 首页-房源列表
│   ├── chat/chat.vue      # AI聊天助手
│   ├── booking/booking.vue # 预约服务
│   └── profile/profile.vue # 个人中心
└── static/                # 静态资源
    └── icons/             # 图标文件
```

## 🔧 开发环境

### 安装依赖
```bash
cd uniapp-miniprogram
npm install
```

### 开发模式（微信小程序）
```bash
npm run dev:mp-weixin
```

### 开发模式（H5网页版）
```bash
npm run dev:h5
```

### 生产构建
```bash
# 微信小程序
npm run build:mp-weixin

# H5网页版
npm run build:h5
```

## 🔗 后端API集成

项目设计为与现有FastAPI后端无缝集成：

```javascript
// 全局API配置 (App.vue)
apiBaseUrl: 'http://localhost:8000'  // 开发环境
// apiBaseUrl: 'https://your-api-domain.com'  // 生产环境
```

### API端点
- `GET /api/properties` - 获取房源列表
- `POST /api/chat` - AI聊天服务
- `POST /api/orders/create` - 创建订单
- `GET /api/orders/count` - 获取订单数量
- `GET /api/favorites` - 获取收藏房源

## 📱 微信小程序配置

### AppID配置
在 `manifest.json` 中配置微信小程序AppID：
```json
{
  "mp-weixin": {
    "appid": "wx7762fea6c5092ef9"
  }
}
```

### 权限配置
```json
{
  "permission": {
    "scope.userLocation": {
      "desc": "您的位置信息将用于推荐附近房源"
    }
  }
}
```

## 🎨 UI设计规范

- **主色调**: #007BFF (蓝色)
- **成功色**: #28a745 (绿色)
- **警告色**: #dc3545 (红色)
- **背景色**: #F4F7F9 (浅灰蓝)
- **卡片圆角**: 16rpx
- **按钮圆角**: 12rpx

## 🔄 数据流向

```
微信小程序 → uni.request() → FastAPI后端 → PostgreSQL数据库
             ↑                           ↓
         用户操作                    AI/房源数据
```

## 🚀 部署流程

### 微信小程序发布
1. 使用微信开发者工具打开项目
2. 构建生产版本：`npm run build:mp-weixin`
3. 上传代码到微信后台
4. 提交审核

### H5版本部署
1. 构建：`npm run build:h5`
2. 部署到Netlify/Vercel等平台
3. 配置域名和HTTPS

## 📋 下一步开发计划

### 立即待办
- [ ] 创建房源详情页面 (`pages/property/detail.vue`)
- [ ] 创建支付成功页面 (`pages/booking/success.vue`)
- [ ] 添加微信小程序图标和启动页
- [ ] 配置真实的微信AppID

### 功能增强
- [ ] 房源收藏功能
- [ ] 订单列表页面
- [ ] 图片轮播组件
- [ ] 地图集成（web-view）
- [ ] 推送通知

### 性能优化
- [ ] 图片懒加载
- [ ] 数据缓存策略
- [ ] 错误处理机制
- [ ] 加载状态优化

## ⚠️ 重要技术约束：web-view域名配置

### 微信小程序web-view限制
基于实际测试，微信小程序的web-view组件有严格限制：

1. **企业账号要求** - 个人小程序无法使用web-view
2. **域名配置要求** - 需要在微信公众平台配置：
   - 业务域名配置
   - request合法域名配置
3. **校验文件要求** - 必须在H5域名根目录放置微信校验文件

### 📋 实际可行方案调整

#### 方案A：小程序内简化地图（推荐）
```vue
<!-- 用静态地图 + 文字描述代替复杂地图 -->
<view class="simple-map">
  <image src="/static/map-preview.jpg" class="map-preview" />
  <view class="location-info">
    <text>📍 Central Park, Chippendale</text>
    <text>🚇 到UTS: 8分钟</text>
    <button @tap="copyAddress">复制地址到地图APP</button>
  </view>
</view>
```

#### 方案B：链接跳转策略
```javascript
// 生成地图链接，让用户手动在浏览器打开
openMapInBrowser() {
  const mapUrl = `https://maps.google.com/search/${encodeURIComponent(address)}`
  uni.setClipboardData({
    data: mapUrl,
    success: () => {
      uni.showModal({
        title: '地图链接已复制',
        content: '请在浏览器中粘贴打开查看详细地图',
        showCancel: false
      })
    }
  })
}
```

## 🤝 与现有项目集成

这个uni-app项目完全复用现有的：
- ✅ FastAPI后端API
- ✅ AI聊天系统
- ✅ PostgreSQL数据库
- ✅ 房源数据ETL

只需要在后端添加一个新的API端点 `/api/wechat/auth` 用于微信登录认证即可。

## 📞 技术支持

如有问题，请通过AI助手页面联系技术支持。
