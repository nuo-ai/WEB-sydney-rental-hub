import React from 'react'
import { useTheme } from 'next-themes'

export default function ThemeSwitcher() {
  const { theme, setTheme, resolvedTheme } = useTheme()
  const mode = (theme === 'system' ? resolvedTheme : theme) ?? 'light'

  return (
    <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
      <span style={{ fontSize: 14, opacity: 0.8 }}>当前主题: {mode}</span>
      <button
        type="button"
        onClick={() => setTheme('light')}
        style={{
          padding: '6px 10px',
          borderRadius: 6,
          border: '1px solid #ccc',
          background: mode === 'light' ? '#efefef' : 'transparent',
          cursor: 'pointer'
        }}
      >
        Light
      </button>
      <button
        type="button"
        onClick={() => setTheme('dark')}
        style={{
          padding: '6px 10px',
          borderRadius: 6,
          border: '1px solid #ccc',
          background: mode === 'dark' ? '#efefef' : 'transparent',
          cursor: 'pointer'
        }}
      >
        Dark
      </button>
      <button
        type="button"
        onClick={() => setTheme('system')}
        style={{
          padding: '6px 10px',
          borderRadius: 6,
          border: '1px solid #ccc',
          background: theme === 'system' ? '#efefef' : 'transparent',
          cursor: 'pointer'
        }}
      >
        System
      </button>
    </div>
  )
}
