import type { Meta, StoryObj } from '@storybook/vue3'
import BaseBadge from './BaseBadge.vue'

const meta: Meta<typeof BaseBadge> = {
  title: 'Components/Base/BaseBadge',
  component: BaseBadge,
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['brand', 'neutral', 'success', 'warning', 'danger', 'info'],
      description: '徽章语义色彩，映射不同业务含义（如“新上线”或“警告”）',
    },
    pill: {
      control: { type: 'boolean' },
      description: '是否展示为完整胶囊形态，前端表现为全圆角',
    },
    default: {
      control: { type: 'text' },
      description: '徽章文本内容',
    },
  },
  args: {
    variant: 'brand',
    pill: true,
    default: '新上线',
  },
  parameters: {
    layout: 'centered',
  },
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
  name: '品牌徽章',
  render: (args) => ({
    components: { BaseBadge },
    setup() {
      return { args }
    },
    template: `<BaseBadge v-bind="args">{{ args.default }}</BaseBadge>`,
  }),
}

export const Variants: Story = {
  name: '语义色对比',
  render: () => ({
    components: { BaseBadge },
    setup() {
      const items = [
        { label: '新上线', variant: 'brand' },
        { label: '默认', variant: 'neutral' },
        { label: '已入住', variant: 'success' },
        { label: '即将下架', variant: 'warning' },
        { label: '风险', variant: 'danger' },
        { label: '提示', variant: 'info' },
      ]
      return { items }
    },
    template: `
      <div style="display: flex; gap: 12px; flex-wrap: wrap;">
        <BaseBadge v-for="item in items" :key="item.variant" :variant="item.variant">
          {{ item.label }}
        </BaseBadge>
      </div>
    `,
  }),
}

export const ShapeComparison: Story = {
  name: '胶囊 vs 矩形',
  render: () => ({
    components: { BaseBadge },
    template: `
      <div style="display: flex; gap: 16px; align-items: center;">
        <BaseBadge variant="brand" pill>胶囊徽章</BaseBadge>
        <BaseBadge variant="brand" :pill="false">矩形徽章</BaseBadge>
      </div>
    `,
  }),
}
