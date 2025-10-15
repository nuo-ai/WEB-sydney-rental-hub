# Domain PDP 覆盖清单（features / description）
slug: 8-1-defries-avenue-zetland-nsw-2017-17803938

目的
- 用“是否已覆盖”的清单，直观看出还有哪些要补，避免遗漏。
- 三断点（1440/1024/390）均按相同口径记录。

总体状态
- features（特征列表）：核心布局与按钮、容器内边距已覆盖；文本/图标/颜色与若干样式项待补。
- description（正文）：标题/正文/段落间距/容器内边距已覆盖；链接样式、列表项间距/缩进、颜色与若干样式项待补。

---

Features（特征列表）
- 选择器与截图
  - [x] selectors.primaryContainer（[data-testid="listing-details__additional-features"]）
  - [x] selectors.itemSelector（[data-testid="listing-details__additional-features-listing"]）
  - [x] selectors.viewMoreSelector（[data-testid="expander-view-more-link"]）
  - [x] screenshots 1440/1024/390（已保存到 Downloads，待相对路径入库）

- 度量（measurements.list / view_more_button）
  - [x] columns_1440 = 3
  - [x] columns_1024 = 3
  - [x] columns_390 = 2
  - [x] row_gap ≈ 6px
  - [x] column_gap ≈ 0px
  - [x] item_height ≈ 24px
  - [ ] item.text_fontSize
  - [ ] item.text_lineHeight
  - [ ] item.text_color
  - [ ] item.icon_size
  - [ ] item.spacing_icon_text
  - [x] view_more_button.rect ≈ 123×42（x≈220, y≈1086）
  - [x] view_more_button.typography.fontSize = 16
  - [x] view_more_button.typography.fontWeight = 400
  - [ ] view_more_button.typography.letterSpacing

- 样式（styles）
  - [x] spacing.container_padding = { top:0, right:10, bottom:0, left:10 }
  - [x] spacing.container_margin
  - [x] spacing.container_margin
  - [x] spacing.list_padding
  - [ ] colors.background
  - [ ] colors.text
  - [ ] colors.icon
  - [x] colors.view_more_text
  - [ ] radius.container
  - [ ] radius.item
  - [ ] shadows.container
  - [ ] shadows.item
  - [ ] typography.title（若有分组标题时）

- 展开态（若存在 “View all features”）
  - [ ] 展开后再次截图（三断点）
  - [ ] 展开后列数/间距/高度变化记录

补齐计划（脚本自动/半自动）
- 回填 item 文本/图标与间距（text_fontSize/lineHeight/color、icon_size、spacing_icon_text）
- 回填 colors/radius/shadows/spacing.*（可计算即回填，无法可靠计算则标 not_present 或保留 null）
- 若存在标题与展开态，补充标题 typography 与展开后的二次度量

---

Description（正文）
- 选择器与截图
  - [x] selectors.primaryContainer（[data-testid="listing-details__description"]）
  - [x] selectors.titleSelector（[data-testid="listing-details__description-headline"]）
  - [x] selectors.readMoreSelector（[data-testid="listing-details__description-button"]）
  - [x] screenshots 1440/1024/390（已保存到 Downloads，待相对路径入库）

- 度量（measurements.container / typography）
  - [x] container.width ≈ 659
  - [x] container.height ≈ 235
  - [x] typography.title.fontSize = 16
  - [x] typography.title.lineHeight = 24
  - [x] typography.title.fontWeight = 700
  - [x] typography.title.margin_bottom ≈ 18
  - [x] typography.body.fontSize = 16
  - [x] typography.body.lineHeight = 24
  - [x] typography.body.color ≈ rgb(60,71,91)
  - [x] typography.paragraph_spacing ≈ 18
  - [ ] typography.list_item_spacing（li 与 li 垂直间距）
  - [ ] typography.link_style（color/textDecoration，含 hover 可选）
  - [ ] list_indent（ul/ol 左缩进，如需）

- 样式（styles）
  - [x] spacing.container_padding = { top:0, right:10, bottom:0, left:10 }
  - [ ] spacing.container_margin
  - [ ] colors.background
  - [x] colors.title
  - [x] colors.body
  - [ ] colors.link（与 link_style 对齐）
  - [ ] radius.container
  - [ ] shadows.container
  - [ ] 强调/斜体：strong/b.fontWeight、em/i.fontStyle（若出现）

- 展开态（若正文折叠）
  - [ ] 点击 readMore 再次截图
  - [ ] 展开后段落/列表项间距、链接样式变化复测

补齐计划（脚本自动/半自动）
- 回填 link_style（color、textDecoration，hover 可选）、list_item_spacing、list_indent
- 回填 colors.* 与 container_margin、radius/shadows（卡片化时）
- 如有强调/斜体，采集相关样式

---

入库与路径（合规）
- [x] 你手动将 Downloads 的 PNG 移动到：docs/blueprints/domain/8-1-defries-avenue-zetland-nsw-2017-17803938/screenshots/
- [ ] 我批量将 JSON 中 screenshots.*.path 替换为相对路径（遵守 file-system-rules）

备注
- 我们只覆盖“可验证”的字段；无法可靠自动抽取的字段保持 null，避免误差；若确实不存在则标注 not_present。
- 跑数脚本：scripts/blueprint/backfill-c.js（支持三断点与容错，后续将扩展点名选择器采样）。
