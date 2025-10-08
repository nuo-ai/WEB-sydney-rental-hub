import BaseIconButton from './BaseIconButton.vue';
import { Heart, Share2 } from 'lucide-vue-next';

export default {
  title: 'Components/BaseIconButton',
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
Default.args = {
  ariaLabel: 'Favorite',
};

export const AllVariants = (args) => ({
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
