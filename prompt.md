# 我的需求：

我需要搭建信息收集总结助手：

- 收集AI行业内相关的新闻、投资报告、学术论文、产品更新动态等内容。
- 收集好信息以后，我需要将他们提交给大语言模型，如deepseek，grok等。他们会帮我输出总结内容，需要格式清晰的展示。
- 输出的内容，支持通过页面展示，并且支持他人通过Rss来订阅。
- 每天触发生成一次。

# 信息源

## AI新闻

- hacker news：https://github.com/HackerNews/API
- venturebeat AI https://venturebeat.com/category/ai/feed/

## 学术论文

- Arxiv

# 大语言模型配置：

deepseek 结构 python

```
import requests

url = "https://api.siliconflow.cn/v1/chat/completions"

payload = {
    "model": "deepseek-ai/DeepSeek-V3",
    "messages": [
        {
            "role": "user",
            "content": "中国大模型行业2025年将会迎来哪些机遇和挑战？"
        }
    ],
    "stream": False,
    "max_tokens": 512,
    "stop": None,
    "temperature": 0.7,
    "top_p": 0.7,
    "top_k": 50,
    "frequency_penalty": 0.5,
    "n": 1,
    "response_format": {"type": "text"},
    "tools": [
        {
            "type": "function",
            "function": {
                "description": "<string>",
                "name": "<string>",
                "parameters": {},
                "strict": False
            }
        }
    ]
}
headers = {
    "Authorization": "Bearer <token>",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
```
# 实现路径
请你分模块给我搭建，整个前端需要有框架来实现，页面风格简约大气。
并且留有未来拓展更多模型的空间。
我需要是一个完整的项目，不需要太复杂，但所说已有的功能必须要先实现。