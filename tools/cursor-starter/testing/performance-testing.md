# 性能测试助手

**使用场景：** 当您需要测试应用程序在负载、压力和各种条件下的性能，以确保其满足性能要求时。

**技能水平：** 中级到高级

---

## 复制此提示：

```
我需要帮助为我的应用程序创建全面的性能测试。请帮助我设计和实施负载测试、压力测试和性能基准测试策略。

## 应用程序上下文：
- **应用程序类型**：[Web 应用、API、移动后端等]
- **技术栈**：[语言、框架、数据库、基础设施]
- **预期负载**：[并发用户数、每秒请求数、数据量]
- **性能要求**：[响应时间 SLA、吞吐量目标]
- **基础设施**：[云提供商、服务器规格、扩展能力]

## 当前性能基线：
[包含任何现有的性能指标或基准]

## 性能测试要求：
- **负载测试**：[正常预期负载模拟]
- **压力测试**：[超出正常容量的测试]
- **峰值测试**：[突发负载增加处理]
- **容量测试**：[大数据量处理]
- **耐久性测试**：[长期运行性能稳定性]

## 性能测试策略：

请创建一个全面的性能测试计划，包括：

### 1. 测试策略概述
- 性能测试目标和成功标准
- 测试类型及其目的
- 测试环境要求
- 基线建立和测量
- 性能测试执行时间表

### 2. 负载测试
- **正常负载模拟**：预期的用户行为模式
- **真实用户旅程**：实际用户工作流模拟
- **逐步增加负载**：预热策略和模式
- **持续负载测试**：随时间维持负载
- **负载分布**：地理和时间负载模式

### 3. 压力测试
- **断点测试**：寻找系统极限
- **资源耗尽**：内存、CPU、连接限制
- **级联故障测试**：故障如何传播
- **恢复测试**：压力后的系统恢复
- **降级分析**：性能降级模式

### 4. 峰值测试
- **流量峰值模拟**：突发负载增加处理
- **自动扩展测试**：扩展机制验证
- **缓存失效**：峰值下的缓存性能
- **数据库连接测试**：连接池行为
- **CDN 性能**：负载下的内容交付

### 5. 容量测试
- **大数据集测试**：大数据处理性能
- **数据库性能**：大表查询性能
- **文件处理**：大文件上传/下载测试
- **内存使用**：大数据集下的内存消耗
- **存储性能**：容量下的磁盘 I/O

### 6. 耐久性测试
- **长期运行稳定性**：24/7 操作模拟
- **内存泄漏检测**：长期内存使用模式
- **资源清理**：随时间推移的适当资源管理
- **性能降级**：逐渐的性能下降
- **系统可靠性**：正常运行时间和可用性测试

### 7. API 性能测试
- **端点负载测试**：单个 API 端点性能
- **并发请求测试**：多个同时请求
- **有效负载大小测试**：大请求/响应处理
- **身份验证负载**：负载下的身份验证系统性能
- **速率限制测试**：API 节流行为

### 8. 数据库性能测试
- **查询性能**：负载下的复杂查询执行
- **连接池测试**：数据库连接管理
- **事务性能**：数据库事务吞吐量
- **索引性能**：负载下的索引效率
- **备份性能**：备份操作影响

### 9. 前端性能测试
- **页面加载测试**：浏览器渲染性能
- **JavaScript 性能**：客户端执行速度
- **资产加载**：图像、CSS、JS 加载性能
- **移动性能**：移动设备上的性能
- **网络模拟**：各种网络条件测试

### 10. 基础设施性能测试
- **服务器资源测试**：CPU、内存、磁盘性能
- **网络性能**：带宽和延迟测试
- **负载均衡器测试**：流量分配效率
- **CDN 性能**：内容分发网络测试
- **自动扩展测试**：扩展机制验证

## 测试实施：

请提供：
- **主要用户工作流的负载测试脚本**
- **具有真实用户模式的性能测试场景**
- **容量测试的测试数据生成策略**
- **监控和指标收集**设置
- **结果分析和报告**模板

## 测试工具和框架：
- 推荐性能测试工具（JMeter、k6、Artillery 等）
- 建议监控和分析工具
- 提供测试基础设施设置
- 推荐结果分析和可视化工具

## 测试场景：

为以下内容创建具体的测试场景：
- **用户注册/登录**：身份验证系统负载
- **核心应用程序功能**：主要功能性能
- **支付处理**：负载下的交易处理
- **文件操作**：上传/下载性能
- **搜索和过滤**：数据查询性能

## 指标和监控：
- **响应时间指标**：平均值、中位数、第 95 百分位数
- **吞吐量指标**：每秒请求数、每分钟事务数
- **错误率监控**：错误百分比和类型
- **资源利用率**：CPU、内存、磁盘、网络使用情况
- **应用程序指标**：自定义业务指标

## 性能基准测试：
- **基线建立**：当前性能测量
- **基准比较**：随时间推移的性能跟踪
- **回归测试**：性能回归检测
- **优化验证**：衡量改进效果
- **容量规划**：未来的扩展要求

## 结果分析：
- **性能报告生成**：全面的测试报告
- **瓶颈识别**：性能约束分析
- **趋势分析**：随时间推移的性能模式
- **比较报告**：优化前后的比较
- **建议**：可操作的性能改进

## CI/CD 集成：
- **自动化性能测试**：流水线集成
- **性能门**：自动化的通过/失败标准
- **持续监控**：持续的性能跟踪
- **警报配置**：性能下降警报
- **历史跟踪**：性能趋势分析

## 高级测试场景：
- **多区域测试**：地理性能测试
- **第三方服务影响**：外部依赖项性能
- **灾难恢复**：故障转移期间的性能
- **安全测试**：采取安全措施后的性能
- **A/B 测试**：版本之间的性能比较

请提供具体的、可立即执行的可运行性能测试脚本，以验证我的系统在各种条件下的性能。
```

