import React, { useMemo, useState } from 'react'
import { useTheme } from 'next-themes'
import dark from '../tokens/dark'
import light from '../tokens/light'

type Tokens = typeof dark

function useTokens(): Tokens {
  const { theme, resolvedTheme } = useTheme()
  const mode = (theme === 'system' ? resolvedTheme : theme) ?? 'light'
  return useMemo(() => (mode === 'dark' ? dark : light), [mode])
}

export default function TokenButton() {
  const tokens = useTokens()
  const [state, setState] = useState<'default' | 'hover' | 'active'>('default')

  const bg =
    state === 'active'
      ? tokens.color.success.active
      : state === 'hover'
      ? tokens.color.success.hover
      : tokens.color.success.primary

  const style: React.CSSProperties = {
    background: bg,
    color: tokens.color.success.on,
    border: `1px solid ${tokens.color.border.subtle}`,
    borderRadius: 8,
    padding: '10px 16px',
    fontSize: 16,
    lineHeight: '24px',
    userSelect: 'none',
    transition: 'background 160ms ease-in-out, transform 80ms ease-in-out',
  }

  return (
    <button
      type="button"
      style={style}
      onMouseEnter={() => setState('hover')}
      onMouseLeave={() => setState('default')}
      onMouseDown={() => setState('active')}
      onMouseUp={() => setState('hover')}
      onTouchStart={() => setState('active')}
      onTouchEnd={() => setState('default')}
      aria-pressed={state === 'active'}
      aria-label="Success Button"
    >
      Success 按钮（hover = {tokens.color.success.hover} / active = {tokens.color.success.active}）
    </button>
  )
}
