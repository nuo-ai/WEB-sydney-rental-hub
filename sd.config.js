/**
 * Style Dictionary config
 */
module.exports = {
  source: ['tokens/design-tokens.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'packages/ui/dist/',
      files: [
        {
          destination: 'tokens.css',
          format: 'css/variables',
          options: {
            outputReferences: true,
          },
        },
      ],
    },
    js: {
      transformGroup: 'js',
      buildPath: 'packages/ui/dist/',
      files: [
        {
          destination: 'tokens.mjs',
          format: 'javascript/es6',
        },
        {
            destination: 'tokens.d.ts',
            format: 'typescript/es6-declarations'
        }
      ],
    },
  },
};
