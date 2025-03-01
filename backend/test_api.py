#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API接口测试脚本
用于测试后端API接口的可用性和功能
"""

import requests
import json
import sys
from datetime import datetime

# 测试配置
BASE_URL = "http://localhost:5001"  # 后端服务地址
TIMEOUT = 5  # 请求超时时间（秒）

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(message):
    """打印带颜色的标题"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {message} ==={Colors.ENDC}\n")

def print_result(success, message, data=None):
    """打印测试结果"""
    if success:
        print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")
    
    if data:
        if isinstance(data, (dict, list)):
            print(f"{Colors.OKBLUE}{json.dumps(data, ensure_ascii=False, indent=2)}{Colors.ENDC}")
        else:
            print(f"{Colors.OKBLUE}{data}{Colors.ENDC}")

def test_health():
    """测试健康检查接口"""
    print_header("测试健康检查接口")
    
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        if data.get("success") and data.get("status") == "healthy":
            print_result(True, "健康检查成功", data)
            return True
        else:
            print_result(False, "健康检查失败", data)
            return False
    except Exception as e:
        print_result(False, f"请求异常: {str(e)}")
        return False

def test_latest_report():
    """测试获取最新报告接口"""
    print_header("测试获取最新报告接口")
    
    try:
        response = requests.get(f"{BASE_URL}/api/reports/latest", timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        if data.get("success"):
            print_result(True, "获取最新报告成功", data)
            return True
        else:
            print_result(False, "获取最新报告失败", data)
            return False
    except Exception as e:
        print_result(False, f"请求异常: {str(e)}")
        return False

def test_reports_list():
    """测试获取报告列表接口"""
    print_header("测试获取报告列表接口")
    
    try:
        response = requests.get(f"{BASE_URL}/api/reports?limit=5", timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        if data.get("success"):
            print_result(True, "获取报告列表成功", data)
            return True
        else:
            print_result(False, "获取报告列表失败", data)
            return False
    except Exception as e:
        print_result(False, f"请求异常: {str(e)}")
        return False

def test_sources():
    """测试获取信息源接口"""
    print_header("测试获取信息源接口")
    
    try:
        response = requests.get(f"{BASE_URL}/api/sources", timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        if data.get("success"):
            print_result(True, "获取信息源成功", data)
            return True
        else:
            print_result(False, "获取信息源失败", data)
            return False
    except Exception as e:
        print_result(False, f"请求异常: {str(e)}")
        return False

def test_generate_report():
    """测试手动生成报告接口"""
    print_header("测试手动生成报告接口")
    
    try:
        response = requests.post(f"{BASE_URL}/api/generate", timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        if data.get("success"):
            print_result(True, "触发报告生成成功", data)
            return True
        else:
            print_result(False, "触发报告生成失败", data)
            return False
    except Exception as e:
        print_result(False, f"请求异常: {str(e)}")
        return False

def test_rss():
    """测试RSS订阅接口"""
    print_header("测试RSS订阅接口")
    
    try:
        response = requests.get(f"{BASE_URL}/rss", timeout=TIMEOUT)
        response.raise_for_status()
        
        if response.status_code == 200 and response.headers.get('Content-Type') and 'xml' in response.headers.get('Content-Type'):
            print_result(True, "获取RSS订阅成功", response.text[:200] + "...")
            return True
        else:
            print_result(False, "获取RSS订阅失败", response.text)
            return False
    except Exception as e:
        print_result(False, f"请求异常: {str(e)}")
        return False

def run_all_tests():
    """运行所有测试"""
    print_header(f"开始API接口测试 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 测试列表
    tests = [
        ("健康检查", test_health),
        ("获取最新报告", test_latest_report),
        ("获取报告列表", test_reports_list),
        ("获取信息源", test_sources),
        ("手动生成报告", test_generate_report),
        ("RSS订阅", test_rss)
    ]
    
    # 运行测试
    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))
    
    # 打印测试结果摘要
    print_header("测试结果摘要")
    success_count = sum(1 for _, result in results if result)
    total_count = len(results)
    success_rate = (success_count / total_count) * 100
    
    print(f"总测试数: {total_count}")
    print(f"成功数: {success_count}")
    print(f"失败数: {total_count - success_count}")
    print(f"成功率: {success_rate:.2f}%")
    
    # 打印详细结果
    print("\n详细结果:")
    for name, result in results:
        if result:
            print(f"{Colors.OKGREEN}✓ {name}{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}✗ {name}{Colors.ENDC}")
    
    # 返回测试是否全部成功
    return success_count == total_count

if __name__ == "__main__":
    try:
        all_success = run_all_tests()
        sys.exit(0 if all_success else 1)
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        sys.exit(2)
    except Exception as e:
        print(f"\n{Colors.FAIL}测试过程中发生错误: {str(e)}{Colors.ENDC}")
        sys.exit(3)
