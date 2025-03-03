import os
import logging
from dotenv import load_dotenv

# 导入各个模型
from .grok_model import generate_summary as grok_generate_summary
from .deepseek_model import generate_summary as deepseek_generate_summary

# 加载环境变量
load_dotenv()

logger = logging.getLogger(__name__)

# 定义模型优先级
MODEL_PRIORITY = [
    "grok",
    "deepseek"
]

def generate_summary(data):
    """
    根据优先级使用可用的模型生成总结
    
    Args:
        data: 包含新闻和论文的数据字典
        
    Returns:
        元组 (生成的总结文本, 使用的模型名称)
    """
    logger.info("开始根据优先级选择模型生成总结")
    
    # 检查环境变量中设置的模型优先级
    env_priority = os.getenv("MODEL_PRIORITY")
    if env_priority:
        try:
            priority_list = env_priority.split(',')
            logger.info(f"使用环境变量中的模型优先级: {priority_list}")
        except Exception as e:
            logger.error(f"解析环境变量中的模型优先级失败: {e}")
            priority_list = MODEL_PRIORITY
    else:
        priority_list = MODEL_PRIORITY
        
    # 记录当前使用的优先级
    logger.info(f"当前模型优先级: {priority_list}")
    
    # 尝试按优先级使用模型
    for model in priority_list:
        try:
            if model.lower() == "grok":
                # 检查是否配置了Grok API密钥
                if not os.getenv("GROK_API_KEY"):
                    logger.warning("未配置Grok API密钥，跳过Grok模型")
                    continue
                    
                logger.info("使用Grok模型生成总结")
                summary = grok_generate_summary(data)
                return summary, "Grok"
                
            elif model.lower() == "deepseek":
                # 检查是否配置了DeepSeek API密钥
                if not os.getenv("DEEPSEEK_API_KEY"):
                    logger.warning("未配置DeepSeek API密钥，跳过DeepSeek模型")
                    continue
                    
                logger.info("使用DeepSeek模型生成总结")
                summary = deepseek_generate_summary(data)
                return summary, "DeepSeek"
        except Exception as e:
            logger.error(f"使用{model}模型生成总结失败: {e}")
            continue
    
    # 如果所有模型都失败，返回错误信息
    logger.error("所有可用模型都无法生成总结")
    return "无法生成总结：所有可用模型都失败了", "None"
