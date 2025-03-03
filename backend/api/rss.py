from http.server import BaseHTTPRequestHandler
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
    from backend.db.supabase_client import init_supabase, get_reports
    # 初始化 Supabase 客户端
    supabase = init_supabase()
    USE_SUPABASE = supabase is not None
except ImportError as e:
    logger.warning(f"无法导入 Supabase 客户端: {e}")
    USE_SUPABASE = False
    
    # 定义占位函数，防止程序崩溃
    def get_reports(limit=10):
        return []

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理 GET 请求"""
        try:
            # 设置响应头
            self.send_response(200)
            self.send_header('Content-Type', 'application/xml')
            self.end_headers()
            
            # 获取报告数据
            if USE_SUPABASE:
                # 使用 Supabase 获取报告
                reports = get_reports(10)
            else:
                # 读取本地文件
                import json
                data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data')
                reports_file = os.path.join(data_dir, 'reports.json')
                
                try:
                    with open(reports_file, 'r', encoding='utf-8') as f:
                        reports = json.load(f)
                        # 按日期排序
                        reports.sort(key=lambda x: x.get('date', ''), reverse=True)
                        reports = reports[:10]  # 只取最新的10条
                except Exception as e:
                    logger.error(f"读取报告数据失败: {e}")
                    reports = []
            
            # 生成 RSS 内容
            from feedgen.feed import FeedGenerator
            import datetime
            
            # 获取主机 URL
            host_url = os.environ.get('VERCEL_URL', 'http://localhost:5002')
            if not host_url.startswith('http'):
                host_url = f"https://{host_url}"
            
            fg = FeedGenerator()
            fg.title('AI行业信息收集总结助手')
            fg.description('每日AI行业新闻和论文总结')
            fg.link(href=host_url)
            fg.language('zh-CN')
            
            for report in reports:
                fe = fg.add_entry()
                fe.title(f"AI行业日报 {report['date']}")
                fe.description(report['summary'])
                fe.link(href=f"{host_url}/report/{report['date']}")
                fe.guid(report['date'])
                fe.pubDate(datetime.datetime.strptime(report['date'], "%Y-%m-%d"))
            
            rssfeed = fg.rss_str(pretty=True)
            
            # 发送响应
            self.wfile.write(rssfeed)
        except Exception as e:
            logger.error(f"生成RSS失败: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"生成RSS失败: {e}".encode('utf-8'))

def handler(event, context):
    """Vercel Serverless Function 处理程序"""
    return Handler(event, context)
