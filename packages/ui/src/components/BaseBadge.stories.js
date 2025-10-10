import BaseBadge from './BaseBadge.vue';

export default {
  title: '组件 (Components)/Data Display/BaseBadge',
  component: BaseBadge,
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['brand', 'neutral', 'success', 'warning', 'danger', 'info'],
    },
    pill: {
      control: { type: 'boolean' },
    },
    default: {
      control: { type: 'text' },
      description: '徽章内部的文本内容 (默认插槽)',
    },
  },
  args: {
    variant: 'brand',
    pill: true,
    default: '新房源',
  },
  parameters: {
    layout: 'centered',
  },
};

const Template = (args) => ({
  components: { BaseBadge },
  setup() {
    return { args };
  },
  template: '<BaseBadge v-bind="args">{{ args.default }}</BaseBadge>',
});

export const Default = Template.bind({});
Default.storyName = '默认交互';

export const Variants = (args) => ({
  components: { BaseBadge },
  setup() {
    return { args };
  },
  template: `
    <div style="display: flex; flex-direction: column; gap: 16px;">
      <div style="display: flex; gap: 8px;">
        <BaseBadge variant="brand">Brand</BaseBadge>
        <BaseBadge variant="neutral">Neutral</BaseBadge>
        <BaseBadge variant="success">Success</BaseBadge>
        <BaseBadge variant="warning">Warning</BaseBadge>
        <BaseBadge variant="danger">Danger</BaseBadge>
        <BaseBadge variant="info">Info</BaseBadge>
      </div>
      <div style="display: flex; gap: 8px;">
        <BaseBadge :pill="false" variant="brand">Brand (Square)</BaseBadge>
        <BaseBadge :pill="false" variant="neutral">Neutral (Square)</BaseBadge>
        <BaseBadge :pill="false" variant="success">Success (Square)</BaseBadge>
      </div>
    </div>
  `,
});
Variants.storyName = '所有变体';
