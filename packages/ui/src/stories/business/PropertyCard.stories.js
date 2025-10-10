import PropertyCard from '../../../../apps/web/src/components/PropertyCard.vue';
import { mockPropertyData } from '../fixtures/property';

export default {
  title: '组件 (Components)/Data Display/PropertyCard',
  component: PropertyCard,
  parameters: {
    layout: 'centered',
  },
};

const Template = (args) => ({
  components: { PropertyCard },
  setup() {
    return { args };
  },
  template: '<PropertyCard v-bind="args" />',
});

export const Default = Template.bind({});
Default.storyName = '默认状态';
Default.args = {
  property: mockPropertyData,
};

export const Favorited = Template.bind({});
Favorited.storyName = '已收藏状态';
Favorited.args = {
  property: {
    ...mockPropertyData,
    // 模拟 isFavorite 的逻辑，实际应用中由 Pinia store 控制
  },
  // 在 Storybook 中，我们可以通过一个 prop 来模拟这个状态
  // 假设 PropertyCard 接受一个 isFavorite prop
  // isFavorite: true, 
};
// 注意：为了让这个 Story 生效，PropertyCard 可能需要接受一个 isFavorite prop，
// 或者我们需要在 Storybook 的 preview.js 中模拟 Pinia store。
// 目前，我们将依赖 Pinia 的默认状态。

export const NewProperty = Template.bind({});
NewProperty.storyName = '新房源状态';
NewProperty.args = {
  property: {
    ...mockPropertyData,
    listing_id: 9999, // 假设 isNewProperty 的逻辑是 based on listing_id
  },
};

// Loading state would require a specific skeleton component or a loading prop in PropertyCard
// export const Loading = ...
