import type { Meta, StoryObj } from '@storybook/vue3'
import BaseChip from './BaseChip.vue'

const meta: Meta<typeof BaseChip> = {
  title: 'Components/Base/BaseChip',
  component: BaseChip,
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['default', 'selected', 'hover'],
      description: '芯片的语义样式（默认 / 已选 / 悬浮），前端影响背景与边框',
    },
    removable: {
      control: { type: 'boolean' },
      description: '是否展示右侧删除按钮，前端表现为可点击的“x”',
    },
    removeLabel: {
      control: { type: 'text' },
      description: '删除按钮的无障碍文案（屏幕阅读器朗读）',
    },
    default: {
      control: { type: 'text' },
      description: '芯片文本内容',
    },
  },
  args: {
    variant: 'default',
    removable: true,
    removeLabel: '移除标签',
    default: 'Ultimo',
  },
  parameters: {
    layout: 'centered',
  },
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
  name: '默认芯片',
  render: (args) => ({
    components: { BaseChip },
    setup() {
      const handleRemove = () => {
        // 中文注释：示例输出，Storybook Console / Actions 可观察
        // eslint-disable-next-line no-console
        console.log('Remove chip clicked')
      }
      return { args, handleRemove }
    },
    template: `<BaseChip v-bind="args" @remove="handleRemove">{{ args.default }}</BaseChip>`,
  }),
}

export const Variants: Story = {
  name: '状态对比',
  render: () => ({
    components: { BaseChip },
    setup() {
      const chips = [
        { text: '默认', variant: 'default' },
        { text: '已选', variant: 'selected' },
        { text: '鼠标悬浮', variant: 'hover' },
      ]
      const handleRemove = (label: string) => {
        // eslint-disable-next-line no-console
        console.log(`Remove ${label}`)
      }
      return { chips, handleRemove }
    },
    template: `
      <div style="display: flex; gap: 12px;">
        <BaseChip
          v-for="chip in chips"
          :key="chip.variant"
          :variant="chip.variant"
          @remove="handleRemove(chip.text)"
        >
          {{ chip.text }}
        </BaseChip>
      </div>
    `,
  }),
}

export const NonRemovable: Story = {
  name: '不可移除',
  render: () => ({
    components: { BaseChip },
    template: `<BaseChip variant="selected" :removable="false">固定标签</BaseChip>`,
  }),
}
