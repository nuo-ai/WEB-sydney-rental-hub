import BaseListItem from './BaseListItem.vue';
import { ChevronRight, Mail } from 'lucide-vue-next';

export default {
  title: 'Components/BaseListItem',
  component: BaseListItem,
  argTypes: {
    selected: { control: 'boolean' },
    disabled: { control: 'boolean' },
    clickable: { control: 'boolean' },
    bordered: { control: 'boolean' },
  },
};

const Template = (args) => ({
  components: { BaseListItem },
  setup() {
    return { args };
  },
  template: `
    <BaseListItem v-bind="args">
      List Item Title
      <template #description>Description for the list item</template>
    </BaseListItem>
  `,
});

export const Default = Template.bind({});
Default.args = {};

export const WithSlots = (args) => ({
  components: { BaseListItem, ChevronRight, Mail },
  setup() {
    return { args };
  },
  template: `
    <div style="max-width: 320px;">
      <BaseListItem>
        <template #prefix><Mail /></template>
        List Item with Prefix
        <template #description>Description text</template>
        <template #suffix><ChevronRight /></template>
      </BaseListItem>
      <BaseListItem selected>
        <template #prefix><Mail /></template>
        Selected Item
        <template #description>This item is selected</template>
        <template #suffix><ChevronRight /></template>
      </BaseListItem>
      <BaseListItem disabled>
        <template #prefix><Mail /></template>
        Disabled Item
        <template #description>This item is disabled</template>
        <template #suffix><ChevronRight /></template>
      </BaseListItem>
    </div>
  `,
});
