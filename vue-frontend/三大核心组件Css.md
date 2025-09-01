/* ========================================
   房源详情页 - 三大核心组件 CSS 规范
   基于 Renta UI Kit 设计系统
   ======================================== */

/* ========== 1. PropertyDetailHeader 顶部栏组件 ========== */

.property-detail-header {
  /* 布局 */
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  width: 100%;
  height: 53px;

  /* 背景和边框 */
  background: var(--background-primary);
  border-bottom: var(--border-width-thin) solid var(--border-color-primary);

  /* 内部布局 */
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-4);
}

.property-detail-header__left {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.property-detail-header__logo {
  width: 18px;
  height: 14px;
}

.property-detail-header__brand {
  /* 字体规范 */
  font-family: var(--font-family-primary);
  font-size: 22px;           /* 提取值: text-[22px] */
  font-weight: var(--font-weight-regular);
  color: #44bb3a;            /* 提取值: text-[#44bb3a] - Domain 绿色 */
  line-height: 1;
}

.property-detail-header__right {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.property-detail-header__divider {
  width: 1px;               /* 提取值: w-px */
  height: 30px;             /* 提取值: h-[30px] */
  background: var(--border-color-primary);
}

.property-detail-header__login {
  /* 字体规范 */
  font-family: var(--font-family-primary);
  font-size: 14.6px;        /* 提取值: text-[14.6px] */
  font-weight: var(--font-weight-bold);
  color: #57bb4e;           /* 提取值: text-[#57bb4e] - 登录绿色 */
  background: none;
  border: none;
  cursor: pointer;
  transition: var(--transition-colors);
}

.property-detail-header__login:hover {
  color: var(--success-color);
}

/* ========== 2. PropertyImageGallery 图片轮播组件 ========== */

.property-image-gallery {
  /* 布局尺寸 */
  width: 100%;
  height: 217px;            /* 提取值: h-[217px] */
  position: relative;
  overflow: hidden;

  /* 视觉效果 */
  border-radius: 0;         /* 提取显示无圆角 */
  margin-bottom: var(--space-0);  /* 与下一区块无间距 */
}

.property-image-gallery__main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}

.property-image-gallery__navigation {
  position: absolute;
  bottom: var(--space-4);
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: var(--space-2);
}

.property-image-gallery__dot {
  width: 8px;
  height: 8px;
  border-radius: var(--radius-full);
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: var(--transition-colors);
}

.property-image-gallery__dot--active {
  background: var(--background-primary);
}

.property-image-gallery__controls {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  justify-content: space-between;
  width: 100%;
  padding: 0 var(--space-4);
  pointer-events: none;
}

.property-image-gallery__arrow {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  background: rgba(255, 255, 255, 0.9);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  pointer-events: auto;
  transition: var(--transition-all);
}

.property-image-gallery__arrow:hover {
  background: var(--background-primary);
  transform: scale(1.1);
}

/* ========== 3. PropertySummaryCard 房源摘要信息卡片 ========== */

.property-summary-card {
  /* 布局 */
  width: 100%;
  background: var(--background-primary);

  /* 内边距 */
  padding: var(--space-4);   /* 基础内边距 16px */

  /* 区块间距 */
  margin-bottom: var(--space-6); /* 与下一区块间距 24px */

  /* 无边框和阴影 - 基于设计提取 */
  border: none;
  box-shadow: none;
}

.property-summary-card__price {
  /* 价格显示 */
  font-family: var(--font-family-primary);
  font-size: 17.9px;        /* 提取值: text-[17.9px] */
  font-weight: 800;         /* 提取值: font-extrabold */
  color: #686d81;           /* 提取值: text-[#686d81] */
  line-height: 1;
  margin-bottom: var(--space-4);
}

.property-summary-card__address {
  /* 地址信息区域 */
  margin-bottom: var(--space-4);
}

.property-summary-card__wechat {
  /* WeChat 联系信息 */
  font-family: var(--font-family-primary);
  font-size: 15.2px;        /* 提取值: text-[15.2px] */
  font-weight: var(--font-weight-regular);
  color: #7e8093;           /* 提取值: text-[#7e8093] */
  line-height: 1.51;        /* 提取值: leading-[22.9px] / 15.2px ≈ 1.51 */
  margin-bottom: var(--space-3);
}

.property-summary-card__actions {
  /* 操作按钮区域 */
  display: flex;
  justify-content: flex-end;
  gap: var(--space-4);      /* 按钮间距 */
  margin-bottom: var(--space-4);
}

.property-summary-card__action-btn {
  width: 24px;              /* 提取值: size-6 = 24px */
  height: 24px;
  background: none;
  border: none;
  cursor: pointer;
  transition: var(--transition-transform);
}

.property-summary-card__action-btn:hover {
  transform: scale(1.1);
}

.property-summary-card__features {
  /* 房型信息展示区域 */
  display: flex;
  align-items: center;
  gap: var(--space-6);      /* 特征之间的间距 */
  margin-bottom: var(--space-4);
}

.property-summary-card__feature {
  display: flex;
  align-items: center;
  gap: var(--space-1);      /* 图标和数字的间距 */
}

.property-summary-card__feature-icon {
  width: 22px;              /* 提取值: w-[22px] */
  height: 20px;             /* 提取值: h-5 = 20px */
}

.property-summary-card__feature-text {
  font-family: var(--font-family-primary);
  font-size: 15.5px;        /* 提取值: text-[15.5px] */
  font-weight: var(--font-weight-bold);
  color: #676a7c;           /* 提取值: text-[#676a7c] */
  line-height: 1;
}

.property-summary-card__availability {
  /* 可租时间信息 */
  font-family: var(--font-family-primary);
  font-size: 14.6px;        /* 提取值: text-[14.6px] */
  font-weight: var(--font-weight-bold);
  color: #727689;           /* 提取值: text-[#727689] */
  line-height: 1;
  margin-bottom: var(--space-2);
}

.property-summary-card__bond {
  /* 押金信息 */
  font-family: var(--font-family-primary);
  font-size: 15.3px;        /* 提取值: text-[15.3px] */
  font-weight: var(--font-weight-regular);
  color: #75778a;           /* 提取值: text-[#75778a] */
  line-height: 1;
}

/* ========================================
   组件间距系统
   ======================================== */

/* 页面顶部到图片轮播：无间距 */
.property-image-gallery {
  margin-top: 0;
}

/* 图片轮播到摘要卡片：无间距 */
.property-summary-card {
  margin-top: 0;
}

/* 摘要卡片到下一区块：24px 间距 */
.property-summary-card + .property-features {
  margin-top: var(--space-6); /* 24px */
}

/* 区块内部元素间距 */
.property-summary-card__price {
  margin-bottom: var(--space-4); /* 16px */
}

.property-summary-card__features {
  margin-bottom: var(--space-4); /* 16px */
}

.property-summary-card__availability {
  margin-bottom: var(--space-2); /* 8px */
}

/* ========================================
   响应式断点设计
   ======================================== */

/* 当前设计基于移动端 (368px 宽度) */
/* 基础断点值从设计中提取 */

/* 移动端 (默认) - 基于 368px 设计 */
@media (max-width: 767px) {
  .property-detail-header {
    height: 53px;           /* 保持设计尺寸 */
    padding: 0 var(--space-4);
  }

  .property-image-gallery {
    height: 217px;          /* 保持设计比例 */
  }

  .property-summary-card {
    padding: var(--space-4); /* 16px 内边距 */
  }

  .property-summary-card__features {
    gap: var(--space-4);     /* 减少间距适应小屏 */
  }
}

/* 平板端 (768px+) - 扩展设计 */
@media (min-width: 768px) {
  .property-detail-header {
    height: 64px;            /* 增加高度 */
    padding: 0 var(--space-6);
  }

  .property-image-gallery {
    height: 300px;           /* 增加图片高度 */
    border-radius: var(--radius-large); /* 添加圆角 */
    margin-bottom: var(--space-4);
  }

  .property-summary-card {
    padding: var(--space-6); /* 增加内边距 */
    border-radius: var(--card-radius);
    box-shadow: var(--card-shadow);
    border: var(--border-width-thin) solid var(--border-color-primary);
  }

  .property-summary-card__features {
    gap: var(--space-8);     /* 增加特征间距 */
  }
}

/* 桌面端 (1024px+) - 完整体验 */
@media (min-width: 1024px) {
  .property-detail-header {
    height: 72px;
    padding: 0 var(--space-8);
  }

  .property-image-gallery {
    height: 400px;           /* 大屏幕更大图片 */
    margin-bottom: var(--space-6);
  }

  .property-summary-card {
    padding: var(--space-8); /* 最大内边距 */
  }

  .property-summary-card__price {
    font-size: 24px;         /* 放大价格显示 */
  }
}

/* ========================================
   精确的尺寸和间距提取值
   ======================================== */

/* 从 Figma 设计中提取的精确值 */
.property-detail-measurements {
  /* 容器宽度 */
  --design-width: 368px;    /* 设计稿宽度 */

  /* Header 组件尺寸 */
  --header-height: 53px;     /* 顶部栏高度 */
  --header-padding: 15px;    /* 左右内边距 (基于 right-[54px] 计算) */

  /* Logo 尺寸 */
  --logo-width: 18px;        /* w-[18px] */
  --logo-height: 14px;       /* h-3.5 = 14px */

  /* 分割线 */
  --divider-width: 1px;      /* w-px */
  --divider-height: 30px;    /* h-[30px] */

  /* Image Gallery 尺寸 */
  --gallery-height: 217px;   /* h-[217px] */
  --gallery-margin-bottom: 3px; /* bottom-[3px] 到下一区块 */

  /* Summary Card 尺寸 */
  --summary-padding: 18px;   /* 基于 right-[350px] 和总宽368px计算 */
  --summary-price-size: 17.9px;  /* text-[17.9px] */
  --summary-address-size: 15.2px; /* text-[15.2px] */
  --summary-feature-size: 15.5px; /* text-[15.5px] */

  /* 房型图标尺寸 */
  --bed-icon-width: 22px;    /* w-[22px] */
  --bed-icon-height: 20px;   /* h-5 */
  --bath-icon-width: 24px;   /* w-6 */
  --bath-icon-height: 22px;  /* h-[22px] */
  --parking-icon-width: 22px; /* w-[22px] */
  --parking-icon-height: 19px; /* h-[19px] */

  /* 操作按钮尺寸 */
  --action-btn-size: 24px;   /* size-6 */

  /* 特征间距 */
  --feature-gap: 48px;       /* 基于布局位置计算的间距 */

  /* 文本行高计算 */
  --address-line-height: 1.51; /* leading-[22.9px] / 15.2px ≈ 1.51 */
}

/* ========================================
   区块间距系统 (从设计中精确提取)
   ======================================== */

/* 主要区块间距 */
.property-detail-layout {
  /* Header 到 Gallery: 0px 间距 */
  --header-to-gallery: 0px;

  /* Gallery 到 Summary: 3px 间距 */
  --gallery-to-summary: 3px;

  /* Summary 内部元素间距 */
  --price-to-address: 46px;     /* 基于 bottom-[202.5px] 到 bottom-[156.5px] */
  --address-to-features: 49px;  /* 基于位置计算 */
  --features-to-availability: 49px; /* 基于位置计算 */
  --availability-to-bond: 24px;     /* 基于位置计算 */
}

/* ========================================
   颜色提取值记录
   ======================================== */

/* 从设计中提取的精确颜色值 */
.extracted-colors {
  /* Header 颜色 */
  --domain-green: #44bb3a;    /* Domain logo 颜色 */
  --login-green: #57bb4e;     /* 登录按钮颜色 */

  /* Summary Card 文本颜色 */
  --price-color: #686d81;     /* 价格颜色 */
  --address-color: #7e8093;   /* 地址颜色 */
  --feature-color: #676a7c;   /* 房型数字颜色 */
  --availability-color: #727689; /* 可租时间颜色 */
  --bond-color: #75778a;      /* 押金颜色 */
}

/* ========================================
   完整组件示例用法
   ======================================== */

/* Vue 组件样式示例 */
.property-detail-page {
  background: var(--background-secondary);
  min-height: 100vh;
}

.property-detail-page .property-detail-header {
  /* 已定义样式 */
}

.property-detail-page .property-image-gallery {
  /* 图片轮播紧贴顶部栏 */
  margin-top: 0;
}

.property-detail-page .property-summary-card {
  /* 摘要卡片紧贴图片 */
  margin-top: var(--gallery-to-summary);
}
