# Web Benchmark Agent

一款帮助用户快速构建HTML groundtruth markdown的工具，通过数据预处理和LLM优化，生成高质量的markdown文本。

## 功能特点

- 支持多种网页数据抽取方式，包括Firecrawl和Jina.ai
- 使用LLM优化提取结果，提高markdown质量
- 提供简单易用的命令行和API接口
- 支持批量处理URL
- 支持保存HTML源文件和元数据

## 系统架构

系统由四个主要模块组成：用户接口、提取模块、处理模块和输出模块。

### 架构图

下面是系统架构的文本表示：

```
+------------------------+    +------------------------+    +------------------------+
|       用户接口       |    |       提取模块       |    |       处理模块       |
+------------------------+    +------------------------+    +------------------------+
| 命令行接口  API接口   |    | 提取器管理器          |    | LLM处理器             |
|                      |    | - Firecrawl提取器     |    | - 优化处理            |
|                      |    | - Jina.ai提取器       |    |                      |
+------------------------+    +------------------------+    +------------------------+
           |                           |                             |
           |                           |                             |
           v                           v                             v
+------------------------------------------------------------------------------------------------------------------------+
|                                                 输出模块                                                                 |
+------------------------------------------------------------------------------------------------------------------------+
|                          Markdown输出                    HTML输出                    元数据输出                           |
+------------------------------------------------------------------------------------------------------------------------+
```

### 数据流

1. **用户输入**: 用户通过命令行或API提供URL
2. **数据提取**: 系统使用Firecrawl或Jina.ai提取网页内容
3. **LLM处理**: 使用LLM模型优化提取的markdown内容
4. **结果输出**: 生成优化后的markdown、原始HTML和相关元数据

### 架构说明

- **用户接口**: 提供命令行界面和API接口，接收用户输入的URL或URL列表
- **提取模块**: 负责从网页获取内容，支持多种提取方式
  - Firecrawl提取器: 使用Firecrawl API获取内容
  - Jina.ai提取器: 使用Jina.ai Reader API获取内容
- **处理模块**: 使用LLM优化提取的内容
  - LLM处理器: 连接OpenAI等LLM服务
  - 优化处理: 应用专门的提示词优化markdown质量
- **输出模块**: 生成多种格式的输出
  - Markdown输出: 优化后的markdown内容
  - HTML输出: 原始HTML内容
  - 元数据输出: 标题、URL等信息

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用

```python
from src.main import convert_url_to_markdown

# 单个URL转换
markdown_text = convert_url_to_markdown("https://example.com")

# 或使用命令行
# python -m src.main --url https://example.com
```

### 命令行参数

```bash
# 处理单个URL并保存结果
python -m src.main --url https://example.com --output-file output.md

# 批量处理URL列表
python -m src.main --urls-file urls.txt --output-dir output_dir

# 指定提取器
python -m src.main --url https://example.com --extractor jina

# 禁用LLM优化
python -m src.main --url https://example.com --no-optimize

# 保存HTML源文件
python -m src.main --url https://example.com --output-file output.md --save-html
```

### 环境变量配置

可以通过创建`.env`文件配置API密钥和其他设置：

```
# API密钥
FIRECRAWL_API_KEY=your_firecrawl_api_key
JINA_API_KEY=your_jina_api_key
OPENAI_API_KEY=your_openai_api_key

# 是否保存HTML源文件
SAVE_HTML=true
```

## 项目结构

```
web-benchmark-agent/
├── src/                    # 源代码
│   ├── extractors/         # 数据预处理模块
│   │   ├── base.py         # 提取器基类
│   │   ├── firecrawl.py    # Firecrawl提取器
│   │   └── jina.py         # Jina.ai提取器
│   ├── llm/                # LLM合成模块
│   │   └── processor.py    # LLM处理器
│   ├── benchmark/          # 评估模块
│   ├── utils/              # 工具函数
│   └── main.py             # 主入口
├── tests/                  # 测试用例
├── examples/               # 使用示例
├── docs/                   # 文档
├── config/                 # 配置文件
└── .env.example            # 环境变量示例
```

## 开发

1. 克隆项目
2. 安装依赖: `pip install -r requirements.txt`
3. 安装开发依赖: `pip install -r requirements-dev.txt`
4. 安装pre-commit钩子: `pre-commit install`
5. 复制`.env.example`为`.env`并填写API密钥
6. 运行测试: `pytest tests/`

## 代码质量

本项目使用以下工具保证代码质量：

- **Black**: 自动格式化代码
- **isort**: 对导入进行排序
- **Flake8**: 代码风格检查
- **MyPy**: 静态类型检查
- **pre-commit**: 在提交前自动检查代码

所有的检查都会在提交代码前自动运行。你也可以手动运行：

```bash
# 运行所有检查
pre-commit run --all-files

# 运行单个检查（例如black）
pre-commit run black --all-files
```
