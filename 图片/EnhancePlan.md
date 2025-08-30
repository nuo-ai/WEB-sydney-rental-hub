● 📋 通勤查询功能技术改造方案 V3.0（基于实际设计稿）

  一、设计稿关键要素分析

  基于截图，我识别出以下关键设计要素：

  截图1 - PropertyDetail页面入口

- "See travel times"按钮：位于地图下方，带定位图标
- 描述文字："Find out travel times from this property to your destinations"
- 按钮样式：白色背景，圆角，带阴影
- 底部有红色CTA按钮："Enquire"和"Inspect"

  截图2 - 注册模态框

- 全屏模态设计，白色背景
- 顶部："Create an account"标题，左上角关闭按钮(×)
- 输入框带标签："Email address"、"Password"
- 主按钮："Create account"（红色背景）
- 底部链接："Sign in"切换

  截图3 - 邮箱验证提示

- 清晰的验证步骤说明
- "Check your email"标题
- 验证邮件发送确认

  截图4 - 通勤时间页面

- 顶部导航：返回箭头 + "Location"标题
- 地图占上半部分
- "Travel Time"区域：
  - "From 505/69-81 Foveaux, Surry Hills, NSW 2010"
  - 三个交通方式图标（圆形按钮）
  - "+ Add location"按钮（红框标注）

  截图6 - 地址搜索模态框

- 全屏白色模态框
- 顶部：关闭按钮(×) + "Add location"标题
- 搜索框带搜索图标
- 提示文字："Search for your location's address"
- 实时搜索结果列表

  截图7 - 地址分类页面

- 顶部："Back"按钮 + "Name location"标题 + "Skip"链接
- 显示选中的地址
- 四个单选选项：Work/School/Home/Other
- 底部红色"Add location"按钮

  截图8 - 通勤结果展示

- 地址卡片显示：
  - 标签（如"School"）
  - 完整地址
  - 通勤时间和距离（7 min / 1.9 km）
  - 右侧删除按钮(×)

  二、优化后的技术实现方案

1. 组件文件结构

  vue-frontend/src/
  ├── views/
  │   ├── PropertyDetail.vue      [修改] - 添加"See travel times"按钮
  │   └── CommuteTimes.vue        [新建] - 通勤时间主页面
  ├── components/
  │   ├── modals/
  │   │   ├── AuthModal.vue       [新建] - 注册/登录模态框
  │   │   ├── EmailVerifyModal.vue [新建] - 邮箱验证提示
  │   │   ├── AddLocationModal.vue [新建] - 地址搜索模态框
  │   │   └── NameLocationModal.vue [新建] - 地址分类模态框
  │   ├── commute/
  │   │   ├── TravelTimeSection.vue [新建] - Travel Time主区域
  │   │   ├── TransportModes.vue   [新建] - 交通方式选择器
  │   │   ├── LocationCard.vue     [新建] - 地址结果卡片
  │   │   └── AddLocationButton.vue [新建] - 添加地址按钮
  │   └── GoogleMap.vue            [现有] - 地图组件
  └── stores/
      ├── auth.js                  [修改] - 添加注册/验证逻辑
      └── commute.js               [新建] - 通勤状态管理

2. 核心组件实现规格

  2.1 PropertyDetail.vue 修改

<!-- 在地图组件后添加 -->

<div class="travel-times-section">
    <button class="see-travel-times-btn" @click="handleSeeTravelTimes">
      <i class="fas fa-map-marker-alt"></i>
      <div class="btn-content">
        <span class="btn-title">See travel times</span>
        <span class="btn-subtitle">Find out travel times from this property to your destinations</span>
      </div>
    </button>
  </div>

<style>
  .see-travel-times-btn {
    width: 100%;
    padding: 16px;
    background: white;
    border: 1px solid #e3e3e3;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 16px 0;
  }

  .btn-content {
    text-align: left;
  }

  .btn-title {
    font-size: 16px;
    font-weight: 600;
    color: #333;
    display: block;
  }

  .btn-subtitle {
    font-size: 14px;
    color: #666;
    margin-top: 4px;
  }
  </style>

  2.2 AuthModal.vue 设计

<template>
    <el-dialog
      v-model="visible"
      fullscreen
      :show-close="false"
      class="auth-modal"
    >
      <template #header>
        <div class="modal-header">
          <button class="close-btn" @click="$emit('close')">
            <i class="fas fa-times"></i>
          </button>
          <h2>{{ isLogin ? 'Sign in' : 'Create an account' }}</h2>
        </div>
      </template>
