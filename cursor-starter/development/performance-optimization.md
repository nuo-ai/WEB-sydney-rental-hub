# 性能优化助手

**使用场景：** 当您需要系统地提高应用程序、API 或特定代码组件的性能时。

**技能水平：** 中级到高级

---

## 复制此提示：

```
我需要帮助优化我的应用程序的性能。请帮助我系统地识别瓶颈并实施性能改进。

## 应用程序上下文：
- **应用程序类型**：[Web 应用、API、移动应用、桌面应用等]
- **技术栈**：[语言、框架、数据库等]
- **当前性能问题**：[加载缓慢、响应时间长、内存使用量大等]
- **性能目标**：[目标响应时间、吞吐量、资源使用量]
- **用户规模**：[当前和预期的用户负载]

## 要分析的性能区域：
[描述您遇到性能问题的具体区域]

## 当前性能指标：
[包含任何现有性能数据——响应时间、内存使用量、CPU 使用量等]

## 性能优化策略：

请提供一个全面的性能优化计划，涵盖：

### 1. 性能分析
- **当前状态评估**：分析现有性能指标
- **瓶颈识别**：识别主要的性能瓶颈
- **分析策略**：推荐分析工具和技术
- **测量基线**：建立性能基线
- **监控设置**：持续性能监控

### 2. 前端性能（如果适用）
- **捆绑包优化**：代码分割、摇树优化、代码压缩
- **资产优化**：图像压缩、延迟加载、CDN 使用
- **渲染性能**：虚拟 DOM 优化、减少重新渲染
- **网络优化**：HTTP/2、资源提示、缓存策略
- **JavaScript 性能**：异步操作、内存管理

### 3. 后端性能
- **API 优化**：减少响应时间、优化负载
- **数据库性能**：查询优化、索引策略
- **缓存实现**：Redis、内存缓存、CDN 缓存
- **连接管理**：连接池、保持活动设置
- **异步处理**：后台作业、消息队列

### 4. 数据库优化
- **查询性能**：慢查询识别和优化
- **索引策略**：常见查询的最佳索引
- **模式优化**：数据库设计改进
- **连接池**：数据库连接管理
- **缓存层**：查询结果缓存、ORM 优化

### 5. 内存优化
- **内存使用分析**：内存泄漏检测和预防
- **垃圾回收**：GC 优化和调整
- **对象池**：可重用对象管理
- **内存分析**：内存分析工具和技术
- **资源清理**：适当的资源释放

### 6. CPU 优化
- **算法优化**：更高效的算法和数据结构
- **计算复杂度**：大 O 分析和改进
- **并行处理**：多线程、异步操作
- **CPU 分析**：识别 CPU 密集型操作
- **优化模式**：缓存、记忆化、延迟评估

### 7. 网络性能
- **API 响应优化**：减少负载大小、压缩
- **HTTP 优化**：保持活动、连接重用、HTTP/2
- **CDN 实现**：内容分发网络设置
- **带宽优化**：图像优化、资产压缩
- **请求减少**：批处理、合并请求

### 8. 缓存策略
- **多级缓存**：浏览器、CDN、应用程序、数据库缓存
- **缓存失效**：智能缓存失效策略
- **缓存预热**：预加载频繁访问的数据
- **缓存大小**：最佳缓存大小配置
- **缓存监控**：缓存命中率和性能指标

### 9. 可伸缩性改进
- **横向扩展**：负载均衡、自动扩展设置
- **纵向扩展**：单实例资源优化
- **数据库扩展**：读副本、分片策略
- **微服务**：服务分解以实现可伸缩性
- **负载测试**：容量规划和压力测试

### 10. 监控和警报
- **性能指标**：关键性能指标 (KPI)
- **实时监控**：应用程序性能监控 (APM)
- **警报配置**：性能下降警报
- **性能仪表盘**：可视化和报告
- **持续监控**：持续性能跟踪

## 代码级优化：

对于我提供的代码，请分析和优化：
- **算法效率**：更高效的算法
- **数据结构选择**：最佳数据结构
- **循环优化**：高效的迭代模式
- **函数优化**：纯函数、记忆化
- **资源管理**：内存和连接清理

## 实施计划：

请提供：
- **优先优化列表**：首先是高影响、低工作量的改进
- **前后对比**：显示性能改进
- **具体代码示例**：优化后的代码实现
- **测量策略**：如何衡量改进成功
- **实施时间表**：建议的实施顺序

## 性能测试：
- **负载测试**：在实际条件下进行压力测试
- **基准创建**：性能基准套件
- **回归测试**：防止性能回归
- **A/B 测试**：比较优化效果
- **持续性能测试**：自动化性能验证

## 工具和技术：
- 推荐性能分析工具
- 建议监控和警报解决方案
- 提供基准测试和负载测试工具
- 推荐优化库和框架

[在此处粘贴您的代码或描述具体的性能问题]

请专注于提供显著性能提升的实用、可衡量的改进。
```

---

## 获得更好结果的提示：

- **包含具体的性能指标**——当前响应时间、内存使用量
- **提及您的性能目标**——目标改进、SLA 要求
- **提供代码示例**——具有性能问题的特定函数或组件
- **包含您的监控设置**——您目前使用的工具
- **指定限制**——预算、时间、向后兼容性要求

# Performance Optimization Assistant

**Use this when:** You need to systematically improve the performance of your application, API, or specific code components.

**Skill Level:** Intermediate to Advanced

---

## Copy This Prompt:

