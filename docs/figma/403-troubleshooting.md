# Figma API 403 问题排查与稳定性指南

适用场景
- 访问以下文件节点有时成功、有时 403（Forbidden）：
  - https://www.figma.com/design/lXOwmixlbhaJZWc4w2pk1s/1011-UI-kit?node-id=1-497
  - https://www.figma.com/design/lXOwmixlbhaJZWc4w2pk1s/1011-UI-kit?node-id=1-1220

核心结论
- 403 基本为“令牌所属账号无权限访问该文件”。浏览器可见不代表 API 可读。
- 偶发“有时行有时不行”通常由以下因素导致：用错 PAT、令牌账号权限变化、跨组织权限、缓存与重启后的令牌切换、节点 ID 调整等。

——

一、快速定位令牌账号（必须）
- 目的：找出当前 PAT 对应的 Figma 账号邮箱，并将该邮箱邀请为该文件的 Viewer 以上权限。
- PowerShell（Windows）或 bash（Mac/Linux）执行：
  - PowerShell:
    $headers = @{ "X-Figma-Token" = "YOUR_PAT" }
    Invoke-RestMethod -Headers $headers -Uri "https://api.figma.com/v1/me"
  - bash:
    curl -H "X-Figma-Token: YOUR_PAT" https://api.figma.com/v1/me
- 返回结果中包含 email。到 Figma 文件右上角 Share，邀请此 email 为 Viewer 或更高。

二、最小复现与验证（手动 API 调用）
- 注意：nodeId 中的冒号需要 URL 编码（: → %3A）
- 测试某节点：
  curl -H "X-Figma-Token: YOUR_PAT" "https://api.figma.com/v1/files/lXOwmixlbhaJZWc4w2pk1s/nodes?ids=1%3A1220"
- 若返回 403：
  - 几乎可以确认是权限问题（非限流；限流通常 429）
- 若返回 200：
  - 说明当前 PAT 有权限；若工具仍失败，见第六节“工具稳定性”

三、常见权限误区
- 误区1：文件“Anyone with the link can view（任何人可查看）”即可 → 错。API 仍基于 PAT 账号权限。
- 误区2：邀请了公司域用户，但 PAT 属于个人或其他组织 → PAT 所属账号也必须被邀请。
- 误区3：SSO/团队隔离 → 若文件在组织A，PAT 账号在组织B，仍需明确邀请。
- 误区4：只赋予 Prototype 访问或受限链接 → 需保证是文件 Viewer 及以上。
- 误区5：节点权限/可见性被组件库隔离 → 通常不是 403 的直接原因，但建议确保文件为主文件而非仅外链组件。

四、为何“有时行有时不行”
- 可能原因：
  1) PAT 更换或工具重启后使用了不同 PAT（不同账号权限不同）
  2) 文件共享权限被临时修改（被移除/降级）
  3) 节点 ID 发生变化（例如组件重构、复制后产生新 ID）
  4) 网络代理/防火墙导致请求头丢失或被拦截（罕见）
- 建议：
  - 固化使用同一 PAT，确认其 email 并永久邀请
  - 记录 nodeId 与节点命名，避免频繁调整导致 ID 变更
  - 发生 403 立即用 /v1/me 与 /v1/files/*/nodes 手动验证，切断“工具层干扰”

五、错误码速查
- 401 Unauthorized：PAT 无效或未携带
- 403 Forbidden：PAT 有效但无访问该资源的权限（本次问题）
- 404 Not Found：fileKey/nodeId 不存在或不可见
- 429 Too Many Requests：限流（需退避重试）

六、MCP 工具稳定性建议（针对“有时行”）
- 固定 PAT：在 MCP 启动参数 --figma-api-key 中使用你确认过的 PAT，不要多处切换
- 重启后验证：每次更换 PAT/重启后，先用 /v1/me 与一个已知节点做一次 curl 验证
- URL 编码：nodeId 需编码冒号（工具一般会处理，但手动调试必须编码）
- 指定范围小抓取：先对单一 root node（如 1:1220）抓取，避免全量导致耗时或边界问题
- 记录日志：捕获返回码与响应体，区分权限问题与其他报错

七、临时替代方案（不阻塞设计落地）
- 图标：在 Figma 手动导出 SVG（kebab-case 命名），放入 packages/ui/src/icons/
- Tokens：导出或截图颜色/字体/间距/圆角/阴影清单；我方据此填充 docs/figma/token-draft.md
- 这样可先推进 UI 与 Storybook，对后续自动化不产生冲突

八、恢复自动化后的标准流程
1) 使用确认过权限的 PAT
2) 抓取节点（例如 1:1220、1:497）到 docs/figma/raw.json（结构遵循 raw.schema.json）
3) 更新 docs/figma/token-draft.md 为真实值
4) 生成 icons-checklist.md 节点表，批量下载 SVG 到 packages/ui/src/icons/
5) 可选：新增 Storybook 对照页“Figma 基线映射”

附：常用命令模板（PowerShell）
$headers = @{ "X-Figma-Token" = "YOUR_PAT" }
Invoke-RestMethod -Headers $headers -Uri "https://api.figma.com/v1/me"
Invoke-RestMethod -Headers $headers -Uri "https://api.figma.com/v1/files/lXOwmixlbhaJZWc4w2pk1s/nodes?ids=1%3A1220"
Invoke-RestMethod -Headers $headers -Uri "https://api.figma.com/v1/files/lXOwmixlbhaJZWc4w2pk1s/nodes?ids=1%3A497"

若以上仍无法解决，请将 /v1/me 返回的 email 与当前文件共享面板截图（可打码）对齐，重点核查是否正是该 email 被邀请为 Viewer/Editor。
