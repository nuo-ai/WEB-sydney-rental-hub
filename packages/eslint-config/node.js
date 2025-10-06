import { defineConfig, globalIgnores } from 'eslint/config';
import js from '@eslint/js';
import globals from 'globals';
import skipFormatting from '@vue/eslint-config-prettier/skip-formatting';
import tsParser from '@typescript-eslint/parser';

const ignores = ['**/dist/**', '**/build/**', '**/coverage/**', '**/node_modules/**'];

export default defineConfig([
  {
    files: ['**/*.{js,mjs,cjs,ts,tsx}'],
  },
  globalIgnores(ignores),
  js.configs.recommended,
  {
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module'
      },
      globals: {
        ...globals.node,
      },
    },
  },
  skipFormatting,
]);
