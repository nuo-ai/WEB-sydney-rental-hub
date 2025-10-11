import React, { useEffect, useState } from 'react';
import Layout from '@theme/Layout';
import Card from '../components/Card';

export default function ComponentsGallery() {
  const [tokens, setTokens] = useState(null);

  useEffect(() => {
    fetch('/tokens/srh.json', { cache: 'no-store' })
      .then(r => r.json())
      .then(setTokens)
      .catch(() => {
        setTokens({
          colorTextPrimary: '#3d3b40',
          colorTextSecondary: '#3d3b40',
          cardBg: '#ffffff',
          shadow: '0 1px 4px 0 rgba(0,0,0,0.16)',
          space2xs: 4, spaceXs: 8, spaceSm: 12, spaceMd: 16, spaceLg: 20,
          radiusSm: 6, radiusMd: 8,
          fontSizePrice: 20, lineHeightPrice: 28,
          fontSizeAddress: 16, lineHeightAddress: 24,
          fontSizeInspection: 14, lineHeightInspection: 20,
          metaIconSize: 16, metaGap: 8,
          buttonSize: 40, imageAspect: 0.75
        });
      });
  }, []);

  if (!tokens) return (
    <Layout title="Components" description="SRH Components Gallery">
      <main style={{padding: '24px 16px', maxWidth: 1200, margin: '0 auto'}}>加载中…</main>
    </Layout>
  );

  const row = {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))',
    gap: 16
  };

  return (
    <Layout title="Components" description="SRH Components Gallery">
      <main style={{padding: '24px 16px', maxWidth: 1200, margin: '0 auto'}}>
        <h1 style={{ marginTop: 0 }}>Components</h1>
        <p style={{ color: '#666' }}>
          常见卡片状态对照，用于检查 token 对不同场景的适配性。
        </p>

        <h2 style={{ marginTop: 24, fontSize: 18 }}>标签状态（badges/labels）</h2>
        <div style={row}>
          <Card tokens={tokens} label={null} />
          <Card tokens={tokens} label="Inspection today 2:15pm" />
          <Card tokens={tokens} label="Added yesterday" />
          <Card tokens={tokens} label="Deposit taken" />
          <Card tokens={tokens} label="Build to Rent" />
        </div>

        <h2 style={{ marginTop: 32, fontSize: 18 }}>Meta 组合（bed/bath/car/study 等）</h2>
        <div style={row}>
          <Card tokens={tokens} meta={['1 Bed', '1 Bath']} />
          <Card tokens={tokens} meta={['2 Bed', '1 Bath', '1 Car']} />
          <Card tokens={tokens} meta={['3 Bed', '2 Bath', '2 Car', 'Study']} />
          <Card tokens={tokens} meta={['Studio', '1 Bath']} />
        </div>

        <h2 style={{ marginTop: 32, fontSize: 18 }}>地址与价格长度</h2>
        <div style={row}>
          <Card tokens={tokens} price="$650 pw" address="1 Short St, Sydney NSW" />
          <Card tokens={tokens} price="$1,200 pw" address="101/123-125 Very Long Address Road, Alexandria NSW 2015" />
          <Card tokens={tokens} price="$980 pw" address="Apt 9, 55 Example Ave, Zetland NSW 2017" />
        </div>
      </main>
    </Layout>
  );
}
