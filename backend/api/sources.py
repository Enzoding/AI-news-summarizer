from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from datetime import datetime
import logging

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 导入数据库客户端
try:
    from backend.db.supabase_client import get_sources
except ImportError:
    logger.error("无法导入 Supabase 客户端，请确保已安装相关依赖")
    
    # 回退到本地文件存储
    def read_sources():
        """读取信息源数据"""
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data')
        sources_file = os.path.join(data_dir, 'sources.json')
        try:
            with open(sources_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"读取信息源数据失败: {e}")
            return []
    
    def get_sources():
        """获取信息源列表"""
        return read_sources()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理 GET 请求"""
        try:
            # 设置响应头
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # 获取信息源
            sources = get_sources()
            response = {"success": True, "data": sources}
            
            # 发送响应
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            logger.error(f"处理请求失败: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

def handler(event, context):
    """Vercel Serverless Function 处理程序"""
    return Handler(event, context)
