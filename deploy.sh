#!/bin/bash

# 设置颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}开始部署 AI 新闻摘要器到 Vercel...${NC}"

# 检查是否安装了 Vercel CLI
if ! command -v vercel &> /dev/null
then
    echo -e "${YELLOW}未找到 Vercel CLI，正在安装...${NC}"
    npm install -g vercel
fi

# 检查环境变量文件
if [ ! -f .env ]; then
    echo -e "${YELLOW}未找到 .env 文件，正在从 .env.example 创建...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}请在 .env 文件中填写您的环境变量！${NC}"
    exit 1
fi

# 检查 Supabase 环境变量
if ! grep -q "SUPABASE_URL" .env || ! grep -q "SUPABASE_KEY" .env; then
    echo -e "${RED}错误: .env 文件中缺少 Supabase 环境变量！${NC}"
    echo -e "${YELLOW}请确保 .env 文件中包含 SUPABASE_URL 和 SUPABASE_KEY${NC}"
    exit 1
fi

# 检查 AI 模型环境变量
if ! grep -q "GROK_API_KEY" .env && ! grep -q "DEEPSEEK_API_KEY" .env; then
    echo -e "${RED}警告: .env 文件中缺少 AI 模型 API 密钥！${NC}"
    echo -e "${YELLOW}请确保至少配置了一个 AI 模型的 API 密钥${NC}"
fi

# 运行数据迁移脚本
echo -e "${GREEN}运行数据迁移脚本...${NC}"
python scripts/migrate_data.py

# 部署到 Vercel
echo -e "${GREEN}部署到 Vercel...${NC}"
vercel --prod

echo -e "${GREEN}部署完成！${NC}"
echo -e "${YELLOW}请确保在 Vercel 控制台中设置了所有必要的环境变量！${NC}"
echo -e "${YELLOW}您可以在 Vercel 控制台中设置定时任务，以定期生成报告。${NC}"
