import BaseListItem from './BaseListItem.vue';
import { ChevronRight, Mail } from 'lucide-vue-next';

export default {
  title: '组件 (Components)/Data Display/BaseListItem',
  component: BaseListItem,
  argTypes: {
    selected: { control: 'boolean' },
    disabled: { control: 'boolean' },
    clickable: { control: 'boolean' },
    bordered: { control: 'boolean' },
    default: {
      control: { type: 'text' },
      description: '列表项主标题 (默认插槽)',
    },
    description: {
      control: { type: 'text' },
      description: '列表项描述文本 (description 插槽)',
    },
  },
  args: {
    selected: false,
    disabled: false,
    clickable: true,
    bordered: true,
    default: '个人资料',
    description: '设置您的账户信息',
  },
  parameters: {
    layout: 'padded',
  },
};

const Template = (args) => ({
  components: { BaseListItem, Mail, ChevronRight },
  setup() {
    return { args };
  },
  template: `
    <BaseListItem v-bind="args">
      <template #prefix><Mail /></template>
      {{ args.default }}
      <template #description>{{ args.description }}</template>
      <template #suffix><ChevronRight /></template>
    </BaseListItem>
  `,
});

export const Default = Template.bind({});
Default.storyName = '默认交互';

export const States = (args) => ({
  components: { BaseListItem, ChevronRight, Mail },
  setup() {
    return { args };
  },
  template: `
    <div style="max-width: 320px;">
      <BaseListItem clickable>
        <template #prefix><Mail /></template>
        默认状态
        <template #description>这是一个标准的列表项</template>
        <template #suffix><ChevronRight /></template>
      </BaseListItem>
      <BaseListItem clickable selected>
        <template #prefix><Mail /></template>
        选中状态
        <template #description>此项目已被选中</template>
        <template #suffix><ChevronRight /></template>
      </BaseListItem>
      <BaseListItem clickable disabled>
        <template #prefix><Mail /></template>
        禁用状态
        <template #description>此项目不可用</template>
        <template #suffix><ChevronRight /></template>
      </BaseListItem>
    </div>
  `,
});
States.storyName = '状态对比';
