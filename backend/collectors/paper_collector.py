import arxiv
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def collect_arxiv_papers():
    """
    从arXiv收集AI相关论文
    返回格式化的论文列表
    """
    logger.info("开始收集arXiv论文")
    papers_list = []
    
    try:
        # 设置查询参数
        # 搜索AI相关领域的论文
        search_query = 'cat:cs.AI OR cat:cs.CL OR cat:cs.CV OR cat:cs.LG OR cat:cs.NE'
        
        # 获取最近7天的论文
        date_filter = datetime.now() - timedelta(days=7)
        
        # 执行查询
        search = arxiv.Search(
            query=search_query,
            max_results=50,  # 限制结果数量
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        for result in search.results():
            # 检查发布日期
            if result.published > date_filter:
                # 格式化论文数据
                paper = {
                    'title': result.title,
                    'authors': [author.name for author in result.authors],
                    'summary': result.summary,
                    'published_at': result.published.isoformat(),
                    'url': result.entry_id,
                    'pdf_url': result.pdf_url,
                    'categories': result.categories
                }
                papers_list.append(paper)
                logger.debug(f"收集到arXiv论文: {paper['title']}")
        
        logger.info(f"arXiv论文收集完成，共{len(papers_list)}篇")
        return papers_list
    
    except Exception as e:
        logger.error(f"收集arXiv论文失败: {e}")
        return []

if __name__ == "__main__":
    # 设置日志
    logging.basicConfig(level=logging.INFO)
    
    # 测试收集功能
    papers = collect_arxiv_papers()
    print(f"arXiv Papers: {len(papers)} papers")
