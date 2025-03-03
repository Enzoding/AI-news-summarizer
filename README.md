# AI行业信息助手

一个基于 AI 的行业信息聚合项目，每天自动收集AI行业相关新闻和研究论文，通过 AI 生成中文总结并提供便捷阅读体验。

## 功能特点

- 自动收集AI行业相关新闻和研究论文
- 使用大语言模型（如Grok、DeepSeek）生成高质量中文总结
- 通过Vue网页界面展示内容，支持RSS订阅
- 每日自动更新
- 支持部署到 Vercel 和 Supabase

## 项目结构

- `backend/`: 后端API服务
  - `api/`: Vercel Serverless Functions
  - `collectors/`: 数据收集模块
  - `db/`: 数据库访问层
  - `models/`: AI模型接口
- `frontend/`: 基于Vue的前端Web应用
- `scripts/`: 数据收集和处理脚本
- `data/`: 存储收集的数据和生成的报告

## 安装与使用

### 环境要求

- Python 3.8+
- Node.js 14+

### 本地开发

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
复制 `.env.example` 文件为 `.env` 并配置必要的 API 密钥
```bash
cp .env.example .env
```

5. 启动服务
```bash
./start.sh
```

## 部署到 Vercel 和 Supabase

### Supabase 设置

1. 创建 Supabase 账户和项目
   - 访问 [Supabase](https://supabase.io/) 并创建一个新项目

2. 创建数据库表
   - 在 Supabase 控制台中，打开 SQL 编辑器，执行以下 SQL 语句：

```sql
-- 报告表
CREATE TABLE reports (
  id SERIAL PRIMARY KEY,
  date DATE UNIQUE NOT NULL,
  summary TEXT NOT NULL,
  model VARCHAR(100),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 信息源表
CREATE TABLE sources (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  type VARCHAR(50) NOT NULL,
  url TEXT NOT NULL,
  description TEXT
);

-- 新闻条目表
CREATE TABLE news_items (
  id SERIAL PRIMARY KEY,
  report_id INTEGER REFERENCES reports(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  url TEXT NOT NULL,
  source VARCHAR(100) NOT NULL,
  published_at TIMESTAMP WITH TIME ZONE,
  score INTEGER,
  comments INTEGER,
  summary TEXT
);

-- 论文条目表
CREATE TABLE paper_items (
  id SERIAL PRIMARY KEY,
  report_id INTEGER REFERENCES reports(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  authors TEXT[] NOT NULL,
  summary TEXT,
  published_at TIMESTAMP WITH TIME ZONE,
  url TEXT NOT NULL,
  pdf_url TEXT,
  categories TEXT[]
);
```

3. 获取 Supabase URL 和 API 密钥
   - 在项目设置中找到 API URL 和 API Key (anon, public)

4. 迁移数据到 Supabase
   - 配置 `.env` 文件中的 Supabase 环境变量
   - 运行数据迁移脚本：
   ```bash
   python scripts/migrate_data.py
   ```

### Vercel 部署

1. 安装 Vercel CLI
```bash
npm install -g vercel
```

2. 登录 Vercel
```bash
vercel login
```

3. 配置环境变量
   - 在 Vercel 控制台中，添加以下环境变量：
     - `SUPABASE_URL`
     - `SUPABASE_KEY`
     - `GROK_API_KEY`
     - `DEEPSEEK_API_KEY`
     - `MODEL_PRIORITY`

4. 部署项目
```bash
vercel
```

5. 设置定时任务
   - 在 Vercel 控制台中，创建一个 Cron Job 来定期触发报告生成：
   ```
   0 8 * * * curl https://your-vercel-app.vercel.app/api/generate
   ```

## 许可证

MIT
