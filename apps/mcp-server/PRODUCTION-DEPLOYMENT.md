# 🏭 生产环境部署指南

## 📋 部署架构概览

### 当前开发环境 vs 生产环境

```
开发环境 (MCP服务器):
Cline ──▶ MCP Server ──▶ GraphQL API ──▶ PostgreSQL

生产环境 (微服务架构):
Frontend ──▶ API Gateway ──▶ REST API ──▶ GraphQL API ──▶ PostgreSQL
    │              │           │             │
    │              │           │             └── Redis (缓存)
    │              │           └── 监控&日志
    │              └── 负载均衡&SSL
    └── CDN (Netlify/Vercel)
```

## 🚀 部署选项

### 1. **云平台部署 (推荐)**

#### A. Railway 部署
```bash
# 1. 安装 Railway CLI
npm install -g @railway/cli

# 2. 登录
railway login

# 3. 初始化项目
railway init

# 4. 配置环境变量
railway variables set NODE_ENV=production
railway variables set GRAPHQL_ENDPOINT=https://your-api.railway.app/graphql
railway variables set ALLOWED_ORIGINS=https://your-frontend.netlify.app

# 5. 部署
railway up
```

#### B. Render 部署
1. 连接GitHub仓库
2. 选择 `production-server.js` 作为启动文件
3. 设置环境变量
4. 部署完成

#### C. Vercel 部署
```bash
# 1. 安装 Vercel CLI
npm i -g vercel

# 2. 部署
vercel --prod

# 3. 配置环境变量
vercel env add GRAPHQL_ENDPOINT
vercel env add ALLOWED_ORIGINS
```

### 2. **Docker 容器化部署**

```bash
# 1. 构建镜像
docker build -t sydney-rental-api .

# 2. 运行容器
docker run -d \
  --name sydney-rental-api \
  -p 3001:3001 \
  --env-file .env.production \
  sydney-rental-api

# 3. 使用 Docker Compose
docker-compose up -d
```

### 3. **Kubernetes 部署**

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sydney-rental-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sydney-rental-api
  template:
    metadata:
      labels:
        app: sydney-rental-api
    spec:
      containers:
      - name: api
        image: sydney-rental-api:latest
        ports:
        - containerPort: 3001
        env:
        - name: NODE_ENV
          value: "production"
        - name: GRAPHQL_ENDPOINT
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: graphql-endpoint
---
apiVersion: v1
kind: Service
metadata:
  name: sydney-rental-api-service
spec:
  selector:
    app: sydney-rental-api
  ports:
  - port: 80
    targetPort: 3001
  type: LoadBalancer
```

## 🔒 安全配置

### 1. 环境变量管理
```bash
# 使用密钥管理服务
# AWS Secrets Manager / Azure Key Vault / Google Secret Manager

# 运行时加载
const secrets = await getSecrets();
process.env.DB_PASSWORD = secrets.DB_PASSWORD;
```

### 2. API认证
```javascript
// 在 production-server.js 中添加
const jwt = require('jsonwebtoken');

// JWT认证中间件
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: '需要访问令牌' });
  }
  
  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) return res.status(403).json({ error: '无效令牌' });
    req.user = user;
    next();
  });
};

// 保护路由
app.use('/api/', authenticateToken);
```

### 3. HTTPS和SSL
```nginx
# Nginx 配置
server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 监控和日志

### 1. 应用监控
```javascript
// 集成 Winston 日志
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

// 集成 Sentry 错误追踪
const Sentry = require('@sentry/node');
Sentry.init({ dsn: process.env.SENTRY_DSN });
```

### 2. 性能监控
```javascript
// 集成 New Relic / DataDog
const newrelic = require('newrelic');

// 自定义指标
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    logger.info('Request completed', {
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration
    });
  });
  next();
});
```

## 🔄 CI/CD 流水线

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        uses: railwayapp/railway-deploy-action@v1
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: sydney-rental-api
```

## 📈 扩展性考虑

### 1. 水平扩展
```yaml
# Docker Compose 多实例
version: '3.8'
services:
  api:
    image: sydney-rental-api
    deploy:
      replicas: 3
    ports:
      - "3001-3003:3001"
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

### 2. 缓存策略
```javascript
// Redis 缓存
const redis = require('redis');
const client = redis.createClient(process.env.REDIS_URL);

// 缓存搜索结果
app.post('/api/properties/search', async (req, res) => {
  const cacheKey = `search:${JSON.stringify(req.body)}`;
  
  // 检查缓存
  const cached = await client.get(cacheKey);
  if (cached) {
    return res.json(JSON.parse(cached));
  }
  
  // 执行搜索
  const results = await performSearch(req.body);
  
  // 缓存结果 (5分钟)
  await client.setex(cacheKey, 300, JSON.stringify(results));
  
  res.json(results);
});
```

## 💰 成本优化

### 1. 服务器选择
- **开发/测试**: Railway Free Tier, Render Free
- **小规模生产**: Railway Pro ($5/月), Render Starter ($7/月)
- **中等规模**: DigitalOcean Droplet ($12/月), AWS t3.small
- **大规模**: AWS/GCP/Azure 企业级服务

### 2. 数据库优化
```sql
-- 添加索引优化查询
CREATE INDEX idx_properties_university_commute 
ON properties_commute (university_name, walk_time_minutes);

CREATE INDEX idx_properties_rent_bedrooms 
ON properties (rent_pw, bedrooms) 
WHERE is_active = true;
```

## 🚨 灾难恢复

### 1. 数据备份
```bash
# 自动化数据库备份
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump $DATABASE_URL > backup_$DATE.sql
aws s3 cp backup_$DATE.sql s3://your-backup-bucket/
```

### 2. 健康检查
```javascript
// 高级健康检查
app.get('/health', async (req, res) => {
  const health = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    version: process.env.npm_package_version
  };
  
  // 检查数据库连接
  try {
    await graphqlClient.post('', {
      query: 'query { __typename }'
    });
    health.database = 'connected';
  } catch (error) {
    health.database = 'disconnected';
    health.status = 'degraded';
  }
  
  res.status(health.status === 'ok' ? 200 : 503).json(health);
});
```

## 📋 部署检查清单

### 🔍 部署前检查
- [ ] 环境变量已配置
- [ ] SSL证书已安装
- [ ] 数据库迁移已执行
- [ ] 安全扫描已通过
- [ ] 负载测试已完成

### 🚀 部署后验证
- [ ] 健康检查端点响应正常
- [ ] API功能测试通过
- [ ] 监控指标正常
- [ ] 日志输出正确
- [ ] 性能指标达标

### 📊 持续监控
- [ ] 错误率 < 1%
- [ ] 响应时间 < 500ms
- [ ] 可用性 > 99.9%
- [ ] CPU使用率 < 70%
- [ ] 内存使用率 < 80%

## 🎯 总结

MCP服务器投入生产环境需要：

1. **架构转换**: MCP → REST API
2. **容器化**: Docker + Kubernetes
3. **安全加固**: HTTPS + JWT + 速率限制
4. **监控告警**: 日志 + 指标 + 错误追踪
5. **CI/CD**: 自动化测试 + 部署
6. **扩展性**: 负载均衡 + 缓存 + 数据库优化

遵循以上步骤，您的MCP服务器就能稳定运行在生产环境中！
