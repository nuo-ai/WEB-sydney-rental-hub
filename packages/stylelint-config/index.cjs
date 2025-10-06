const baseConfig = {
  customSyntax: 'postcss-html',
  extends: ['stylelint-config-standard'],
  plugins: ['stylelint-declaration-strict-value'],
  rules: {
    'color-named': null,
    'color-no-hex': null,
    'scale-unlimited/declaration-strict-value': null,
    'selector-pseudo-class-no-unknown': [
      true,
      {
        ignorePseudoClasses: ['deep', 'global']
      }
    ],
    'selector-class-pattern': null,
    'declaration-property-value-no-unknown': null,
    'declaration-property-value-disallowed-list': null
  }
};

module.exports = baseConfig;
