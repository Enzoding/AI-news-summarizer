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

# 导入 Supabase 客户端
try:
    from backend.db.supabase_client import init_supabase, get_reports, get_sources
    # 初始化 Supabase 客户端
    supabase = init_supabase()
    USE_SUPABASE = supabase is not None
except ImportError as e:
    logger.warning(f"无法导入 Supabase 客户端: {e}")
    USE_SUPABASE = False
    
    # 定义占位函数，防止程序崩溃
    def get_reports(limit=1):
        return []
    
    def get_sources():
        return []

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理 GET 请求"""
        try:
            # 设置响应头
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # 检查数据是否可读
            if USE_SUPABASE:
                reports = get_reports(1)
                sources = get_sources()
                db_status = "supabase"
            else:
                # 读取本地文件
                data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data')
                reports_file = os.path.join(data_dir, 'reports.json')
                sources_file = os.path.join(data_dir, 'sources.json')
                
                try:
                    with open(reports_file, 'r', encoding='utf-8') as f:
                        reports = json.load(f)
                except Exception:
                    reports = []
                
                try:
                    with open(sources_file, 'r', encoding='utf-8') as f:
                        sources = json.load(f)
                except Exception:
                    sources = []
                
                db_status = "local"
            
            # 返回健康状态和基本信息
            response = {
                "success": True,
                "status": "healthy",
                "version": "1.0.0",
                "reports_count": len(reports),
                "sources_count": len(sources),
                "db_status": db_status,
                "timestamp": datetime.now().isoformat(),
                "environment": "vercel" if os.environ.get("VERCEL") else "local"
            }
            
            # 发送响应
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            logger.error(f"健康检查失败: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = {
                "success": False,
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

def handler(event, context):
    """Vercel Serverless Function 处理程序"""
    return Handler(event, context)
