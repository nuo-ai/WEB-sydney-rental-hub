#!/usr/bin/env node
/**
 * 半自动回填 C（Playwright 采样版 · 增强选择器取样）
 *
 * 目标：
 * - 在不依赖浏览器扩展注入的前提下，从真实渲染页面读取 computedStyle 与几何信息
 * - 仅覆盖 JSON 中为 null 的字段；任何不确定值一律保留为 null（遵循“占位→回填”）
 * - 支持三断点（1440 / 1024 / 390），默认首个断点
 * - 增强：更稳健地取到 features item 文本/图标样式、icon–text 间距；description 链接样式、列表项间距/缩进、标题/正文颜色、容器外边距等
 *
 * 使用前提：
 *   pnpm add -D playwright 或 npm i -D playwright
 *   可选：npx playwright install chromium
 *
 * 运行示例：
 *   node scripts/blueprint/backfill-c.js \\
 *     --url https://www.domain.com.au/8-1-defries-avenue-zetland-nsw-2017-17803938 \\
 *     --slug 8-1-defries-avenue-zetland-nsw-2017-17803938 \\
 *     --bp 1440,1024,390 --wait 1500
 *
 * 输出：
 * - 原地更新：
 *   docs/blueprints/domain/<slug>/modules/features.json
 *   docs/blueprints/domain/<slug>/modules/description.json
 *
 * 重要约束：
 * - 仅回填可验证字段；遇到缺失/不可测/结构差异，自动跳过并保留 null
 * - 不改动截图路径与文件移动（遵循 file-system-rules）
 */

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const args = parseArgs(process.argv.slice(2));
const url = args.url || 'https://www.domain.com.au/8-1-defries-avenue-zetland-nsw-2017-17803938';
const slug = args.slug || '8-1-defries-avenue-zetland-nsw-2017-17803938';
const wait = Number(args.wait || 1500);
const breakpoints = (args.bp ? String(args.bp).split(',').map(n => Number(n)) : [1440]).filter(Boolean);

// 目标 JSON 文件路径
const ROOT = process.cwd();
const FEATURES_JSON = path.join(ROOT, 'docs/blueprints/domain', slug, 'modules/features.json');
const DESCRIPTION_JSON = path.join(ROOT, 'docs/blueprints/domain', slug, 'modules/description.json');

main().catch(err => {
  console.error('[backfill-c] 运行失败：', err);
  process.exit(1);
});

async function main() {
  console.log('[backfill-c] 启动，URL =', url, 'slug =', slug, 'bp =', breakpoints.join(','), 'wait =', wait, 'ms');

  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({
    viewport: { width: breakpoints[0] || 1440, height: 900 },
    deviceScaleFactor: 2, // DPR=2
  });
  const page = await ctx.newPage();

  await page.setDefaultNavigationTimeout(90000);
  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  } catch (e) {
    console.warn('[backfill-c] networkidle 超时，降级为 domcontentloaded：', e.name);
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  }
  // 等待关键模块任一可见，避免因广告/追踪请求导致的长尾阻塞
  try {
    await Promise.race([
      page.waitForSelector('[data-testid="listing-details__additional-features"]', { timeout: 5000 }),
      page.waitForSelector('[data-testid="listing-details__description"]', { timeout: 5000 })
    ]);
  } catch (_) { /* 忽略，无阻塞 */ }
  await page.waitForTimeout(wait);

  // 仅以第一个断点回填（保持最小增量；如需多断点可多次运行）
  const bp = breakpoints[0] || 1440;

  // 回填 features
  await backfillFeatures(page, bp);

  // 回填 description
  await backfillDescription(page, bp);

  await browser.close();
  console.log('[backfill-c] 完成回填（bp =', bp, '）。如需 1024/390，可使用 --bp 扩展后续采集。');
}

// ========== Features 回填 ==========

