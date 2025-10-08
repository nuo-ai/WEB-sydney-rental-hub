import BaseChip from './BaseChip.vue';

export default {
  title: 'Components/BaseChip',
  component: BaseChip,
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['default', 'selected', 'hover'],
    },
    removable: {
      control: { type: 'boolean' },
    },
    onRemove: { action: 'removed' },
  },
};

const Template = (args) => ({
  components: { BaseChip },
  setup() {
    return { args };
  },
  template: '<BaseChip v-bind="args" @remove="args.onRemove">Chip Label</BaseChip>',
});

export const Default = Template.bind({});
Default.args = {
  variant: 'default',
  removable: true,
};

export const Selected = Template.bind({});
Selected.args = {
  variant: 'selected',
  removable: true,
};

export const NotRemovable = Template.bind({});
NotRemovable.args = {
  variant: 'default',
  removable: false,
};

export const LongText = Template.bind({});
LongText.args = {
    variant: 'default',
    removable: true,
    default: 'This is a very long chip label that should be truncated'
};
LongText.slots = {
    default: 'This is a very long chip label that should be truncated'
}
