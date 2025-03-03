import requests
import feedparser
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def collect_hackernews():
    """
    从Hacker News收集AI相关新闻
    返回格式化的新闻列表，按照分数降序排序，只返回前10条
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
            
            # 检查是否与AI相关 (增强的关键词匹配和内容分析)
            title = story.get('title', '').lower()
            url = story.get('url', '').lower()
            
            # 扩展AI关键词列表
            ai_keywords = [
                'ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning', 
                'neural network', 'llm', 'large language model', 'gpt', 'chatgpt', 
                'openai', 'anthropic', 'claude', 'gemini', 'deepseek', 'mistral', 'stable diffusion',
                'midjourney', 'dall-e', 'diffusion model', 'transformer', 'bert', 'nlp', 
                'natural language processing', 'computer vision', 'cv', 'reinforcement learning',
                'rl', 'generative ai', 'gen ai', 'foundation model', 'multimodal', 'embedding',
                'vector database', 'fine-tuning', 'prompt engineering', 'rag', 'retrieval augmented',
                'ai agent', 'ai assistant', 'ai model', 'ai system', 'ai technology', 'ai research',
                'ai development', 'ai application', 'ai ethics', 'ai safety', 'ai regulation',
                'ai policy', 'ai governance', 'ai alignment', 'ai capabilities', 'ai benchmark',
                'ai performance', 'ai training', 'ai inference', 'ai hardware', 'ai chip',
                'ai accelerator', 'ai startup', 'ai company', 'ai industry', 'ai market',
                'ai investment', 'ai funding', 'ai venture', 'ai capital', 'ai acquisition',
                'ai merger', 'ai partnership', 'ai collaboration', 'ai alliance', 'ai consortium',
                'ai initiative', 'ai project', 'ai program', 'ai framework', 'ai platform',
                'ai infrastructure', 'ai stack', 'ai pipeline', 'ai workflow', 'ai automation',
                'ai tool', 'ai solution', 'ai service', 'ai product', 'ai feature',
                'ai capability', 'ai function', 'ai algorithm', 'ai technique', 'ai method',
                'ai approach', 'ai strategy', 'ai vision', 'ai mission', 'ai goal',
                'ai objective', 'ai target', 'ai milestone', 'ai achievement', 'ai success',
                'ai failure', 'ai challenge', 'ai problem', 'ai issue', 'ai concern',
                'ai risk', 'ai threat', 'ai danger', 'ai harm', 'ai bias',
                'ai fairness', 'ai transparency', 'ai explainability', 'ai interpretability', 'ai accountability',
                'ai responsibility', 'ai liability', 'ai compliance', 'ai standard', 'ai certification',
                'ai audit', 'ai assessment', 'ai evaluation', 'ai testing', 'ai validation',
                'ai verification', 'ai quality', 'ai reliability', 'ai robustness', 'ai resilience',
                'ai security', 'ai privacy', 'ai confidentiality', 'ai integrity', 'ai availability'
            ]
            
            # 公司和产品名称关键词
            company_keywords = [
                'openai', 'anthropic', 'google ai', 'microsoft ai', 'meta ai', 'deepmind',
                'nvidia ai', 'amazon ai', 'ibm ai', 'apple ai', 'tesla ai', 'baidu ai',
                'tencent ai', 'alibaba ai', 'huawei ai', 'samsung ai', 'intel ai', 'amd ai',
                'qualcomm ai', 'arm ai', 'oracle ai', 'salesforce ai', 'adobe ai', 'sap ai',
                'siemens ai', 'ge ai', 'philips ai', 'bosch ai', 'toyota ai', 'honda ai',
                'bmw ai', 'mercedes ai', 'volkswagen ai', 'ford ai', 'gm ai', 'tesla autopilot',
                'waymo', 'cruise', 'argo ai', 'aurora', 'zoox', 'nuro', 'mobileye',
                'comma ai', 'scale ai', 'databricks', 'datarobot', 'c3.ai', 'palantir',
                'snowflake', 'confluent', 'cloudera', 'sas', 'h2o.ai', 'dataiku',
                'domino data lab', 'weights & biases', 'cohere', 'hugging face', 'replicate',
                'stability ai', 'runway', 'jasper', 'copy.ai', 'writer.com', 'grammarly ai',
                'notion ai', 'coda ai', 'figma ai', 'canva ai', 'adobe firefly',
                'microsoft copilot', 'github copilot', 'amazon q', 'google duet',
                'deepseek', 'perplexity', 'claude', 'gemini', 'grok', 'llama', 'falcon',
                'mistral', 'mixtral', 'phi', 'qwen', 'yi', 'baichuan', 'chatglm'
            ]
            
            # 检查标题是否包含AI关键词
            title_match = any(keyword in title for keyword in ai_keywords + company_keywords)
            
            # 检查URL是否包含AI相关域名或路径
            ai_domains = [
                'ai.', '.ai/', '/ai/', '/artificial-intelligence/', '/machine-learning/',
                'openai.com', 'anthropic.com', 'huggingface.co', 'deepmind.com',
                'stability.ai', 'replicate.com', 'midjourney.com', 'runwayml.com'
            ]
            url_match = url and any(domain in url for domain in ai_domains)
            
            if title_match or url_match:
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
        
        # 按照分数降序排序并只返回前10条
        news_list.sort(key=lambda x: x.get('score', 0), reverse=True)
        top_news = news_list[:10]
        
        logger.info(f"Hacker News收集完成，共{len(news_list)}条，返回前{len(top_news)}条")
        return top_news
    
    except Exception as e:
        logger.error(f"收集Hacker News失败: {e}")
        return []

def collect_venturebeat():
    """
    从VentureBeat收集AI相关新闻
    返回格式化的新闻列表，只保留当天的文章
    """
    logger.info("开始收集VentureBeat数据")
    news_list = []
    
    try:
        # 解析RSS feed
        feed_url = "https://venturebeat.com/category/ai/feed/"
        feed = feedparser.parse(feed_url)
        
        # 获取当天日期（去除时间部分）
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        for entry in feed.entries:
            # 解析发布日期
            published = datetime(*entry.published_parsed[:6])
            
            # 将发布日期也去除时间部分，只保留日期进行比较
            published_date = published.replace(hour=0, minute=0, second=0, microsecond=0)
            
            # 只保留当天的文章
            if published_date == today:
                news_item = {
                    'title': entry.title,
                    'url': entry.link,
                    'source': 'VentureBeat AI',
                    'published_at': published.isoformat(),
                    'summary': entry.summary if hasattr(entry, 'summary') else ''
                }
                news_list.append(news_item)
                logger.debug(f"收集到VentureBeat: {news_item['title']}")
        
        logger.info(f"VentureBeat收集完成，共{len(news_list)}条（仅当天文章）")
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
