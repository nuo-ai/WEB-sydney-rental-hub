import React from 'react';
import Layout from '@theme/Layout';
import TokenPreview from '../components/TokenPreview';

export default function TokensPlayground() {
  return (
    <Layout title="Tokens Playground" description="SRH Design Tokens Playground">
      <main style={{padding: '24px 16px', maxWidth: 1200, margin: '0 auto'}}>
        <h1 style={{ marginTop: 0 }}>Tokens Playground</h1>
        <p style={{ color: '#666' }}>
          从左侧调整 Token，右侧预览卡片将实时更新。可复制 JSON 或 SCSS，回填到小程序/WEB 项目。
        </p>
        <TokenPreview />
      </main>
    </Layout>
  );
}
