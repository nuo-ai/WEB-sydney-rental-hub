const StyleDictionary = require('style-dictionary');
const fs = require('fs-extra');
const path = require('path');

console.log('Build started...');
console.log('==============================================');

// Clean previous build
const srcBuildPath = path.join(__dirname, '../../packages/ui/src/styles');
const distBuildPath = path.join(__dirname, '../../packages/ui/dist');

if (fs.existsSync(srcBuildPath)) {
  console.log(`\nCleaning old build files in ${srcBuildPath}`);
  fs.emptyDirSync(srcBuildPath);
}
if (fs.existsSync(distBuildPath)) {
    console.log(`\nCleaning old build files in ${distBuildPath}`);
    fs.emptyDirSync(distBuildPath);
}

// Get Style Dictionary Config
const myStyleDictionary = StyleDictionary.extend(path.join(__dirname, 'config.cjs'));

// Build all platforms
myStyleDictionary.buildAllPlatforms();

console.log('\n==============================================');
console.log('\nBuild completed!');