---

## 获得更好结果的提示：

- **定义明确的性能目标**——具体的响应时间、吞吐量目标
- **包含您的基础设施详细信息**——云提供商、服务器规格、扩展设置
- **提及您的用户模式**——典型用法、高峰时间、地理分布
- **指定您的限制**——预算、测试时间窗口、生产影响
- **包含您的监控设置**——您当前用于性能跟踪的工具

# Performance Testing Assistant

**Use this when:** You need to test your application's performance under load, stress, and various conditions to ensure it meets performance requirements.

**Skill Level:** Intermediate to Advanced

---

## Copy This Prompt:

```
I need help creating comprehensive performance tests for my application. Please help me design and implement load testing, stress testing, and performance benchmarking strategies.

## Application Context:
- **Application Type**: [Web app, API, mobile backend, etc.]
- **Technology Stack**: [Languages, frameworks, databases, infrastructure]
- **Expected Load**: [Concurrent users, requests per second, data volume]
- **Performance Requirements**: [Response time SLAs, throughput targets]
- **Infrastructure**: [Cloud provider, server specs, scaling capabilities]

## Current Performance Baseline:
[Include any existing performance metrics or benchmarks]

## Performance Testing Requirements:
- **Load Testing**: [Normal expected load simulation]
- **Stress Testing**: [Beyond normal capacity testing]
- **Spike Testing**: [Sudden load increase handling]
- **Volume Testing**: [Large data volume handling]
- **Endurance Testing**: [Long-running performance stability]

## Performance Testing Strategy:

Please create a comprehensive performance testing plan that includes:

### 1. Testing Strategy Overview
- Performance testing objectives and success criteria
- Testing types and their purposes
- Testing environment requirements
- Baseline establishment and measurement
- Performance test execution timeline

### 2. Load Testing
- **Normal Load Simulation**: Expected user behavior patterns
- **Realistic User Journeys**: Actual user workflow simulation
- **Gradual Load Increase**: Ramp-up strategies and patterns
- **Sustained Load Testing**: Maintaining load over time
- **Load Distribution**: Geographic and temporal load patterns

### 3. Stress Testing
- **Breaking Point Testing**: Finding system limits
- **Resource Exhaustion**: Memory, CPU, connection limits
- **Cascading Failure Testing**: How failures propagate
- **Recovery Testing**: System recovery after stress
- **Degradation Analysis**: Performance degradation patterns

### 4. Spike Testing
- **Traffic Spike Simulation**: Sudden load increase handling
- **Auto-scaling Testing**: Scaling mechanism validation
- **Cache Invalidation**: Cache performance under spikes
- **Database Connection Testing**: Connection pool behavior
- **CDN Performance**: Content delivery under load

### 5. Volume Testing
- **Large Dataset Testing**: Big data processing performance
- **Database Performance**: Large table query performance
- **File Processing**: Large file upload/download testing
- **Memory Usage**: Memory consumption with large datasets
- **Storage Performance**: Disk I/O under volume

### 6. Endurance Testing
- **Long-running Stability**: 24/7 operation simulation
- **Memory Leak Detection**: Long-term memory usage patterns
- **Resource Cleanup**: Proper resource management over time
- **Performance Degradation**: Gradual performance decline
- **System Reliability**: Uptime and availability testing

### 7. API Performance Testing
- **Endpoint Load Testing**: Individual API endpoint performance
- **Concurrent Request Testing**: Multiple simultaneous requests
- **Payload Size Testing**: Large request/response handling
- **Authentication Load**: Auth system performance under load
- **Rate Limiting Testing**: API throttling behavior

### 8. Database Performance Testing
- **Query Performance**: Complex query execution under load
- **Connection Pool Testing**: Database connection management
- **Transaction Performance**: Database transaction throughput
- **Index Performance**: Index efficiency under load
- **Backup Performance**: Backup operation impact

### 9. Frontend Performance Testing
- **Page Load Testing**: Browser rendering performance
- **JavaScript Performance**: Client-side execution speed
- **Asset Loading**: Image, CSS, JS loading performance
- **Mobile Performance**: Performance on mobile devices
- **Network Simulation**: Various network condition testing

### 10. Infrastructure Performance Testing
- **Server Resource Testing**: CPU, memory, disk performance
- **Network Performance**: Bandwidth and latency testing
- **Load Balancer Testing**: Traffic distribution efficiency
- **CDN Performance**: Content delivery network testing
- **Auto-scaling Testing**: Scaling mechanism validation

## Test Implementation:

Please provide:
- **Load testing scripts** for major user workflows
- **Performance test scenarios** with realistic user patterns
- **Test data generation** strategies for volume testing
- **Monitoring and metrics collection** setup
- **Result analysis and reporting** templates

## Testing Tools and Framework:
- Recommend performance testing tools (JMeter, k6, Artillery, etc.)
- Suggest monitoring and profiling tools
- Provide infrastructure setup for testing
- Recommend result analysis and visualization tools

## Test Scenarios:

Create specific test scenarios for:
- **User Registration/Login**: Authentication system load
- **Core Application Features**: Main functionality performance
- **Payment Processing**: Transaction processing under load
- **File Operations**: Upload/download performance
- **Search and Filtering**: Data query performance

## Metrics and Monitoring:
- **Response Time Metrics**: Average, median, 95th percentile
- **Throughput Metrics**: Requests per second, transactions per minute
- **Error Rate Monitoring**: Error percentage and types
- **Resource Utilization**: CPU, memory, disk, network usage
- **Application Metrics**: Custom business metrics

## Performance Benchmarking:
- **Baseline Establishment**: Current performance measurement
- **Benchmark Comparison**: Performance over time tracking
- **Regression Testing**: Performance regression detection
- **Optimization Validation**: Measuring improvement effectiveness
- **Capacity Planning**: Future scaling requirements

## Result Analysis:
- **Performance Report Generation**: Comprehensive test reports
- **Bottleneck Identification**: Performance constraint analysis
- **Trend Analysis**: Performance patterns over time
- **Comparison Reports**: Before/after optimization comparison
- **Recommendations**: Actionable performance improvements

## CI/CD Integration:
- **Automated Performance Testing**: Pipeline integration
- **Performance Gates**: Automated pass/fail criteria
- **Continuous Monitoring**: Ongoing performance tracking
- **Alert Configuration**: Performance degradation alerts
- **Historical Tracking**: Performance trend analysis

## Advanced Testing Scenarios:
- **Multi-region Testing**: Geographic performance testing
- **Third-party Service Impact**: External dependency performance
- **Disaster Recovery**: Performance during failover
- **Security Testing**: Performance with security measures
- **A/B Testing**: Performance comparison between versions

Please provide specific, runnable performance test scripts that I can execute immediately to validate my system's performance under various conditions.
```

---

## Tips for Better Results:

- **Define clear performance targets** - specific response times, throughput goals
- **Include your infrastructure details** - cloud provider, server specs, scaling setup
- **Mention your user patterns** - typical usage, peak times, geographic distribution
- **Specify your constraints** - budget, testing time windows, production impact
- **Include your monitoring setup** - what tools you currently use for performance tracking
