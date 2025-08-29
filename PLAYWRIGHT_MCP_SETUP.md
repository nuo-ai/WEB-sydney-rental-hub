# Playwright MCP 安装配置说明

## 安装完成时间
2025-01-29

## 配置内容

### 1. Claude 配置文件更新
位置：`C:\Users\nuoai\AppData\Roaming\Claude\config.json`

已添加 Playwright MCP 服务器配置：
```json
"playwright": {
  "command": "npx",
  "args": [
    "-y",
    "@playwright/mcp@latest",
    "--isolated",
    "--storage-state=C:/Users/nuoai/AppData/Roaming/Claude/playwright-storage/storage.json"
  ]
}
```

### 2. 存储状态文件
创建了存储目录和文件：
- 目录：`C:\Users\nuoai\AppData\Roaming\Claude\playwright-storage\`
- 文件：`storage.json`（用于保存浏览器会话状态）

### 3. 项目依赖安装
在项目中安装了 Playwright 测试框架：
```bash
npm install -D @playwright/test playwright
```

## 使用说明

### 重启 Claude Desktop
配置完成后，需要重启 Claude Desktop 应用才能加载新的 MCP 服务器。

### 验证安装
重启后，Playwright MCP 将自动加载，你可以在 Claude 中使用 Playwright 相关功能进行：
- 网页自动化测试
- UI 测试
- 截图和录屏
- 跨浏览器测试

### 参数说明
- `--isolated`：在隔离环境中运行，提高安全性
- `--storage-state`：指定存储状态文件路径，用于保存登录状态等会话信息
- `-y`：自动安装最新版本，无需确认

## 注意事项
1. 首次使用时可能需要下载浏览器驱动，这可能需要一些时间
2. storage.json 文件会自动保存浏览器的 cookies 和 localStorage 数据
3. 如果遇到权限问题，请确保 Claude Desktop 有访问相应目录的权限

## 故障排除
如果 MCP 服务器无法启动，可以尝试：
1. 检查 Node.js 是否正确安装
2. 手动运行 `npx @playwright/mcp@latest` 测试是否能正常启动
3. 查看 Claude Desktop 的日志文件了解详细错误信息