import React, { useEffect, useMemo, useState } from 'react';

const numberKeysPx = [
  'space2xs', 'spaceXs', 'spaceSm', 'spaceMd', 'spaceLg',
  'radiusSm', 'radiusMd',
  'fontSizePrice', 'lineHeightPrice',
  'fontSizeAddress', 'lineHeightAddress',
  'fontSizeInspection', 'lineHeightInspection',
  'metaIconSize', 'metaGap',
  'buttonSize'
];

const colorKeys = ['colorTextPrimary', 'colorTextSecondary', 'cardBg'];

const otherKeys = ['shadow', 'imageAspect'];

function toPx(v) {
  if (v === null || v === undefined || v === '') return '';
  const n = Number(v);
  return Number.isFinite(n) ? `${n}px` : String(v);
}

function download(filename, text) {
  const blob = new Blob([text], { type: 'application/json;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.setAttribute('href', url);
  a.setAttribute('download', filename);
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

function generateScss(vars) {
  // 将 JSON token 映射为 uni.scss 的 $srh-* 变量（部分为 px，部分为原样文本/比值）
  const lines = [];
  const map = [
    ['colorTextPrimary', '$srh-color-text-primary', v => v],
    ['colorTextSecondary', '$srh-color-text-secondary', v => v],
    ['cardBg', '$srh-color-card-bg', v => v],
    ['shadow', '$srh-shadow-card', v => v],

    ['space2xs', '$srh-space-2xs', v => `${Number(v)}px`],
    ['spaceXs', '$srh-space-xs', v => `${Number(v)}px`],
    ['spaceSm', '$srh-space-sm', v => `${Number(v)}px`],
    ['spaceMd', '$srh-space-md', v => `${Number(v)}px`],
    ['spaceLg', '$srh-space-lg', v => `${Number(v)}px`],

    ['radiusSm', '$srh-radius-sm', v => `${Number(v)}px`],
    ['radiusMd', '$srh-radius-md', v => `${Number(v)}px`],

    ['fontSizePrice', '$srh-font-size-price', v => `${Number(v)}px`],
    ['lineHeightPrice', '$srh-line-height-price', v => `${Number(v)}px`],

    ['fontSizeAddress', '$srh-font-size-address', v => `${Number(v)}px`],
    ['lineHeightAddress', '$srh-line-height-address', v => `${Number(v)}px`],

    ['fontSizeInspection', '$srh-font-size-inspection', v => `${Number(v)}px`],
    ['lineHeightInspection', '$srh-line-height-inspection', v => `${Number(v)}px`],

    ['metaIconSize', '$srh-meta-icon-size', v => `${Number(v)}px`],
    ['metaGap', '$srh-meta-gap', v => `${Number(v)}px`],

    ['buttonSize', '$srh-button-size', v => `${Number(v)}px`],
    ['imageAspect', '$srh-image-aspect', v => String(v)]
  ];

  lines.push('/* 由 docs-site 导出，回填到 apps/uni-app/src/uni.scss */');
  for (const [k, scss, fmt] of map) {
    if (vars[k] !== undefined) {
      lines.push(`${scss}: ${fmt(vars[k])};`);
    }
  }
  return lines.join('\n');
}

export default function TokenPreview() {
  const [initial, setInitial] = useState(null);
  const [tokens, setTokens] = useState(null);

  useEffect(() => {
    // 读取静态初始 tokens
    fetch('/tokens/srh.json', { cache: 'no-store' })
      .then((r) => r.json())
      .then((data) => {
        setInitial(data);
        setTokens(data);
      })
      .catch((e) => {
        console.error('加载初始 tokens 失败', e);
        const fallback = {
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
        };
        setInitial(fallback);
        setTokens(fallback);
      });
  }, []);

  const styleVars = useMemo(() => {
    if (!tokens) return {};
    return {
      '--srh-color-text-primary': tokens.colorTextPrimary,
      '--srh-color-text-secondary': tokens.colorTextSecondary,
      '--srh-card-bg': tokens.cardBg,
      '--srh-shadow-card': tokens.shadow,

      '--srh-space-2xs': toPx(tokens.space2xs),
      '--srh-space-xs': toPx(tokens.spaceXs),
      '--srh-space-sm': toPx(tokens.spaceSm),
      '--srh-space-md': toPx(tokens.spaceMd),
      '--srh-space-lg': toPx(tokens.spaceLg),

      '--srh-radius-sm': toPx(tokens.radiusSm),
      '--srh-radius-md': toPx(tokens.radiusMd),

      '--srh-font-size-price': toPx(tokens.fontSizePrice),
      '--srh-line-height-price': toPx(tokens.lineHeightPrice),

      '--srh-font-size-address': toPx(tokens.fontSizeAddress),
      '--srh-line-height-address': toPx(tokens.lineHeightAddress),

      '--srh-font-size-inspection': toPx(tokens.fontSizeInspection),
      '--srh-line-height-inspection': toPx(tokens.lineHeightInspection),

      '--srh-meta-icon-size': toPx(tokens.metaIconSize),
      '--srh-meta-gap': toPx(tokens.metaGap),

      '--srh-button-size': toPx(tokens.buttonSize),
      '--srh-image-aspect': String(tokens.imageAspect)
    };
  }, [tokens]);

  if (!tokens) return <div>加载中…</div>;

  const setVal = (key, value) => {
    setTokens((prev) => ({ ...prev, [key]: value }));
  };

  const setNumber = (key, value) => {
    const n = Number(value);
    if (Number.isFinite(n)) setVal(key, n);
  };

  const copyJSON = async () => {
    const text = JSON.stringify(tokens, null, 2);
    try {
      await navigator.clipboard.writeText(text);
      alert('已复制 JSON 到剪贴板');
    } catch {
      download('srh.tokens.json', text);
    }
  };

  const copySCSS = async () => {
    const text = generateScss(tokens);
    try {
      await navigator.clipboard.writeText(text);
      alert('已复制 SCSS 变量到剪贴板');
    } catch {
      download('srh.tokens.scss', text);
    }
  };

  const reset = () => {
    if (initial) setTokens(initial);
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '360px 1fr', gap: 16 }}>
      <div style={{ border: '1px solid #eee', borderRadius: 8, padding: 12 }}>
        <h3 style={{ marginTop: 0 }}>参数</h3>

        <fieldset style={{ border: 'none', padding: 0, marginBottom: 12 }}>
          <legend style={{ fontWeight: 600 }}>颜色</legend>
          {colorKeys.map((k) => (
            <div key={k} style={{ display: 'flex', alignItems: 'center', gap: 8, margin: '6px 0' }}>
              <label style={{ width: 160 }}>{k}</label>
              <input
                type="color"
                value={tokens[k]}
                onChange={(e) => setVal(k, e.target.value)}
                style={{ width: 42, height: 28, padding: 0, border: '1px solid #ccc' }}
              />
              <input
                type="text"
                value={tokens[k]}
                onChange={(e) => setVal(k, e.target.value)}
                style={{ flex: 1 }}
              />
            </div>
          ))}
        </fieldset>

        <fieldset style={{ border: 'none', padding: 0, marginBottom: 12 }}>
          <legend style={{ fontWeight: 600 }}>阴影</legend>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <label style={{ width: 160 }}>shadow</label>
            <input
              type="text"
              value={tokens.shadow}
              onChange={(e) => setVal('shadow', e.target.value)}
              placeholder="例如：0 1px 4px 0 rgba(0,0,0,.16)"
              style={{ flex: 1 }}
            />
          </div>
        </fieldset>

        <fieldset style={{ border: 'none', padding: 0, marginBottom: 12 }}>
          <legend style={{ fontWeight: 600 }}>尺寸（px）</legend>
          {numberKeysPx.map((k) => (
            <div key={k} style={{ display: 'flex', alignItems: 'center', gap: 8, margin: '6px 0' }}>
              <label style={{ width: 160 }}>{k}</label>
              <input
                type="number"
                value={tokens[k]}
                onChange={(e) => setNumber(k, e.target.value)}
                style={{ width: 120 }}
              />
            </div>
          ))}
        </fieldset>

        <fieldset style={{ border: 'none', padding: 0, marginBottom: 12 }}>
          <legend style={{ fontWeight: 600 }}>其他</legend>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, margin: '6px 0' }}>
            <label style={{ width: 160 }}>imageAspect</label>
            <input
              type="number" step="0.01"
              value={tokens.imageAspect}
              onChange={(e) => setNumber('imageAspect', e.target.value)}
              style={{ width: 120 }}
            />
          </div>
        </fieldset>

        <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
          <button className="button button--secondary" onClick={reset}>重置</button>
          <button className="button button--primary" onClick={copyJSON}>复制 JSON</button>
          <button className="button" onClick={copySCSS}>复制 SCSS</button>
        </div>
      </div>

      <div>
        <h3 style={{ marginTop: 0 }}>预览</h3>
        <div style={previewWrapperStyle}>
          <div
            style={{
              ...cardStyle,
              background: styleVars['--srh-card-bg'],
              padding: styleVars['--srh-card-padding'] || styleVars['--srh-space-md'],
              boxShadow: styleVars['--srh-shadow-card'],
              borderRadius: styleVars['--srh-radius-md']
            }}
          >
            <div
              style={{
                width: '100%',
                height: 0,
                paddingTop: `calc(${styleVars['--srh-image-aspect']} * 100%)`,
                background: '#eee',
                borderRadius: '6px',
                marginBottom: '12px'
              }}
            />
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div
                style={{
                  fontSize: styleVars['--srh-font-size-price'],
                  lineHeight: styleVars['--srh-line-height-price'],
                  color: styleVars['--srh-color-text-primary'],
                  fontWeight: 600
                }}
              >
                $800 pw
              </div>
              <div
                style={{
                  width: styleVars['--srh-button-size'],
                  height: styleVars['--srh-button-size'],
                  borderRadius: styleVars['--srh-radius-md'],
                  background: '#f5f5f5',
                  color: '#333',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
                aria-label="fav"
                title="Favorite"
              >
                ♥
              </div>
            </div>

            <div
              style={{
                fontSize: styleVars['--srh-font-size-address'],
                lineHeight: styleVars['--srh-line-height-address'],
                color: styleVars['--srh-color-text-primary'],
                marginTop: '8px'
              }}
            >
              12 Example St, Zetland NSW 2017
            </div>

            <div style={{ display: 'flex', flexDirection: 'row', marginTop: '4px' }}>
              {['2 Bed', '2 Bath', '1 Car'].map((item, idx) => (
                <div
                  key={idx}
                  style={{
                    color: styleVars['--srh-color-text-secondary'],
                    marginRight: styleVars['--srh-meta-gap']
                  }}
                >
                  {item}
                </div>
              ))}
            </div>

            <div
              style={{
                fontSize: styleVars['--srh-font-size-inspection'],
                lineHeight: styleVars['--srh-line-height-inspection'],
                color: styleVars['--srh-color-text-secondary'],
                marginTop: '6px'
              }}
            >
              Inspection today 2:15pm
            </div>
          </div>
        </div>

        <details style={{ marginTop: 16 }}>
          <summary>当前 JSON</summary>
          <pre style={{ background: '#f6f8fa', padding: 12, borderRadius: 8, overflow: 'auto' }}>
{JSON.stringify(tokens, null, 2)}
          </pre>
        </details>

        <details style={{ marginTop: 12 }}>
          <summary>回填 SCSS（复制到 apps/uni-app/src/uni.scss）</summary>
          <pre style={{ background: '#f6f8fa', padding: 12, borderRadius: 8, overflow: 'auto' }}>
{generateScss(tokens)}
          </pre>
        </details>
      </div>
    </div>
  );
}

const previewWrapperStyle = {
  background: '#fafafa',
  padding: 12,
  border: '1px solid #eee',
  borderRadius: 8
};

const cardStyle = {
  width: 360,
  boxSizing: 'border-box'
};
