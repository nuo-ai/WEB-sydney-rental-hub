# JUWO 桔屋找房 · 样式与 Design Token Code Review 规则（可直接采用）

目的：阻止“硬编码样式”继续蔓延，确保所有新增/修改遵循“品牌蓝 + 中性灰”的 Design Token 体系。  
范围：Vue 组件（template/script/style）、全局样式、局部 scoped 样式、内联样式。

---

## 1. 不可接受（Reject）清单

- 新增/修改中出现以下任意情形，直接 **Request Changes**：
  1) 硬编码颜色字面量：
     - Hex：`#fff/#333/#e5e7eb/#2563eb/#FF5824` 等
     - `rgb()/rgba()/hsl()/hsla()` 任意形式
     - 命名色：`white/black/orange/blue/gray/*grey*/*silver*` 等
  2) 在 **非 CTA 场景** 使用品牌色（例如输入框 `:focus`、下拉项 hover、滚动条等）  
     - 原则：品牌色仅用于 CTA 按钮、文本链接、导航 hover；其余交互态用 **中性灰**。
  3) 在组件内 **私自声明“全局语义变量”**（如 `:root { --color-xxx: ... }`）
     - 新增语义必须先补充至 `src/style.css` 或 `src/styles/design-tokens.css` 的 :root，再被组件使用。
  4) 模板/脚本内联颜色样式：
     - `<div :style="{ color: '#2563eb' }">` / `style="border: 1px solid #e5e7eb"`
  5) 使用非规范变量名：
     - 允许前缀：`--juwo-* | --link-* | --color-* | --text-* | --bg-* | --border-* | --space-* | --radius-* | --shadow-* | --brand-* | --button-* | --chip-* | --panel-* | --list-item-* | --search-* | --clear-* | --checkbox-* | --filter-field-*`
     - 其它自造全局变量名一律拒绝（局部作用域变量例外，但不建议）

---

## 2. 必须要求（Require）清单

- 语义化：所有颜色/边框/背景/阴影/圆角/间距/焦点样式均使用 **Design Token**：
  - 品牌（CTA/链接）：`--juwo-primary | --juwo-primary-light | --juwo-primary-dark | --link-color | --link-hover-color`
  - 文本：`--color-text-primary | --color-text-secondary | --text-tertiary`
  - 背景：`--color-bg-page | --color-bg-card | --bg-hover`
  - 边框：`--color-border-default | --color-border-strong`
  - 焦点/滚动：`--focus-ring-* | --neutral-scrollbar-*`
  - 筛选域：`--panel-* / --chip-* / --list-item-* / --search-* / --filter-field-*`（仅筛选面板域）
- 变更说明：PR 描述必须包含“前端表现”段落（示例见第 5 节模板）
- 渐进式：修改现有文件时，遵循 **童子军军规**（见第 4 节）；范围内顺手替换 1–3 处硬编码为 Token，小步提交。
- 向后兼容：若 Token 更名或切换值会影响大范围，采用“旧名 → 新值”的别名过渡，待稳定后再清理。

---

## 3. 审查要点（Reviewer Checklist）

- [ ] 无硬编码颜色/内联颜色样式
- [ ] CTA/链接使用品牌蓝；其余交互态（hover/focus/滚动条等）为中性灰
- [ ] 所有样式角色映射到 Token（颜色/边框/背景/阴影/圆角/间距/焦点）
- [ ] 若新增语义，已先在 :root 中声明并复用 var()
- [ ] PR 描述包含“前端表现”，并与预期一致
- [ ] 改动范围可回滚（小补丁，无大规模重构）
- [ ] 与 `REFACTORING_TODO.md` 的 backlog 对齐：新增项已登记/完成项已勾选

---

## 4. 童子军军规（Opportunistic Refactoring）

- 每次进入文件修 bug/加功能时，**顺手替换 1–3 处**最明显的硬编码为 Token：
  - 先判断角色（text/border/bg/link/cta/focus）
  - 再替换为对应 Token（如 `--color-text-secondary`、`--link-color`、`--color-border-default`）
  - 回滚成本低，避免一次性大改
- 无法确定语义时：记录到 `REFACTORING_TODO.md`，后续集中处理

---

## 5. PR 模板片段（可加入 .github/pull_request_template.md）

### 变更类型
- [ ] 样式调整（Design Token 合规）
- [ ] 组件 UI 一致性
- [ ] 其它（请说明）

### 本次改动
- 将 XXX 的硬编码颜色替换为 Token（示例：#666666 → var(--color-text-secondary)）
- 统一 XXX 的交互态为中性灰（示例：:hover 边框 → var(--color-border-strong)）
- 链接颜色与 hover 改为 `var(--link-color)` / `var(--link-hover-color)`

### 前端表现
- 示例页面/组件：XXX
- 视觉变化：副标题统一中性灰；分隔线中性化；链接为品牌蓝，hover 深一档；CTA 保持品牌蓝
- 截图（可选）：Before / After

### 回滚策略
- 删除本次提交差异即可回退；未改动 JS/数据流

---

## 6. 工具与脚本建议（团队自选）

- Stylelint（样式自动化检查）
  - 规则：禁止颜色字面量；强制使用变量；Token 文件豁免
  - 推荐脚本：
    - `lint:style`: `stylelint "src/**/*.{css,vue}" --fix`
- ESLint/Vue
  - 规则：`vue/no-inline-styles`（或 PR 审查禁止）
- lint-staged（提交前自动修复）
  - `"*.{css,vue}": "stylelint --fix"`
  - `"*.{js,vue}": "eslint --fix"`

---

## 7. 常见映射对照表（速查）

- `#333333` → `var(--color-text-primary)`（前端表现：主文本色）
- `#666666/#6b7280` → `var(--color-text-secondary)`（前端表现：次要文本/副文案）
- `#e5e7eb/#e3e3e3` → `var(--color-border-default)`（前端表现：分隔线/卡片边界）
- `#f7f8fa` → `var(--bg-hover)`（前端表现：hover 浅灰背景）
- `#2196f3/#1976d2/#2563eb`（旧蓝） → `var(--link-color)` / `var(--juwo-primary)`（视角色而定）
- `outline: 2px solid var(--juwo-primary)`（非 CTA 焦点） → `box-shadow: 0 0 0 var(--focus-ring-width) var(--focus-ring-color)`

---

## 8. 示例（Before → After）

- Before（坏例）
  ```css
  .card { background: #fff; border: 1px solid #e5e7eb; }
  .subtitle { color: #666666; }
  a { color: #2563eb; }
  input:focus { outline: 2px solid var(--juwo-primary); }
  ```
- After（好例）
  ```css
  .card { background: var(--color-bg-card); border: 1px solid var(--color-border-default); }
  .subtitle { color: var(--color-text-secondary); }
  a { color: var(--link-color); }
  a:hover { color: var(--link-hover-color); }
  input:focus-visible { outline: none; box-shadow: 0 0 0 var(--focus-ring-width) var(--focus-ring-color); }
  ```

——  
本规则自发布之日起执行；如需调整 Token 或例外情况，请在 PR 中说明“前端表现”和回滚策略后由 Reviewer 评估。
