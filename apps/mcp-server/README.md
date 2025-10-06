# Sydney Rental MCP Server

悉尼租房 Model Context Protocol (MCP) 服务器，为 AI 助手提供悉尼租房搜索功能。

## 功能特性

- 🏠 **房产搜索**: 根据郊区、价格、房型等条件搜索租房信息
- 📋 **详细信息**: 获取特定房产的详细信息
- 🚌 **通勤计算**: 计算到指定地点的通勤时间和路线
- 🎯 **智能推荐**: 基于用户需求提供个性化房产推荐

> 📁 该包现在位于 `apps/mcp-server/`，作为 Turborepo 工作空间的一部分。

## 安装和运行

### 前置要求

- Node.js 18+
- pnpm 8+

### 安装依赖

```bash
pnpm install
```

### 编译 TypeScript

```bash
pnpm run build
```

### 启动服务器

```bash
pnpm start
```

或直接运行编译后的文件：

```bash
node dist/index.js
```

### 环境变量

复制 `.env.example` 创建 `.env`，配置 GraphQL 与地图密钥：

```bash
cp .env.example .env
```

| 变量名 | 说明 |
| --- | --- |
| `GRAPHQL_ENDPOINT` | 后端 GraphQL 服务地址，例如 `http://127.0.0.1:8000/graphql` |
| `GOOGLE_MAPS_API_KEY` | Google Maps Directions API 密钥 |

## 可用工具

### 1. search_properties

搜索悉尼租房信息

**参数:**
- `suburb` (string, 可选): 郊区名称
- `minPrice` (number, 可选): 最低价格
- `maxPrice` (number, 可选): 最高价格
- `propertyType` (string, 可选): 房产类型
- `bedrooms` (number, 可选): 卧室数量

**示例:**
```json
{
  "suburb": "Surry Hills",
  "minPrice": 400,
  "maxPrice": 800,
  "bedrooms": 2
}
```

### 2. get_property_details

获取房产详细信息

**参数:**
- `propertyId` (string, 必需): 房产ID

**示例:**
```json
{
  "propertyId": "12345"
}
```

## 在 Claude Desktop 中使用

1. 打开 Claude Desktop 配置文件
2. 添加 MCP 服务器配置：

```json
{
  "mcpServers": {
    "sydney-rental": {
      "command": "node",
      "args": ["/path/to/apps/mcp-server/dist/index.js"],
      "env": {}
    }
  }
}
```

3. 重启 Claude Desktop
4. 现在可以询问悉尼租房相关问题了！

## 测试

运行测试脚本验证服务器功能：

```bash
node test-mcp.js
```

## 开发

### 项目结构

```
apps/
└── mcp-server/
    ├── api/
    │   └── index.ts          # 主服务器文件
    ├── dist/                 # 编译输出目录
    ├── package.json
    ├── tsconfig.json
    ├── test-mcp.js           # 测试脚本
    └── README.md
```

### 开发模式

```bash
# 监听文件变化并自动编译
pnpm run dev
```

## 技术栈

- **TypeScript**: 类型安全的 JavaScript
- **@modelcontextprotocol/sdk**: MCP 官方 SDK
- **Axios**: HTTP 客户端
- **Zod**: 运行时类型验证

## API 集成

服务器集成了以下 API：
- 悉尼租房数据 API
- 通勤时间计算 API
- 地理位置服务 API

## 故障排除

### 常见问题

1. **模块导入错误**: 确保 `package.json` 中设置了 `"type": "module"`
2. **TypeScript 编译错误**: 检查 SDK 版本是否为 0.6.1+
3. **服务器无响应**: 确认服务器正在监听 stdio 输入

### 调试

使用测试脚本验证服务器功能：

```bash
node test-mcp.js
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
