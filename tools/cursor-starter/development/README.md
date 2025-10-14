# 开发阶段提示

此文件夹包含用于主动开发工作的提示——编写代码、审查实现、调试问题和重构现有代码。这些是您在项目实施阶段最常使用的提示。

## 可用提示

### 代码创建与生成
- **[代码生成](./code-generation.md)** - 生成样板代码、组件和结构
- **[代码审查](./code-review.md)** - 获取有关代码质量的全面反馈

### 代码改进
- **[重构助手](./refactoring-assistant.md)** - 系统地改进现有代码结构和质量

### 问题解决
- **[调试助手](./debugging-assistant.md)** - 系统地查找和修复 bug 的方法

## 何时使用开发提示

### 编写新代码
- 当您需要创建新组件、函数或模块时，使用**代码生成**
- 将此用于样板代码、API 端点、UI 组件等。

### 审查您的工作
- 在提交重要更改之前进行**代码审查**
- 使用此功能获取有关代码质量、安全性和最佳实践的反馈

### 改进现有代码
- 当代码有效但需要改进时，使用**重构助手**
- 将此用于清理技术债务、提高性能或增强可维护性

### 修复问题
- 当您遇到 bug 或意外行为时，使用**调试助手**
- 将此用于系统的问题解决和根本原因分析

## 开发工作流

使用这些提示的典型开发工作流：

1. **生成** → 使用代码生成创建初始实现
2. **审查** → 使用代码审查验证您的方法
3. **调试** → 当出现问题时使用调试助手
4. **重构** → 使用重构助手改进代码质量
5. **再次审查** → 完成前的最终代码审查

## 开发技巧

### 代码生成
- 具体说明要求和限制
- 包含现有代码库中的示例
- 指定编码标准和约定

### 代码审查
- 包含有关项目的相关上下文
- 提及具体的担忧或重点领域
- 要求对反馈进行优先级排序（关键与锦上添花）

### 调试
- 包含完整的错误消息和堆栈跟踪
- 描述重现问题的步骤
- 提及您已尝试过的内容

### 重构
- 明确说明您的重构目标
- 包含代码的完整上下文
- 指定任何限制（向后兼容性等）

## 与其他阶段的集成

- **从规划**：使用架构决策指导代码生成
- **到测试**：使用[测试阶段](../testing/)提示生成测试
- **到文档**：使用[文档阶段](../documentation/)提示记录您的代码
- **到部署**：使用[部署阶段](../deployment/)提示准备部署

## 快速参考

| 我想... | 使用此提示 |
|---|---|
| 从头开始创建新代码 | 代码生成 |
| 获取有关我的代码的反馈 | 代码审查 |
| 修复 bug 或错误 | 调试助手 |
| 改进工作代码 | 重构助手 |

## 后续步骤

开发工作完成后：
- 使用[测试阶段](../testing/)提示创建全面的测试
- 使用[文档阶段](../documentation/)提示记录您的代码
- 使用[部署阶段](../deployment/)提示发布您的代码

# Development Phase Prompts

This folder contains prompts for active development work - writing code, reviewing implementations, debugging issues, and refactoring existing code. These are the prompts you'll use most during the implementation phase of your project.

##  Available Prompts

### Code Creation & Generation
- **[Code Generation](./code-generation.md)** - Generate boilerplate code, components, and structures
- **[Code Review](./code-review.md)** - Get comprehensive feedback on your code quality

### Code Improvement
- **[Refactoring Assistant](./refactoring-assistant.md)** - Systematically improve existing code structure and quality

### Problem Solving
- **[Debugging Assistant](./debugging-assistant.md)** - Systematic approach to finding and fixing bugs

##  When to Use Development Prompts

### Writing New Code
- **Code Generation** when you need to create new components, functions, or modules
- Use this for boilerplate code, API endpoints, UI components, etc.

### Reviewing Your Work
- **Code Review** before committing important changes
- Use this to get feedback on code quality, security, and best practices

### Improving Existing Code
- **Refactoring Assistant** when code works but needs improvement
- Use this for cleaning up technical debt, improving performance, or enhancing maintainability

### Fixing Issues
- **Debugging Assistant** when you encounter bugs or unexpected behavior
- Use this for systematic problem-solving and root cause analysis

##  Development Workflow

A typical development workflow using these prompts:

1. **Generate** → Use Code Generation to create initial implementations
2. **Review** → Use Code Review to validate your approach
3. **Debug** → Use Debugging Assistant when issues arise
4. **Refactor** → Use Refactoring Assistant to improve code quality
5. **Review Again** → Final code review before completion

##  Tips for Development

### Code Generation
- Be specific about requirements and constraints
- Include examples from your existing codebase
- Specify coding standards and conventions

### Code Review  
- Include relevant context about the project
- Mention specific concerns or areas of focus
- Ask for prioritized feedback (critical vs. nice-to-have)

### Debugging
- Include complete error messages and stack traces
- Describe steps to reproduce the issue
- Mention what you've already tried

### Refactoring
- Clearly state your refactoring goals
- Include the full context of the code
- Specify any constraints (backward compatibility, etc.)

##  Integration with Other Phases

- **From Planning**: Use architecture decisions to guide code generation
- **To Testing**: Generate tests using [Testing Phase](../testing/) prompts
- **To Documentation**: Document your code using [Documentation Phase](../documentation/) prompts
- **To Deployment**: Prepare for deployment using [Deployment Phase](../deployment/) prompts

##  Quick Reference

| I want to... | Use this prompt |
|--------------|----------------|
| Create new code from scratch | Code Generation |
| Get feedback on my code | Code Review |
| Fix a bug or error | Debugging Assistant |
| Improve working code | Refactoring Assistant |

##  Next Steps

After development work:
- Use [Testing Phase](../testing/) prompts to create comprehensive tests
- Use [Documentation Phase](../documentation/) prompts to document your code
- Use [Deployment Phase](../deployment/) prompts to ship your code
