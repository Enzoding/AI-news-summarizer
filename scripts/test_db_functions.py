#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试数据库函数
"""

import os
import sys
import json
from datetime import datetime
import logging

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 配置日志
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 导入 Supabase 客户端
try:
    from backend.db.supabase_client import init_supabase
except ImportError as e:
    logger.error(f"导入 Supabase 客户端失败: {e}")
    sys.exit(1)

def test_supabase_connection():
    """测试 Supabase 连接"""
    logger.info("测试 Supabase 连接...")
    supabase = init_supabase()
    if supabase:
        logger.info("Supabase 连接成功！")
        return True, supabase
    else:
        logger.error("Supabase 连接失败！")
        return False, None

def test_tables(supabase):
    """测试数据库表"""
    logger.info("测试数据库表...")
    tables = ['reports', 'sources', 'news_items', 'paper_items']
    results = {}
    
    for table in tables:
        try:
            response = supabase.table(table).select('count').execute()
            count = len(response.data)
            logger.info(f"表 {table} 存在，包含 {count} 条记录")
            results[table] = True
        except Exception as e:
            logger.error(f"表 {table} 测试失败: {e}")
            results[table] = False
    
    return all(results.values()), results

def main():
    """主函数"""
    logger.info("开始测试数据库函数...")
    
    # 测试 Supabase 连接
    connection_success, supabase = test_supabase_connection()
    if not connection_success:
        logger.error("Supabase 连接失败，无法继续测试")
        return 1
    
    # 测试数据库表
    tables_success, table_results = test_tables(supabase)
    
    # 输出测试结果
    logger.info("\n测试结果:")
    logger.info(f"Supabase 连接: {'成功' if connection_success else '失败'}")
    
    for table, result in table_results.items():
        logger.info(f"表 {table}: {'存在' if result else '不存在或无法访问'}")
    
    if connection_success and tables_success:
        logger.info("所有测试通过")
        return 0
    else:
        logger.error("部分测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
