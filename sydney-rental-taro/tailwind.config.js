/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./public/index.html",
    "./src/**/*.{html,js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#e4002b',      // Domain Red: 主品牌色，用于关键操作按钮、高亮状态
        action: '#0073e6',       // Interactive Blue: 交互蓝色，用于链接、次级按钮和可点击元素
        'grey-darkest': '#1d2f38', // 用于正文标题
        'grey-darker': '#334854',  // 用于次级标题、正文文本
        'grey-dark': '#697684',   // 用于辅助性文本、图标
        'grey-base': '#c5c9d1',    // 用于边框、分割线
        'grey-light': '#e5e7eb',   // 用于输入框、卡片背景
        'grey-lighter': '#f2f3f5',  // 用于页面背景、悬浮状态背景
        'grey-lightest': '#f8f9fa', // 用于最浅的背景层
      },
      fontSize: {
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],    // 36px
        '2xl': ['1.5rem', { lineHeight: '2rem' }],      // 24px
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],   // 20px
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],  // 18px
        'base': ['1rem', { lineHeight: '1.5rem' }],       // 16px
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],  // 14px
        'xs': ['0.75rem', { lineHeight: '1rem' }],      // 12px
      },
      borderRadius: {
        'sm': '2px',
        'DEFAULT': '4px',
        'md': '8px',
        'lg': '12px',
      },
      boxShadow: {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'DEFAULT': '0 2px 4px 0 rgba(29, 47, 56, 0.16)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      }
    },
  },
  plugins: [],
}
