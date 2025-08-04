import http from 'http';
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
  // Vercel's `req` is a stream, but we need to parse the body for local dev.
  // This is a simplified body parser for local testing.
  if (typeof req.body === 'undefined' && req.method === 'POST') {
    let body = '';
    req.on('data', (chunk: Buffer) => {
      body += chunk.toString();
    });
    req.on('end', async () => {
      try {
        req.body = JSON.parse(body);
        await mcpServer.handleRequest(req, res);
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Invalid JSON' }));
      }
    });
  } else {
    await mcpServer.handleRequest(req, res);
  }
}

// Local development server - only runs when not in a serverless environment
if (process.env.NODE_ENV !== 'production') {
  const PORT = process.env.PORT || 3002; // Use a different port to avoid conflicts
  const localServer = http.createServer(async (req, res) => {
    // A mock response object for Vercel-like environment
    const mockRes = {
      statusCode: 200,
      headers: {} as Record<string, string>,
      body: '',
      status: function(code: number) {
        this.statusCode = code;
        return this;
      },
      send: function(data: any) {
        this.body = data;
        res.writeHead(this.statusCode, this.headers);
        res.end(this.body);
      },
      json: function(data: any) {
        this.setHeader('Content-Type', 'application/json');
        this.body = JSON.stringify(data);
        res.writeHead(this.statusCode, this.headers);
        res.end(this.body);
      },
      setHeader: function(name: string, value: string) {
        this.headers[name] = value;
      },
      writeHead: function(statusCode: number, headers: Record<string, string>) {
        res.writeHead(statusCode, headers);
      },
      end: function(data: any) {
        res.end(data);
      }
    };
    await handler(req, mockRes as any);
  });

  localServer.listen(PORT, () => {
    console.log(`[Local MCP Server] Running for development at http://localhost:${PORT}`);
    console.log('This server simulates a Vercel environment for the serverless function.');
  });
}
