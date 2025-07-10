<template>
  <view class="page-container">
    <!-- iOS状态栏 -->
    <view class="ios-status-bar">
        <text class="status-time">9:41</text>
        <view class="status-indicators">
            <FeatherIcon name="signal" :size="12" />
            <FeatherIcon name="wifi" :size="12" />
            <FeatherIcon name="battery" :size="14" />
        </view>
    </view>

    <view class="page-content">
        <!-- 搜索栏 -->
        <view class="search-container">
            <view class="search-bar">
                <FeatherIcon name="search" :size="16" color="#8E8E93" class="search-icon" />
                <input type="text" class="search-input" placeholder="搜索区域，如 Zetland, Redfern" v-model="searchKeyword" @input="onSearchInput">
                <button class="filter-button" @tap="showFilters">
                    <FeatherIcon name="sliders" :size="18" color="#007AFF" />
                </button>
            </view>
        </view>

        <!-- 结果数量 -->
        <view class="results-count">
            找到 {{ properties.length }} 套房源
        </view>

        <!-- 房源列表 -->
        <scroll-view scroll-y="true" class="properties-list">
            <view 
              class="property-card" 
              v-for="property in properties" 
              :key="property.id" 
              @tap="viewPropertyDetail(property.id)"
            >
                <view class="property-image">
                    <image :src="property.image" mode="aspectFill"></image>
                    <view class="property-badge" v-if="property.isNew">New</view>
                    <view class="property-favorite" @tap.stop="toggleFavorite(property.id)">
                        <FeatherIcon name="heart" :size="16" :color="property.isFavorite ? '#FF3B30' : '#48484A'" :fill="property.isFavorite ? '#FF3B30' : 'none'" />
                    </view>
                </view>
                <view class="property-info">
                    <view class="property-price">${{ property.weekly_rent }} per week</view>
                    <view class="property-address">{{ property.address }}</view>
                    <view class="property-suburb">{{ property.suburb }}</view>
                    <view class="property-features">
                        <view class="feature-item">
                            <FeatherIcon name="home" :size="14" color="#8E8E93" />
                            <text>{{ property.bedrooms }}</text>
                        </view>
                        <view class="feature-item">
                            <FeatherIcon name="droplet" :size="14" color="#8E8E93" />
                            <text>{{ property.bathrooms }}</text>
                        </view>
                        <view class="feature-item">
                            <FeatherIcon name="truck" :size="14" color="#8E8E93" />
                            <text>{{ property.parking }}</text>
                        </view>
                        <view class="feature-item">
                            <text>{{ property.property_type }}</text>
                        </view>
                    </view>
                    <view class="property-date">Available {{ property.available_date }}</view>
                    <view class="university-distance" v-if="property.commute_info">{{ property.commute_info }}</view>
                </view>
            </view>
        </scroll-view>
    </view>

    <!-- iOS底部Tab Bar -->
    <view class="ios-tab-bar">
        <view class="tab-item active" @tap="navigateTo('/pages/index/index')">
            <FeatherIcon name="search" :size="20" />
            <text>搜索</text>
        </view>
        <view class="tab-item" @tap="navigateTo('/pages/saved/saved')">
            <FeatherIcon name="heart" :size="20" />
            <text>收藏</text>
        </view>
        <view class="tab-item" @tap="navigateTo('/pages/map/map')">
            <FeatherIcon name="map" :size="20" />
            <text>地图</text>
        </view>
        <view class="tab-item" @tap="navigateTo('/pages/services/services')">
            <FeatherIcon name="bell" :size="20" />
            <text>服务</text>
        </view>
        <view class="tab-item" @tap="navigateTo('/pages/profile/profile')">
            <FeatherIcon name="user" :size="20" />
            <text>我的</text>
        </view>
    </view>
  </view>
</template>

<script>
import FeatherIcon from '@/components/FeatherIcon.vue'

