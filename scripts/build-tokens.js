const StyleDictionary = require('style-dictionary').default;
const fs = require('fs');
const path = require('path');

console.log(`Build started at: ${new Date().toISOString()}`);
console.log('\\n==============================================');

// Register custom format for wxss files with single-line comments
StyleDictionary.registerFormat({
  name: 'wxss/variables',
  format: function({ dictionary, options }) {
    const header = '/* Do not edit directly, this file was auto-generated. */\n\n';
    const selector = options.selector || ':root';
    
    let output = header;
    output += `${selector} {\n`;
    
    dictionary.allTokens.forEach(function(token) {
      output += `  --${token.name}: ${token.value};\n`;
    });
    
    output += '}\n';
    return output;
  }
});

// Register custom transform for rpx units with better error handling
StyleDictionary.registerTransform({
  name: 'size/pxToRpx',
  type: 'value',
  transitive: true,
  matcher: function(token) {
    // 只处理 dimension, sizing, spacing, borderRadius, fontSizes 类型的 px 值
    const sizeTypes = ['dimension', 'sizing', 'spacing', 'borderRadius', 'fontSizes'];
    return sizeTypes.includes(token.type) && 
           typeof token.value === 'string' && 
           token.value.endsWith('px');
  },
  transform: function(token) {
    try {
      const value = parseFloat(token.value.replace('px', ''));
      if (isNaN(value)) {
        return token.value;
      }
      return `${value * 2}rpx`;
    } catch (error) {
      return token.value;
    }
  }
});

// Register transform for line-height (keep as number)
StyleDictionary.registerTransform({
  name: 'lineHeight/number',
  type: 'value',
  transitive: true,
  matcher: function(token) {
    return token.type === 'lineHeight' && 
           typeof token.value === 'string' && 
           token.value.endsWith('px');
  },
  transform: function(token) {
    try {
      const value = parseFloat(token.value.replace('px', ''));
      if (isNaN(value)) {
        return token.value;
      }
      return value.toString();
    } catch (error) {
      return token.value;
    }
  }
});

// Register transform for font weights (keep as number)
StyleDictionary.registerTransform({
  name: 'fontWeight/number',
  type: 'value',
  transitive: true,
  matcher: function(token) {
    return token.type === 'fontWeight' && 
           typeof token.value === 'string' && 
           token.value.endsWith('px');
  },
  transform: function(token) {
    try {
      const value = parseFloat(token.value.replace('px', ''));
      if (isNaN(value)) {
        return token.value;
      }
      return value.toString();
    } catch (error) {
      return token.value;
    }
  }
});

// 添加增量构建检查
function getSourceFileHashes() {
  const sources = ['tokens/base/**/*.json', 'tokens/themes/*.json', 'tokens/components/**/*.json'];
  const hashes = {};
  // 简化实现，实际项目中可以使用 crypto 模块计算文件哈希
  return hashes;
}

function shouldRebuild() {
  // 检查源文件是否发生变化
  // 简化实现，总是返回 true
  return true;
}

function getStyleDictionaryConfig(theme) {
  return {
    "source": [
      `tokens/base/**/*.json`,
      `tokens/themes/${theme}.json`,
      `tokens/components/**/*.json`  // 添加组件令牌支持
    ],
    "platforms": {
      "wxss": {
        "transforms": ['attribute/cti', 'name/kebab', 'size/pxToRpx', 'lineHeight/number', 'fontWeight/number', 'color/css'],
        "buildPath": `apps/mini-program/src/styles/generated/`,
        "files": [{
          "destination": `${theme}.wxss`,
          "format": "wxss/variables",
          "options": {
            "selector": `.${theme}-theme`
          }
        }]
      },
      "css": {
        "transforms": ['attribute/cti', 'name/kebab', 'color/css'],
        "buildPath": `packages/ui/src/styles/`,
        "files": [{
          "destination": theme === 'light' ? `tokens.css` : `tokens.dark.css`,
          "format": "css/variables",
          "options": {
            "outputReferences": true,
            "selector": theme === 'light' ? `:root` : `[data-theme='dark']`
          }
        }]
      },
      "json": {
        "transformGroup": "js",
        "buildPath": `packages/ui/dist/style-dictionary/json/`,
        "files": [{
          "destination": "tokens.json",
          "format": "json/nested"
        }]
      },
      "ts": {
        "transformGroup": "js",
        "buildPath": `packages/ui/dist/`,
        "files": [{
          "destination": "tokens.mjs",
          "format": "javascript/es6"
        }]
      }
    }
  };
}

// 生成构建报告
function generateBuildReport(startTime, results) {
  const endTime = new Date();
  const duration = endTime - startTime;
  
  console.log('\\n=== Build Report ===');
  console.log(`Themes processed: ${Object.keys(results).length}`);
  console.log(`Files generated: ${Object.values(results).flat().length}`);
  console.log(`Build duration: ${duration}ms`);
  console.log(`Build completed at: ${endTime.toISOString()}`);
}

// 主构建函数
async function buildTokens() {
  const startTime = new Date();
  const results = {};
  
  if (!shouldRebuild()) {
    console.log('No changes detected, skipping build...');
    return;
  }

  console.log('Processing Light theme...');
  const sdLight = new StyleDictionary(getStyleDictionaryConfig('light'));
  await sdLight.buildAllPlatforms();
  results.light = ['light.wxss'];

  console.log('Processing Dark theme...');
  const sdDark = new StyleDictionary(getStyleDictionaryConfig('dark'));
  await sdDark.buildAllPlatforms();
  results.dark = ['dark.wxss'];

  generateBuildReport(startTime, results);
}

buildTokens().catch(error => {
  console.error('Build failed:', error);
  process.exit(1);
});
