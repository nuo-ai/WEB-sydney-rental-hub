import BaseInput from './BaseInput.vue';

export default {
  title: 'Components/BaseInput',
  component: BaseInput,
  argTypes: {
    modelValue: {
      control: { type: 'text' },
      description: '输入框的绑定值',
    },
    placeholder: {
      control: { type: 'text' },
      description: '占位提示文字',
    },
    disabled: {
      control: { type: 'boolean' },
      description: '禁用状态',
    },
  },
  args: {
    modelValue: '',
    placeholder: '请输入...',
    disabled: false,
  },
  parameters: {
    layout: 'centered',
  },
};

const Template = (args) => ({
  components: { BaseInput },
  setup() {
    return { args };
  },
  template: '<BaseInput v-bind="args" style="width: 240px;" />',
});

export const Default = Template.bind({});
Default.storyName = '默认状态';

export const Disabled = Template.bind({});
Disabled.storyName = '禁用状态';
Disabled.args = {
  modelValue: '已禁用',
  disabled: true,
};
