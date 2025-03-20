"""
默认配置文件
"""

# API密钥配置
FIRECRAWL_API_KEY = ""  # 填入你的Firecrawl API密钥
JINA_API_KEY = ""       # 填入你的Jina.ai API密钥
OPENAI_API_KEY = ""     # 填入你的OpenAI API密钥

# 提取器配置
DEFAULT_EXTRACTOR = "firecrawl"  # 可选: "firecrawl", "jina", "combined"

# LLM配置
LLM_PROVIDER = "openai"      # 可选: "openai", "azure", "local"
LLM_MODEL = "gpt-4"          # 模型名称
LLM_TEMPERATURE = 0.1        # 温度参数，越低输出越确定

# 处理配置
MAX_URLS_PER_BATCH = 10      # 批处理URL数量上限
TIMEOUT = 30                 # API请求超时时间(秒)
RETRY_COUNT = 3              # 失败重试次数

# 输出配置
OUTPUT_DIR = "./output"      # 输出目录
SAVE_INTERMEDIATE = True     # 是否保存中间结果 