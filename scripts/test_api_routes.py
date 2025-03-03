#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试 API 路由
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 测试 API 的基础 URL
BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:5000')

def test_health_endpoint():
    """测试健康检查接口"""
    logger.info("测试健康检查接口...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            logger.info(f"健康检查接口返回: {data}")
            return True
        else:
            logger.error(f"健康检查接口返回错误状态码: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"测试健康检查接口失败: {e}")
        return False

def test_reports_endpoint():
    """测试报告接口"""
    logger.info("测试报告接口...")
    try:
        response = requests.get(f"{BASE_URL}/api/reports")
        if response.status_code == 200:
            data = response.json()
            logger.info(f"报告接口返回 {len(data)} 条记录")
            return True
        else:
            logger.error(f"报告接口返回错误状态码: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"测试报告接口失败: {e}")
        return False

def test_sources_endpoint():
    """测试信息源接口"""
    logger.info("测试信息源接口...")
    try:
        response = requests.get(f"{BASE_URL}/api/sources")
        if response.status_code == 200:
            data = response.json()
            logger.info(f"信息源接口返回 {len(data)} 条记录")
            return True
        else:
            logger.error(f"信息源接口返回错误状态码: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"测试信息源接口失败: {e}")
        return False

def test_rss_endpoint():
    """测试 RSS 接口"""
    logger.info("测试 RSS 接口...")
    try:
        response = requests.get(f"{BASE_URL}/api/rss")
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            if 'application/xml' in content_type or 'application/rss+xml' in content_type:
                logger.info(f"RSS 接口返回正确的内容类型: {content_type}")
                return True
            else:
                logger.error(f"RSS 接口返回错误的内容类型: {content_type}")
                return False
        else:
            logger.error(f"RSS 接口返回错误状态码: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"测试 RSS 接口失败: {e}")
        return False

def test_report_by_date_endpoint():
    """测试获取指定日期报告接口"""
    logger.info("测试获取指定日期报告接口...")
    today = datetime.now().strftime('%Y-%m-%d')
    try:
        response = requests.get(f"{BASE_URL}/api/reports/{today}")
        if response.status_code == 200:
            data = response.json()
            logger.info(f"获取到日期为 {today} 的报告")
            return True
        elif response.status_code == 404:
            logger.info(f"未找到日期为 {today} 的报告，这是正常的")
            return True
        else:
            logger.error(f"获取指定日期报告接口返回错误状态码: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"测试获取指定日期报告接口失败: {e}")
        return False

def main():
    """主函数"""
    logger.info(f"开始测试 API 路由，基础 URL: {BASE_URL}")
    
    tests = [
        test_health_endpoint,
        test_reports_endpoint,
        test_sources_endpoint,
        test_rss_endpoint,
        test_report_by_date_endpoint
    ]
    
    results = {}
    all_passed = True
    
    for test in tests:
        test_name = test.__name__
        result = test()
        results[test_name] = "通过" if result else "失败"
        if not result:
            all_passed = False
    
    logger.info("\n测试结果:")
    for test_name, result in results.items():
        logger.info(f"{test_name}: {result}")
    
    if all_passed:
        logger.info("所有 API 路由测试通过")
        return 0
    else:
        logger.error("部分 API 路由测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
