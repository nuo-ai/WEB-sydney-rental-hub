# 文档阶段提示

此文件夹包含用于为项目创建全面文档的提示。这些提示可帮助您记录代码、API 和项目结构，使代码库更易于维护和访问。

## 可用提示

### 项目文档
- **[README 生成器](./readme-generator.md)** - 创建全面、专业的 README 文件
- **[仓库快照](./repository-snapshot.md)** - 生成高级项目概述并识别文档空白

## 何时使用文档提示

### 项目文档
- 当您需要创建或改进项目的主要文档时，使用**README 生成器**
- 当您想了解和记录整个项目结构时，使用**仓库快照**

### 对于新项目
- 使用**README 生成器**从头开始创建专业的项目文档
- 使用**仓库快照**审计项目并识别缺失的文档

### 对于现有项目
- 使用**仓库快照**获取全面概述并查找文档空白
- 使用**README 生成器**改进现有文档

## 文档工作流

记录项目的系统方法：

1. **项目分析** → 使用仓库快照了解项目结构
2. **文档规划** → 识别需要哪些文档
3. **README 创建** → 使用 README 生成器创建主要项目文档
4. **持续文档** → 定期快照以保持文档最新

## 文档专业提示

### 仓库快照
- 随着项目的演变定期运行此功能
- 非常适合新团队成员入职
- 使用建议优先改进文档
- 非常适合项目审计和健康检查

### README 生成器
- 包含来自实际项目的具体示例
- 关注用户旅程——从安装到使用
- 随着功能变化保持更新
- 使用良好的格式使其易于扫描

## 与其他阶段的集成

- **从规划**：使用 PRD 和架构文档作为文档的输入
- **从开发**：记录使用[开发阶段](../development/)提示创建的代码
- **从测试**：包含测试文档和覆盖率报告
- **到维护**：文档有助于持续的项目维护

## 文档策略快速参考

| 我想... | 使用此提示 |
|---|---|
| 了解我的整个项目结构 | 仓库快照 |
| 创建专业的 README | README 生成器 |
| 查找文档空白 | 仓库快照 |
| 改进现有文档 | README 生成器 |

## 文档最佳实践

### 仓库快照使用
- **以完全访问权限运行**——确保 Cursor 可以查看您的整个仓库
- **根据建议采取行动**——使用建议来改进您的项目
- **定期审计**——定期运行以捕获文档漂移
- **与团队共享**——非常适合项目健康讨论

### README 质量
- **从用户需求开始**——他们首先需要了解什么？
- **包含实用示例**——可工作的代码片段
- **保持准确性**——使文档与代码同步
- **考虑您的受众**——技术用户与非技术用户

## 后续步骤

创建文档后：
- 使用[部署阶段](../deployment/)提示包含部署文档
- 使用[维护阶段](../maintenance/)提示保持文档最新
- 考虑使用文档作为其他规划和开发提示的输入

# Documentation Phase Prompts

This folder contains prompts for creating comprehensive documentation for your projects. These prompts help you document your code, APIs, and project structure to make your codebase more maintainable and accessible.

## Available Prompts

### Project Documentation
- **[README Generator](./readme-generator.md)** - Create comprehensive, professional README files
- **[Repository Snapshot](./repository-snapshot.md)** - Generate high-level project overview and identify documentation gaps

## When to Use Documentation Prompts

### Project Documentation
- **README Generator** when you need to create or improve your project's main documentation
- **Repository Snapshot** when you want to understand and document your entire project structure

### For New Projects
- Use **README Generator** to create professional project documentation from scratch
- Use **Repository Snapshot** to audit your project and identify missing documentation

### For Existing Projects
- Use **Repository Snapshot** to get a comprehensive overview and find documentation gaps
- Use **README Generator** to improve existing documentation

## Documentation Workflow

A systematic approach to documenting your project:

1. **Project Analysis** → Use Repository Snapshot to understand your project structure
2. **Documentation Planning** → Identify what documentation is needed
3. **README Creation** → Use README Generator for main project documentation
4. **Ongoing Documentation** → Regular snapshots to keep documentation current

## Pro Tips for Documentation

### Repository Snapshot
- Run this regularly as your project evolves
- Great for onboarding new team members
- Use suggestions to prioritise documentation improvements
- Perfect for project audits and health checks

### README Generator
- Include concrete examples from your actual project
- Focus on the user journey - installation to usage
- Keep it updated as features change
- Make it scannable with good formatting

## Integration with Other Phases

- **From Planning**: Use PRD and architecture documents as input for documentation
- **From Development**: Document code created with [Development Phase](../development/) prompts
- **From Testing**: Include testing documentation and coverage reports
- **To Maintenance**: Documentation helps with ongoing project maintenance

## Documentation Strategy Quick Reference

| I want to... | Use this prompt |
|--------------|----------------|
| Understand my entire project structure | Repository Snapshot |
| Create a professional README | README Generator |
| Find documentation gaps | Repository Snapshot |
| Improve existing documentation | README Generator |

## Documentation Best Practices

### Repository Snapshot Usage
- **Run with full access** - make sure Cursor can see your entire repository
- **Act on suggestions** - use the recommendations to improve your project
- **Regular audits** - run periodically to catch documentation drift
- **Share with team** - great for project health discussions

### README Quality
- **Start with user needs** - what do they need to know first?
- **Include practical examples** - working code snippets
- **Maintain accuracy** - keep documentation in sync with code
- **Consider your audience** - technical vs non-technical users

## Next Steps

After creating documentation:
- Use [Deployment Phase](../deployment/) prompts to include deployment documentation
- Use [Maintenance Phase](../maintenance/) prompts to keep documentation current
- Consider using the documentation as input for other planning and development prompts
