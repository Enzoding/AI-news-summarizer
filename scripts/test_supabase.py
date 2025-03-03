#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试 Supabase 连接和功能
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
    from backend.db.supabase_client import (
        init_supabase,
        get_reports,
        get_report_by_date,
        create_report,
        update_report,
        get_sources
    )
except ImportError as e:
    logger.error(f"导入 Supabase 客户端失败: {e}")
    sys.exit(1)

def test_connection():
    """测试 Supabase 连接"""
    logger.info("测试 Supabase 连接...")
    supabase = init_supabase()
    if supabase:
        logger.info("Supabase 连接成功！")
        return True
    else:
        logger.error("Supabase 连接失败！")
        return False

def test_get_reports():
    """测试获取报告列表"""
    logger.info("测试获取报告列表...")
    reports = get_reports(limit=5)
    if reports is not None:
        logger.info(f"获取到 {len(reports)} 条报告")
        return True
    else:
        logger.error("获取报告列表失败！")
        return False

def test_get_report_by_date():
    """测试获取指定日期的报告"""
    # 获取最新的报告日期
    reports = get_reports(limit=1)
    if not reports:
        logger.warning("没有找到报告，跳过测试")
        return True
    
    date = reports[0].get('date')
    logger.info(f"测试获取 {date} 的报告...")
    report = get_report_by_date(date)
    if report:
        logger.info(f"成功获取到 {date} 的报告")
        return True
    else:
        logger.error(f"获取 {date} 的报告失败！")
        return False

def test_create_and_update_report():
    """测试创建和更新报告"""
    test_date = datetime.now().strftime("%Y-%m-%d") + "-test"
    logger.info(f"测试创建报告 {test_date}...")
    
    # 创建测试报告
    test_report = {
        "date": test_date,
        "summary": "这是一个测试报告",
        "raw_data": {
            "news": [],
            "papers": []
        },
        "created_at": datetime.now().isoformat(),
        "model": "test"
    }
    
    # 创建报告
    success = create_report(test_report)
    if not success:
        logger.error("创建报告失败！")
        return False
    
    logger.info(f"报告 {test_date} 创建成功，测试更新...")
    
    # 更新报告
    test_report["summary"] = "这是一个更新后的测试报告"
    success = update_report(test_date, test_report)
    if not success:
        logger.error("更新报告失败！")
        return False
    
    logger.info(f"报告 {test_date} 更新成功")
    return True

def test_get_sources():
    """测试获取信息源列表"""
    logger.info("测试获取信息源列表...")
    sources = get_sources()
    if sources is not None:
        logger.info(f"获取到 {len(sources)} 个信息源")
        return True
    else:
        logger.error("获取信息源列表失败！")
        return False

def run_tests():
    """运行所有测试"""
    tests = [
        test_connection,
        test_get_reports,
        test_get_report_by_date,
        test_create_and_update_report,
        test_get_sources
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append((test.__name__, result))
        except Exception as e:
            logger.error(f"测试 {test.__name__} 出错: {e}")
            results.append((test.__name__, False))
    
    # 打印测试结果
    logger.info("\n测试结果:")
    all_passed = True
    for name, result in results:
        status = "通过" if result else "失败"
        color = "\033[92m" if result else "\033[91m"  # 绿色或红色
        reset = "\033[0m"
        logger.info(f"{color}{name}: {status}{reset}")
        if not result:
            all_passed = False
    
    if all_passed:
        logger.info("\033[92m所有测试通过！\033[0m")
        return 0
    else:
        logger.error("\033[91m部分测试失败！\033[0m")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())
