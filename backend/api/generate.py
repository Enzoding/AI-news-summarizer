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

# 导入必要的模块
try:
    from backend.collectors.news_collector import collect_hackernews, collect_venturebeat
    from backend.collectors.paper_collector import collect_arxiv_papers
    from backend.models.model_manager import generate_summary
    from backend.db.supabase_client import create_report, get_report_by_date, update_report
except ImportError as e:
    logger.error(f"导入模块失败: {e}")
    
    # 定义占位函数，防止程序崩溃
    def collect_hackernews():
        return []
    
    def collect_venturebeat():
        return []
    
    def collect_arxiv_papers():
        return []
    
    def generate_summary(data):
        return "无法生成摘要，请检查依赖", "Unknown"
    
    def create_report(report_data):
        return False
    
    def get_report_by_date(date):
        return None
    
    def update_report(date, report_data):
        return False

def generate_daily_report():
    """生成每日报告"""
    logger.info("开始生成每日报告")
    today = datetime.now().strftime("%Y-%m-%d")
    
    try:
        # 收集信息
        news_data = []
        news_data.extend(collect_hackernews())
        news_data.extend(collect_venturebeat())
        
        papers_data = collect_arxiv_papers()
        
        # 准备提交给大语言模型的数据
        prompt_data = {
            "news": news_data,
            "papers": papers_data,
            "date": today
        }
        
        # 使用大语言模型生成总结
        summary, model_name = generate_summary(prompt_data)
        
        # 保存报告
        report = {
            "date": today,
            "summary": summary,
            "raw_data": {
                "news": news_data,
                "papers": papers_data
            },
            "created_at": datetime.now().isoformat(),
            "model": model_name
        }
        
        # 检查是否已存在同日期的报告
        existing_report = get_report_by_date(today)
        if existing_report:
            # 更新已存在的报告
            success = update_report(today, report)
        else:
            # 添加新报告
            success = create_report(report)
        
        if success:
            logger.info(f"报告生成成功: {today}，使用模型: {model_name}")
            return {"success": True, "date": today, "model": model_name}
        else:
            logger.error("报告保存失败")
            return {"success": False, "error": "报告保存失败"}
    except Exception as e:
        logger.error(f"报告生成失败: {e}")
        return {"success": False, "error": str(e)}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """处理 POST 请求"""
        try:
            # 设置响应头
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # 生成报告
            result = generate_daily_report()
            
            # 发送响应
            self.wfile.write(json.dumps(result).encode('utf-8'))
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
