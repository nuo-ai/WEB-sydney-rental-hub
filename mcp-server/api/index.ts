import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import {
  CallToolRequestSchema,
  ErrorCode,
  ListToolsRequestSchema,
  McpError,
} from '@modelcontextprotocol/sdk/types.js';
import axios from 'axios';

// This is a Vercel Serverless Function

// GraphQL API配置
const GRAPHQL_ENDPOINT = 'http://127.0.0.1:8000/graphql';

// ... (rest of the SydneyRentalMCP class code from the previous version)
class SydneyRentalMCP {
  private server: Server;
  private axiosInstance;

  constructor() {
    this.server = new Server(
      {
        name: 'sydney-rental-mcp',
        version: '0.1.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.axiosInstance = axios.create({
      baseURL: GRAPHQL_ENDPOINT,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    });

    this.setupToolHandlers();
    
    // 错误处理
    this.server.onerror = (error) => console.error('[MCP Error]', error);
  }

  private setupToolHandlers() {
    // ... (same setupToolHandlers code as before)
  }

  // ... (all the handle... and format... methods as before)

  async handleRequest(req: any, res: any) {
    const requestStr = JSON.stringify(req.body);
    let output = '';
    const transport = {
      send: (data: string) => {
        output += data;
      },
      registerHandler: (handler: (data: string) => void) => {
        handler(requestStr);
      },
      close: () => {},
    };
    
    await this.server.connect(transport as any);
    
    res.status(200).send(output);
  }
}

const mcpServer = new SydneyRentalMCP();

export default async function handler(req: any, res: any) {
  await mcpServer.handleRequest(req, res);
}
