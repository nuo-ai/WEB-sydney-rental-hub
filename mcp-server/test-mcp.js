#!/usr/bin/env node

// Simple test script to verify MCP server functionality
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Start the MCP server
const serverPath = join(__dirname, 'build', 'index.js');
const server = spawn('node', [serverPath], {
  stdio: ['pipe', 'pipe', 'pipe']
});

let responseData = '';

// Listen for server output
server.stdout.on('data', (data) => {
  responseData += data.toString();
  console.log('Server response:', data.toString());
});

server.stderr.on('data', (data) => {
  console.error('Server error:', data.toString());
});

// Send initialization request
const initRequest = {
  jsonrpc: '2.0',
  id: 1,
  method: 'initialize',
  params: {
    protocolVersion: '2024-11-05',
    capabilities: {
      tools: {}
    },
    clientInfo: {
      name: 'test-client',
      version: '1.0.0'
    }
  }
};

console.log('Sending initialization request...');
server.stdin.write(JSON.stringify(initRequest) + '\n');

// Send tools/list request after a delay
setTimeout(() => {
  const toolsRequest = {
    jsonrpc: '2.0',
    id: 2,
    method: 'tools/list'
  };
  
  console.log('Sending tools/list request...');
  server.stdin.write(JSON.stringify(toolsRequest) + '\n');
}, 1000);

// Clean up after 5 seconds
setTimeout(() => {
  console.log('Test completed. Terminating server...');
  server.kill();
  process.exit(0);
}, 5000);

server.on('close', (code) => {
  console.log(`Server process exited with code ${code}`);
});