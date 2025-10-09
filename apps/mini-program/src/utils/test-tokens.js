// 测试令牌系统是否正常工作
import themeManager from './theme.js'
import { getTokens } from './tokens.js'

// 测试主题切换
console.log('=== 令牌系统测试 ===')
console.log('当前主题:', themeManager.getCurrentTheme())
console.log('Light 主题令牌:', getTokens('light'))
console.log('Dark 主题令牌:', getTokens('dark'))

// 测试主题切换
console.log('\\n=== 主题切换测试 ===')
themeManager.setTheme('dark')
console.log('切换后主题:', themeManager.getCurrentTheme())

themeManager.setTheme('light')
console.log('切换回 Light:', themeManager.getCurrentTheme())
