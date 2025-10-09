// 主题管理工具
class ThemeManager {
  constructor() {
    this.currentTheme = 'light'
    this.themeChangeCallbacks = []
  }

  // 初始化主题
  init() {
    // 从本地存储获取主题设置
    const savedTheme = uni.getStorageSync('theme')
    if (savedTheme) {
      this.currentTheme = savedTheme
    }
    
    // 应用主题
    this.applyTheme(this.currentTheme)
    
    // 监听系统主题变化
    this.watchSystemTheme()
  }

  // 应用主题
  applyTheme(theme) {
    this.currentTheme = theme
    
    // 保存到本地存储
    uni.setStorageSync('theme', theme)
    
    // 更新页面根元素类名
    const pages = getCurrentPages()
    if (pages.length > 0) {
      const currentPage = pages[pages.length - 1]
      const pageInstance = currentPage.$vm
      if (pageInstance && pageInstance.$el) {
        // 移除旧主题类名
        pageInstance.$el.classList.remove('theme-light', 'theme-dark')
        // 添加新主题类名
        pageInstance.$el.classList.add(`theme-${theme}`)
      }
    }
    
    // 触发回调
    this.themeChangeCallbacks.forEach(callback => callback(theme))
  }

  // 切换主题
  toggleTheme() {
    const newTheme = this.currentTheme === 'light' ? 'dark' : 'light'
    this.applyTheme(newTheme)
  }

  // 设置主题
  setTheme(theme) {
    if (theme === 'light' || theme === 'dark') {
      this.applyTheme(theme)
    }
  }

  // 获取当前主题
  getCurrentTheme() {
    return this.currentTheme
  }

  // 监听系统主题变化
  watchSystemTheme() {
    // UniApp 获取系统主题
    uni.onThemeChange((res) => {
      console.log('系统主题变化:', res.theme)
      // 可以选择是否跟随系统主题
      // this.applyTheme(res.theme)
    })
  }

  // 添加主题变化回调
  onThemeChange(callback) {
    this.themeChangeCallbacks.push(callback)
  }

  // 移除主题变化回调
  offThemeChange(callback) {
    const index = this.themeChangeCallbacks.indexOf(callback)
    if (index > -1) {
      this.themeChangeCallbacks.splice(index, 1)
    }
  }
}

// 创建单例
const themeManager = new ThemeManager()

// 导出实例
export default themeManager

// 导出便捷方法
export const useTheme = () => {
  return {
    theme: themeManager.getCurrentTheme(),
    toggleTheme: () => themeManager.toggleTheme(),
    setTheme: (theme) => themeManager.setTheme(theme),
    onThemeChange: (callback) => themeManager.onThemeChange(callback),
    offThemeChange: (callback) => themeManager.offThemeChange(callback)
  }
}
