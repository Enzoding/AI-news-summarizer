#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
运行开发服务器
"""

import os
import sys
import logging
from dotenv import load_dotenv

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 配置日志
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

def run_server():
    """运行开发服务器"""
    try:
        from backend.app import app
        
        host = os.environ.get('FLASK_HOST', '0.0.0.0')
        port = int(os.environ.get('FLASK_PORT', 5002))
        
        logger.info(f"启动开发服务器，监听 {host}:{port}")
        app.run(host=host, port=port, debug=True)
        
        return 0
    except Exception as e:
        logger.error(f"启动开发服务器失败: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_server())
