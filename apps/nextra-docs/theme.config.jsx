export default {
  logo: 'SRH Tokens',
  project: {
    link: 'https://github.com/nuo-ai/WEB-sydney-rental-hub'
  },
  docsRepositoryBase:
    'https://github.com/nuo-ai/WEB-sydney-rental-hub/tree/main/apps/nextra-docs',
  useNextSeoProps() {
    return { titleTemplate: '%s – SRH Tokens' }
  },
  primaryHue: 20, // 近似品牌色 #E95420 的色相
  sidebar: {
    defaultMenuCollapseLevel: 1
  },
  footer: {
    text: 'SRH Tokens Docs'
  }
}
