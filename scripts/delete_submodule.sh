#!/bin/bash

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <submodule_path>"
  echo "Example: $0 themes/green-magpie"
  exit 1
fi

SUBMODULE_PATH="$1"

echo "🚀 开始删除子模块: $SUBMODULE_PATH"

# 检查 .gitmodules 是否有未暂存的改动
if git diff --quiet -- .gitmodules; then
  # 没有未暂存改动
  :
else
  echo "⚠️ 你有未暂存的 .gitmodules 改动，请先暂存或放弃它们。"
  echo "你可以使用 'git add .gitmodules' 暂存，或者 'git checkout -- .gitmodules' 放弃改动。"
  exit 1
fi


# 1. 取消初始化子模块
git submodule deinit -f "$SUBMODULE_PATH"

# 2. 从索引中移除子模块（会删除子模块目录）
git rm -f "$SUBMODULE_PATH"

# 3. 从 .gitmodules 中安全删除子模块配置段
git config -f .gitmodules --remove-section "submodule.$SUBMODULE_PATH" || echo ".gitmodules 中无此配置"

# 4. 提交 .gitmodules 的修改（你可以根据需要决定是否自动提交）
git add .gitmodules

# 5. 从 Git 配置中删除子模块配置
git config --remove-section "submodule.$SUBMODULE_PATH" 2>/dev/null || echo "Git 配置中无此节"

# 6. 删除子模块本地残留
rm -rf ".git/modules/$SUBMODULE_PATH"
rm -rf "$SUBMODULE_PATH"

echo "✅ 子模块 $SUBMODULE_PATH 已彻底删除！"
echo "请执行 'git commit -m \"Remove submodule $SUBMODULE_PATH\"' 完成提交。"
