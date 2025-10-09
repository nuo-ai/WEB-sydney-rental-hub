<template>
  <view 
    class="property-card" 
    :class="{ 'property-card--favorite': isFavorite, 'property-card--loading': loading }"
    @click="handleClick"
  >
    <!-- 加载状态 -->
    <view v-if="loading" class="property-card__loading">
      <text class="property-card__loading-text">Loading...</text>
    </view>
    
    <!-- 错误状态 -->
    <view v-else-if="error" class="property-card__error">
      <text class="property-card__error-text">Error loading property</text>
    </view>
    
    <!-- 正常内容 -->
    <view v-else class="property-card__content">
      <image 
        class="property-card__image" 
        :src="property.image || '/static/placeholder.jpg'" 
        mode="aspectFill"
        @error="handleImageError"
      />
      
      <view class="property-card__info">
        <text class="property-card__price">{{ property.price }}</text>
        
        <view class="property-card__address">
          <text class="property-card__address-line1">{{ property.address?.line1 }}</text>
          <text class="property-card__address-line2">{{ property.address?.line2 }}</text>
        </view>
        
        <view class="property-card__features">
          <text class="property-card__feature" v-if="property.bedrooms">
            🛏️ {{ property.bedrooms }} beds
          </text>
          <text class="property-card__feature" v-if="property.bathrooms">
            🛁 {{ property.bathrooms }} baths
          </text>
          <text class="property-card__feature" v-if="property.parking">
            🚗 {{ property.parking }} parking
          </text>
        </view>
      </view>
      
      <view class="property-card__actions">
        <button 
          class="property-card__favorite-btn"
          @click.stop="toggleFavorite"
          :aria-label="isFavorite ? 'Remove from favorites' : 'Add to favorites'"
        >
          {{ isFavorite ? '❤️' : '🤍' }}
        </button>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  name: 'PropertyCard',
  props: {
    property: {
      type: Object,
      required: true,
      validator: (prop) => {
        return prop.id && prop.price;
      },
      default: () => ({
        id: '',
        image: '',
        price: '',
        address: {
          line1: '',
          line2: ''
        },
        bedrooms: 0,
        bathrooms: 0,
        parking: 0
      })
    },
    isFavorite: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: Boolean,
      default: false
    }
  },
  emits: ['toggle-favorite', 'property-click', 'image-error'],
  methods: {
    toggleFavorite() {
      this.$emit('toggle-favorite', this.property.id);
    },
    handleClick() {
      this.$emit('property-click', this.property.id);
    },
    handleImageError() {
      this.$emit('image-error', this.property.id);
    }
  }
}
</script>

<style lang="scss">
@import '../../styles/generated/light.wxss';
@import '../../styles/generated/dark.wxss';

.property-card {
  background-color: var(--color-semantic-bg-primary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  margin: var(--space-md);
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  
  &:active {
    transform: scale(0.98);
  }
}

.property-card--favorite {
  box-shadow: 0 0 0 2px var(--color-semantic-feedback-success);
}

.property-card__loading,
.property-card__error {
  padding: var(--space-xl);
  text-align: center;
}

.property-card__loading-text,
.property-card__error-text {
  color: var(--color-semantic-text-secondary);
  font-size: var(--font-size-md);
}

.property-card__image {
  width: 100%;
  height: 200px;
  background-color: var(--color-semantic-bg-secondary);
}

.property-card__info {
  padding: var(--space-lg);
}

.property-card__price {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-semantic-text-primary);
  margin-bottom: var(--space-sm);
}

.property-card__address {
  margin-bottom: var(--space-md);
}

.property-card__address-line1 {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-semantic-text-primary);
  display: block;
  margin-bottom: var(--space-xs);
}

.property-card__address-line2 {
  font-size: var(--font-size-md);
  color: var(--color-semantic-text-secondary);
  display: block;
}

.property-card__features {
  display: flex;
  gap: var(--space-lg);
  margin-bottom: var(--space-md);
  flex-wrap: wrap;
}

.property-card__feature {
  font-size: var(--font-size-sm);
  color: var(--color-semantic-text-secondary);
  white-space: nowrap;
}

.property-card__actions {
  display: flex;
  justify-content: flex-end;
  padding: 0 var(--space-lg) var(--space-lg);
}

.property-card__favorite-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: var(--space-sm);
  border-radius: 50%;
  transition: background-color 0.2s ease;
  
  &:active {
    background-color: var(--color-semantic-bg-secondary);
  }
}
</style>
