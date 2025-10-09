const StyleDictionary = require('style-dictionary').default;
const fs = require('fs');
const path = require('path');

function getStyleDictionaryConfig(theme) {
  return {
    "source": [
      `tokens/base/**/*.json`,
      `tokens/themes/${theme}.json`,
      `tokens/components/**/*.json`
    ],
    "platforms": {
      "wxss": {
        "transforms": ['attribute/cti', 'name/kebab', 'size/pxToRpx', 'lineHeight/number', 'fontWeight/number', 'color/css'],
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

// 测试配置
console.log('Testing Light theme configuration...');
try {
  const config = getStyleDictionaryConfig('light');
  console.log('Configuration loaded successfully');
  console.log('Source files:', config.source);
  
  const sd = new StyleDictionary(config);
  console.log('StyleDictionary instance created');
  
  // 尝试获取令牌
  console.log('Getting tokens...');
  const tokens = sd.tokens;
  console.log('Tokens retrieved successfully');
  
} catch (error) {
  console.error('Error:', error);
}
