#!/bin/bash

set -e

echo "🔄 Updating submodule: themes/green-magpie ..."

cd "$(dirname "$0")/.."

# 确保子模块初始化
git submodule update --init --recursive

# 进入子模块
cd themes/green-magpie

# 可选：切换到你想要跟踪的分支，比如 main、SCUTEEE
branch="SCUTEEE-Tailwind4"  # 改成你实际使用的分支名

echo "📌 Checking out branch '$branch'..."
git checkout $branch

echo "⬇️ Pulling latest changes..."
git pull origin $branch

cd ../..  # 返回项目根目录

echo "✅ green-magpie 子模块已更新完毕。"