import os
import time
import subprocess

# --- 1. 顶层设计：直接在当前文件夹执行 ---
# 确保这个脚本就在 /Users/zhangxiaoan/Desktop/stock_python 目录下
REPO_PATH = os.path.dirname(os.path.abspath(__file__))

# 获取当前时间
timestamp = time.strftime('%H:%M:%S')
commit_message = f"🚀 Alpha数据更新: {timestamp}"

def run_git(cmd_list):
    try:
        subprocess.run(cmd_list, cwd=REPO_PATH, check=True, timeout=30)
        return True
    except Exception as e:
        print(f"❌ Git执行失败: {e}")
        return False

print(f"📡 启动同步... 目标目录: {REPO_PATH}")

# --- 2. 检查是否有数据更新 ---
# 只有当 alpha_radar_results.csv 发生变化时才推送
status_res = subprocess.run(["git", "status", "--porcelain"], cwd=REPO_PATH, capture_output=True, text=True)

# --- 2. 检查是否有任何变化 (包括新挪进来的脚本) ---
status_res = subprocess.run(["git", "status", "--porcelain"], cwd=REPO_PATH, capture_output=True, text=True)

if not status_res.stdout.strip():
    print("ℹ️ 提示: 没有任何文件变化，无需推送。")
    exit(0)

# --- 3. 执行标准三部曲 (由精确匹配改为全局匹配 '.') ---
steps = [
    ["git", "add", "."],  # 改为 . 确保脚本自己和CSV都能被装箱
    ["git", "commit", "-m", commit_message],
    ["git", "push"]
]

success = True
for step in steps:
    print(f"⏳ 正在执行: {' '.join(step)}")
    if not run_git(step):
        success = False
        break

if success:
    print(f"✅ 【同步成功】 画面将在 5 秒内感应更新 | {timestamp}")
else:
    print(f"❌ 【同步失败】 请检查网络或 GitHub 权限")