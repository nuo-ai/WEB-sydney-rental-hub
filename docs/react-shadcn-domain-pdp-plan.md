# React + shadcn/ui + Tailwind 像素级复刻 Domain 房源详情页（PDP）实施方案

结论先行
- 单仓独立：用 Next.js（App Router）+ Tailwind + shadcn/ui，独立于任何旧站，降低复杂度。
- 流程：视觉拆解 → 令牌落表（Design Tokens）→ 组件装配 → 状态接入 → 可访问性/性能 → 像素验收。
- 目标：多断点（Desktop/Tablet/Mobile）对比偏差 ≤ 2px，交互/动画/可访问与 Domain 等效或更优。

一、技术栈与原则
- Next.js 14+（App Router，RSC 支持）
- Tailwind CSS v4（或 v3 稳定版）+ CSS 变量（HSL）做主题
- shadcn/ui（Radix primitives）+ lucide-react（图标）
- 数据：App Router + RSC（服务器加载）+（可选）TanStack Query 处理客户端增量
- 表单：react-hook-form + zod
- 富文本：react-markdown（或 MDX）
- 质量：Playwright 视觉回归 + Lighthouse + Axe

二、初始化（命令仅供运行时参考，本文档不自动执行）
- 创建项目
  - npx create-next-app@latest web-react-shadcn --ts --eslint
- 安装 Tailwind
  - v4 路线：@tailwindcss/vite + @import "tailwindcss"
  - v3 路线：传统 postcss + tailwind.config.ts
