#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简化版 Supabase 连接测试
"""

import os
import sys
from dotenv import load_dotenv
import logging

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 配置日志
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

def test_supabase_connection():
    """测试 Supabase 连接"""
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        logger.error("缺少 Supabase 环境变量，请设置 SUPABASE_URL 和 SUPABASE_KEY")
        return False
    
    try:
        from supabase import create_client, Client
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # 测试连接 - 尝试获取 reports 表
        response = supabase.table('reports').select('id').limit(1).execute()
        logger.info(f"连接成功！获取到 {len(response.data)} 条记录")
        
        # 测试获取 sources 表
        response = supabase.table('sources').select('*').execute()
        logger.info(f"获取到 {len(response.data)} 个信息源")
        
        # 测试获取最新报告
        response = supabase.table('reports').select('*').order('date', desc=True).limit(1).execute()
        if response.data:
            logger.info(f"最新报告日期: {response.data[0].get('date')}")
        
        return True
    except Exception as e:
        logger.error(f"连接失败: {e}")
        return False

if __name__ == "__main__":
    if test_supabase_connection():
        logger.info("Supabase 连接测试成功！")
        sys.exit(0)
    else:
        logger.error("Supabase 连接测试失败！")
        sys.exit(1)
