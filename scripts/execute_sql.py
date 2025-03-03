#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
执行 SQL 语句创建数据库表
"""

import os
import sys
import logging
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 检查 Supabase 环境变量
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    logger.error("缺少 Supabase 环境变量，请设置 SUPABASE_URL 和 SUPABASE_KEY")
    sys.exit(1)

try:
    from supabase import create_client, Client
    supabase: Client = create_client(supabase_url, supabase_key)
    logger.info("Supabase 客户端初始化成功")
except ImportError:
    logger.error("请安装 supabase 库: pip install supabase")
    sys.exit(1)
except Exception as e:
    logger.error(f"Supabase 客户端初始化失败: {e}")
    sys.exit(1)

def execute_sql(sql):
    """执行 SQL 语句"""
    try:
        # 使用 rpc 方法执行 SQL 语句
        response = supabase.rpc('exec_sql', {'query': sql}).execute()
        logger.info(f"SQL 语句执行成功: {response}")
        return True
    except Exception as e:
        logger.error(f"SQL 语句执行失败: {e}")
        return False

def create_tables():
    """创建数据库表"""
    # 报告表
    reports_sql = """
    CREATE TABLE IF NOT EXISTS reports (
      id SERIAL PRIMARY KEY,
      date DATE UNIQUE NOT NULL,
      summary TEXT NOT NULL,
      model VARCHAR(100),
      created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """
    
    # 信息源表
    sources_sql = """
    CREATE TABLE IF NOT EXISTS sources (
      id SERIAL PRIMARY KEY,
      name VARCHAR(100) UNIQUE NOT NULL,
      type VARCHAR(50) NOT NULL,
      url TEXT NOT NULL,
      description TEXT
    );
    """
    
    # 新闻条目表
    news_items_sql = """
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
    """
    
    # 论文条目表
    paper_items_sql = """
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
    """
    
    # 执行 SQL 语句
    logger.info("开始创建数据库表...")
    
    # 尝试直接查询表是否存在
    try:
        # 检查 reports 表是否存在
        response = supabase.table('reports').select('id').limit(1).execute()
        logger.info("reports 表已存在")
    except Exception as e:
        logger.info(f"reports 表不存在，将创建: {e}")
        # 尝试创建表
        try:
            # 使用 REST API 创建表
            import requests
            headers = {
                'apikey': supabase_key,
                'Authorization': f'Bearer {supabase_key}',
                'Content-Type': 'application/json',
                'Prefer': 'return=minimal'
            }
            
            # 创建 reports 表
            logger.info("创建 reports 表...")
            response = requests.post(
                f"{supabase_url}/rest/v1/rpc/exec_sql",
                headers=headers,
                json={"query": reports_sql}
            )
            logger.info(f"创建 reports 表结果: {response.status_code} {response.text}")
            
            # 创建 sources 表
            logger.info("创建 sources 表...")
            response = requests.post(
                f"{supabase_url}/rest/v1/rpc/exec_sql",
                headers=headers,
                json={"query": sources_sql}
            )
            logger.info(f"创建 sources 表结果: {response.status_code} {response.text}")
            
            # 创建 news_items 表
            logger.info("创建 news_items 表...")
            response = requests.post(
                f"{supabase_url}/rest/v1/rpc/exec_sql",
                headers=headers,
                json={"query": news_items_sql}
            )
            logger.info(f"创建 news_items 表结果: {response.status_code} {response.text}")
            
            # 创建 paper_items 表
            logger.info("创建 paper_items 表...")
            response = requests.post(
                f"{supabase_url}/rest/v1/rpc/exec_sql",
                headers=headers,
                json={"query": paper_items_sql}
            )
            logger.info(f"创建 paper_items 表结果: {response.status_code} {response.text}")
            
        except Exception as e:
            logger.error(f"创建表失败: {e}")
            logger.info("请在 Supabase 控制台中手动执行以下 SQL 语句创建表:")
            logger.info(reports_sql)
            logger.info(sources_sql)
            logger.info(news_items_sql)
            logger.info(paper_items_sql)
            sys.exit(1)

if __name__ == "__main__":
    create_tables()
