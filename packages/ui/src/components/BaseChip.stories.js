import BaseChip from './BaseChip.vue';

export default {
  title: '组件 (Components)/Data Display/BaseChip',
  component: BaseChip,
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['default', 'selected', 'hover'],
    },
    removable: {
      control: { type: 'boolean' },
    },
    default: {
      control: { type: 'text' },
      description: 'Chip 内部的文本内容 (默认插槽)',
    },
    onRemove: { action: 'removed' },
  },
  args: {
    variant: 'default',
    removable: true,
    default: '筛选标签',
  },
  parameters: {
    layout: 'centered',
  },
};

const Template = (args) => ({
  components: { BaseChip },
  setup() {
    return { args };
  },
  template: '<BaseChip v-bind="args" @remove="args.onRemove">{{ args.default }}</BaseChip>',
});

export const Default = Template.bind({});
Default.storyName = '默认交互';

export const States = (args) => ({
  components: { BaseChip },
  setup() {
    return { args };
  },
  template: `
    <div style="display: flex; align-items: flex-start; gap: 8px;">
      <BaseChip variant="default" removable @remove="args.onRemove">Default</BaseChip>
      <BaseChip variant="selected" removable @remove="args.onRemove">Selected</BaseChip>
      <BaseChip variant="default" :removable="false">Not Removable</BaseChip>
      <BaseChip variant="default" removable @remove="args.onRemove" style="max-width: 150px;">
        This is a very long chip label
      </BaseChip>
    </div>
  `,
});
States.storyName = '状态对比';
