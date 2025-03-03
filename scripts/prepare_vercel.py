#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
准备 Vercel 部署
"""

import os
import sys
import json
import shutil
from dotenv import load_dotenv
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 项目根目录
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def check_vercel_config():
    """检查 Vercel 配置文件"""
    vercel_json = os.path.join(ROOT_DIR, 'vercel.json')
    
    if not os.path.exists(vercel_json):
        logger.error("vercel.json 文件不存在！")
        return False
    
    try:
        with open(vercel_json, 'r') as f:
            config = json.load(f)
            
        # 检查必要的配置
        if 'version' not in config:
            logger.error("vercel.json 缺少 version 字段")
            return False
            
        if 'builds' not in config:
            logger.error("vercel.json 缺少 builds 字段")
            return False
            
        if 'routes' not in config:
            logger.error("vercel.json 缺少 routes 字段")
            return False
            
        logger.info("vercel.json 配置检查通过")
        return True
    except Exception as e:
        logger.error(f"检查 vercel.json 失败: {e}")
        return False

def check_api_routes():
    """检查 API 路由文件"""
    api_dir = os.path.join(ROOT_DIR, 'backend', 'api')
    
    if not os.path.exists(api_dir):
        logger.error("backend/api 目录不存在！")
        return False
    
    required_routes = ['health.py', 'reports.py', 'sources.py', 'generate.py', 'rss.py']
    missing_routes = []
    
    for route in required_routes:
        if not os.path.exists(os.path.join(api_dir, route)):
            missing_routes.append(route)
    
    if missing_routes:
        logger.error(f"缺少以下 API 路由文件: {', '.join(missing_routes)}")
        return False
    
    logger.info("API 路由文件检查通过")
    return True

def check_environment_variables():
    """检查环境变量"""
    required_vars = ['SUPABASE_URL', 'SUPABASE_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"缺少以下环境变量: {', '.join(missing_vars)}")
        return False
    
    logger.info("环境变量检查通过")
    return True

def check_requirements():
    """检查依赖文件"""
    requirements_file = os.path.join(ROOT_DIR, 'requirements.txt')
    
    if not os.path.exists(requirements_file):
        logger.error("requirements.txt 文件不存在！")
        return False
    
    try:
        with open(requirements_file, 'r') as f:
            requirements = f.read()
            
        # 检查必要的依赖
        required_packages = ['flask', 'supabase', 'python-dotenv']
        missing_packages = []
        
        for package in required_packages:
            if package not in requirements:
                missing_packages.append(package)
        
        if missing_packages:
            logger.error(f"requirements.txt 缺少以下依赖: {', '.join(missing_packages)}")
            return False
        
        logger.info("requirements.txt 检查通过")
        return True
    except Exception as e:
        logger.error(f"检查 requirements.txt 失败: {e}")
        return False

def main():
    """主函数"""
    logger.info("开始检查 Vercel 部署准备情况...")
    
    checks = [
        check_vercel_config,
        check_api_routes,
        check_environment_variables,
        check_requirements
    ]
    
    all_passed = True
    
    for check in checks:
        if not check():
            all_passed = False
    
    if all_passed:
        logger.info("所有检查通过，可以部署到 Vercel")
        return 0
    else:
        logger.error("部分检查未通过，请修复后再部署")
        return 1

if __name__ == "__main__":
    sys.exit(main())