```
I need help optimizing the performance of my application. Please help me systematically identify bottlenecks and implement performance improvements.

## Application Context:
- **Application Type**: [Web app, API, mobile app, desktop app, etc.]
- **Technology Stack**: [Languages, frameworks, databases, etc.]
- **Current Performance Issues**: [Slow loading, high response times, memory usage, etc.]
- **Performance Goals**: [Target response times, throughput, resource usage]
- **User Scale**: [Current and expected user load]

## Performance Areas to Analyze:
[Describe specific areas where you're experiencing performance issues]

## Current Performance Metrics:
[Include any existing performance data - response times, memory usage, CPU usage, etc.]

## Performance Optimization Strategy:

Please provide a comprehensive performance optimization plan that covers:

### 1. Performance Analysis
- **Current State Assessment**: Analyze existing performance metrics
- **Bottleneck Identification**: Identify primary performance bottlenecks
- **Profiling Strategy**: Recommend profiling tools and techniques
- **Measurement Baseline**: Establish performance baselines
- **Monitoring Setup**: Ongoing performance monitoring

### 2. Frontend Performance (if applicable)
- **Bundle Optimization**: Code splitting, tree shaking, minification
- **Asset Optimization**: Image compression, lazy loading, CDN usage
- **Rendering Performance**: Virtual DOM optimization, re-render reduction
- **Network Optimization**: HTTP/2, resource hints, caching strategies
- **JavaScript Performance**: Async operations, memory management

### 3. Backend Performance
- **API Optimization**: Response time reduction, payload optimization
- **Database Performance**: Query optimization, indexing strategies
- **Caching Implementation**: Redis, in-memory caching, CDN caching
- **Connection Management**: Connection pooling, keep-alive settings
- **Async Processing**: Background jobs, message queues

### 4. Database Optimization
- **Query Performance**: Slow query identification and optimization
- **Index Strategy**: Optimal indexing for common queries
- **Schema Optimization**: Database design improvements
- **Connection Pooling**: Database connection management
- **Caching Layer**: Query result caching, ORM optimization

### 5. Memory Optimization
- **Memory Usage Analysis**: Memory leak detection and prevention
- **Garbage Collection**: GC optimization and tuning
- **Object Pooling**: Reusable object management
- **Memory Profiling**: Tools and techniques for memory analysis
- **Resource Cleanup**: Proper resource disposal

### 6. CPU Optimization
- **Algorithm Optimization**: More efficient algorithms and data structures
- **Computational Complexity**: Big O analysis and improvements
- **Parallel Processing**: Multi-threading, async operations
- **CPU Profiling**: Identifying CPU-intensive operations
- **Optimization Patterns**: Caching, memoization, lazy evaluation

### 7. Network Performance
- **API Response Optimization**: Payload size reduction, compression
- **HTTP Optimization**: Keep-alive, connection reuse, HTTP/2
- **CDN Implementation**: Content delivery network setup
- **Bandwidth Optimization**: Image optimization, asset compression
- **Request Reduction**: Batching, combining requests

### 8. Caching Strategies
- **Multi-Level Caching**: Browser, CDN, application, database caching
- **Cache Invalidation**: Smart cache invalidation strategies
- **Cache Warming**: Preloading frequently accessed data
- **Cache Sizing**: Optimal cache size configuration
- **Cache Monitoring**: Cache hit rates and performance metrics

### 9. Scalability Improvements
- **Horizontal Scaling**: Load balancing, auto-scaling setup
- **Vertical Scaling**: Resource optimization for single instances
- **Database Scaling**: Read replicas, sharding strategies
- **Microservices**: Service decomposition for scalability
- **Load Testing**: Capacity planning and stress testing

### 10. Monitoring and Alerting
- **Performance Metrics**: Key performance indicators (KPIs)
- **Real-time Monitoring**: Application performance monitoring (APM)
- **Alert Configuration**: Performance degradation alerts
- **Performance Dashboards**: Visualization and reporting
- **Continuous Monitoring**: Ongoing performance tracking

## Code-Level Optimizations:

For the code I provide, please analyze and optimize:
- **Algorithm Efficiency**: More efficient algorithms
- **Data Structure Selection**: Optimal data structures
- **Loop Optimization**: Efficient iteration patterns
- **Function Optimization**: Pure functions, memoization
- **Resource Management**: Memory and connection cleanup

## Implementation Plan:

Please provide:
- **Prioritized Optimization List**: High-impact, low-effort improvements first
- **Before/After Comparisons**: Show performance improvements
- **Specific Code Examples**: Optimized code implementations
- **Measurement Strategies**: How to measure improvement success
- **Implementation Timeline**: Suggested order of implementation

## Performance Testing:
- **Load Testing**: Stress testing under realistic conditions
- **Benchmark Creation**: Performance benchmark suite
- **Regression Testing**: Preventing performance regressions
- **A/B Testing**: Comparing optimization effectiveness
- **Continuous Performance Testing**: Automated performance validation

## Tools and Techniques:
- Recommend performance profiling tools
- Suggest monitoring and alerting solutions
- Provide benchmarking and load testing tools
- Recommend optimization libraries and frameworks

[PASTE YOUR CODE OR DESCRIBE SPECIFIC PERFORMANCE ISSUES HERE]

Please focus on practical, measurable improvements that provide significant performance gains.
```

---

## Tips for Better Results:

- **Include specific performance metrics** - current response times, memory usage
- **Mention your performance goals** - target improvements, SLA requirements
- **Provide code samples** - specific functions or components with performance issues
- **Include your monitoring setup** - what tools you currently use
- **Specify constraints** - budget, time, backwards compatibility requirements
