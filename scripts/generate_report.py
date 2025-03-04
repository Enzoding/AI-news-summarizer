#!/usr/bin/env python3
import os
import sys

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from backend.app import generate_daily_report
import logging

# 配置日志
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("开始手动生成日报...")
    try:
        success = generate_daily_report()
        if success:
            logger.info("日报生成成功！")
            sys.exit(0)
        else:
            logger.error("日报生成失败！")
            sys.exit(1)
    except Exception as e:
        logger.error(f"生成日报时发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 