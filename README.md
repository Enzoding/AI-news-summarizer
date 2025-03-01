# AI行业信息助手

一个基于 AI 的行业信息聚合项目，每天自动收集AI行业相关新闻和研究论文，通过 AI 生成中文总结并提供便捷阅读体验。

## 功能特点

- 自动收集AI行业相关新闻和研究论文
- 使用大语言模型（如DeepSeek）生成高质量中文总结
- 通过Vue网页界面展示内容，支持RSS订阅
- 每日自动更新

## 项目结构

- `backend/`: 后端API服务
- `frontend/`: 基于Vue的前端Web应用
- `scripts/`: 数据收集和处理脚本
- `data/`: 存储收集的数据和生成的报告

## 安装与使用

### 环境要求

- Python 3.8+
- Node.js 14+

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yourusername/ai_industry_assistant.git
cd ai_industry_assistant
```

2. 安装后端依赖
```bash
cd backend
pip install -r requirements.txt
```

3. 安装前端依赖
```bash
cd frontend
npm install
```

4. 配置环境变量
在`backend`目录下创建`.env`文件并配置必要的API密钥

5. 启动服务
```bash
./start.sh
```

## 许可证

MIT
