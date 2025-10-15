# Domain PDP 仍缺字段清单（features / description）
slug: 8-1-defries-avenue-zetland-nsw-2017-17803938
口径：仅列仍为 null/not_present 或需二次校验的字段；三断点（1440/1024/390）如未特别说明，则同口径缺失。

说明
- fontSize=字号，lineHeight=行高，icon_size=图标尺寸，spacing_icon_text=图标与文字间距，list_indent=列表缩进
- 透明背景（rgba(0,0,0,0)）不作为有效颜色写入

---

## Features（特征列表）
文件：modules/features.json

1) 文本与图标（list.item）
- item.text_fontSize
- item.text_lineHeight
- item.text_color
- item.icon_size
- item.spacing_icon_text

2) 样式（styles）
- colors.text
- colors.icon
- radius.container
- radius.item
- shadows.container
- shadows.item
- view_more_button.typography.letterSpacing（按钮字距，若可稳定获取则写入）

3) 已完成但建议二次核验（跨断点一致性）
- spacing.container_margin（当前已写：{0,0,24,0}）
- spacing.list_padding（当前已写：{0,0,0,0}）
- row_gap = 6、column_gap = 0（复核三断点一致性）

4) 展开态（如存在 “View all features”）
- 展开后列数/间距/高度变化（需要点击后二次采集）

截图入库（模块级）
- modules-level screenshots.*.path 仍为绝对路径（~/Downloads/...）。如需入库，请你先把 PNG 移至：
  docs/blueprints/domain/8-1-defries-avenue-zetland-nsw-2017-17803938/modules/screenshots/
  然后我统一改为相对路径（遵循 file-system-rules）

---

## Description（正文）
文件：modules/description.json

1) 正文与列表/链接
- measurements.typography.body.paragraph_spacing（页面级对照为 18，模块内目前 null 或需对齐确认）
- measurements.typography.body.list_item_spacing（li 与 li 的垂直间距）
- measurements.typography.body.link_style（color、textDecorationLine，hover 可选）
- list_indent（ul/ol 左缩进，paddingLeft 或 marginLeft）

2) 样式（styles）
- colors.link（与 link_style 对齐）
- radius.container
- shadows.container
- colors.background（若为透明或不可测可保持 null）

3) 强调/斜体（如页面出现）
- strong/b.fontWeight
- em/i.fontStyle

截图入库（模块级）
- modules-level screenshots.*.path 仍为绝对路径（~/Downloads/...）。如需入库，请你先把 PNG 移至：
  docs/blueprints/domain/8-1-defries-avenue-zetland-nsw-2017-17803938/modules/screenshots/
  然后我统一改为相对路径

---

## 建议执行顺序（自动/半自动）
1) 运行脚本补齐 features 与 description 的“可测量 null 字段”，优先 1440→1024→390
2) 若有展开态，执行展开后二次采集（features / description）
3) 统一更新模块级 screenshots.*.path 为相对路径（待你移动 PNG 后）
4) 复核 compare-1440-1024-390.md 与 coverage-checklist.md，勾选新增“已覆盖”项

备注
- 脚本仅覆盖 null，安全可复跑；确实不存在标注 not_present；透明背景不写入
+ 