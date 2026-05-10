# 5G通信基建数智化交付系统 (Demo 版)

这是一个基于 Streamlit 的单页面 Demo 应用，用于演示“基站设计元数据表 -> 规则引擎校验 -> 大模型生成 -> 施工 BOM 清单与工序指导书”的自动化转化流程。

当前版本默认使用本地 `mock_llm_response(data, mode)` 模拟 AI 生成结果，便于无密钥演示；同时预留了 OpenAI 兼容的 Chat Completions 接口配置，可在侧边栏切换为真实大模型 API。

## 功能概览

- 上传 `.xlsx` 或 `.csv` 格式的基站设计元数据表
- 支持三种生成模式：生成 BOM 清单、生成工艺指导书、全量生成
- 未上传文件时自动展示 5 行模拟基站数据
- 使用 Pandas 读取和预览前 5 行原始数据
- 对上传数据做必填字段和线缆距离校验
- 使用规则引擎估算电源线、光缆、接地线、标签、桥架和防水套件数量
- 支持本地 Mock 或真实大模型 API 两种生成引擎
- 生成通信施工文档风格的结果，包含物料统计、安全注意事项和验收要点
- 提供 Demo 版下载按钮，生成 Word 可打开的 `.doc` 报告文件

## 数据字段

Demo 内置数据和推荐上传表头如下：

| 字段 | 说明 |
|---|---|
| 站点编号 | 基站或站点唯一编号 |
| 站点类型 | 如宏站、楼面站、室分站、微站 |
| AAU型号 | AAU 或 pRRU 设备型号 |
| BBU型号 | BBU 设备型号 |
| 线缆敷设距离 | 线缆路由长度，单位默认为米 |
| 取电方式 | 市电直供、交流配电箱、弱电井取电等 |

## 项目结构

```text
.
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 本地运行

建议使用 Python 3.10 及以上版本。

```bash
pip install -r requirements.txt
streamlit run app.py
```

启动后在浏览器访问 Streamlit 输出的本地地址，通常是：

```text
http://localhost:8501
```

## 真实大模型 API 配置

默认情况下无需 API Key，直接使用本地 Mock 结果。

如果要接入真实大模型，在侧边栏选择：

```text
AI引擎 -> 真实大模型API（OpenAI兼容）
```

然后填写：

| 配置项 | 说明 |
|---|---|
| API地址 | 兼容 Chat Completions 的接口地址 |
| 模型名称 | 模型 ID，如平台提供的具体模型名 |
| API Key | 对应平台的访问密钥 |

也可以通过环境变量预设：

```bash
set LLM_API_URL=https://api.openai.com/v1/chat/completions
set LLM_MODEL=gpt-4.1-mini
set LLM_API_KEY=你的API密钥
```

## 依赖

```text
streamlit
pandas
openpyxl
```

## Demo 说明

本项目是演示版本，重点验证交互流程和业务表达：

- 默认大语言模型调用为本地 Mock 函数，真实 API 为可选配置
- “一键下载转化报告”当前生成 Word 可打开的 `.doc` 文件，暂不生成真实 PDF
- BOM 数量采用简化经验规则估算，不作为真实工程采购依据

后续可继续扩展模板化 Word/PDF 导出、更完整的 BOM 规则库、项目级交付记录管理和权限控制。
