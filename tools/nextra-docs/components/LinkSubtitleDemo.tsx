import React, { useMemo } from 'react'
import { useTheme } from 'next-themes'
import dark from '../tokens/dark'
import light from '../tokens/light'

type Tokens = typeof dark

function useTokens(): Tokens {
  const { theme, resolvedTheme } = useTheme()
  const mode = (theme === 'system' ? resolvedTheme : theme) ?? 'light'
  return useMemo(() => (mode === 'dark' ? dark : light), [mode])
}

export default function LinkSubtitleDemo() {
  const tokens = useTokens()

  return (
    <div
      style={{
        background: tokens.color.surface.base,
        padding: 16,
        border: `1px solid ${tokens.color.border.subtle}`,
        borderRadius: 8
      }}
    >
      <p
        style={{
          margin: 0,
          color: tokens.color.text.subtitle,
          fontSize: 16,
          lineHeight: '24px'
        }}
      >
        这是“副标题（subtitle）”示例，等同链接主色：{tokens.color.text.subtitle}
      </p>
      <p style={{ marginTop: 8 }}>
        <a
          href="#"
          style={{
            color: tokens.color.link.primary,
            textDecoration: 'underline'
          }}
          onClick={(e) => e.preventDefault()}
        >
          链接示例（link.primary = {tokens.color.link.primary}）
        </a>
      </p>
    </div>
  )
}
