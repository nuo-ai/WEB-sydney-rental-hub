import { defineConfig, globalIgnores } from 'eslint/config';
import js from '@eslint/js';
import pluginVue from 'eslint-plugin-vue';
import globals from 'globals';
import skipFormatting from '@vue/eslint-config-prettier/skip-formatting';
import tsParser from '@typescript-eslint/parser';
import vueParser from 'vue-eslint-parser';

const ignores = ['**/dist/**', '**/dist-ssr/**', '**/coverage/**', '**/node_modules/**', '**/*.config.cjs'];

export default defineConfig([
  {
    files: ['**/*.{js,mjs,jsx,ts,tsx,vue}'],
  },
  globalIgnores(ignores),
  js.configs.recommended,
  ...pluginVue.configs['flat/essential'],
  {
    languageOptions: {
      parser: vueParser,
      parserOptions: {
        parser: tsParser,
        ecmaVersion: 'latest',
        sourceType: 'module'
      },
      globals: {
        ...globals.browser,
        google: 'readonly',
      },
    },
  },
  skipFormatting,
]);
