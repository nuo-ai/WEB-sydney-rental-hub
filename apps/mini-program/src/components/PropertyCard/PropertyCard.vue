<template>
  <view class="property-card">
    <image 
      class="property-card__image" 
      :src="property.image" 
      mode="aspectFill"
    />
    
    <view class="property-card__content">
      <text class="property-card__price">{{ property.price }}</text>
      
      <view class="property-card__address">
        <text class="property-card__address-line1">{{ property.address.line1 }}</text>
        <text class="property-card__address-line2">{{ property.address.line2 }}</text>
      </view>
      
      <view class="property-card__features">
        <text class="property-card__feature">{{ property.bedrooms }} beds</text>
        <text class="property-card__feature">{{ property.bathrooms }} baths</text>
        <text class="property-card__feature">{{ property.parking }} parking</text>
      </view>
      
      <view class="property-card__actions">
        <button 
          class="property-card__favorite-btn"
          @click="toggleFavorite"
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
    }
  },
  methods: {
    toggleFavorite() {
      this.$emit('toggle-favorite', this.property.id);
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
}

.property-card__image {
  width: 100%;
  height: 200px;
}

.property-card__content {
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
}

.property-card__feature {
  font-size: var(--font-size-sm);
  color: var(--color-semantic-text-secondary);
}

.property-card__actions {
  display: flex;
  justify-content: flex-end;
}

.property-card__favorite-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: var(--space-sm);
}
</style>
