# 使用官方 Node.js 18 Alpine 镜像
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apk add --no-cache \
    dumb-init \
    && addgroup -g 1001 -S nodejs \
    && adduser -S nodejs -u 1001

# 复制 package.json 和 package-lock.json
COPY production-package.json package.json
COPY package-lock.json* ./

# 安装生产依赖
RUN npm ci --only=production && npm cache clean --force

# 复制应用代码
COPY production-server.js ./
COPY .env.production .env

# 设置权限
RUN chown -R nodejs:nodejs /app
USER nodejs

# 暴露端口
EXPOSE 3001

# 使用 dumb-init 作为初始化进程
ENTRYPOINT ["dumb-init", "--"]

# 启动应用
CMD ["node", "production-server.js"]

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3001/health', (res) => { process.exit(res.statusCode === 200 ? 0 : 1) })"
