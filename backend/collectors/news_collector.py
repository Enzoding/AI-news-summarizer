import requests
import feedparser
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def collect_hackernews():
    """
    从Hacker News收集AI相关新闻
    返回格式化的新闻列表
    """
    logger.info("开始收集Hacker News数据")
    news_list = []
    
    try:
        # 获取最新的500条故事ID
        top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(top_stories_url)
        story_ids = response.json()[:100]  # 只取前100条
        
        # 获取每个故事的详细信息
        for story_id in story_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_response = requests.get(story_url)
            story = story_response.json()
            
            # 检查是否与AI相关 (简单的关键词匹配)
            title = story.get('title', '').lower()
            ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning', 
                          'neural network', 'llm', 'large language model', 'gpt', 'chatgpt', 
                          'openai', 'anthropic', 'claude', 'gemini', 'deepseek']
            
            if any(keyword in title for keyword in ai_keywords):
                # 格式化新闻数据
                news_item = {
                    'title': story.get('title', ''),
                    'url': story.get('url', ''),
                    'source': 'Hacker News',
                    'published_at': datetime.fromtimestamp(story.get('time', 0)).isoformat(),
                    'score': story.get('score', 0),
                    'comments': story.get('descendants', 0)
                }
                news_list.append(news_item)
                logger.debug(f"收集到Hacker News: {news_item['title']}")
        
        logger.info(f"Hacker News收集完成，共{len(news_list)}条")
        return news_list
    
    except Exception as e:
        logger.error(f"收集Hacker News失败: {e}")
        return []

def collect_venturebeat():
    """
    从VentureBeat收集AI相关新闻
    返回格式化的新闻列表
    """
    logger.info("开始收集VentureBeat数据")
    news_list = []
    
    try:
        # 解析RSS feed
        feed_url = "https://venturebeat.com/category/ai/feed/"
        feed = feedparser.parse(feed_url)
        
        # 获取过去7天的文章
        one_week_ago = datetime.now() - timedelta(days=7)
        
        for entry in feed.entries:
            # 解析发布日期
            published = datetime(*entry.published_parsed[:6])
            
            # 只保留最近7天的文章
            if published >= one_week_ago:
                news_item = {
                    'title': entry.title,
                    'url': entry.link,
                    'source': 'VentureBeat AI',
                    'published_at': published.isoformat(),
                    'summary': entry.summary if hasattr(entry, 'summary') else ''
                }
                news_list.append(news_item)
                logger.debug(f"收集到VentureBeat: {news_item['title']}")
        
        logger.info(f"VentureBeat收集完成，共{len(news_list)}条")
        return news_list
    
    except Exception as e:
        logger.error(f"收集VentureBeat失败: {e}")
        return []

if __name__ == "__main__":
    # 设置日志
    logging.basicConfig(level=logging.INFO)
    
    # 测试收集功能
    hn_news = collect_hackernews()
    vb_news = collect_venturebeat()
    
    print(f"Hacker News: {len(hn_news)} articles")
    print(f"VentureBeat: {len(vb_news)} articles")
