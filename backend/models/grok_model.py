import requests
import os
import json
from dotenv import load_dotenv
import logging

# 加载环境变量
load_dotenv()

logger = logging.getLogger(__name__)

def generate_summary(data):
    """
    使用Grok模型生成总结
    
    Args:
        data: 包含新闻和论文的数据字典
        
    Returns:
        生成的总结文本
    """
    logger.info("开始使用Grok生成总结")
    
    try:
        # 获取API密钥
        api_key = os.getenv("GROK_API_KEY")
        if not api_key:
            logger.error("未找到Grok API密钥")
            return "无法生成总结：未配置API密钥"
        
        # 准备提示词
        news_text = ""
        for i, news in enumerate(data.get('news', []), 1):
            news_text += f"{i}. {news['title']} - {news['source']}\n"
            if 'summary' in news and news['summary']:
                news_text += f"   摘要: {news['summary'][:200]}...\n"
            news_text += f"   链接: {news['url']}\n\n"
        
        papers_text = ""
        for i, paper in enumerate(data.get('papers', []), 1):
            papers_text += f"{i}. {paper['title']}\n"
            papers_text += f"   作者: {', '.join(paper['authors'])}\n"
            papers_text += f"   摘要: {paper['summary'][:200]}...\n"
            papers_text += f"   链接: {paper['url']}\n\n"
        
        prompt = f"""请你作为最专业的AI行业分析师，根据以下AI行业的新闻和学术论文，生成一份全面的行业日报。
日期: {data.get('date', '')}

## 新闻资讯:
{news_text}

## 学术论文:
{papers_text}

请生成一份结构清晰的AI行业日报，包含以下部分，每天生成的格式必须严格统一:
1. 行业概述：概括当天AI行业的主要动态和趋势，需要严格结合当天最新新闻内容，不可出现幻觉随意生成
2. 重要新闻：分析当天3-5条最重要的新闻，并解释其影响，内容必须足够丰富，需要严格结合当天最新新闻内容，不可出现幻觉随意生成
3. 学术进展：总结当天2-3篇最有影响力的论文及其创新点，需要严格结合当天最新新闻内容，不可出现幻觉随意生成
4. 趋势洞察：基于以上信息，分析AI行业的发展趋势和机会，并且给出你的建议

请确保内容客观、专业，并保持格式清晰。"""

        # 调用Grok API
        url = "https://api.x.ai/v1/chat/completions"
        
        payload = {
            "model": "grok-2-1212",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "max_tokens": 10000,
            "temperature": 0.7,
            "top_p": 0.7
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            summary = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            logger.info("Grok总结生成成功")
            return summary
        else:
            logger.error(f"Grok API调用失败: {response.status_code} - {response.text}")
            return f"生成总结失败: API返回错误 {response.status_code}"
    
    except Exception as e:
        logger.error(f"Grok总结生成失败: {e}")
        return f"生成总结失败: {str(e)}"
