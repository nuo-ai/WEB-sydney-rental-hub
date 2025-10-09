const StyleDictionary = require('style-dictionary').default;

console.log('Build started...');
console.log('\\n==============================================');

// Register custom transform for rpx units
StyleDictionary.registerTransform({
  name: 'size/pxToRpx',
  type: 'value',
  transitive: true,
  matcher: function(token) {
    // 只转换尺寸、间距、半径等数值类型的 px 单位
    const sizeTypes = ['dimension', 'sizing', 'spacing', 'borderRadius', 'fontSizes'];
    return sizeTypes.includes(token.type) && typeof token.value === 'string' && token.value.endsWith('px');
  },
  transform: function(token) {
    const value = parseInt(token.value.replace('px', ''), 10);
    if (isNaN(value)) {
      console.error('Invalid px value:', token.value, 'for token:', token.name);
      return token.value; // 返回原始值
    }
    return `${value * 2}rpx`;
  }
});

function getStyleDictionaryConfig(theme) {
  return {
    "source": [
      `tokens/base/**/*.json`,
      `tokens/themes/${theme}.json`
    ],
    "platforms": {
      "wxss": {
        "transforms": ['attribute/cti', 'name/kebab', 'size/pxToRpx', 'color/css'],
        "buildPath": `apps/mini-program/src/styles/generated/`,
        "files": [{
          "destination": `${theme}.wxss`,
          "format": "css/variables",
          "options": {
            "selector": `.${theme}-theme`
          }
        }]
      }
    }
  };
}

console.log('Processing Light theme...');
const sdLight = new StyleDictionary(getStyleDictionaryConfig('light'));
sdLight.buildAllPlatforms();

console.log('Processing Dark theme...');
const sdDark = new StyleDictionary(getStyleDictionaryConfig('dark'));
sdDark.buildAllPlatforms();

console.log('\\n==============================================');
console.log('\\nBuild completed!');