async function backfillFeatures(page, bp) {
  if (!fs.existsSync(FEATURES_JSON)) {
    console.warn('[features] 未找到文件：', FEATURES_JSON);
    return;
  }
  const json = readJson(FEATURES_JSON);

  const primarySel = json?.selectors?.primaryContainer;
  const itemSel = json?.selectors?.itemSelector;
  const viewMoreSel = json?.selectors?.viewMoreSelector;

  if (!primarySel || !itemSel) {
    console.warn('[features] 选择器不完整，跳过。');
    return;
  }

  console.log('[features] 采集中…', { primarySel, itemSel, viewMoreSel });

  const data = await page.evaluate(
    ({ primarySel, itemSel, viewMoreSel }) => {
      const toNumber = (v) => {
        if (!v) return null;
        const m = String(v).match(/([-\d.]+)/);
        return m ? Number(m[1]) : null;
      };
      const noneToNull = (v) => {
        if (!v) return null;
        const s = String(v).trim().toLowerCase();
        if (s === 'normal' || s === 'none' || s === '0px') return null;
        return toNumber(v) ?? v;
      };
      const pickTextEl = (root) => {
        const candidates = Array.from(root.querySelectorAll('span, p, div, li')).filter(el => {
          const t = (el.textContent || '').trim();
          if (!t) return false;
          // 避免把容器本身当作文本节点
          const cs = getComputedStyle(el);
          return cs.display !== 'inline-block' || t.length <= 80; // 粗略过滤
        });
        return candidates[0] || null;
      };
      const container = document.querySelector(primarySel);
      if (!container) return { error: 'container_not_found' };

      // 找 items（优先容器内检索）
      const scopedItems = container.querySelectorAll(itemSel);
      const items = scopedItems.length ? Array.from(scopedItems) : Array.from(document.querySelectorAll(itemSel));
      if (!items.length) return { error: 'items_not_found' };

      // 计算列数：优先 gridTemplateColumns，其次按 x 坐标聚类
      const contStyle = container ? getComputedStyle(container) : null;
      let columns = null;

      if (contStyle) {
        const gridCols = contStyle.gridTemplateColumns;
        if (gridCols && gridCols !== 'none') {
          columns = gridCols.split(' ').length;
        }
      }
      if (!columns) {
        const xs = items.slice(0, 20).map((el) => el.getBoundingClientRect().x);
        const sorted = xs.slice().sort((a, b) => a - b);
        const groups = [];
        sorted.forEach((x) => {
          const g = groups.find((arr) => Math.abs(arr[0] - x) <= 8);
          if (g) g.push(x);
          else groups.push([x]);
        });
        columns = groups.length || null;
      }

      // 计算 row/column gap：优先样式 gap，否则通过同列/同行几何推测
      let rowGap = null;
      let colGap = null;
      if (contStyle) {
        const gap = contStyle.gap || contStyle.rowGap || contStyle.columnGap;
        const row = contStyle.rowGap ? toNumber(contStyle.rowGap) : null;
        const col = contStyle.columnGap ? toNumber(contStyle.columnGap) : null;
        rowGap = row ?? (gap ? toNumber(gap) : null);
        colGap = col ?? (gap ? toNumber(gap) : null);
      }

      const samples = items.slice(0, 6).map((el) => el.getBoundingClientRect());
      if (!rowGap && columns && columns >= 1) {
        const byX = {};
        samples.forEach((r) => {
          const key = String(Math.round(r.x / 8) * 8);
          byX[key] = byX[key] || [];
          byX[key].push(r);
        });
        const gaps = [];
        Object.values(byX).forEach((arr) => {
          arr.sort((a, b) => a.y - b.y);
          for (let i = 1; i < arr.length; i++) {
            const g = arr[i].y - (arr[i - 1].y + arr[i - 1].height);
            if (g >= 0) gaps.push(g);
          }
        });
        if (gaps.length) rowGap = Math.round(gaps.reduce((a, b) => a + b, 0) / gaps.length);
      }
      if (!colGap && samples.length >= 2) {
        const byY = {};
        samples.forEach((r) => {
          const key = String(Math.round(r.y / 8) * 8);
          byY[key] = byY[key] || [];
          byY[key].push(r);
        });
        const gaps = [];
        Object.values(byY).forEach((arr) => {
          arr.sort((a, b) => a.x - b.x);
          for (let i = 1; i < arr.length; i++) {
            const g = arr[i].x - (arr[i - 1].x + arr[i - 1].width);
            if (g >= 0) gaps.push(g);
          }
        });
        if (gaps.length) colGap = Math.round(gaps.reduce((a, b) => a + b, 0) / gaps.length);
      }

      // 采集单项的 icon / text / 间距 / 高度
      const first = items[0];
      let iconSize = null;
      let textFontSize = null;
      let textLineHeight = null;
      let textColor = null;
      let itemHeight = null;
      let iconTextSpacing = null;

      if (first) {
        const r = first.getBoundingClientRect();
        itemHeight = Math.round(r.height);

        // 图标：svg 或 img 或 class 包含 icon
        const icon = first.querySelector('svg, img, [class*="icon" i], [data-testid*="icon" i]');
        const text = pickTextEl(first);

        if (icon) {
          const ir = icon.getBoundingClientRect();
          iconSize = Math.round(Math.max(ir.width, ir.height));
        }
        if (text) {
          const cs = getComputedStyle(text);
          textFontSize = toNumber(cs.fontSize);
          textLineHeight = toNumber(cs.lineHeight);
          textColor = cs.color || null;
        }
        if (icon && text) {
          const ir = icon.getBoundingClientRect();
          const tr = text.getBoundingClientRect();
          const spacing = tr.x - (ir.x + ir.width);
          iconTextSpacing = Math.round(spacing);
        }
      }

      // view more
      let viewMore = null;
      if (viewMoreSel) {
        const el = document.querySelector(viewMoreSel);
        if (el) {
          const rect = el.getBoundingClientRect();
          const cs = getComputedStyle(el);
          viewMore = {
            rect: {
              x: Math.round(rect.x),
              y: Math.round(rect.y),
              width: Math.round(rect.width),
              height: Math.round(rect.height),
            },
            typography: {
              fontSize: toNumber(cs.fontSize),
              fontWeight: cs.fontWeight || null,
              letterSpacing: noneToNull(cs.letterSpacing),
            },
          };
        }
      }

      // 容器 padding / margin
      let containerPadding = null;
      let containerMargin = null;
      if (container) {
        const cs = getComputedStyle(container);
        containerPadding = {
          top: toNumber(cs.paddingTop),
          right: toNumber(cs.paddingRight),
          bottom: toNumber(cs.paddingBottom),
          left: toNumber(cs.paddingLeft),
        };
        containerMargin = {
          top: toNumber(cs.marginTop),
          right: toNumber(cs.marginRight),
          bottom: toNumber(cs.marginBottom),
          left: toNumber(cs.marginLeft),
        };
      }

      // 列表内边距（若存在 ul/ol 包裹）
      let listPadding = null;
      const listWrapper = container.querySelector('ul, ol');
      if (listWrapper) {
        const cs = getComputedStyle(listWrapper);
        listPadding = {
          top: toNumber(cs.paddingTop),
          right: toNumber(cs.paddingRight),
          bottom: toNumber(cs.paddingBottom),
          left: toNumber(cs.paddingLeft),
        };
      }

      // 颜色（若可辨识）
      const colors = {
        background: container ? getComputedStyle(container).backgroundColor : null,
        text: textColor,
        icon: null,
        view_more_text: (viewMore && document.querySelector(viewMoreSel)) ? getComputedStyle(document.querySelector(viewMoreSel)).color : null,
      };

      return {
        columns,
        rowGap,
        colGap,
        iconSize,
        textFontSize,
        textLineHeight,
        textColor,
        itemHeight,
        iconTextSpacing,
        viewMore,
        containerPadding,
        containerMargin,
        listPadding,
        colors,
      };
    },
    { primarySel, itemSel, viewMoreSel }
  );

  if (data?.error) {
    console.warn('[features] 采集失败：', data.error);
    return;
  }

  // 写回 JSON（仅覆盖 null 字段）
  json.measurements = json.measurements || {};
  json.measurements.list = json.measurements.list || {};
  json.styles = json.styles || {};
  json.styles.spacing = json.styles.spacing || {};
  json.styles.colors = json.styles.colors || {};

  const setIfNull = (obj, key, val) => {
    if (val === null || val === undefined) return;
    if (obj[key] === null || obj[key] === undefined) obj[key] = val;
  };

  setIfNull(json.measurements.list, `columns_${bp}`, safeInt(data.columns));
  setIfNull(json.measurements.list, 'row_gap', safeInt(data.rowGap));
  setIfNull(json.measurements.list, 'column_gap', safeInt(data.colGap));

  json.measurements.list.item = json.measurements.list.item || {};
  setIfNull(json.measurements.list.item, 'icon_size', safeInt(data.iconSize));
  setIfNull(json.measurements.list.item, 'text_fontSize', safeInt(data.textFontSize));
  setIfNull(json.measurements.list.item, 'text_lineHeight', safeInt(data.textLineHeight));
  setIfNull(json.measurements.list.item, 'text_color', data.textColor || null);
  setIfNull(json.measurements.list.item, 'item_height', safeInt(data.itemHeight));
  setIfNull(json.measurements.list.item, 'spacing_icon_text', safeInt(data.iconTextSpacing));

  json.measurements.view_more_button = json.measurements.view_more_button || { exists: true, rect: null, typography: {} };
  if (data.viewMore?.rect) {
    setIfNull(json.measurements.view_more_button, 'rect', data.viewMore.rect);
  }
  if (data.viewMore?.typography) {
    json.measurements.view_more_button.typography = json.measurements.view_more_button.typography || {};
    setIfNull(json.measurements.view_more_button.typography, 'fontSize', safeInt(data.viewMore.typography.fontSize));
    setIfNull(json.measurements.view_more_button.typography, 'fontWeight', data.viewMore.typography.fontWeight || null);
    setIfNull(json.measurements.view_more_button.typography, 'letterSpacing', safeFloat(data.viewMore.typography.letterSpacing));
  }

  if (data.containerPadding) {
    setIfNull(json.styles.spacing, 'container_padding', data.containerPadding);
  }
  if (data.containerMargin) {
    setIfNull(json.styles.spacing, 'container_margin', data.containerMargin);
  }
  if (data.listPadding) {
    setIfNull(json.styles.spacing, 'list_padding', data.listPadding);
  }
  if (data.colors) {
    setIfNull(json.styles.colors, 'background', data.colors.background);
    setIfNull(json.styles.colors, 'text', data.colors.text);
    setIfNull(json.styles.colors, 'icon', data.colors.icon);
    setIfNull(json.styles.colors, 'view_more_text', data.colors.view_more_text);
  }

  writeJson(FEATURES_JSON, json);
  console.log('[features] 已写回（仅覆盖原 null 字段）。');
}

