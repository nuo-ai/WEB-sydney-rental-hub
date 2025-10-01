# Implementation Plan

[Overview]
目标：将 MarkItDown MCP 使用“系统/用户级安装 + Cline 全局配置”的标准方式接入，避免在项目仓库内安装或克隆任何 MCP 代码，统一采用 STDIO 传输，保证稳定、可复用与最小耦合。

背景与范围：
- 之前曾在项目目录或临时目录克隆/运行 MCP 服务（不合规，易污染仓库且不可复用）。
- 本方案改为“命令化”启动：官方 Python 包通过 pipx 安装为全局可执行（markitdown-mcp），或使用 npx 包装器（markitdown-mcp-npx）零维护运行。二者均不依赖项目路径。
- Cline 层面采用“全局 MCP 设置”（cline_mcp_settings.json，经由 UI 打开编辑），登记 STDIO 启动命令，项目仓库内不再保存 MCP 服务器配置（可清理 add-mcp-server.json 的 markitdown 项）。

高层做法：
- 官方推荐：pipx install markitdown-mcp → Cline 全局配置中登记 command=markitdown-mcp（STDIO，args=[]）。
- 备选：npx -y markitdown-mcp-npx → Cline 全局配置中登记 command=npx args=["-y","markitdown-mcp-npx"]（STDIO）。
- 如需网络访问/共享，可切到 HTTP/SSE，但优先 STDIO（简单、低延迟、无端口暴露）。

[Types]  
不涉及业务类型系统，仅涉及 Cline MCP 配置 JSON 结构。

配置对象结构（STDIO 传输）：
- mcpServers: object
  - <serverName>: object
    - command: string（可执行名或运行时入口，如 "markitdown-mcp" 或 "npx"）
    - args: string[]（命令参数；无参时为空数组）
    - env?: object（可选，环境变量键值对）
    - alwaysAllow?: string[]（可选，默认允许工具列表）
    - disabled?: boolean（可选，启停开关）

[Files]
本方案不修改业务源码，仅触达配置与文档：
- 全局设置（由 Cline 托管）：cline_mcp_settings.json
  - 打开方式：Cline 侧边栏 → MCP Servers → Installed → Configure MCP Servers / Advanced MCP Settings
  - 写入/更新 “markitdown” 服务器配置（STDIO）
- 项目仓库（本次新增）：
  - implementation_plan.md（当前文件，方案说明）
- 项目仓库（可选清理）：
  - add-mcp-server.json 中的 “markitdown” 项（建议移除，避免与全局配置重复）

[Functions]
此处“函数”指运维命令与操作步骤：
- 官方安装（推荐，Python 包 + pipx）：
  - 安装：pipx install markitdown-mcp
  - 验证：markitdown-mcp --help
- 备选安装（npx 包装器，无需 Python 维护）：
  - 运行/验证：npx -y markitdown-mcp-npx --help
- Cline 全局 STDIO 配置示例（推荐）：
  ```
  {
    "mcpServers": {
      "markitdown": {
        "command": "markitdown-mcp",
        "args": []
      }
    }
  }
  ```
- Cline 全局 STDIO 配置（npx 备选）：
  ```
  {
    "mcpServers": {
      "markitdown": {
        "command": "npx",
        "args": ["-y", "markitdown-mcp-npx"]
      }
    }
  }
  ```
- 可选 HTTP/SSE（不推荐作为默认）：
  - markitdown-mcp --http --host 127.0.0.1 --port 3001
  - 对应 Cline 可配为 SSE 远程 URL，但本地优先 STDIO。

[Classes]
无类/面向对象改动。

[Dependencies]
- 新增/确认依赖：
  - pipx（系统/用户级）与 markitdown-mcp（官方 Python 包）
  - 备选：npx 包装器 markitdown-mcp-npx（第三方）
- 可选系统依赖：
  - ffmpeg（当需要音频相关处理时，pydub 会提示；安装：sudo apt install -y ffmpeg）

[Testing]
- 本地命令验证：
  - markitdown-mcp --help 输出正常，说明可执行已安装（pipx 路径通常位于 ~/.local/bin/）
- Cline 验证：
  - 打开 Cline → MCP Servers → Installed → Configure MCP Servers
  - 在 cline_mcp_settings.json 中确认 “markitdown” 项（STDIO）
  - 启用并重启该服务器，查看工具列表
- 工具验证：
  - 使用 MCP Inspector 或直接通过对话调用 markitdown 的文档转 Markdown 能力（PDF/DOCX/图片/Excel 等）

[Implementation Order]
1) 确认 pipx 已安装（若无则安装）；确认 markitdown-mcp 已通过 pipx 安装（或执行安装）
2) 在 Cline UI 打开全局 cline_mcp_settings.json
3) 写入/确认 STDIO 配置：
   - "markitdown": { "command": "markitdown-mcp", "args": [] }
4) 在 Cline “Installed” 列表启用 markitdown 并重启服务器，验证工具可用
5) 清理项目内重复配置（建议删除 add-mcp-server.json 中 “markitdown” 节点，避免歧义）
6) 可选：安装 ffmpeg 以启用音频处理
7) 回归测试：转多种文档到 Markdown，观察日志与输出质量
