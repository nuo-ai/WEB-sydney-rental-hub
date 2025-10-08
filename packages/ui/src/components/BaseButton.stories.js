import BaseButton from './BaseButton.vue';

// More on how to set up stories at: https://storybook.js.org/docs/writing-stories
export default {
  title: 'Design System/Components/BaseButton',
  component: BaseButton,
  tags: ['autodocs'],
  argTypes: {
    size: {
      control: { type: 'select' },
      options: ['sm', 'md', 'lg'],
    },
    // We use a slot for the button's label, which we can control via a custom arg.
    label: {
        control: 'text',
        name: 'Label'
    }
  },
};

// A template for all stories to reuse
const Template = (args) => ({
    components: { BaseButton },
    setup() {
      return { args };
    },
    template: '<BaseButton v-bind="args">{{ args.label }}</BaseButton>',
});

export const Primary = Template.bind({});
Primary.args = {
  primary: true,
  label: 'Primary Button',
  size: 'md',
};

export const Secondary = Template.bind({});
Secondary.args = {
  primary: false,
  label: 'Secondary Button',
  size: 'md',
};

export const Large = Template.bind({});
Large.args = {
    ...Secondary.args,
    size: 'lg',
    label: 'Large Button',
};

export const Small = Template.bind({});
Small.args = {
    ...Secondary.args,
    size: 'sm',
    label: 'Small Button',
};
