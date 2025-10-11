import React, { useMemo } from 'react';

function toPx(v) {
  if (v === null || v === undefined || v === '') return '';
  const n = Number(v);
  return Number.isFinite(n) ? `${n}px` : String(v);
}

export default function Card({ tokens, price = '$800 pw', address = '12 Example St, Zetland NSW 2017', meta = ['2 Bed', '2 Bath', '1 Car'], label }) {
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

  return (
    <div
      style={{
        ...cardStyle,
        background: styleVars['--srh-card-bg'],
        padding: styleVars['--srh-space-md'],
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
          marginBottom: '12px',
          position: 'relative',
        }}
      >
        {label && (
          <div style={badgeStyle}>
            {label}
          </div>
        )}
      </div>

      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div
          style={{
            fontSize: styleVars['--srh-font-size-price'],
            lineHeight: styleVars['--srh-line-height-price'],
            color: styleVars['--srh-color-text-primary'],
            fontWeight: 600
          }}
        >
          {price}
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
        {address}
      </div>

      <div style={{ display: 'flex', flexDirection: 'row', marginTop: '4px' }}>
        {meta.map((item, idx) => (
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
        {label || 'Inspection today 2:15pm'}
      </div>
    </div>
  );
}

const cardStyle = {
  width: 360,
  boxSizing: 'border-box'
};

const badgeStyle = {
  position: 'absolute',
  left: 8,
  top: 8,
  background: 'rgba(0,0,0,0.75)',
  color: '#fff',
  fontSize: 12,
  lineHeight: '20px',
  height: 20,
  borderRadius: 12,
  padding: '0 8px'
};
