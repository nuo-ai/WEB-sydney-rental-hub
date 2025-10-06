const baseConfig = require('@web-sydney/stylelint-config');

module.exports = {
  ...baseConfig,
  overrides: [
    {
      files: ['src/styles/design-tokens.css', 'src/style.css'],
      rules: {
        'color-no-hex': null,
        'declaration-property-value-disallowed-list': null
      }
    },
    {
      files: ['src/**/*.vue'],
      rules: {
        'color-no-hex': [true, { severity: 'warning' }],
        'color-named': ['never', { severity: 'warning' }],
        'scale-unlimited/declaration-strict-value': [
          [
            '/color/',
            'fill',
            'stroke',
            'background',
            'background-color',
            'border',
            'border-color',
            'box-shadow',
            'outline',
            'outline-color'
          ],
          { ignoreValues: ['transparent', 'currentColor', 'currentcolor', 'inherit', 'none'] }
        ]
      }
    }
  ]
};
