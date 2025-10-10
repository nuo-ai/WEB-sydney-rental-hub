import BaseIconButton from './BaseIconButton.vue';
import { Heart, Share2 } from 'lucide-vue-next';

export default {
  title: '组件 (Components)/Form Elements/BaseIconButton',
  component: BaseIconButton,
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['ghost', 'secondary'],
    },
    size: {
      control: { type: 'select' },
      options: ['sm', 'md'],
    },
    disabled: {
      control: 'boolean',
    },
    ariaLabel: {
      control: 'text',
    },
    default: {
      control: { type: 'text' },
      description: '按钮内部的内容 (默认插槽)，通常是一个图标组件',
    },
  },
  args: {
    variant: 'ghost',
    size: 'md',
    disabled: false,
    ariaLabel: 'Icon Button',
  },
  parameters: {
    layout: 'centered',
  },
};

const Template = (args) => ({
  components: { BaseIconButton, Heart },
  setup() {
    return { args };
  },
  template: `
    <BaseIconButton v-bind="args">
      <Heart />
    </BaseIconButton>
  `,
});

export const Default = Template.bind({});
Default.storyName = '默认交互';
Default.args = {
  ariaLabel: 'Favorite',
};

export const States = (args) => ({
  components: { BaseIconButton, Heart, Share2 },
  setup() {
    return { args };
  },
  template: `
    <div style="display: flex; align-items: center; gap: 16px;">
      <BaseIconButton aria-label="Ghost MD"><Heart /></BaseIconButton>
      <BaseIconButton variant="secondary" aria-label="Secondary MD"><Share2 /></BaseIconButton>
      <BaseIconButton size="sm" aria-label="Ghost SM"><Heart /></BaseIconButton>
      <BaseIconButton variant="secondary" size="sm" aria-label="Secondary SM"><Share2 /></BaseIconButton>
      <BaseIconButton disabled aria-label="Disabled"><Heart /></BaseIconButton>
    </div>
  `,
});
States.storyName = '状态对比';
