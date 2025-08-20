import http from 'http';
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { 
  CallToolRequestSchema, 
  ListToolsRequestSchema,
  CallToolRequest,
  ListToolsRequest 
} from '@modelcontextprotocol/sdk/types.js';
import { z } from 'zod';
import axios from 'axios';

// GraphQL API配置
const GRAPHQL_ENDPOINT = 'http://127.0.0.1:8000/graphql';

// 定义参数验证 schema
const SearchPropertiesSchema = z.object({
  suburb: z.string().optional(),
  minPrice: z.number().optional(),
  maxPrice: z.number().optional(),
  propertyType: z.string().optional(),
  bedrooms: z.number().optional()
});

const PropertyDetailsSchema = z.object({
  propertyId: z.string()
});

type SearchPropertiesArgs = z.infer<typeof SearchPropertiesSchema>;
type PropertyDetailsArgs = z.infer<typeof PropertyDetailsSchema>;

class SydneyRentalMCP {
  private server: Server;
  private axiosInstance: any;

  constructor() {
    this.server = new Server({
      name: 'sydney-rental-mcp',
      version: '0.1.0',
    }, {
      capabilities: {
        tools: {},
      },
    });

    this.axiosInstance = axios.create({
      baseURL: GRAPHQL_ENDPOINT,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    });

    this.setupTools();
  }

  private setupTools() {
    // 注册工具列表处理器
    this.server.setRequestHandler(ListToolsRequestSchema, async (request: ListToolsRequest) => {
      return {
        tools: [
          {
            name: 'search_properties',
            description: '搜索悉尼租房信息',
            inputSchema: {
              type: 'object',
              properties: {
                suburb: { type: 'string', description: '郊区名称' },
                minPrice: { type: 'number', description: '最低价格' },
                maxPrice: { type: 'number', description: '最高价格' },
                propertyType: { type: 'string', description: '房产类型' },
                bedrooms: { type: 'number', description: '卧室数量' }
              }
            }
          },
          {
            name: 'get_property_details',
            description: '获取房产详细信息',
            inputSchema: {
              type: 'object',
              properties: {
                propertyId: { type: 'string', description: '房产ID' }
              },
              required: ['propertyId']
            }
          }
        ]
      };
    });

    // 注册工具调用处理器
    this.server.setRequestHandler(CallToolRequestSchema, async (request: CallToolRequest) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'search_properties': {
            const validatedArgs = SearchPropertiesSchema.parse(args);
            const result = await this.searchProperties(validatedArgs);
            return {
              content: [{
                type: 'text',
                text: JSON.stringify(result, null, 2)
              }]
            };
          }
          case 'get_property_details': {
            const validatedArgs = PropertyDetailsSchema.parse(args);
            const result = await this.getPropertyDetails(validatedArgs.propertyId);
            return {
              content: [{
                type: 'text',
                text: JSON.stringify(result, null, 2)
              }]
            };
          }
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [{
            type: 'text',
            text: `Error: ${error instanceof Error ? error.message : String(error)}`
          }],
          isError: true
        };
      }
    });
  }

  private async searchProperties(filters: SearchPropertiesArgs) {
    const query = `
      query SearchProperties($filters: PropertyFilters) {
        properties(filters: $filters) {
          id
          address
          suburb
          price
          propertyType
          bedrooms
          bathrooms
          parkingSpaces
          description
          images
          features
          lastSeen
        }
      }
    `;

    try {
      const response = await this.axiosInstance.post('', {
        query,
        variables: { filters }
      });

      if (response.data.errors) {
        throw new Error(`GraphQL errors: ${JSON.stringify(response.data.errors)}`);
      }

      return response.data.data.properties;
    } catch (error) {
      console.error('Error searching properties:', error);
      throw error;
    }
  }

  private async getPropertyDetails(propertyId: string) {
    const query = `
      query GetPropertyDetails($id: String!) {
        property(id: $id) {
          id
          address
          suburb
          price
          propertyType
          bedrooms
          bathrooms
          parkingSpaces
          description
          images
          features
          lastSeen
          commuteInfo {
            university
            transportMode
            duration
            distance
          }
        }
      }
    `;

    try {
      const response = await this.axiosInstance.post('', {
        query,
        variables: { id: propertyId }
      });

      if (response.data.errors) {
        throw new Error(`GraphQL errors: ${JSON.stringify(response.data.errors)}`);
      }

      return response.data.data.property;
    } catch (error) {
      console.error('Error getting property details:', error);
      throw error;
    }
  }

  async start() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
  }

  async handleRequest(req: any, res: any) {
    // Vercel Serverless Function handler
    res.status(200).json({ message: 'MCP Server is running' });
  }
}

// 创建服务器实例
const mcpServer = new SydneyRentalMCP();

// 在非生产环境下启动服务器
if (process.env.NODE_ENV !== 'production') {
  mcpServer.start().catch(console.error);
}

// Vercel Serverless Function 导出
export default async function handler(req: any, res: any) {
  return mcpServer.handleRequest(req, res);
}

// 本地开发服务器
if (process.env.NODE_ENV === 'development') {
  const server = http.createServer(async (req, res) => {
    await handler(req, res);
  });

  const port = process.env.PORT || 3001;
  server.listen(port, () => {
    console.log(`MCP Server running on port ${port}`);
  });
}
