-- 创建报告表
CREATE TABLE IF NOT EXISTS reports (
  id SERIAL PRIMARY KEY,
  date DATE UNIQUE NOT NULL,
  summary TEXT NOT NULL,
  model VARCHAR(100),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建信息源表
CREATE TABLE IF NOT EXISTS sources (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  type VARCHAR(50) NOT NULL,
  url TEXT NOT NULL,
  description TEXT
);

-- 创建新闻条目表
CREATE TABLE IF NOT EXISTS news_items (
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

-- 创建论文条目表
CREATE TABLE IF NOT EXISTS paper_items (
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
