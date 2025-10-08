import BaseButton from './BaseButton.vue';
import { Plus } from 'lucide-vue-next';

export default {
  title: 'Components/BaseButton',
  component: BaseButton,
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['primary', 'secondary', 'ghost', 'danger'],
      description: '按钮视觉风格，对应不同品牌语义（主操作/次要/悬浮/警示）',
    },
    size: {
      control: { type: 'select' },
      options: ['small', 'medium', 'large'],
      description: '按钮尺寸，影响前端高度与左右内边距',
    },
    loading: {
      control: { type: 'boolean' },
      description: '显示旋转指示，表明系统正在处理中',
    },
    disabled: {
      control: { type: 'boolean' },
      description: '禁用状态：半透明且不可交互',
    },
    block: {
      control: { type: 'boolean' },
      description: '块级按钮（宽度占满父容器），适合移动端底部操作条',
    },
    default: {
      control: { type: 'text' },
      description: '按钮内部的文本内容（默认插槽）',
    },
    type: { table: { disable: true } },
  },
  args: {
    variant: 'primary',
    size: 'medium',
    loading: false,
    disabled: false,
    block: false,
    default: '立即联系',
  },
  parameters: {
    layout: 'centered',
  },
};

const renderFactory = (options = {}) => (args) => ({
  components: { BaseButton, Plus },
  setup() {
    const handleClick = (event) => {
      console.log('BaseButton clicked', event);
    };
    return { args, withIcon: options.withIcon ?? false, handleClick };
  },
  template: `
    <BaseButton
      v-bind="args"
      :type="args.type ?? 'button'"
      @click="handleClick"
    >
      <template v-if="withIcon" #icon>
        <Plus />
      </template>
      {{ args.default }}
    </BaseButton>
  `,
});

export const Primary = {
  name: '主要按钮',
  args: {
    variant: 'primary',
    default: '立即联系',
  },
  render: renderFactory(),
};

export const Secondary = {
  name: '次要按钮',
  args: {
    variant: 'secondary',
    default: '查看更多',
  },
  render: renderFactory(),
};

export const Ghost = {
  name: '幽灵按钮',
  args: {
    variant: 'ghost',
    default: '轻量操作',
  },
  render: renderFactory(),
};

export const Danger = {
  name: '危险按钮',
  args: {
    variant: 'danger',
    default: '删除房源',
  },
  render: renderFactory(),
};

export const WithIcon = {
  name: '前置图标',
  args: {
    variant: 'primary',
    default: '添加收藏',
  },
  render: renderFactory({ withIcon: true }),
};

export const States = {
  name: '状态对比',
  render: () => ({
    components: { BaseButton },
    setup() {
      const variants = [
        { label: '加载中', props: { variant: 'primary', loading: true } },
        { label: '禁用', props: { variant: 'secondary', disabled: true } },
        { label: '块级', props: { variant: 'primary', block: true } },
      ];
      const handleClick = (label) => {
        console.log(`Clicked button: ${label}`);
      };
      return { variants, handleClick };
    },
    template: `
      <div style="display: flex; flex-direction: column; gap: 16px; width: 320px;">
        <BaseButton
          v-for="item in variants"
          :key="item.label"
          v-bind="item.props"
          @click="handleClick(item.label)"
        >
          {{ item.label }}
        </BaseButton>
      </div>
    `,
  }),
};
