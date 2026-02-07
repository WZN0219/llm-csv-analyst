# 📊 LLM CSV Data Analyst (基于大模型的智能数据分析师)

> 一个基于 Qwen 大模型与 ReAct 范式的本地数据分析智能体。

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![DashScope](https://img.shields.io/badge/LLM-Qwen--Plus-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📖 项目简介

本项目实现了一个**全自动化的 CSV 数据分析 Agent**。它能够理解用户的自然语言查询（如“分析销售额趋势”），自动编写并执行 Python 代码，进行数据清洗、统计分析，并根据运行结果生成专业的业务洞察。

项目旨在解决传统数据分析中“清洗繁琐”和“门槛高”的问题，通过 **Prompt Engineering**，实现了对脏数据（货币符号、隐藏空格等）的鲁棒处理。

## ✨ 核心特性

- **🧠 智能代码生成**：基于 Qwen-Plus 模型，将自然语言转译为高质量 Pandas 代码。
- **🛡️ 鲁棒性清洗 SOP**：内置工业级数据清洗逻辑，自动识别并处理 `$`, `,`, `%` 及不可见字符，防止 `NaN` 错误。
- **🔄 自我纠错**：具备运行时异常捕获机制。当代码报错时，Agent 会自动分析 Traceback 并重写代码（支持最大 3 次重试）。
- **💾 多轮对话记忆**：支持上下文关联分析。

## 🚀 运行指引 (Quick Start)

请按照以下步骤配置并运行本项目。

### 1. 基础环境
* **Python**: 3.8+
* **API Key**: 阿里云 DashScope (Qwen) 有效密钥

### 2. 基础环境快速安装

```bash
# 创建并激活虚拟环境
python -m venv venv

# Linux/macOS 激活方式:
source venv/bin/activate

# Windows 激活方式:
# venv\Scripts\activate

# 安装项目依赖
pip install -r requirements.txt
```

### 3. 配置密钥

在项目根目录下新建 `.env` 文件，并填入你的 API 密钥：

```ini
# .env 文件内容
DASHSCOPE_API_KEY=你的sk-密钥内容
```

### 4. 启动 Agent

```bash
python main.py
```

### 5. 交互规范

* **输入需求**：在 `用户>` 提示符后输入自然语言指令（如：“对比 2016 年各品类的总销售额”）。
* **查看过程**：Agent 将自动展示生成的代码及执行结果。
* **退出程序**：输入 `exit` 或 `quit` 结束会话。

## 📂 项目结构

```text
llm-csv-analyst/
├── data/
│   └── test.csv              # 测试数据文件
├── main.py                   # [入口] 主程序与 Agent 调度逻辑
├── prompts.py                # [核心] 提示词工程 (SOP, 纠错, 解释模版)
├── code_executor.py          # [执行] Python 代码执行与结果捕获
├── llm_client.py             # [接口] DashScope API 封装
├── requirements.txt          # 依赖包列表
└── README.md                 # 项目说明文档