- 初始化 shadcn
  - npx shadcn@latest init（alias 选择 @/*，风格走 CSS 变量）
  - npx shadcn add button card badge input textarea avatar dialog drawer sheet alert skeleton separator tooltip carousel sonner tabs scroll-area

三、预期目录结构（骨架）
- app/
  - layout.tsx（主题变量/字体/Toaster 注入）
  - page.tsx（示例页）
  - property/[id]/page.tsx（详情页入口）
- components/
  - gallery/ (Hero/Gallery + Dialog 放大)
  - pdp/ (SummaryCard、Facts、Description、Inspections、Map、AgentCard、Recommendations)
  - ui/ (shadcn 生成组件与二次封装)
- lib/
  - tokens.ts（设计令牌表，可选）
  - fetchers.ts（数据拉取）
  - seo.ts（JSON-LD）
- styles/
  - globals.css（:root 变量 + Tailwind 指令）

四、Design Tokens（最小集）
- 颜色（HSL 变量）
  - --bg、--fg、--muted、--card、--border、--primary、--ring
  - 暗色：:root[data-theme="dark"] 重载以上变量
- 半径
  - --radius-sm: 6px; --radius-md: 10px; --radius-lg: 14px
- 阴影
  - --shadow-sm/md/lg （按 Domain 的层次测量）
- 间距尺度
  - 4/8/12/16/24/32/48/64（以 4 为基数，覆盖 PDP 常见间距）
- 字体系统
  - 标题/正文/小字尺寸、行高、字重（按 Domain 标注测量）

Tailwind 颜色映射（示例）
- theme.extend.colors.primary = hsl(var(--primary))
- backgroundColor: hsl(var(--bg))；textColor: hsl(var(--fg))
- ringColor: hsl(var(--ring))；borderColor: hsl(var(--border))

五、像素拆解（Domain PDP）
- 截图断点：1440/1280、1024、390 宽
- 标注：容器宽度/边距、网格比例（主列/侧栏）、段落间距、字体层级、按钮尺寸、卡片半径与阴影
- 输出“复刻蓝图”：带标注的图 + Tokens 表（上节）

六、组件清单（对应 Domain）
- 头图区（Hero/Gallery）
  - 功能：轮播、左右箭头/分页、键盘左右、点击放大（Dialog）、Lazy 加载
  - 技术：Carousel（embla）+ Dialog + next/image
- SummaryCard（价格/地址/参数/标签/操作）
  - 参数图标：lucide-react（Bed/Bath/Car）
  - 操作：收藏/分享（Tooltip + Sheet/Drawer）
- Key Facts（要点）
  - Grid + Badge/Chip；含分隔线（Separator）
- Description（详情）
  - react-markdown + @tailwindcss/typography（保证段落/列表/链接样式）
- Inspections/Availability（看房时间/可租日期）
  - Tabs + 列表；预约（Dialog/Sheet + 表单）
- Map & Nearby（地图与周边）
  - 懒加载地图（Mapbox/Google Maps），可切换卫星/交通；附近学校/交通列表
- AgentCard（中介信息 + 表单）
  - Avatar + 联系方式；react-hook-form + zod；提交 toast（sonner）
- Breadcrumb/TopNav（可选）
- Recommendations（同区域推荐）
  - 横向滚动或 Grid；Skeleton 占位

七、页面与数据流（/property/[id]）
- 服务器数据（优先）：在 page.tsx 使用 RSC 获取主数据（SEO 与首屏更快）
- 客户端增强：局部组件（地图、轮播、表单）使用非阻塞 Client Components
- 状态分支：Skeleton（加载）、Alert（错误）、内容（正常）
- 图片策略：next/image sizes/priority；首图优先加载，其他懒加载

八、可访问性与交互
- Dialog/Drawer/Tooltip：焦点陷阱与 ESC 退出；Tab 键全流程
- 焦点环（focus-visible）：统一 ring；暗/亮模式对比度达标（WCAG AA）
- 键盘：轮播左右切换，Dialog 关闭
- 表单：即时校验、错误提示与 aria 描述

九、性能与 SEO
- 代码拆分：按路由/组件边界；地图懒加载
- JSON-LD（RealEstateListing）：价格、地址、经纬度、图片、代理信息
- Open Graph：首图、标题、描述
- 样式预算：避免过度自定义，复用 tokens 与 tailwind 原子

十、验收与像素对齐
- 视觉回归：Playwright 截图（1440/1024/390），误差阈值设置 0.1–0.2%
- 人工验收：对比叠加（CSS overlay/浏览器扩展），关键模块误差 ≤ 2px
- 交互验收：图片放大/键盘操作/Toast/表单校验/地图交互

十一、里程碑
- M1（T+1.5d）
  - 详情页骨架：Gallery 放大、SummaryCard、Description（Markdown）、AgentCard 表单（toast）、Skeleton/Alert 分支、移动端布局
- M2（T+3d）
  - Inspections、Map & Nearby、Recommendations、暗色主题；断点细节对齐
- M3（T+5d）
  - 像素验收流水化（Playwright）、JSON-LD/OG、性能调优（LCP/CLS）

十二、风险与对策
- 视觉偏差：先出“复刻蓝图”（标注图+Tokens 表），编码前对齐尺度
- 组件差异：必要时做轻量二次封装覆盖样式，不改 shadcn 源
- 首屏性能：RSC + 分块加载；图片 sizes/priority 调优
- 可访问：使用 Radix primitives；Axe 扫描 + 键盘完整走查

十三、最小代码片段（示例，仅示意）
- app/layout.tsx（Toaster 注入）
  ```tsx
  import './globals.css'
  import { Toaster } from '@/components/ui/sonner'
  export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
      <html lang="en">
        <body>
          {children}
          <Toaster />
        </body>
      </html>
    )
  }
  ```
- app/property/[id]/page.tsx（骨架）
  ```tsx
  import { Suspense } from 'react'
  import { Gallery } from '@/components/gallery/Gallery'
  import { SummaryCard } from '@/components/pdp/SummaryCard'
  import { Description } from '@/components/pdp/Description'
  import { AgentCard } from '@/components/pdp/AgentCard'
  import { Skeleton } from '@/components/ui/skeleton'

  export default async function Page({ params }: { params: { id: string } }) {
    // const data = await getProperty(params.id) // RSC 拉取
    return (
      <div className="container mx-auto px-4">
        <Suspense fallback={<Skeleton className="w-full aspect-[16/9]" />}>
          <Gallery images={[]} />
        </Suspense>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 py-6">
          <div className="lg:col-span-2 space-y-6">
            <SummaryCard /* ... */ />
            <Description /* markdown */ />
            {/* Inspections / Facts / Recommendations */}
          </div>
          <div className="lg:col-span-1">
            <AgentCard /* form+toast */ />
          </div>
        </div>
      </div>
    )
  }
  ```

十四、交付物清单
- 设计：标注图（多断点）+ 令牌表（.md 或 .json）
- 代码：Next + shadcn 项目骨架；PDP 页面与组件；RSC 数据拉取占位；表单校验
- 质量：Playwright 视觉回归脚本；Lighthouse 报告；Axe 可访问性报告

附录：安装依赖（React 侧）
- npm i @tanstack/react-query react-hook-form zod react-markdown embla-carousel-react lucide-react
- npx shadcn add ...（见上方清单）

备注
- 本方案聚焦“像素级复刻 + 开发效率 + 可维护性”，避免任何与旧站的耦合。
- 如果需要，我可以基于此文档在 apps/ 下新建 web-react-shadcn 并一次性脚手架，但这涉及安装依赖与网络操作，请先确认再切到 Act 执行。
