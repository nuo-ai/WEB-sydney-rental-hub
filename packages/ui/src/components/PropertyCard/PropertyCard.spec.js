import { mount } from '@vue/test-utils';
import PropertyCard from './PropertyCard.vue';

describe('PropertyCard', () => {
  const mockProperty = {
    id: '1',
    price: '$500/wk',
    address: {
      line1: '123 Main St',
      line2: 'Sydney, NSW 2000'
    },
    bedrooms: 2,
    bathrooms: 1,
    parking: 1,
    image: 'https://example.com/image.jpg'
  };

  it('renders property information correctly', () => {
    const wrapper = mount(PropertyCard, {
      props: { property: mockProperty }
    });
    
    expect(wrapper.text()).toContain('$500/wk');
    expect(wrapper.text()).toContain('123 Main St');
    expect(wrapper.text()).toContain('Sydney, NSW 2000');
  });

  it('emits toggle-favorite event when favorite button is clicked', async () => {
    const wrapper = mount(PropertyCard, {
      props: { 
        property: mockProperty,
        isFavorite: false
      }
    });
    
    await wrapper.find('.property-card__favorite-btn').trigger('click');
    expect(wrapper.emitted('toggle-favorite')).toBeTruthy();
    expect(wrapper.emitted('toggle-favorite')[0]).toEqual(['1']);
  });

  it('shows loading state when loading prop is true', () => {
    const wrapper = mount(PropertyCard, {
      props: { 
        property: mockProperty,
        loading: true
      }
    });
    
    expect(wrapper.find('.property-card__loading').exists()).toBe(true);
    expect(wrapper.find('.property-card__content').exists()).toBe(false);
  });

  it('shows error state when error prop is true', () => {
    const wrapper = mount(PropertyCard, {
      props: { 
        property: mockProperty,
        error: true
      }
    });
    
    expect(wrapper.find('.property-card__error').exists()).toBe(true);
  });

  it('validates required property prop', () => {
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation();
    
    mount(PropertyCard, {
      props: { property: {} } // 缺少必需的 id 和 price
    });
    
    expect(consoleSpy).toHaveBeenCalled();
    consoleSpy.mockRestore();
  });

  it('handles image error events', async () => {
    const wrapper = mount(PropertyCard, {
      props: { property: mockProperty }
    });
    
    await wrapper.find('.property-card__image').trigger('error');
    expect(wrapper.emitted('image-error')).toBeTruthy();
  });

  it('emits property-click event when card is clicked', async () => {
    const wrapper = mount(PropertyCard, {
      props: { property: mockProperty }
    });
    
    await wrapper.find('.property-card').trigger('click');
    expect(wrapper.emitted('property-click')).toBeTruthy();
    expect(wrapper.emitted('property-click')[0]).toEqual(['1']);
  });

  it('stops event propagation when favorite button is clicked', async () => {
    const wrapper = mount(PropertyCard, {
      props: { property: mockProperty }
    });
    
    const favoriteButton = wrapper.find('.property-card__favorite-btn');
    const clickEvent = new Event('click');
    const stopPropagationSpy = jest.spyOn(clickEvent, 'stopPropagation');
    
    await favoriteButton.trigger('click', clickEvent);
    expect(stopPropagationSpy).toHaveBeenCalled();
  });

  it('uses placeholder image when no image is provided', () => {
    const propertyWithoutImage = { ...mockProperty, image: '' };
    const wrapper = mount(PropertyCard, {
      props: { property: propertyWithoutImage }
    });
    
    const image = wrapper.find('.property-card__image');
    expect(image.attributes('src')).toBe('/static/placeholder.jpg');
  });

  it('applies favorite class when isFavorite is true', () => {
    const wrapper = mount(PropertyCard, {
      props: { 
        property: mockProperty,
        isFavorite: true
      }
    });
    
    expect(wrapper.classes()).toContain('property-card--favorite');
  });
});
