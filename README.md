# Web Benchmark Agent

一款帮助用户快速构建HTML groundtruth markdown的工具，通过数据预处理和LLM优化，生成高质量的markdown文本。

## 功能特点

- 支持多种网页数据抽取方式，包括Firecrawl和Jina.ai
- 使用LLM优化提取结果，提高markdown质量
- 提供简单易用的命令行和API接口
- 支持批量处理URL

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

```python
from src.main import convert_url_to_markdown

# 单个URL转换
markdown_text = convert_url_to_markdown("https://example.com")

# 或使用命令行
# python -m src.main --url https://example.com
```

## 项目结构

```
web-benchmark-agent/
├── src/                    # 源代码
│   ├── extractors/         # 数据预处理模块
│   ├── llm/                # LLM合成模块
│   ├── benchmark/          # 评估模块
│   └── utils/              # 工具函数
├── tests/                  # 测试用例
├── examples/               # 使用示例
└── config/                 # 配置文件
```

## 开发

1. 克隆项目
2. 安装依赖: `pip install -r requirements.txt`
3. 运行测试: `pytest tests/`
