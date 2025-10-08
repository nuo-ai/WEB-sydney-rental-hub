

import { join, dirname } from "path"
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
    "../src/components/**/*.stories.js"
  ],
  "addons": [
    getAbsolutePath('@chromatic-com/storybook'),
    getAbsolutePath('@storybook/addon-docs'),
    getAbsolutePath("@storybook/addon-a11y"),
    getAbsolutePath("@storybook/addon-vitest")
  ],
  "framework": {
    "name": getAbsolutePath('@storybook/vue3-vite'),
    "options": {}
  },
  async viteFinal(config) {
    // Add the vue plugin to the vite config.
    config.plugins = config.plugins ?? [];
    config.plugins.push(vue());
    return config;
  },
};
export default config;
