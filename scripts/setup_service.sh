#!/bin/bash

# 遇到错误即退出
set -e

SERVICE_NAME="notebooklm2openai.service"
# 获取脚本所在的绝对路径目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# 上级目录即项目根目录
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SERVICE_FILE="$PROJECT_DIR/scripts/$SERVICE_NAME"
SYSTEMD_DIR="/etc/systemd/system"

echo "=== 🔍 正在检查服务文件 ==="
if [ ! -f "$SERVICE_FILE" ]; then
    echo "❌ 错误: 找不到服务文件 $SERVICE_FILE"
    echo "请确认项目根目录下的 scripts 目录中是否存在该 service 文件。"
    exit 1
fi
echo "✅ 找到服务文件: $SERVICE_FILE"

# echo "=== 🚚 复制服务文件到 $SYSTEMD_DIR ==="
# sudo cp "$SERVICE_FILE" "$SYSTEMD_DIR/"

echo "=== 🚚 创建软链接到 $SYSTEMD_DIR ==="
sudo ln -sf "$SERVICE_FILE" "$SYSTEMD_DIR/$SERVICE_NAME"

echo "=== 🔄 重新加载 systemd 守护进程 ==="
sudo systemctl daemon-reload

echo "=== 📌 设置服务开机自启 ==="
sudo systemctl enable "$SERVICE_NAME"

echo "=== ▶️ 启动/重启服务 ==="
sudo systemctl restart "$SERVICE_NAME"

echo "=== ✅ 服务安装完成！当前运行状态: ==="
sudo systemctl status "$SERVICE_NAME" --no-pager
