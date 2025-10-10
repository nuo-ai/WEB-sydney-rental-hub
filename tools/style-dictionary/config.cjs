const path = require('path');

// 将路径统一为 POSIX 以兼容 fast-glob（避免 Windows 反斜杠导致的 glob 失效）
const toPosix = (p) => p.replace(/\\/g, '/');
const ROOT = path.resolve(__dirname, '../..');
const TOKENS_DIR = toPosix(path.join(ROOT, 'tokens'));
const DIST_DIR = toPosix(path.join(ROOT, 'packages/ui/dist'));
const SRC_DIR = toPosix(path.join(ROOT, 'packages/ui/src'));

module.exports = {
  source: [
    `${TOKENS_DIR}/base/**/*.json`,
    `${TOKENS_DIR}/themes/*.json`,
    `${TOKENS_DIR}/components/**/*.json`,
  ],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: `${SRC_DIR}/styles/`,
      files: [
        {
          destination: 'tokens.css',
          format: 'css/variables',
          options: {
            outputReferences: true
          }
        }
      ]
    },
    json: {
      transformGroup: 'js',
      buildPath: `${DIST_DIR}/style-dictionary/json/`,
      files: [
        {
          destination: 'tokens.json',
          format: 'json/nested'
        }
      ]
    },
    ts: {
      transformGroup: 'js',
      buildPath: `${DIST_DIR}/style-dictionary/ts/`,
      files: [
        {
          destination: 'types.ts',
          format: 'typescript/module-declarations'
        }
      ]
    }
  }
};