export default {
  name: 'Index',
  components: {
    FeatherIcon
  },
  data() {
    return {
      searchKeyword: '',
      properties: [
        {
          id: 1,
          image: 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
          isNew: true,
          isFavorite: false,
          weekly_rent: 780,
          address: '942/8 Ascot Avenue',
          suburb: 'Zetland NSW 2017',
          bedrooms: 1,
          bathrooms: 1,
          parking: 1,
          property_type: 'Apartment',
          available_date: '1 Feb 2025',
          commute_info: 'UTS: 8 min walk'
        },
        {
          id: 2,
          image: 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=600&fit=crop',
          isNew: false,
          isFavorite: true,
          weekly_rent: 650,
          address: '15/120 Bowden Street',
          suburb: 'Meadowbank NSW 2114',
          bedrooms: 1,
          bathrooms: 1,
          parking: 1,
          property_type: 'Unit',
          available_date: '15 Jan 2025',
          commute_info: 'Macquarie Uni: 15 min bus'
        },
        {
          id: 3,
          image: 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800&h=600&fit=crop',
          isNew: false,
          isFavorite: false,
          weekly_rent: 920,
          address: '302/81 Macleay Street',
          suburb: 'Potts Point NSW 2011',
          bedrooms: 2,
          bathrooms: 1,
          parking: 0,
          property_type: 'Apartment',
          available_date: '1 Mar 2025',
          commute_info: 'Sydney Uni: 12 min bus'
        },
        {
          id: 4,
          image: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&h=600&fit=crop',
          isNew: false,
          isFavorite: false,
          weekly_rent: 550,
          address: '8/45 Campbell Street',
          suburb: 'Surry Hills NSW 2010',
          bedrooms: 1,
          bathrooms: 1,
          parking: 0,
          property_type: 'Studio',
          available_date: 'Available Now',
          commute_info: 'UTS: 10 min walk'
        }
      ]
    }
  },
  methods: {
    onSearchInput(e) {
      this.searchKeyword = e.detail.value
    },
    showFilters() {
      uni.showToast({ title: '打开筛选', icon: 'none' });
    },
    viewPropertyDetail(id) {
      uni.navigateTo({ url: `/pages/property/detail?id=${id}` });
    },
    toggleFavorite(id) {
      const property = this.properties.find(p => p.id === id);
      if (property) {
        property.isFavorite = !property.isFavorite;
      }
    },
    navigateTo(url) {
      uni.navigateTo({ url });
    }
  }
}
</script>

<style lang="scss" scoped>
/* 导入原型样式 */
.page-container {
  width: 393px;
  height: 852px;
  overflow: hidden;
  position: relative;
  font-family: 'SF Pro Text', -apple-system, sans-serif;
  background: #F2F2F7;
}

/* iOS状态栏 */
.ios-status-bar {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 44px;
    background: transparent;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 24px;
    font-size: 14px;
    font-weight: 600;
    color: #000;
    z-index: 1000;
}

.status-time {
    font-family: 'SF Pro Text', sans-serif;
}

.status-indicators {
    display: flex;
    align-items: center;
    gap: 6px;
}

/* iOS底部Tab Bar */
.ios-tab-bar {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 84px;
    background: rgba(255,255,255,0.9);
    backdrop-filter: blur(20px);
    border-top: 0.5px solid rgba(0,0,0,0.1);
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding-top: 8px;
    z-index: 1000;
}

.tab-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    padding: 8px 12px;
    text-decoration: none;
    color: #8E8E93;
    transition: color 0.2s ease;
    min-width: 60px;
}

.tab-item.active {
    color: #007AFF;
}

.tab-item .feather-icon {
    font-size: 20px;
}

.tab-item text {
    font-size: 10px;
    font-weight: 500;
    font-family: 'PingFang SC', sans-serif;
}

/* 主内容区域 */
.page-content {
    padding-top: 44px;
    padding-bottom: 84px;
    height: 100%;
    box-sizing: border-box;
}

/* 搜索栏 */
.search-container {
    padding: 16px;
    background: white;
    border-bottom: 0.5px solid rgba(0,0,0,0.1);
}

.search-bar {
    position: relative;
    display: flex;
    align-items: center;
    gap: 12px;
}

.search-input {
    flex: 1;
    height: 44px;
    background: #F2F2F7;
    border: none;
    border-radius: 22px;
    padding: 0 16px 0 40px;
    font-size: 16px;
}

.search-icon {
    position: absolute;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    z-index: 1;
}

.filter-button {
    width: 44px;
    height: 44px;
    background: #F2F2F7;
    border: none;
    border-radius: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
}

.results-count {
    padding: 12px 16px;
    background: white;
    border-bottom: 0.5px solid rgba(0,0,0,0.1);
    font-size: 14px;
    color: #8E8E93;
    font-family: 'PingFang SC', sans-serif;
}

.properties-list {
    height: calc(100% - 120px); /* 44px status + 77px search + 41px results */
}

.property-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    margin: 16px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.property-image {
    position: relative;
    width: 100%;
    height: 220px;
}

.property-image image {
    width: 100%;
    height: 100%;
}

.property-badge {
    position: absolute;
    top: 12px;
    left: 12px;
    background: #007AFF;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
}

.property-favorite {
    position: absolute;
    top: 12px;
    right: 12px;
    width: 32px;
    height: 32px;
    background: rgba(255,255,255,0.9);
    backdrop-filter: blur(10px);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.property-info {
    padding: 16px;
}

.property-price {
    font-size: 22px;
    font-weight: 700;
    color: #000;
    margin-bottom: 8px;
}

.property-address {
    font-size: 16px;
    color: #000;
    font-weight: 500;
    margin-bottom: 4px;
}

.property-suburb {
    font-size: 14px;
    color: #8E8E93;
    margin-bottom: 12px;
}

.property-features {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 12px;
    font-size: 14px;
    color: #48484A;
}

.feature-item {
    display: flex;
    align-items: center;
    gap: 4px;
}

.feature-item .feather-icon {
    color: #8E8E93;
}

.property-date {
    font-size: 13px;
    color: #8E8E93;
}

.university-distance {
    background: #34C759;
    color: white;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    margin-top: 8px;
    display: inline-block;
}
</style>
