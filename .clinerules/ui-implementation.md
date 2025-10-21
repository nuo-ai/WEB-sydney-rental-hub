## Brief overview
This rule file defines the UI component implementation plan for the Sydney Rental Hub project using shadcn-vue components. It maps the application structure to appropriate shadcn components.

## Navigation Components

### Bottom Navigation Bar (2.2)
- navigation-menu - 用于底部导航栏，包含首页、消息、收藏、我的四个主要导航项

### Top Header Bar (2.1)
- card - 用于首页顶部栏，包含位置信息和用户状态
- button - 用于返回按钮和用户状态图标按钮
- sheet - 用于汉堡菜单展开面板

## Page Structure Components

### Home Page (3.1)
- input - 用于顶部栏的位置搜索输入框
- button - 用于过滤栏的位置、排序、筛选按钮
- card - 用于房源卡片容器
- badge - 用于房源卡片上的"新上线"标签
- button - 用于房源卡片的收藏和更多操作按钮
- skeleton - 用于房源卡片加载状态

### Message Page (3.2)
- card - 用于消息页面的空状态显示
- avatar - 用于消息项的头像显示
- badge - 用于未读消息红点
- card - 用于聊天详情页面的消息气泡容器

### Favorites & History Page (3.3)
- tabs - 用于"我的收藏"和"我的足迹"标签页切换
- card - 用于标签页内容容器
- badge - 用于房源标签网格显示
- button - 用于浮动操作按钮组(PK对比、地图)

### Property Detail Page (3.4)
- carousel - 用于房源图片轮播展示
- card - 用于价格、地址、房型元数据等信息展示
- badge - 用于房源特征标签显示
- button - 用于底部主操作栏的电话咨询和立即预约按钮
- collapsible - 用于房源描述的收起/展开功能

### My Page (3.5)
- card - 用于用户信息、统计信息展示
- avatar - 用于用户头像显示
- button - 用于功能卡片和设置按钮
- sheet - 用于设置页面的选项列表

## Popup/Overlay Components

### Listing Options Menu (4.1)
- dropdown-menu - 用于房源操作菜单(分享、隐藏)

### Location Selection Panel (4.2)
- drawer - 用于位置选择面板，从底部上滑显示
- input - 用于搜索框
- button - 用于热门区域标签和确定按钮

### Sorting Options Panel (4.3)
- drawer - 用于排序方式面板
- button - 用于排序选项列表项

### Filter Conditions Panel (4.4)
- drawer - 用于筛选条件面板
- checkbox - 用于多选筛选条件
- select - 用于单选筛选条件
- slider - 用于租金范围筛选
- calendar - 用于入住日期选择

## Form Components

### User Authentication (1.6)
- input - 用于手机号输入
- button - 用于微信一键注册/登录按钮
- dialog - 用于确认登出对话框

### Personal Info Edit (1.7)
- input - 用于用户名、手机号等信息编辑
- select - 用于性别选择
- button - 用于保存按钮
- dialog - 用于注销账号确认

### Appointment Booking (1.4)
- calendar - 用于选择预约日期
- select - 用于选择预约时间
- button - 用于提交预约
- dialog - 用于预约成功确认

## Data Display Components

### Property Cards (3.1, 3.3)
- card - 用于房源卡片整体结构
- table - 用于房型元数据显示(2 🛏️ 2 🛁 1 🚗)
- badge - 用于房源标签显示

### Comparison Features (1.5)
- dialog - 用于房源对比页面显示
- card - 用于对比项容器
- table - 用于对比数据展示

## Layout Components

### Global Layout
- sidebar - 用于整体应用布局管理
- separator - 用于页面元素分割线
- scroll-area - 用于长内容滚动区域

## Utility Components

### Loading & States
- skeleton - 用于加载状态显示
- spinner - 用于加载指示器
- empty - 用于空状态显示

### Notifications
- sonner - 用于消息提示和通知
- tooltip - 用于按钮提示信息
- alert - 用于重要信息提示

## Implementation Priority

1. navigation-menu - 底部导航基础
2. card - 核心内容容器
3. button - 交互按钮
4. tabs - 标签页切换
5. drawer - 弹出面板
6. input/select - 表单输入
7. calendar - 日期选择
8. other components as needed
