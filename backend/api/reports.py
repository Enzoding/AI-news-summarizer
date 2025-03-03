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
    from backend.db.supabase_client import get_reports, get_report_by_date
except ImportError:
    logger.error("无法导入 Supabase 客户端，请确保已安装相关依赖")
    
    # 回退到本地文件存储
    def read_reports():
        """读取报告数据"""
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data')
        reports_file = os.path.join(data_dir, 'reports.json')
        try:
            with open(reports_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"读取报告数据失败: {e}")
            return []
    
    def get_reports(limit=10):
        """获取报告列表"""
        reports = read_reports()
        return reports[:limit] if limit < len(reports) else reports
    
    def get_report_by_date(date):
        """根据日期获取报告"""
        reports = read_reports()
        for report in reports:
            if report.get('date') == date:
                return report
        return None

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理 GET 请求"""
        try:
            # 解析路径
            path_parts = self.path.split('?')[0].split('/')
            path_parts = [p for p in path_parts if p]  # 移除空字符串
            
            # 设置响应头
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # 处理不同的路径
            if len(path_parts) == 0 or path_parts[-1] == 'reports':
                # 获取所有报告
                limit = 10  # 默认限制
                reports = get_reports(limit)
                response = {"success": True, "data": reports}
            elif len(path_parts) > 0 and path_parts[-2] == 'reports':
                # 获取指定日期的报告
                date = path_parts[-1]
                report = get_report_by_date(date)
                if report:
                    response = {"success": True, "data": report}
                else:
                    response = {"success": False, "error": "报告不存在"}
                    self.send_response(404)
            else:
                # 未知路径
                response = {"success": False, "error": "未知路径"}
                self.send_response(404)
            
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
