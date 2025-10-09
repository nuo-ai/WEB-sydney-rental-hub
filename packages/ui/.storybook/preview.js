import { setup } from '@storybook/vue3';
import '../../apps/mini-program/src/styles/generated/light.wxss';
import '../../apps/mini-program/src/styles/generated/dark.wxss';

// 设置全局装饰器
export const decorators = [
  (story, context) => {
    const theme = context.globals.theme || 'light';
    return {
      template: `<div class="${theme}-theme" style="padding: 20px;"><story/></div>`
    };
  }
];

// 全局类型配置
export const globalTypes = {
  theme: {
    name: 'Theme',
    description: 'Global theme for components',
    defaultValue: 'light',
    toolbar: {
      icon: 'circlehollow',
      items: [
        { value: 'light', title: 'Light' },
        { value: 'dark', title: 'Dark' }
      ],
      showName: true
    }
  }
};

// 参数配置
const preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    a11y: {
      test: "todo"
    },
    viewport: {
      viewports: {
        mobile1: { name: 'Mobile 1', styles: { width: '320px', height: '568px' } },
        mobile2: { name: 'Mobile 2', styles: { width: '375px', height: '667px' } },
        tablet: { name: 'Tablet', styles: { width: '768px', height: '1024px' } },
      }
    }
  },
};

export default preview;
