import BaseCard from './BaseCard.vue';

export default {
  title: 'Components/BaseCard',
  component: BaseCard,
  parameters: {
    layout: 'centered',
  },
};

const Template = (args) => ({
  components: { BaseCard },
  setup() {
    return { args };
  },
  template: `
    <BaseCard style="width: 320px;">
      <div style="font-family: sans-serif; color: #333;">
        <h3 style="margin-top: 0; margin-bottom: 8px;">卡片标题</h3>
        <p style="margin: 0;">这是卡片的内容区域。您可以放入任何自定义 HTML 或 Vue 组件。</p>
      </div>
    </BaseCard>
  `,
});

export const Default = Template.bind({});
Default.storyName = '默认卡片';
