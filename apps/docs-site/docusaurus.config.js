/* eslint-disable no-undef */
const config = {
  title: 'SRH Design',
  tagline: 'Design Tokens & Components',
  url: 'https://srh.local',
  baseUrl: '/',
  organizationName: 'srh',
  projectName: 'docs-site',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  i18n: {
    defaultLocale: 'zh-CN',
    locales: ['zh-CN', 'en'],
  },
  presets: [
    [
      'classic',
      ({
        docs: false,
        blog: false,
        theme: {
          // 可按需添加自定义样式文件
          // customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],
  themeConfig: {
    navbar: {
      title: 'SRH Design',
      items: [
        { to: '/tokens', label: 'Tokens Playground', position: 'left' },
        { to: '/components', label: 'Components', position: 'left' },
        { to: '/', label: '首页', position: 'left' },
      ],
    },
    footer: {
      style: 'dark',
      copyright: `© ${new Date().getFullYear()} Sydney Rental Hub`,
    },
  },
};

module.exports = config;
