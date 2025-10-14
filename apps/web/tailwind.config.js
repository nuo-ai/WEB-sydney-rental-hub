/** Tailwind config for apps/web
 * 注意：
 * - 关闭 preflight，避免重置样式干扰 Element Plus
 * - 支持暗色触发：class 与 [data-theme="dark"]（与现有切换逻辑兼容）
 * - 布局/排版刻度（spacing/fontSize/screens）可按需扩展
 */
export default {
  darkMode: ['class', '[data-theme="dark"]'],
  corePlugins: {
    preflight: false
  },
  content: [
    './index.html',
    './src/**/*.{js,ts,vue,jsx,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: 'hsl(var(--primary))',
        secondary: 'hsl(var(--secondary))',
        muted: 'hsl(var(--muted))',
        accent: 'hsl(var(--accent))',
        destructive: 'hsl(var(--destructive))',
        border: 'hsl(var(--border))',
        ring: 'hsl(var(--ring))'
      },
      fontFamily: {
        sans: 'var(--font-sans)'
      },
      borderRadius: {
        DEFAULT: 'var(--radius)',
        lg: 'calc(var(--radius) + 2px)',
        md: 'var(--radius)',
        sm: 'calc(var(--radius) - 2px)'
      },
      // 可按需扩展：spacing / fontSize / boxShadow / zIndex / container 等
      spacing: {
        '1': '4px',
        '2': '8px',
        '3': '12px',
        '4': '16px',
        '5': '20px',
        '6': '24px'
      }
    }
  },
  plugins: []
}
