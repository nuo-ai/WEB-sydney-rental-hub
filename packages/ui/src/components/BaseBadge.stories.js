import BaseBadge from './BaseBadge.vue';

export default {
  title: 'Components/BaseBadge',
  component: BaseBadge,
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['brand', 'neutral', 'success', 'warning', 'danger', 'info'],
    },
    pill: {
      control: { type: 'boolean' },
    },
  },
};

const Template = (args) => ({
  components: { BaseBadge },
  setup() {
    return { args };
  },
  template: '<BaseBadge v-bind="args">Badge</BaseBadge>',
});

export const Default = Template.bind({});
Default.args = {
  variant: 'brand',
  pill: true,
};

export const AllVariants = (args) => ({
  components: { BaseBadge },
  setup() {
    return { args };
  },
  template: `
    <div style="display: flex; gap: 8px;">
      <BaseBadge variant="brand">Brand</BaseBadge>
      <BaseBadge variant="neutral">Neutral</BaseBadge>
      <BaseBadge variant="success">Success</BaseBadge>
      <BaseBadge variant="warning">Warning</BaseBadge>
      <BaseBadge variant="danger">Danger</BaseBadge>
      <BaseBadge variant="info">Info</BaseBadge>
    </div>
  `,
});

export const NonPill = (args) => ({
    components: { BaseBadge },
    setup() {
      return { args };
    },
    template: `
      <div style="display: flex; gap: 8px;">
        <BaseBadge :pill="false" variant="brand">Brand</BaseBadge>
        <BaseBadge :pill="false" variant="neutral">Neutral</BaseBadge>
        <BaseBadge :pill="false" variant="success">Success</BaseBadge>
      </div>
    `,
  });
