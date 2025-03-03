import os
from supabase import create_client, Client
from dotenv import load_dotenv
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# 初始化 Supabase 客户端
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    logger.warning("Supabase 环境变量未设置，将使用本地文件存储")
    supabase = None
else:
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        logger.info("Supabase 客户端初始化成功")
    except Exception as e:
        logger.error(f"Supabase 客户端初始化失败: {e}")
        supabase = None

def init_supabase():
    """初始化 Supabase 客户端"""
    global supabase
    
    # 如果已经初始化，直接返回
    if supabase:
        return supabase
    
    # 尝试重新初始化
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        logger.warning("Supabase 环境变量未设置，将使用本地文件存储")
        return None
    
    try:
        supabase = create_client(supabase_url, supabase_key)
        logger.info("Supabase 客户端初始化成功")
        return supabase
    except Exception as e:
        logger.error(f"Supabase 客户端初始化失败: {e}")
        return None

def get_reports(limit=10):
    """获取报告列表"""
    if not supabase:
        logger.warning("Supabase 客户端未初始化，使用本地文件存储")
        from backend.app import read_reports
        reports = read_reports()
        return reports[:limit] if limit < len(reports) else reports
        
    try:
        response = supabase.table('reports').select('*').order('date', desc=True).limit(limit).execute()
        return response.data
    except Exception as e:
        logger.error(f"获取报告失败: {e}")
        return []

def get_report_by_date(date):
    """根据日期获取报告"""
    if not supabase:
        logger.warning("Supabase 客户端未初始化，使用本地文件存储")
        from backend.app import read_reports
        reports = read_reports()
        for report in reports:
            if report.get('date') == date:
                return report
        return None
        
    try:
        response = supabase.table('reports').select('*').eq('date', date).execute()
        if response.data and len(response.data) > 0:
            report = response.data[0]
            
            # 获取关联的新闻和论文数据
            news_response = supabase.table('news_items').select('*').eq('report_id', report['id']).execute()
            papers_response = supabase.table('paper_items').select('*').eq('report_id', report['id']).execute()
            
            # 组装完整的报告数据
            report['raw_data'] = {
                'news': news_response.data,
                'papers': papers_response.data
            }
            
            return report
        return None
    except Exception as e:
        logger.error(f"获取报告失败: {e}")
        return None

def create_report(report_data):
    """创建新报告"""
    if not supabase:
        logger.warning("Supabase 客户端未初始化，使用本地文件存储")
        from backend.app import read_reports, write_reports
        reports = read_reports()
        
        # 检查是否已存在同日期的报告
        existing_report_index = next((i for i, r in enumerate(reports) if r.get('date') == report_data['date']), None)
        if existing_report_index is not None:
            # 更新已存在的报告
            reports[existing_report_index] = report_data
        else:
            # 添加新报告
            reports.append(report_data)
        
        write_reports(reports)
        return True
        
    try:
        # 1. 插入报告基本信息
        report_response = supabase.table('reports').insert({
            'date': report_data['date'],
            'summary': report_data['summary'],
            'model': report_data.get('model', 'Unknown'),
            'created_at': report_data.get('created_at')
        }).execute()
        
        if not report_response.data:
            raise Exception("创建报告失败")
            
        report_id = report_response.data[0]['id']
        
        # 2. 插入新闻数据
        if 'raw_data' in report_data and 'news' in report_data['raw_data']:
            news_items = []
            for news in report_data['raw_data']['news']:
                news_item = {
                    'report_id': report_id,
                    'title': news['title'],
                    'url': news['url'],
                    'source': news['source'],
                    'published_at': news.get('published_at'),
                    'score': news.get('score'),
                    'comments': news.get('comments'),
                    'summary': news.get('summary')
                }
                news_items.append(news_item)
                
            if news_items:
                supabase.table('news_items').insert(news_items).execute()
        
        # 3. 插入论文数据
        if 'raw_data' in report_data and 'papers' in report_data['raw_data']:
            paper_items = []
            for paper in report_data['raw_data']['papers']:
                paper_item = {
                    'report_id': report_id,
                    'title': paper['title'],
                    'authors': paper['authors'],
                    'summary': paper.get('summary'),
                    'published_at': paper.get('published_at'),
                    'url': paper['url'],
                    'pdf_url': paper.get('pdf_url'),
                    'categories': paper.get('categories', [])
                }
                paper_items.append(paper_item)
                
            if paper_items:
                supabase.table('paper_items').insert(paper_items).execute()
                
        return True
    except Exception as e:
        logger.error(f"创建报告失败: {e}")
        return False

def update_report(date, report_data):
    """更新报告"""
    if not supabase:
        logger.warning("Supabase 客户端未初始化，使用本地文件存储")
        return create_report(report_data)  # 复用创建报告的逻辑
        
    try:
        # 1. 获取报告ID
        report_response = supabase.table('reports').select('id').eq('date', date).execute()
        if not report_response.data or len(report_response.data) == 0:
            return False
            
        report_id = report_response.data[0]['id']
        
        # 2. 更新报告基本信息
        supabase.table('reports').update({
            'summary': report_data['summary'],
            'model': report_data.get('model', 'Unknown')
        }).eq('id', report_id).execute()
        
        # 3. 删除旧的新闻和论文数据
        supabase.table('news_items').delete().eq('report_id', report_id).execute()
        supabase.table('paper_items').delete().eq('report_id', report_id).execute()
        
        # 4. 插入新的新闻数据
        if 'raw_data' in report_data and 'news' in report_data['raw_data']:
            news_items = []
            for news in report_data['raw_data']['news']:
                news_item = {
                    'report_id': report_id,
                    'title': news['title'],
                    'url': news['url'],
                    'source': news['source'],
                    'published_at': news.get('published_at'),
                    'score': news.get('score'),
                    'comments': news.get('comments'),
                    'summary': news.get('summary')
                }
                news_items.append(news_item)
                
            if news_items:
                supabase.table('news_items').insert(news_items).execute()
        
        # 5. 插入新的论文数据
        if 'raw_data' in report_data and 'papers' in report_data['raw_data']:
            paper_items = []
            for paper in report_data['raw_data']['papers']:
                paper_item = {
                    'report_id': report_id,
                    'title': paper['title'],
                    'authors': paper['authors'],
                    'summary': paper.get('summary'),
                    'published_at': paper.get('published_at'),
                    'url': paper['url'],
                    'pdf_url': paper.get('pdf_url'),
                    'categories': paper.get('categories', [])
                }
                paper_items.append(paper_item)
                
            if paper_items:
                supabase.table('paper_items').insert(paper_items).execute()
                
        return True
    except Exception as e:
        logger.error(f"更新报告失败: {e}")
        return False

def get_sources():
    """获取信息源列表"""
    if not supabase:
        logger.warning("Supabase 客户端未初始化，使用本地文件存储")
        from backend.app import read_sources
        return read_sources()
        
    try:
        response = supabase.table('sources').select('*').execute()
        return response.data
    except Exception as e:
        logger.error(f"获取信息源失败: {e}")
        return []
