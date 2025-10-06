#!/bin/bash
# Git pre-commit hook - 确保代码质量和规则遵守

echo "🔍 运行提交前检查..."

# 1. 检查是否有console.log（生产代码不应该有）
echo "检查 console.log..."
if grep -r "console\.log" --include="*.vue" --include="*.js" --exclude-dir=node_modules apps/web/src; then
    echo "⚠️  警告：发现 console.log，请考虑移除或改用 console.error"
    # 不阻止提交，只是警告
fi

# 2. 运行 lint
echo "运行 ESLint..."
pnpm --filter @web-sydney/web lint
if [ $? -ne 0 ]; then
    echo "❌ ESLint 检查失败，请修复错误后再提交"
    exit 1
fi

# 3. 检查 TODO 是否更新
echo "提醒：是否需要更新 TODO.md？"

# 4. 检查是否遵循了开发规则
echo "✅ 请确认已遵循 DEVELOPMENT_RULES.md 中的规则"

echo "✅ 提交前检查完成！"
