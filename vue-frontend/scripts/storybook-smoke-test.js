#!/usr/bin/env node
import { spawn } from 'node:child_process'
import process from 'node:process'

const command = process.platform === 'win32' ? 'npm.cmd' : 'npm'
const args = ['run', 'storybook', '--', '--ci', '--smoke-test']

const child = spawn(command, args, {
  stdio: 'inherit',
  cwd: process.cwd(),
  env: {
    ...process.env,
    STORYBOOK_LOCALSTORAGE_MOCK: 'true',
  },
})

child.on('exit', (code) => {
  process.exit(code ?? 1)
})
