#!/bin/bash

# 设置颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}安装 AI行业信息收集总结助手 依赖...${NC}"

# 安装后端依赖
echo -e "${GREEN}安装后端依赖...${NC}"
cd backend
pip install -r requirements.txt

# 安装前端依赖
echo -e "${GREEN}安装前端依赖...${NC}"
cd ../frontend
npm install

echo -e "${GREEN}依赖安装完成!${NC}"
echo -e "请确保您已经在 ${BLUE}backend/.env${NC} 文件中设置了 DeepSeek API 密钥"
echo -e "运行 ${BLUE}./start.sh${NC} 启动服务"
