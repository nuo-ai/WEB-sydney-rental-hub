// 设计令牌工具函数
import themeManager from './theme.js'

// 获取当前主题的令牌值
export const getTokenValue = (tokenName) => {
  const currentTheme = themeManager.getCurrentTheme()
  
  // 这里可以实现从生成的 WXSS 文件中获取令牌值的逻辑
  // 由于 WXSS 变量在运行时可以通过 getComputedStyle 获取
  // 我们可以提供一个便捷的方法来获取当前主题的令牌值
  
  try {
    // 创建一个临时元素来获取 CSS 变量值
    const tempElement = document.createElement('div')
    tempElement.style.display = 'none'
    document.body.appendChild(tempElement)
    
    const computedStyle = getComputedStyle(tempElement)
    const value = computedStyle.getPropertyValue(`--${tokenName}`).trim()
    
    document.body.removeChild(tempElement)
    
    return value || null
  } catch (error) {
    console.warn(`获取令牌值失败: ${tokenName}`, error)
    return null
  }
}

// 获取组件令牌值
export const getComponentToken = (component, property) => {
  return getTokenValue(`component-${component}-${property}`)
}

// 获取语义令牌值
export const getSemanticToken = (category, property) => {
  return getTokenValue(`color-semantic-${category}-${property}`)
}

// 获取基础令牌值
export const getBaseToken = (category, property) => {
  return getTokenValue(`color-${category}-${property}`)
}

// 获取字体令牌值
export const getFontToken = (property) => {
  return getTokenValue(`font-${property}`)
}

// 获取间距令牌值
export const getSpaceToken = (size) => {
  return getTokenValue(`space-${size}`)
}

// 获取圆角令牌值
export const getRadiusToken = (size) => {
  return getTokenValue(`radius-${size}`)
}

// 获取阴影令牌值
export const getShadowToken = (size) => {
  return getTokenValue(`shadow-${size}`)
}

// 导出所有常用的令牌获取方法
export default {
  get: getTokenValue,
  component: getComponentToken,
  semantic: getSemanticToken,
  base: getBaseToken,
  font: getFontToken,
  space: getSpaceToken,
  radius: getRadiusToken,
  shadow: getShadowToken
}
