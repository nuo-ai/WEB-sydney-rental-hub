

import { join, dirname } from "path";
import { fileURLToPath, URL } from "node:url";
import vue from '@vitejs/plugin-vue';

/** @type { import('@storybook/vue3-vite').StorybookConfig } */
const config = {
  "stories": [
    "../src/stories/**/*.mdx",
    "../src/components/**/*.stories.js"
  ],
  "addons": [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    '@chromatic-com/storybook',
    '@storybook/addon-docs',
    "@storybook/addon-a11y"
  ],
  core: {
    builder: '@storybook/builder-vite',
  },
  "framework": {
    "name": '@storybook/vue3-vite',
    "options": {}
  },
  docs: {
    source: {
      type: 'code', // Renders the source code block as an editable field.
    },
  },
  async viteFinal(config) {
    const { mergeConfig } = await import('vite');
    
    config.plugins = config.plugins ?? [];
    config.plugins.push(vue());

    return mergeConfig(config, {
      resolve: {
        alias: {
          "@": fileURLToPath(new URL("../src", import.meta.url)),
        },
      },
      optimizeDeps: {
        include: ['@storybook/blocks'],
      },
    });
  },
};
export default config;
