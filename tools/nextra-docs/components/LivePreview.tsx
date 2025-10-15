/** 
 * 组件职责：在 Nextra 文档中通过 iframe 实时预览本地运行的 Vue 路由页面
 * 为什么这样设计：
 * 1) 文档站（Next/Nextra）与业务站（Vite/Vue）解耦，仅通过 URL 连接，避免重复实现 Vue 逻辑
 * 2) 加一个“连通性”兜底提示，帮助新人快速定位：若 5173 未启动，预览区不会渲染到页面
 * 权衡：
 * - 浏览器跨域限制下，无法准确探知 iframe 内部状态；这里采用“best-effort”探测（no-cors 请求 + 用户指引）
 */

'use client'

import React, { useEffect, useState } from 'react'

type LivePreviewProps = {
  url: string
  height?: number
  showBorder?: boolean
}

export default function LivePreview({
  url,
  height = 900,
  showBorder = true
}: LivePreviewProps) {
  const [status, setStatus] = useState<'checking' | 'ok' | 'unreachable'>(
    'checking'
  )

  // 尝试探测目标 URL 是否可达（no-cors 下成功返回为 opaque，不抛错则认为可达）
  useEffect(() => {
    let canceled = false

    const check = async () => {
      try {
        const controller = new AbortController()
        const timeout = setTimeout(() => controller.abort(), 1500)
        // 说明：no-cors/GET 常见返回 opaque，不可读但不抛错（可视为“正在服务中”）
        await fetch(url, {
          method: 'GET',
          mode: 'no-cors',
          signal: controller.signal
        } as RequestInit)
        clearTimeout(timeout)
        if (!canceled) setStatus('ok')
      } catch {
        if (!canceled) setStatus('unreachable')
      }
    }

    check()
    return () => {
      canceled = true
    }
  }, [url])

  const borderStyle = showBorder ? '1px solid #e5e7eb' : 'none'

  return (
    <div
      style={{
        width: '100%',
        border: borderStyle,
        borderRadius: 8,
        overflow: 'hidden',
        background: '#fff'
      }}
    >
      {/* 顶部工具条：展示 URL 与“新窗口打开” */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          padding: '8px 12px',
          borderBottom: '1px solid #e5e7eb',
          background: '#f8fafc'
        }}
      >
        <span style={{ fontSize: 12, color: '#64748b' }}>
          预览：{url}{' '}
          {status === 'checking'
            ? '(检测中...)'
            : status === 'ok'
              ? ''
              : '(未检测到本地服务，请先在 monorepo 中运行 vue-juwo 开发服务，默认端口 5173)'}
        </span>
        <a
          href={url}
          target="_blank"
          rel="noreferrer"
          style={{ fontSize: 12, color: '#0ea5e9' }}
          aria-label="在新窗口打开预览页面"
        >
          新窗口打开
        </a>
      </div>

      {/* 预览区域：嵌入目标路由 */}
      <iframe
        title={`Live preview for ${url}`}
        src={url}
        style={{ width: '100%', height, border: 'none', background: '#f1f5f9' }}
      />
    </div>
  )
}
