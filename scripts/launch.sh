#!/bin/bash

# 获取脚本所在的绝对路径目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# 上级目录即项目根目录
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON_BIN="$PROJECT_DIR/venv/bin/python"

# 1. 环境初始化
cd $PROJECT_DIR
source venv/bin/activate

# 2. 启动服务
echo "🚀 Starting Server..."
cd $PROJECT_DIR
export notebook_id='82a4c04e-6094-4888-a523-7e51cbbbf1be'
$PYTHON_BIN server.py