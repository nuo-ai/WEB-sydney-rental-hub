import BaseToggle from './BaseToggle.vue';

export default {
  title: '组件 (Components)/Form Elements/BaseToggle',
  component: BaseToggle,
  argTypes: {
    modelValue: { control: 'boolean' },
    size: { control: { type: 'select' }, options: ['sm', 'md'] },
    disabled: { control: 'boolean' },
    showLabels: { control: 'boolean' },
    ariaLabel: { control: 'text' },
  },
  args: {
    modelValue: false,
    size: 'md',
    disabled: false,
    showLabels: true,
    ariaLabel: 'Toggle feature',
  },
  parameters: {
    layout: 'centered',
  },
};

const Template = (args) => ({
  components: { BaseToggle },
  setup() {
    return { args };
  },
  template: `
    <BaseToggle v-bind="args" />
  `,
});

export const Default = Template.bind({});
Default.storyName = '默认交互';

export const States = (args) => ({
  components: { BaseToggle },
  setup() {
    return { args };
  },
  template: `
    <div style="display: flex; flex-direction: column; gap: 16px; align-items: flex-start;">
      <div style="display: flex; gap: 16px;">
        <BaseToggle aria-label="Default MD" />
        <BaseToggle :modelValue="true" aria-label="On MD" />
      </div>
      <div style="display: flex; gap: 16px;">
        <BaseToggle size="sm" aria-label="Default SM" />
        <BaseToggle size="sm" :modelValue="true" aria-label="On SM" />
      </div>
      <div style="display: flex; gap: 16px;">
        <BaseToggle disabled aria-label="Disabled Off" />
        <BaseToggle disabled :modelValue="true" aria-label="Disabled On" />
      </div>
      <div style="display: flex; gap: 16px;">
        <BaseToggle :showLabels="false" aria-label="No Labels" />
      </div>
    </div>
  `,
});
States.storyName = '状态对比';
