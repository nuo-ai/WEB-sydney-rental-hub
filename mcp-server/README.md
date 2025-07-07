# Sydney Rental MCP Server

为Cline提供悉尼租房搜索功能的MCP服务器。

## 🎯 功能特色

- **结构化搜索**: 精准的大学通勤时间搜索
- **房源详情**: 获取完整的房源信息
- **大学对比**: 比较多个大学附近的租房情况
- **中文支持**: 完全中文界面和输出

## 🛠️ 安装步骤

### 1. 安装依赖
```bash
cd sydney-rental-mcp
npm install
```

### 2. 构建项目
```bash
npm run build
```

### 3. 确保后端运行
确保您的FastAPI GraphQL服务器正在运行：
```bash
# 在 rentalAU_mcp 目录下
uvicorn server.main:app --reload
```
服务器应该运行在 `http://127.0.0.1:8000`

## ⚙️ 配置到Cline

### 方法1: 添加到Cline MCP配置

编辑文件：`c:\Users\nuoai\AppData\Roaming\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`

添加配置：
```json
{
  "mcpServers": {
    "sydney-rental": {
      "command": "node", 
      "args": ["C:/Users/nuoai/Desktop/WEB-sydney-rental-hub/sydney-rental-mcp/build/index.js"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### 方法2: 如果配置文件已存在其他服务器

读取现有配置并添加新服务器到 `mcpServers` 对象中。

## 📝 使用方法

配置完成后，在Cline中可以使用以下命令：

### 基础搜索
```text
搜索UNSW附近的房源，通勤25分钟内，1房，900以内
```

### 具体工具调用

#### 1. search_properties_structured
精准搜索房源：
```json
{
  "university": "UNSW",
  "max_commute_minutes": 25,
  "bedrooms": 1,
  "max_rent_pw": 900
}
```

#### 2. get_property_detail  
获取房源详情：
```json
{
  "listing_id": "14336181"
}
```

#### 3. compare_universities
对比大学：
```json
{
  "universities": ["UNSW", "USYD"],
  "bedrooms": 1,
  "max_rent_pw": 1000
}
```

## 🎓 支持的大学

- **UNSW** - 新南威尔士大学
- **USYD** - 悉尼大学  
- **UTS** - 悉尼科技大学
- **MACQUARIE** - 麦考瑞大学
- **WSU** - 西悉尼大学

## 📊 输出格式

### 搜索结果示例
```text
🎯 搜索条件:
大学: UNSW
通勤时间: ≤25分钟
房型: 1房
价格: ≤$900/周

📍 找到 8 个符合条件的房源:

[1] 房源信息
💰 $850/周 | 🏠 1房1卫 | 📍 Kingsford
🚶 步行15分钟到UNSW
📅 可入住: 2025-01-15
🏡 地址: 66-68 Barker Street, Kingsford NSW 2032
🔗 房源ID: 14336181
---

📈 搜索统计:
• 平均租金: $865/周
• 最近距离: 15分钟步行
• 搜索类型: 大学通勤
```

## 🔧 故障排除

### 常见问题

**1. MCP服务器无法连接**
- 检查build目录是否存在且包含index.js
- 确认路径配置正确
- 重启Cline

**2. GraphQL连接失败**
- 确认FastAPI服务器运行在 http://127.0.0.1:8000
- 测试GraphQL端点：`http://127.0.0.1:8000/graphql`

**3. 无搜索结果**
- 检查数据库是否有数据
- 尝试放宽搜索条件

### 测试连接
```bash
# 测试FastAPI服务器
curl http://127.0.0.1:8000/

# 测试GraphQL
curl -X POST http://127.0.0.1:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"query { __typename }"}'
```

## 📚 开发信息

### 项目结构
```
sydney-rental-mcp/
├── package.json          # 项目配置
├── tsconfig.json         # TypeScript配置
├── README.md            # 使用说明
├── src/
│   └── index.ts         # 主服务器文件
└── build/
    └── index.js         # 编译后的文件
```

### 技术栈
- **TypeScript**: 开发语言
- **@modelcontextprotocol/sdk**: MCP SDK
- **axios**: HTTP客户端
- **Node.js**: 运行环境

## 🚀 使用场景示例

### 学生找房
```text
用户: "帮我找离UNSW 25分钟内的一房，预算900以内"
Cline: 调用search_properties_structured工具...
结果: 显示符合条件的房源列表
```

### 房源对比
```text  
用户: "比较UNSW和USYD附近的1房价格"
Cline: 调用compare_universities工具...
结果: 显示对比表格和统计信息
```

### 详情查询
```text
用户: "房源14336181的详细信息"
Cline: 调用get_property_detail工具...
结果: 显示完整房源信息
```

## 📞 技术支持

如遇问题，请检查：
1. FastAPI服务器状态
2. MCP配置路径
3. 构建文件完整性
4. 网络连接状况

---

**版本**: 0.1.0  
**作者**: Sydney Rental Hub  
**更新**: 2025年7月
