const fs = require('fs');
const path = require('path');

// 读取所有令牌文件
const baseFiles = [
  'tokens/base/color/brand.json',
  'tokens/base/color/neutral.json',
  'tokens/base/size/space.json',
  'tokens/base/font.json',
  'tokens/base/layout.json',
  'tokens/base/radius.json',
  'tokens/base/shadow.json'
];

const themeFiles = [
  'tokens/themes/light.json',
  'tokens/themes/dark.json'
];

const componentFiles = [
  'tokens/components/button.json',
  'tokens/components/card.json',
  'tokens/components/input.json'
];

function readTokensFromFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(content);
  } catch (error) {
    console.error(`Error reading ${filePath}:`, error.message);
    return {};
  }
}

function flattenTokens(obj, prefix = '') {
  const flattened = {};
  
  function flatten(current, keyPrefix) {
    if (typeof current === 'object' && current !== null && !Array.isArray(current)) {
      if (current.value !== undefined) {
        flattened[keyPrefix] = current;
      } else {
        Object.keys(current).forEach(key => {
          const newPrefix = keyPrefix ? `${keyPrefix}.${key}` : key;
          flatten(current[key], newPrefix);
        });
      }
    }
  }
  
  flatten(obj, prefix);
  return flattened;
}

// 收集所有令牌
const allTokens = {};

// 读取基础令牌
baseFiles.forEach(file => {
  const tokens = readTokensFromFile(file);
  Object.assign(allTokens, flattenTokens(tokens));
});

// 读取主题令牌
themeFiles.forEach(file => {
  const tokens = readTokensFromFile(file);
  Object.assign(allTokens, flattenTokens(tokens));
});

// 读取组件令牌
componentFiles.forEach(file => {
  const tokens = readTokensFromFile(file);
  Object.assign(allTokens, flattenTokens(tokens));
});

console.log(`Total tokens loaded: ${Object.keys(allTokens).length}`);

// 查找引用的令牌
function findReferences(tokens) {
  const references = new Set();
  
  Object.keys(tokens).forEach(key => {
    const token = tokens[key];
    if (token.value && typeof token.value === 'string') {
      const matches = token.value.match(/\{([^}]+)\}/g);
      if (matches) {
        matches.forEach(match => {
          const ref = match.slice(1, -1); // 移除大括号
          if (!allTokens[ref]) {
            references.add({ token: key, reference: ref });
          }
        });
      }
    }
  });
  
  return Array.from(references);
}

const missingReferences = findReferences(allTokens);

console.log(`\nMissing token references found: ${missingReferences.length}`);
missingReferences.forEach(ref => {
  console.log(`  Token "${ref.token}" references missing token "${ref.reference}"`);
});

// 显示所有碰撞的令牌
console.log('\n=== Checking for token collisions ===');
const tokenNames = Object.keys(allTokens);
const nameGroups = {};

tokenNames.forEach(name => {
  const baseName = name.replace(/\.[^.]+$/, ''); // 移除最后的属性名
  if (!nameGroups[baseName]) {
    nameGroups[baseName] = [];
  }
  nameGroups[baseName].push(name);
});

const collisions = [];
Object.keys(nameGroups).forEach(baseName => {
  if (nameGroups[baseName].length > 1) {
    collisions.push({
      base: baseName,
      tokens: nameGroups[baseName]
    });
  }
});

console.log(`Token collisions found: ${collisions.length}`);
collisions.forEach(collision => {
  console.log(`  Collision group: ${collision.base}`);
  collision.tokens.forEach(token => {
    console.log(`    - ${token}`);
  });
});

// 验证组件令牌引用
console.log('\n=== Component Token References ===');
const componentTokens = {};
componentFiles.forEach(file => {
  const tokens = readTokensFromFile(file);
  Object.assign(componentTokens, flattenTokens(tokens));
});

const componentReferences = findReferences(componentTokens);
if (componentReferences.length > 0) {
  console.log('Component tokens with missing references:');
  componentReferences.forEach(ref => {
    console.log(`  ${ref.token} -> ${ref.reference}`);
  });
} else {
  console.log('All component token references are valid!');
}
