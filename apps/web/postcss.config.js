/** PostCSS config for apps/web
 * 启用 tailwindcss 与 autoprefixer
 * - Tailwind v4：通过 @import "tailwindcss/..." 在 CSS 中引入
 * - 我们仅引入 utilities，避免 preflight 重置影响 Element Plus
 */
export default {
  plugins: {
    '@tailwindcss/postcss': {},
    autoprefixer: {}
  }
}
