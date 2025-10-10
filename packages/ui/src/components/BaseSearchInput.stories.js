import BaseSearchInput from './BaseSearchInput.vue';

export default {
  title: '组件 (Components)/Form Elements/BaseSearchInput',
  component: BaseSearchInput,
  argTypes: {
    modelValue: { control: 'text' },
    placeholder: { control: 'text' },
    clearable: { control: 'boolean' },
    disabled: { control: 'boolean' },
    autofocus: { control: 'boolean' },
  },
  args: {
    placeholder: '搜索区域，例如 "Sydney CBD"',
    clearable: true,
    disabled: false,
    autofocus: false,
  },
  parameters: {
    layout: 'centered',
  },
};

const Template = (args) => ({
  components: { BaseSearchInput },
  setup() {
    return { args };
  },
  template: `
    <div style="max-width: 320px;">
      <BaseSearchInput v-bind="args" />
    </div>
  `,
});

export const Default = Template.bind({});
Default.storyName = '默认交互';

export const States = (args) => ({
  components: { BaseSearchInput },
  setup() {
    return { args };
  },
  template: `
    <div style="display: flex; flex-direction: column; gap: 16px; max-width: 320px;">
      <BaseSearchInput placeholder="默认状态" />
      <BaseSearchInput modelValue="有内容" />
      <BaseSearchInput modelValue="不可清除" :clearable="false" />
      <BaseSearchInput modelValue="禁用状态" disabled />
    </div>
  `,
});
States.storyName = '状态对比';
