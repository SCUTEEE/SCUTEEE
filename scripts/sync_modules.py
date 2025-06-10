"""
sync_modules.py

用途：
    自动同步 Hugo 博客中的课程模块（Hugo Modules）依赖。

功能包括：
    1. 从根目录的 course-list.yml 中读取课程模块列表（简洁 YAML 列表格式）；
    2. 自动将缺失模块添加到 config/production/module.yml 的 module.imports 中；
    3. 自动挂载模块到 content/courses/<课程名>；
    4. 删除 module.yml 中那些：
       - path 来自 github.com，
       - 且挂载目标为 content/courses/，
       - 但不在 course-list.yml 中的模块；
    5. 自动运行 `hugo mod get -u` 更新所有模块到最新版；
    6. 自动运行 `hugo mod tidy` 清理未使用依赖。

文件结构示例：
    SCUTEEE/
    ├── course-list.yml                  # 存储课程模块列表（纯字符串列表）
    ├── config/
    │   └── production/
    │       └── module.yml              # Hugo 的模块导入配置
    └── scripts/
        └── sync_modules.py             # 本脚本位置

course-list.yml 示例：
    - github.com/scuteee/computer-network
    - github.com/scuteee/probability-and-statistics
    - github.com/scuteee/operating-system

使用方式：
    在项目根目录执行：
        python scripts/sync_modules.py

前提依赖：
    pip install pyyaml
    （要求已安装 Hugo 且初始化为 module 项目）

作者：
    ChatGPT & ToddZZF
"""

import yaml
import subprocess
from pathlib import Path

# 路径配置
root_dir = Path(__file__).resolve().parent.parent
course_list_file = root_dir / "course-list.yml"
module_config_file = root_dir / "config/production/module.yml"

# 读取 course-list.yml（列表）
with course_list_file.open("r", encoding="utf-8") as f:
    course_modules = set(yaml.safe_load(f))

# 读取 module.yml（顶层是 hugoVersion 和 imports）
if module_config_file.exists():
    with module_config_file.open("r", encoding="utf-8") as f:
        module_data = yaml.safe_load(f)
else:
    module_data = {}

module_data.setdefault("hugoVersion", {
    "extended": True,
    "min": "0.136.0"
})
module_data.setdefault("imports", [])
imports = module_data["imports"]

# 清理：删除 github.com 且挂载到 content/courses 的未在列表中的模块
def is_github_path(p):
    return p.startswith("github.com") or "github.com" in p

def is_courses_mount(imp):
    for m in imp.get("mounts", []):
        if m.get("target", "").startswith("content/courses/"):
            return True
    return False

new_imports = []
for imp in imports:
    p = imp.get("path", "")
    if is_github_path(p) and is_courses_mount(imp):
        if p not in course_modules:
            print(f"🗑️ 删除无用模块: {p}")
            continue
    new_imports.append(imp)

module_data["imports"] = new_imports
existing_paths = {imp["path"] for imp in new_imports if "path" in imp}

# 添加缺失模块
new_modules = sorted(course_modules - existing_paths)
for mod in new_modules:
    course_name = mod.strip().split("/")[-1]
    print(f"➕ 添加模块: {mod} → content/courses/{course_name}")
    module_data["imports"].append({
        "path": mod,
        "mounts": [
            {
                "source": ".",
                "target": f"content/courses/{course_name}"
            }
        ]
    })

# 保存回 module.yml
with module_config_file.open("w", encoding="utf-8") as f:
    yaml.dump(module_data, f, sort_keys=False, allow_unicode=True)

# 更新所有模块
for mod in course_modules:
    print(f"🔄 更新模块: {mod}")
    subprocess.run(["hugo", "mod", "get", "-u", mod], check=True)

# 清理
print("🧹 hugo mod tidy")
subprocess.run(["hugo", "mod", "tidy"], check=True)

print("✅ 同步完成")