import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

export default function Home() {
  return (
    <Layout title="SRH Design" description="Design Tokens & Components">
      <main style={{padding: '32px 16px', maxWidth: 960, margin: '0 auto'}}>
        <section style={{marginBottom: 32}}>
          <h1 style={{margin: 0}}>SRH Design</h1>
          <p style={{color: '#666', marginTop: 8}}>
            设计 Token 与组件预览站点（Docusaurus）。用于快速调参、导出与对齐小程序/WEB 风格。
          </p>
          <div style={{marginTop: 16, display: 'flex', gap: 12}}>
            <Link className="button button--primary" to="/tokens">
              打开 Tokens Playground
            </Link>
          </div>
        </section>

        <section>
          <h2>说明</h2>
          <ul>
            <li>Tokens Playground：可加载初始 tokens（static/tokens/srh.json），实时调整并导出 JSON。</li>
            <li>组件预览：内置房源卡片示例（价格、地址、meta、Inspection、收藏按钮）。</li>
            <li>输出闭环：将导出 JSON 回填到 uni.scss 的 $srh-* 或生成 CSS Variables。</li>
          </ul>
        </section>
      </main>
    </Layout>
  );
}
