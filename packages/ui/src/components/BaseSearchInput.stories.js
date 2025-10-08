import BaseSearchInput from './BaseSearchInput.vue';

export default {
  title: 'Components/BaseSearchInput',
  component: BaseSearchInput,
  argTypes: {
    modelValue: { control: 'text' },
    placeholder: { control: 'text' },
    clearable: { control: 'boolean' },
    disabled: { control: 'boolean' },
    autofocus: { control: 'boolean' },
  },
};

const Template = (args) => ({
  components: { BaseSearchInput },
  setup() {
    return { args };
  },
  template: `
    <div style="max-width: 320px;">
      <BaseSearchInput v-bind="args" />
    </div>
  `,
});

export const Default = Template.bind({});
Default.args = {
  placeholder: 'Search...',
};

export const Disabled = Template.bind({});
Disabled.args = {
  modelValue: 'Disabled input',
  disabled: true,
};

export const NotClearable = Template.bind({});
NotClearable.args = {
  modelValue: 'Not clearable',
  clearable: false,
};
