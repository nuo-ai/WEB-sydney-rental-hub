

import { join, dirname } from "path";
import { fileURLToPath, URL } from "node:url";
import vue from '@vitejs/plugin-vue';

/**
* This function is used to resolve the absolute path of a package.
* It is needed in projects that use Yarn PnP or are set up within a monorepo.
*/
function getAbsolutePath(value) {
  return dirname(require.resolve(join(value, 'package.json')))
}

/** @type { import('@storybook/vue3-vite').StorybookConfig } */
const config = {
  "stories": [
    "../src/stories/**/*.mdx",
    "../src/components/**/*.stories.js"
  ],
  "addons": [
    getAbsolutePath('@chromatic-com/storybook'),
    getAbsolutePath('@storybook/addon-docs'),
    getAbsolutePath("@storybook/addon-a11y")
  ],
  core: {
    builder: '@storybook/builder-vite',
  },
  "framework": {
    "name": getAbsolutePath('@storybook/vue3-vite'),
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