// ========== Description 回填 ==========

async function backfillDescription(page, bp) {
  if (!fs.existsSync(DESCRIPTION_JSON)) {
    console.warn('[description] 未找到文件：', DESCRIPTION_JSON);
    return;
  }
  const json = readJson(DESCRIPTION_JSON);

  const primarySel = json?.selectors?.primaryContainer;
  const titleSel = json?.selectors?.titleSelector;
  const readMoreSel = json?.selectors?.readMoreSelector;

  if (!primarySel) {
    console.warn('[description] 选择器不完整，跳过。');
    return;
  }

  console.log('[description] 采集中…', { primarySel, titleSel, readMoreSel });

  const data = await page.evaluate(({ primarySel, titleSel }) => {
    const toNumber = (v) => {
      if (!v) return null;
      const m = String(v).match(/([-\d.]+)/);
      return m ? Number(m[1]) : null;
    };
    const noneToNull = (v) => {
      if (!v) return null;
      const s = String(v).trim().toLowerCase();
      if (s === 'normal' || s === 'none' || s === '0px') return null;
      return toNumber(v) ?? v;
    };

    const container = document.querySelector(primarySel);
    if (!container) return { error: 'container_not_found' };

    // 标题
    let title = null;
    if (titleSel) {
      const el = document.querySelector(titleSel) || container.querySelector(titleSel);
      if (el) {
        const cs = getComputedStyle(el);
        const mb = toNumber(cs.marginBottom);
        title = {
          fontSize: toNumber(cs.fontSize),
          lineHeight: toNumber(cs.lineHeight),
          fontWeight: cs.fontWeight || null,
          letterSpacing: noneToNull(cs.letterSpacing),
          margin_bottom: mb,
          color: cs.color || null,
        };
      }
    }

    // 正文：取容器内第一段落（p 优先）
    const paras = Array.from(container.querySelectorAll('p, div, li')).filter((el) => (el.textContent || '').trim().length > 0);
    let body = null;
    let paragraphSpacing = null;
    let listItemSpacing = null;
    let listIndent = null;

    const firstBody = container.querySelector('p') || paras[0];
    if (firstBody) {
      const cs = getComputedStyle(firstBody);
      body = {
        fontSize: toNumber(cs.fontSize),
        lineHeight: toNumber(cs.lineHeight),
        color: cs.color || null,
      };
    }
    // 段落间距：相邻 p 的下+上的 margin 之和近似
    const ps = Array.from(container.querySelectorAll('p'));
    if (ps.length >= 2) {
      const cs1 = getComputedStyle(ps[0]);
      const cs2 = getComputedStyle(ps[1]);
      const mb = toNumber(cs1.marginBottom);
      const mt = toNumber(cs2.marginTop);
      paragraphSpacing = (mb ?? 0) + (mt ?? 0);
    }
    // 列表项间距/缩进
    const lis = Array.from(container.querySelectorAll('li'));
    if (lis.length >= 2) {
      // 尝试用几何距离减去高度来估算实际垂直间距
      const r1 = lis[0].getBoundingClientRect();
      const r2 = lis[1].getBoundingClientRect();
      const geoGap = Math.round(r2.y - (r1.y + r1.height));
      const cssGap = toNumber(getComputedStyle(lis[0]).marginBottom);
      listItemSpacing = Number.isFinite(geoGap) && geoGap >= 0 ? geoGap : (cssGap ?? null);
    } else if (lis.length === 1) {
      listItemSpacing = toNumber(getComputedStyle(lis[0]).marginBottom);
    }
    const list = container.querySelector('ul, ol');
    if (list) {
      const cs = getComputedStyle(list);
      listIndent = toNumber(cs.paddingLeft) ?? toNumber(cs.marginLeft);
    }

    // 链接样式（基础态）
    let linkStyle = null;
    const a = container.querySelector('a');
    if (a) {
      const cs = getComputedStyle(a);
      linkStyle = {
        color: cs.color,
        textDecorationLine: cs.textDecorationLine || null,
      };
    }

    // 容器 padding / margin
    const csContainer = getComputedStyle(container);
    const containerPadding = {
      top: toNumber(csContainer.paddingTop),
      right: toNumber(csContainer.paddingRight),
      bottom: toNumber(csContainer.paddingBottom),
      left: toNumber(csContainer.paddingLeft),
    };
    const containerMargin = {
      top: toNumber(csContainer.marginTop),
      right: toNumber(csContainer.marginRight),
      bottom: toNumber(csContainer.marginBottom),
      left: toNumber(csContainer.marginLeft),
    };

    // 颜色合集（供 styles.colors 使用）
    const colors = {
      background: csContainer.backgroundColor,
      title: title?.color || null,
      body: body?.color || null,
      link: linkStyle?.color || null,
    };

    return {
      title,
      body,
      paragraphSpacing,
      listItemSpacing,
      listIndent,
      linkStyle,
      containerPadding,
      containerMargin,
      colors,
    };
  }, { primarySel, titleSel });

  if (data?.error) {
    console.warn('[description] 采集失败：', data.error);
    return;
  }

  // 写回 JSON（仅覆盖 null 字段）
  json.measurements = json.measurements || {};
  json.measurements.typography = json.measurements.typography || {};
  json.styles = json.styles || {};
  json.styles.spacing = json.styles.spacing || {};
  json.styles.colors = json.styles.colors || {};

  const setIfNull = (obj, key, val) => {
    if (val === null || val === undefined) return;
    if (obj[key] === null || obj[key] === undefined) obj[key] = val;
  };

  // 标题
  if (data.title) {
    json.measurements.typography.title = json.measurements.typography.title || {};
    setIfNull(json.measurements.typography.title, 'fontSize', safeInt(data.title.fontSize));
    setIfNull(json.measurements.typography.title, 'lineHeight', safeInt(data.title.lineHeight));
    setIfNull(json.measurements.typography.title, 'fontWeight', data.title.fontWeight || null);
    setIfNull(json.measurements.typography.title, 'letterSpacing', safeFloat(data.title.letterSpacing));
    setIfNull(json.measurements.typography.title, 'margin_bottom', safeInt(data.title.margin_bottom));
    // 颜色归入 styles.colors.title
    setIfNull(json.styles.colors, 'title', data.title.color || null);
  }
  // 正文
  if (data.body) {
    json.measurements.typography.body = json.measurements.typography.body || {};
    setIfNull(json.measurements.typography.body, 'fontSize', safeInt(data.body.fontSize));
    setIfNull(json.measurements.typography.body, 'lineHeight', safeInt(data.body.lineHeight));
    setIfNull(json.measurements.typography.body, 'color', data.body.color || null);
    setIfNull(json.styles.colors, 'body', data.body.color || null);
  }

  setIfNull(json.measurements.typography, 'paragraph_spacing', safeInt(data.paragraphSpacing));
  setIfNull(json.measurements.typography, 'list_item_spacing', safeInt(data.listItemSpacing));
  setIfNull(json.measurements.typography, 'link_style', data.linkStyle || null);
  // 列表缩进（如果 schema 未定义，可保存在 measurements.typography.list_indent）
  setIfNull(json.measurements.typography, 'list_indent', safeInt(data.listIndent));

  setIfNull(json.styles.spacing, 'container_padding', data.containerPadding || null);
  setIfNull(json.styles.spacing, 'container_margin', data.containerMargin || null);

  if (data.colors) {
    // 背景为透明时不写入
    const bg = data.colors.background;
    if (bg && !/rgba?\(\s*0\s*,\s*0\s*,\s*0\s*(?:,\s*0\s*)?\)/i.test(bg)) {
      setIfNull(json.styles.colors, 'background', bg);
    }
    setIfNull(json.styles.colors, 'title', data.colors.title || null);
    setIfNull(json.styles.colors, 'body', data.colors.body || null);
    setIfNull(json.styles.colors, 'link', data.colors.link || null);
  }

  writeJson(DESCRIPTION_JSON, json);
  console.log('[description] 已写回（仅覆盖原 null 字段）。');
}

// ========== 工具函数 ==========

function readJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf-8'));
}

function writeJson(p, obj) {
  const content = JSON.stringify(obj, null, 2);
  fs.writeFileSync(p, content, 'utf-8');
}

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const k = a.slice(2);
      const v = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
      out[k] = v;
    }
  }
  return out;
}

function safeInt(v) {
  if (v === null || v === undefined) return null;
  const n = Number(v);
  if (Number.isNaN(n)) return null;
  return Math.round(n);
}

function safeFloat(v) {
  if (v === null || v === undefined) return null;
  const n = Number(v);
  if (Number.isNaN(n)) return null;
  return Number(n.toFixed(2));
}
