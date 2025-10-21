#!/usr/bin/env node

// Test script to verify MCP server connections
const { spawn } = require('child_process');
const path = require('path');

console.log('Testing MCP Server Connections...\n');

// Test MCP Task Manager
console.log('1. Testing MCP Task Manager...');
const taskManagerPath = path.join(__dirname, 'apps', 'mcp-taskmanager', 'dist', 'index.js');
const taskManager = spawn('C:\\nvm4w\\nodejs\\node.exe', [taskManagerPath], {
  stdio: ['pipe', 'pipe', 'pipe']
});

let taskManagerReady = false;

taskManager.stdout.on('data', (data) => {
  const output = data.toString();
  if (output.includes('Task Manager MCP Server running')) {
    console.log('✅ MCP Task Manager started successfully');
    taskManagerReady = true;
    taskManager.kill();
  }
});

taskManager.stderr.on('data', (data) => {
  console.error('❌ MCP Task Manager error:', data.toString());
});

taskManager.on('close', (code) => {
  if (!taskManagerReady) {
    console.log('⚠️  MCP Task Manager closed with code:', code);
  }
});

// Test MCP Server
console.log('\n2. Testing MCP Server...');
const mcpServerPath = path.join(__dirname, 'apps', 'mcp-server', 'dist', 'index.js');
const mcpServer = spawn('C:\\nvm4w\\nodejs\\node.exe', [mcpServerPath], {
  stdio: ['pipe', 'pipe', 'pipe']
});

let mcpServerReady = false;

mcpServer.stdout.on('data', (data) => {
  const output = data.toString();
  if (output.includes('Express server for REST API running')) {
    console.log('✅ MCP Server started successfully');
    mcpServerReady = true;
    mcpServer.kill();
  }
});

mcpServer.stderr.on('data', (data) => {
  console.error('❌ MCP Server error:', data.toString());
});

mcpServer.on('close', (code) => {
  if (!mcpServerReady) {
    console.log('⚠️  MCP Server closed with code:', code);
  }
});

// Test Uni-app-x MCP
console.log('\n3. Testing Uni-app-x MCP...');
const uniAppPath = path.join(__dirname, 'node_modules', 'uni-app-x-mcp', 'index');
const uniAppMcp = spawn('C:\\nvm4w\\nodejs\\node.exe', [uniAppPath], {
  stdio: ['pipe', 'pipe', 'pipe']
});

let uniAppReady = false;

uniAppMcp.stdout.on('data', (data) => {
  const output = data.toString();
  if (output.includes('MCP') || output.includes('server')) {
    console.log('✅ Uni-app-x MCP started successfully');
    uniAppReady = true;
    uniAppMcp.kill();
  }
});

uniAppMcp.stderr.on('data', (data) => {
  console.error('❌ Uni-app-x MCP error:', data.toString());
});

uniAppMcp.on('close', (code) => {
  if (!uniAppReady) {
    console.log('⚠️  Uni-app-x MCP closed with code:', code);
  }
});

// Timeout after 10 seconds
setTimeout(() => {
  console.log('\n✨ MCP Connection Test Complete');
  process.exit(0);
}, 10000);
