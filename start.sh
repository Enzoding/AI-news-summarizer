#!/bin/bash

# 设置颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 进程ID存储
BACKEND_PID=""
FRONTEND_PID=""

# 清理函数
cleanup() {
  echo -e "${RED}正在关闭服务...${NC}"
  
  if [ ! -z "$BACKEND_PID" ]; then
    echo "终止后端进程 (PID: $BACKEND_PID)"
    kill $BACKEND_PID 2>/dev/null || true
  fi
  
  if [ ! -z "$FRONTEND_PID" ]; then
    echo "终止前端进程 (PID: $FRONTEND_PID)"
    kill $FRONTEND_PID 2>/dev/null || true
  fi
  
  echo -e "${GREEN}服务已关闭${NC}"
  exit 0
}

# 捕获中断信号
trap cleanup SIGINT SIGTERM

echo -e "${BLUE}启动 AI行业信息助手...${NC}"

# 确保数据目录存在
mkdir -p data

# 启动后端
echo -e "${GREEN}启动后端服务...${NC}"
cd backend
python3 app.py &
BACKEND_PID=$!
echo "后端进程ID: $BACKEND_PID"

# 检查后端是否成功启动
sleep 2
if ! ps -p $BACKEND_PID > /dev/null; then
  echo -e "${RED}后端启动失败，请检查错误信息${NC}"
  cleanup
fi

cd ..

# 启动前端
echo -e "${GREEN}启动前端服务...${NC}"
cd frontend
if [ -d "node_modules" ]; then
  echo "前端依赖已安装，启动开发服务器..."
  npm run dev &
else
  echo "首次启动，安装前端依赖..."
  npm install && npm run dev &
fi
FRONTEND_PID=$!
echo "前端进程ID: $FRONTEND_PID"

# 检查前端是否成功启动
sleep 2
if ! ps -p $FRONTEND_PID > /dev/null; then
  echo -e "${RED}前端启动失败，请检查错误信息${NC}"
  cleanup
fi

cd ..

echo -e "${GREEN}服务已启动${NC}"
echo -e "${BLUE}后端API地址: ${GREEN}http://localhost:5002${NC}"
echo -e "${BLUE}前端页面地址: ${GREEN}http://localhost:5173${NC}"
echo -e "${BLUE}按 Ctrl+C 停止服务${NC}"

# 等待中断信号
wait
