/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // 统一以 CSS 变量驱动主题色，便于暗色/品牌切换
        primary: {
          DEFAULT: "var(--color-primary)",
          foreground: "var(--color-primary-foreground)",
        },
        background: "var(--color-background)",
        foreground: "var(--color-foreground)",
        muted: "var(--color-muted)",
        "muted-foreground": "var(--color-muted-foreground)",
        border: "var(--color-border)",
        panel: "var(--color-panel)",
        selected: "var(--color-selected)",
      },
      maxWidth: {
        // 移动端容器规范
        mobile: "420px",
      },
      zIndex: {
        // 分层口径：Dialog/Sheet > Header > TabBar > 内容
        sheet: "50",
        header: "40",
        tabbar: "30",
      },
      boxShadow: {
        card: "0 2px 8px rgba(0,0,0,0.08)",
      },
      borderRadius: {
        "sheet-top": "1rem", // 底部弹层顶部圆角
      },
    },
  },
  plugins: [],
}
