from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging

# 导入自定义模块
from collectors.news_collector import collect_hackernews, collect_venturebeat
from collectors.paper_collector import collect_arxiv_papers
from models.model_manager import generate_summary

# 配置日志
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)

# 数据存储路径
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
REPORTS_FILE = os.path.join(DATA_DIR, 'reports.json')
SOURCES_FILE = os.path.join(DATA_DIR, 'sources.json')

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)

# 初始化数据文件
if not os.path.exists(REPORTS_FILE):
    with open(REPORTS_FILE, 'w') as f:
        json.dump([], f)

if not os.path.exists(SOURCES_FILE):
    with open(SOURCES_FILE, 'w') as f:
        json.dump([], f)

def read_reports():
    """读取报告数据"""
    try:
        with open(REPORTS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"读取报告数据失败: {e}")
        return []

def write_reports(reports):
    """写入报告数据"""
    try:
        with open(REPORTS_FILE, 'w') as f:
            json.dump(reports, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"写入报告数据失败: {e}")

def read_sources():
    """读取信息源数据"""
    try:
        with open(SOURCES_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"读取信息源数据失败: {e}")
        return []

def write_sources(sources):
    """写入信息源数据"""
    try:
        with open(SOURCES_FILE, 'w') as f:
            json.dump(sources, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"写入信息源数据失败: {e}")

@app.route('/api/reports', methods=['GET'])
def get_reports():
    """获取所有报告"""
    try:
        limit = int(request.args.get('limit', 10))
        reports = read_reports()
        # 按日期排序
        reports.sort(key=lambda x: x.get('date', ''), reverse=True)
        return jsonify({"success": True, "data": reports[:limit]})
    except Exception as e:
        logger.error(f"获取报告失败: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/reports/<date>', methods=['GET'])
def get_report_by_date(date):
    """获取指定日期的报告"""
    try:
        reports = read_reports()
        report = next((r for r in reports if r.get('date') == date), None)
        if report:
            return jsonify({"success": True, "data": report})
        else:
            return jsonify({"success": False, "error": "报告不存在"}), 404
    except Exception as e:
        logger.error(f"获取报告失败: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/reports/latest', methods=['GET'])
def get_latest_report():
    """获取最新报告"""
    try:
        reports = read_reports()
        if not reports:
            return jsonify({"success": False, "error": "没有报告"}), 404
            
        # 按日期排序
        reports.sort(key=lambda x: x.get('date', ''), reverse=True)
        return jsonify({"success": True, "data": reports[0]})
    except Exception as e:
        logger.error(f"获取最新报告失败: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/sources', methods=['GET'])
def get_sources():
    """获取所有信息源"""
    try:
        sources = read_sources()
        return jsonify({"success": True, "data": sources})
    except Exception as e:
        logger.error(f"获取信息源失败: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def manual_generate():
    """手动触发生成报告"""
    try:
        generate_daily_report()
        return jsonify({"success": True, "message": "报告生成任务已触发"})
    except Exception as e:
        logger.error(f"手动生成报告失败: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/rss', methods=['GET'])
def get_rss():
    """获取RSS订阅"""
    from feedgen.feed import FeedGenerator
    import datetime
    
    try:
        reports = read_reports()
        reports.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        fg = FeedGenerator()
        fg.title('AI行业信息收集总结助手')
        fg.description('每日AI行业新闻和论文总结')
        fg.link(href=request.host_url)
        fg.language('zh-CN')
        
        for report in reports[:10]:  # 只取最新的10条
            fe = fg.add_entry()
            fe.title(f"AI行业日报 {report['date']}")
            fe.description(report['summary'])
            fe.link(href=f"{request.host_url}report/{report['date']}")
            fe.guid(report['date'])
            fe.pubDate(datetime.datetime.strptime(report['date'], "%Y-%m-%d"))
        
        rssfeed = fg.rss_str(pretty=True)
        return rssfeed, 200, {'Content-Type': 'application/xml'}
    except Exception as e:
        logger.error(f"生成RSS失败: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    try:
        # 检查数据文件是否可读
        reports = read_reports()
        sources = read_sources()
        
        # 返回健康状态和基本信息
        return jsonify({
            "success": True,
            "status": "healthy",
            "version": "1.0.0",
            "reports_count": len(reports),
            "sources_count": len(sources),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        return jsonify({
            "success": False,
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

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
        summary = generate_summary(prompt_data)
        
        # 保存报告到本地文件
        report = {
            "date": today,
            "summary": summary,
            "raw_data": {
                "news": news_data,
                "papers": papers_data
            },
            "created_at": datetime.now().isoformat()
        }
        
        reports = read_reports()
        
        # 检查是否已存在同日期的报告
        existing_report_index = next((i for i, r in enumerate(reports) if r.get('date') == today), None)
        if existing_report_index is not None:
            # 更新已存在的报告
            reports[existing_report_index] = report
        else:
            # 添加新报告
            reports.append(report)
        
        write_reports(reports)
        logger.info(f"报告生成成功: {today}")
        
        return True
    except Exception as e:
        logger.error(f"报告生成失败: {e}")
        return False

def init_scheduler():
    """初始化定时任务"""
    scheduler = BackgroundScheduler()
    # 每天凌晨2点执行
    scheduler.add_job(generate_daily_report, 'cron', hour=2, minute=0)
    scheduler.start()
    logger.info("定时任务已启动")

def init_sources():
    """初始化信息源"""
    sources = [
        {
            "name": "Hacker News",
            "type": "news",
            "url": "https://github.com/HackerNews/API",
            "description": "Hacker News API"
        },
        {
            "name": "VentureBeat AI",
            "type": "news",
            "url": "https://venturebeat.com/category/ai/feed/",
            "description": "VentureBeat AI RSS Feed"
        },
        {
            "name": "arXiv",
            "type": "papers",
            "url": "https://arxiv.org/",
            "description": "arXiv论文库"
        }
    ]
    
    write_sources(sources)
    logger.info("信息源初始化完成")

if __name__ == '__main__':
    # 初始化信息源
    init_sources()
    
    # 启动定时任务
    init_scheduler()
    
    # 启动Flask应用
    port = 5002
    app.run(host='0.0.0.0', port=port, debug=True)
