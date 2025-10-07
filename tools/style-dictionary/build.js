const StyleDictionary = require('style-dictionary');
const fs = require('fs-extra');
const path = require('path');

console.log('Build started...');
console.log('==============================================');

// Clean previous build
const buildPath = path.join(__dirname, '../../vue-frontend/src/generated-tokens');
if (fs.existsSync(buildPath)) {
  console.log(`\nCleaning old build files in ${buildPath}`);
  fs.rmSync(buildPath, { recursive: true, force: true });
}

// Get Style Dictionary Config
const myStyleDictionary = StyleDictionary.extend(path.join(__dirname, 'config.cjs'));

// Build all platforms
myStyleDictionary.buildAllPlatforms();

console.log('\n==============================================');
console.log('\nBuild completed!');
