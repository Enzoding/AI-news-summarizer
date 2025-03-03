import json
import os
import sys
from dotenv import load_dotenv
import logging

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

# 数据文件路径
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
REPORTS_FILE = os.path.join(DATA_DIR, 'reports.json')
SOURCES_FILE = os.path.join(DATA_DIR, 'sources.json')

# 检查 Supabase 环境变量
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    logger.error("缺少 Supabase 环境变量，请设置 SUPABASE_URL 和 SUPABASE_KEY")
    sys.exit(1)

try:
    from supabase import create_client, Client
    supabase: Client = create_client(supabase_url, supabase_key)
    logger.info("Supabase 客户端初始化成功")
except ImportError:
    logger.error("请安装 supabase 库: pip install supabase")
    sys.exit(1)
except Exception as e:
    logger.error(f"Supabase 客户端初始化失败: {e}")
    sys.exit(1)

def create_tables():
    """创建数据库表"""
    logger.info("开始检查数据库表...")
    
    try:
        # 检查表是否存在
        reports_sql = """
        CREATE TABLE IF NOT EXISTS reports (
          id SERIAL PRIMARY KEY,
          date DATE UNIQUE NOT NULL,
          summary TEXT NOT NULL,
          model VARCHAR(100),
          created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        sources_sql = """
        CREATE TABLE IF NOT EXISTS sources (
          id SERIAL PRIMARY KEY,
          name VARCHAR(100) UNIQUE NOT NULL,
          type VARCHAR(50) NOT NULL,
          url TEXT NOT NULL,
          description TEXT
        );
        """
        
        news_items_sql = """
        CREATE TABLE IF NOT EXISTS news_items (
          id SERIAL PRIMARY KEY,
          report_id INTEGER REFERENCES reports(id) ON DELETE CASCADE,
          title TEXT NOT NULL,
          url TEXT NOT NULL,
          source VARCHAR(100) NOT NULL,
          published_at TIMESTAMP WITH TIME ZONE,
          score INTEGER,
          comments INTEGER,
          summary TEXT
        );
        """
        
        paper_items_sql = """
        CREATE TABLE IF NOT EXISTS paper_items (
          id SERIAL PRIMARY KEY,
          report_id INTEGER REFERENCES reports(id) ON DELETE CASCADE,
          title TEXT NOT NULL,
          authors TEXT[] NOT NULL,
          summary TEXT,
          published_at TIMESTAMP WITH TIME ZONE,
          url TEXT NOT NULL,
          pdf_url TEXT,
          categories TEXT[]
        );
        """
        
        logger.info("请确保在 Supabase 控制台中已经执行了以下 SQL 语句创建表:")
        logger.info(reports_sql)
        logger.info(sources_sql)
        logger.info(news_items_sql)
        logger.info(paper_items_sql)
        
    except Exception as e:
        logger.error(f"检查数据库表失败: {e}")
        sys.exit(1)

def migrate_sources():
    """迁移信息源数据"""
    logger.info("开始迁移信息源数据...")
    
    try:
        with open(SOURCES_FILE, 'r', encoding='utf-8') as f:
            sources = json.load(f)
            
        for source in sources:
            supabase.table('sources').insert({
                'name': source['name'],
                'type': source['type'],
                'url': source['url'],
                'description': source['description']
            }).execute()
            
        logger.info(f"成功迁移 {len(sources)} 条信息源数据")
    except Exception as e:
        logger.error(f"迁移信息源数据失败: {e}")
        sys.exit(1)

def migrate_reports():
    """迁移报告数据"""
    logger.info("开始迁移报告数据...")
    
    try:
        with open(REPORTS_FILE, 'r', encoding='utf-8') as f:
            reports = json.load(f)
            
        for report in reports:
            # 1. 插入报告基本信息
            report_response = supabase.table('reports').insert({
                'date': report['date'],
                'summary': report['summary'],
                'model': report.get('model', 'Unknown'),
                'created_at': report.get('created_at')
            }).execute()
            
            if not report_response.data:
                logger.warning(f"插入报告 {report['date']} 失败，跳过")
                continue
                
            report_id = report_response.data[0]['id']
            
            # 2. 插入新闻数据
            if 'raw_data' in report and 'news' in report['raw_data']:
                news_items = []
                for news in report['raw_data']['news']:
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
            if 'raw_data' in report and 'papers' in report['raw_data']:
                paper_items = []
                for paper in report['raw_data']['papers']:
                    paper_item = {
                        'report_id': report_id,
                        'title': paper['title'],
                        'authors': paper.get('authors', []),
                        'summary': paper.get('summary'),
                        'published_at': paper.get('published_at'),
                        'url': paper['url'],
                        'pdf_url': paper.get('pdf_url'),
                        'categories': paper.get('categories', [])
                    }
                    paper_items.append(paper_item)
                    
                if paper_items:
                    supabase.table('paper_items').insert(paper_items).execute()
                    
            logger.info(f"成功迁移报告: {report['date']}")
            
        logger.info(f"成功迁移 {len(reports)} 条报告数据")
    except Exception as e:
        logger.error(f"迁移报告数据失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        create_tables()
        migrate_sources()
        migrate_reports()
        logger.info("数据迁移完成")
    except Exception as e:
        logger.error(f"数据迁移失败: {e}")
        sys.exit(1)
