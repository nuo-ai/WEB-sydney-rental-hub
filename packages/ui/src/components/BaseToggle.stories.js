import BaseToggle from './BaseToggle.vue';

export default {
  title: 'Components/BaseToggle',
  component: BaseToggle,
  argTypes: {
    modelValue: { control: 'boolean' },
    size: { control: { type: 'select' }, options: ['sm', 'md'] },
    disabled: { control: 'boolean' },
    showLabels: { control: 'boolean' },
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
Default.args = {
  ariaLabel: 'Toggle feature',
};

export const AllStates = (args) => ({
  components: { BaseToggle },
  setup() {
    return { args };
  },
  template: `
    <div style="display: flex; flex-direction: column; gap: 16px;">
      <BaseToggle aria-label="Default MD" />
      <BaseToggle :modelValue="true" aria-label="On MD" />
      <BaseToggle size="sm" aria-label="Default SM" />
      <BaseToggle size="sm" :modelValue="true" aria-label="On SM" />
      <BaseToggle disabled aria-label="Disabled Off" />
      <BaseToggle disabled :modelValue="true" aria-label="Disabled On" />
      <BaseToggle :showLabels="false" aria-label="No Labels" />
    </div>
  `,
});
