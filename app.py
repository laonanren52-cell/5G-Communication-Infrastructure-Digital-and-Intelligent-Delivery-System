import html
import json
import os
import socket
import time
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from urllib import error, request

import pandas as pd
import streamlit as st


REQUIRED_COLUMNS = ["站点编号", "站点类型", "AAU型号", "BBU型号", "线缆敷设距离", "取电方式"]
DEFAULT_API_TIMEOUT = 180
DEFAULT_SAMPLE_ROWS = 30


# =============================
# 页面基础配置
# =============================
st.set_page_config(
    page_title="5G通信基建数智化交付系统",
    page_icon="📡",
    layout="wide",
)


# =============================
# 极简专业化样式
# =============================
st.markdown(
    """
    <style>
    :root {
        --ink: #111827;
        --muted: #6b7280;
        --line: #e5e7eb;
        --panel: #ffffff;
        --soft: #f8fafc;
        --accent: #2563eb;
        --accent-dark: #1d4ed8;
        --accent-soft: #eff6ff;
        --ok: #0f766e;
        --ok-soft: #f0fdfa;
    }
    .stApp {
        background: #f4f6f8;
        color: var(--ink);
    }
    [data-testid="stHeader"] {
        background: rgba(244, 246, 248, 0.9);
        backdrop-filter: blur(10px);
    }
    [data-testid="stToolbar"] {
        opacity: 0.35;
    }
    .block-container {
        max-width: 1240px;
        padding-top: 28px;
        padding-bottom: 48px;
    }
    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }
    section[data-testid="stSidebar"] * {
        color: var(--ink);
    }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stCaption {
        color: #374151 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
        border: 1px dashed #cbd5e1;
        border-radius: 8px;
        padding: 10px;
        background: #f9fafb;
    }
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] select {
        color: var(--ink) !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="select"] * {
        color: var(--ink) !important;
    }
    .sidebar-brand {
        border: 1px solid #e5e7eb;
        background: #ffffff;
        border-radius: 8px;
        padding: 14px 14px 13px;
        margin: 8px 0 18px;
        box-shadow: 0 1px 2px rgba(17, 24, 39, 0.03);
    }
    .brand-mark {
        width: 34px;
        height: 34px;
        border-radius: 8px;
        background: linear-gradient(135deg, #111827 0%, #0f766e 100%);
        color: #ffffff;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
        font-weight: 800;
        margin-bottom: 10px;
    }
    .brand-title {
        color: #111827;
        font-size: 15px;
        font-weight: 800;
        line-height: 1.3;
    }
    .brand-sub {
        color: #6b7280;
        font-size: 12px;
        margin-top: 4px;
    }
    .hero-shell {
        border: 1px solid #e5e7eb;
        background: #ffffff;
        border-radius: 8px;
        padding: 24px 26px 22px;
        margin-bottom: 20px;
        box-shadow: 0 10px 28px rgba(17, 24, 39, 0.055);
    }
    .hero-topline {
        display: grid;
        grid-template-columns: minmax(0, 1fr) minmax(250px, 360px);
        gap: 22px;
        align-items: start;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        border: 1px solid #99f6e4;
        background: var(--ok-soft);
        color: var(--ok);
        border-radius: 6px;
        padding: 5px 9px;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .main-title {
        color: var(--ink);
        font-size: 32px;
        line-height: 1.15;
        font-weight: 800;
        margin-bottom: 10px;
        letter-spacing: 0;
    }
    .sub-title {
        color: var(--muted);
        font-size: 15px;
        margin-bottom: 0;
        max-width: 780px;
    }
    .hero-chip-row {
        display: grid;
        gap: 8px;
        margin-top: 2px;
    }
    .hero-chip {
        border: 1px solid #e5e7eb;
        background: #f8fafc;
        color: #374151;
        border-radius: 8px;
        padding: 9px 11px;
        font-size: 12px;
        line-height: 1.35;
        overflow-wrap: anywhere;
    }
    .workflow-row {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
        margin-top: 22px;
    }
    .workflow-step {
        border: 1px solid #e5e7eb;
        border-top: 3px solid #94a3b8;
        border-radius: 8px;
        background: #f8fafc;
        padding: 12px 12px 11px;
    }
    .workflow-kicker {
        color: #2563eb;
        font-size: 11px;
        font-weight: 800;
        margin-bottom: 3px;
        text-transform: uppercase;
    }
    .workflow-title {
        color: #111827;
        font-size: 13px;
        font-weight: 750;
    }
    .section-card {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--panel);
        padding: 16px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
        margin-bottom: 16px;
    }
    .section-title {
        color: var(--ink);
        font-size: 16px;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .section-note {
        color: var(--muted);
        font-size: 13px;
        margin-bottom: 12px;
    }
    .result-card {
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 22px 24px;
        background: var(--panel);
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
    }
    .metric-strip {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
        margin: 0 0 22px 0;
    }
    .metric-box {
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 16px 17px;
        background: var(--panel);
        box-shadow: 0 1px 3px rgba(17, 24, 39, 0.04);
    }
    .metric-label {
        color: var(--muted);
        font-size: 13px;
    }
    .metric-value {
        color: var(--ink);
        font-size: 24px;
        font-weight: 700;
        margin-top: 4px;
        line-height: 1.2;
    }
    div.stButton > button[kind="primary"] {
        background-color: var(--accent);
        border-color: var(--accent);
        color: #ffffff;
        font-weight: 800;
        border-radius: 8px;
        min-height: 46px;
        box-shadow: 0 8px 16px rgba(37, 99, 235, 0.18);
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: var(--accent-dark);
        border-color: var(--accent-dark);
        color: #ffffff;
    }
    div.stDownloadButton > button {
        border-radius: 8px;
        min-height: 44px;
        font-weight: 800;
    }
    .report-hint {
        border-left: 4px solid var(--accent);
        background: #eff6ff;
        color: #1e3a8a;
        padding: 12px 14px;
        border-radius: 8px;
        margin: 10px 0 18px;
        font-size: 14px;
    }
    .phase-box {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--panel);
        padding: 16px;
        margin: 12px 0;
        box-shadow: 0 1px 3px rgba(17, 24, 39, 0.04);
    }
    .phase-line {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        font-size: 14px;
        color: #334155;
    }
    .phase-percent {
        color: var(--accent);
        font-weight: 700;
    }
    .data-card {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        background: #ffffff;
        padding: 18px;
        box-shadow: 0 1px 3px rgba(17, 24, 39, 0.04);
        min-height: 100%;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 8px;
        overflow: hidden;
        background: #ffffff;
    }
    div[data-testid="stAlert"] {
        border-radius: 8px;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 8px;
        border-color: #e5e7eb;
        box-shadow: 0 1px 3px rgba(17, 24, 39, 0.035);
    }
    @media (max-width: 900px) {
        .main-title {
            font-size: 26px;
        }
        .hero-topline {
            grid-template-columns: 1fr;
        }
        .hero-shell {
            padding: 18px;
        }
        .workflow-row {
            grid-template-columns: 1fr;
        }
        .metric-strip {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================
# 模拟数据：未上传文件时用于演示
# =============================
def build_demo_dataframe() -> pd.DataFrame:
    """生成前序设计软件导出的基站设计元数据样例。"""
    return pd.DataFrame(
        [
            ["GD-GZ-5G-001", "宏站", "AAU5636", "BBU5900", 85, "市电直供"],
            ["GD-GZ-5G-002", "楼面站", "AAU5639", "BBU5900", 42, "交流配电箱"],
            ["GD-SZ-5G-017", "室分站", "pRRU5935", "BBU3910", 120, "弱电井取电"],
            ["GD-FS-5G-026", "微站", "AAU5339", "BBU5900", 28, "路灯杆取电"],
            ["GD-DG-5G-031", "宏站", "AAU5636", "BBU5900", 96, "市电直供"],
        ],
        columns=["站点编号", "站点类型", "AAU型号", "BBU型号", "线缆敷设距离", "取电方式"],
    )


# =============================
# 文件读取：支持 CSV 与 Excel
# =============================
def load_design_file(uploaded_file) -> pd.DataFrame:
    """读取上传的设计元数据表，并返回 DataFrame。"""
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        raw = uploaded_file.getvalue()
        try:
            return pd.read_csv(BytesIO(raw), encoding="utf-8-sig")
        except UnicodeDecodeError:
            return pd.read_csv(BytesIO(raw), encoding="gbk")

    return pd.read_excel(uploaded_file)


# =============================
# 数据校验与规则引擎
# =============================
def validate_design_data(data: pd.DataFrame) -> tuple[pd.DataFrame, list[str], list[str]]:
    """校验设计元数据表结构，并返回清洗后的 DataFrame。"""
    errors = []
    warnings = []
    cleaned = data.copy()

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in cleaned.columns]
    if missing_columns:
        errors.append("缺少必填字段：" + "、".join(missing_columns))
        return cleaned, errors, warnings

    cable_distance = pd.to_numeric(cleaned["线缆敷设距离"], errors="coerce")
    invalid_distance_count = int(cable_distance.isna().sum())
    negative_distance_count = int((cable_distance < 0).sum())

    if invalid_distance_count:
        warnings.append(f"有 {invalid_distance_count} 行线缆敷设距离无法识别，已按 0 米估算。")
    if negative_distance_count:
        warnings.append(f"有 {negative_distance_count} 行线缆敷设距离为负数，已按 0 米估算。")

    cleaned["线缆敷设距离"] = cable_distance.fillna(0).clip(lower=0)

    empty_site_count = int(cleaned["站点编号"].isna().sum())
    if empty_site_count:
        warnings.append(f"有 {empty_site_count} 行站点编号为空，建议补齐后再用于正式交付。")

    return cleaned, errors, warnings


def estimate_bom(data: pd.DataFrame) -> dict[str, int]:
    """根据通信工程经验规则估算关键物料数量。"""
    row_count = len(data)
    if "线缆敷设距离" in data.columns:
        cable_distance = pd.to_numeric(data["线缆敷设距离"], errors="coerce").fillna(0).clip(lower=0)
    else:
        cable_distance = pd.Series([0] * row_count)
    cable_total = int(cable_distance.sum())

    return {
        "site_count": row_count,
        "cable_total": cable_total,
        "power_cable": cable_total + row_count * 8,
        "optical_cable": cable_total + row_count * 12,
        "grounding_cable": row_count * 18,
        "labels": row_count * 24,
        "cable_tray": max(1, round(cable_total * 0.35)),
        "waterproof_kits": row_count * 6,
    }


def join_unique(data: pd.DataFrame, column: str) -> str:
    """拼接某列去重后的非空值。"""
    if column not in data.columns:
        return ""
    return "、".join(data[column].dropna().astype(str).unique())


def value_counts_dict(data: pd.DataFrame, column: str, limit: int = 12) -> dict[str, int]:
    """返回适合放入 LLM 上下文的字段分布。"""
    if column not in data.columns:
        return {}
    counts = data[column].fillna("未填写").astype(str).value_counts().head(limit)
    return {str(key): int(value) for key, value in counts.items()}


def build_engineering_summary(data: pd.DataFrame, sample_rows: int) -> dict:
    """将大型设计表压缩为工程摘要，避免把整表塞给大模型导致超时。"""
    bom = estimate_bom(data)
    cable_distance = pd.to_numeric(data.get("线缆敷设距离", pd.Series(dtype=float)), errors="coerce").fillna(0)
    sample_columns = [column for column in REQUIRED_COLUMNS if column in data.columns]
    long_distance_sites = []

    if "站点编号" in data.columns and "线缆敷设距离" in data.columns:
        top_rows = data.assign(线缆敷设距离=cable_distance).nlargest(min(10, len(data)), "线缆敷设距离")
        long_distance_sites = top_rows[["站点编号", "站点类型", "线缆敷设距离"]].to_dict("records")

    return {
        "record_count": int(len(data)),
        "bom_estimate": bom,
        "site_type_distribution": value_counts_dict(data, "站点类型"),
        "aau_model_distribution": value_counts_dict(data, "AAU型号"),
        "bbu_model_distribution": value_counts_dict(data, "BBU型号"),
        "power_source_distribution": value_counts_dict(data, "取电方式"),
        "cable_distance": {
            "total_m": int(cable_distance.sum()),
            "max_m": int(cable_distance.max()) if len(cable_distance) else 0,
            "avg_m": round(float(cable_distance.mean()), 2) if len(cable_distance) else 0,
            "long_distance_sites": long_distance_sites,
        },
        "sample_rows": data[sample_columns].head(sample_rows).to_dict("records") if sample_columns else [],
    }


def build_llm_context(data: pd.DataFrame, sample_rows: int) -> str:
    """生成面向外接 API 的紧凑上下文。"""
    summary = build_engineering_summary(data, sample_rows)
    return json.dumps(summary, ensure_ascii=False, indent=2)


# =============================
# 报告导出：生成 Word 可打开的 HTML 文档
# =============================
def build_word_report(report_text: str, data: pd.DataFrame, mode: str) -> bytes:
    """
    生成可下载的 .doc 文件内容。
    为保持 Demo 极简，不引入 python-docx；Word/WPS 可直接打开 HTML 格式的 .doc 文件。
    """
    preview_table = data.head(5).to_html(index=False, escape=True, border=0)
    escaped_report = html.escape(report_text)

    document = f"""
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>5G通信基建数智化交付报告</title>
    <style>
        body {{
            font-family: "Microsoft YaHei", Arial, sans-serif;
            color: #1f2937;
            line-height: 1.6;
        }}
        h1 {{
            font-size: 22px;
            border-bottom: 2px solid #16a34a;
            padding-bottom: 8px;
        }}
        .meta {{
            color: #4b5563;
            margin-bottom: 16px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0 18px;
        }}
        th, td {{
            border: 1px solid #d1d5db;
            padding: 6px 8px;
            font-size: 12px;
        }}
        th {{
            background: #f3f4f6;
        }}
        pre {{
            white-space: pre-wrap;
            font-family: "Microsoft YaHei", Arial, sans-serif;
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <h1>5G通信基建数智化交付报告</h1>
    <div class="meta">生成模式：{html.escape(mode)} | 数据记录数：{len(data)}</div>
    <h2>原始数据预览</h2>
    {preview_table}
    <h2>智能转化结果</h2>
    <pre>{escaped_report}</pre>
</body>
</html>
"""
    return document.encode("utf-8")


def show_download_toast() -> None:
    """下载按钮点击后的轻量反馈。"""
    st.toast("下载成功", icon="✅")


def render_phase(placeholder, percent: int, title: str, detail: str) -> None:
    """渲染数字化处理阶段。"""
    placeholder.markdown(
        f"""
        <div class="phase-box">
            <div class="phase-line">
                <strong>{html.escape(title)}</strong>
                <span class="phase-percent">{percent}%</span>
            </div>
            <div style="margin-top: 6px; color: #64748b; font-size: 13px;">{html.escape(detail)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================
# Mock LLM：模拟大模型生成专业施工文档
# =============================
def mock_llm_response(data: pd.DataFrame, mode: str) -> str:
    """
    根据基站设计元数据生成伪造的专业施工指令。
    当前阶段不调用真实 API，后续可在此函数内替换为 LLM SDK 请求。
    """
    bom = estimate_bom(data)
    site_types = join_unique(data, "站点类型")
    aau_models = join_unique(data, "AAU型号")
    bbu_models = join_unique(data, "BBU型号")
    power_sources = join_unique(data, "取电方式")
    avg_cable = round(bom["cable_total"] / bom["site_count"], 1) if bom["site_count"] else 0
    terminal_lugs = bom["site_count"] * 10
    firestop_kits = bom["site_count"] * 4
    cable_ties = max(100, bom["cable_total"] * 2)
    long_route_note = "存在长距离放缆场景，建议增加中间牵引点、复核桥架余量并预留光功率测试窗口。" if avg_cable >= 80 else "线缆平均路由较短，重点控制端口防水、标签一致性和现场余量管理。"
    power_note = "涉及弱电井或路灯杆取电时，需提前确认产权边界、计量方式、空开容量和接地条件。" if any(keyword in power_sources for keyword in ["弱电井", "路灯", "交流配电箱"]) else "以市电直供为主，需重点复核进线空开容量、接地排余量和停送电审批。"

    overview_block = f"""
## 5G通信基建数智化交付指令报告

**文档性质：** Demo 版自动生成交付建议，适用于施工准备、物料核对和现场技术交底  
**生成模式：** {mode}  
**站点数量：** {bom["site_count"]} 个  
**站点类型：** {site_types or "未识别"}  
**设备型号：** AAU：{aau_models or "未识别"}；BBU：{bbu_models or "未识别"}  
**取电方式：** {power_sources or "未识别"}  
**线缆路由：** 合计约 {bom["cable_total"]} 米，平均约 {avg_cable} 米/站  

### 一、工程概况与规则引擎结论

| 项目 | 结论 |
|---|---|
| 交付范围 | AAU/BBU 安装、前传光缆、电源接入、接地、防水封堵、基础联调 |
| 规则口径 | 线缆敷设距离按设计表汇总，电源线与光缆按站点预留工艺余量估算 |
| 重点风险 | 电力交越安全净距、楼面临边高处作业、弱电井/路灯杆取电边界、端口防水 |
| 现场建议 | {long_route_note} |
| 取电建议 | {power_note} |
"""

    bom_block = f"""
### 二、BOM 物料统计清单

| 序号 | 物料名称 | 推荐规格 | 估算数量 | 施工用途 |
|---:|---|---|---:|---|
| 1 | 室外电源线 | RVVZ 3x6mm² | {bom["power_cable"]} 米 | AAU/BBU 供电接入 |
| 2 | 室外光缆 | GYTA-12B1 | {bom["optical_cable"]} 米 | BBU 至 AAU 前传链路 |
| 3 | 保护接地线 | BVR 16mm² 黄绿双色 | {bom["grounding_cable"]} 米 | 机柜、抱杆、AAU 接地 |
| 4 | 线缆标识牌 | 防水阻燃型 | {bom["labels"]} 个 | 电源线、光缆、尾纤双端标识 |
| 5 | 镀锌桥架/线槽 | 100x50mm | {bom["cable_tray"]} 米 | 楼面及弱电井线缆保护 |
| 6 | 防水胶泥与热缩套管 | 室外耐候型 | {bom["waterproof_kits"]} 套 | 馈线窗、穿墙孔洞封堵 |
| 7 | 铜鼻子/冷压端子 | 与电源线线径匹配 | {terminal_lugs} 个 | 电源线端接压接 |
| 8 | 防火封堵材料 | 阻燃泥/防火包 | {firestop_kits} 套 | 竖井、穿墙、机房孔洞封堵 |
| 9 | 尼龙扎带/不锈钢扎带 | 室外耐候型 | {cable_ties} 根 | 线缆绑扎与路由整理 |

**物料复核要求：**

- 到货后按站点编号分包核对，重点核对 AAU/BBU 型号、光模块、尾纤规格和电源线线径。
- 电源类材料应提供阻燃等级、合格证和批次记录；室外材料需满足耐候、防水和抗紫外要求。
- 现场若发生路由变更，应同步更新线缆长度、桥架数量、标签数量和竣工图。
"""

    guide_block = f"""
### 三、工序指导书

1. **进场复核**
   - 依据站点编号逐站核对设计图、设备型号、取电方式和路由长度。
   - 对楼面站、宏站需复测 AAU 挂高、抱杆垂直度、安装朝向、方位角和机械下倾角。
   - 对室分站需核对弱电井、走线架、机柜位置、传输资源和供电空开容量。

2. **设备安装**
   - AAU 采用双螺母防松固定，安装完成后检查方位角、下倾角和端口防水帽。
   - BBU 上架前应确认机柜承重、空开容量、接地排余量、传输尾纤路由和散热空间。
   - 室外设备安装后需完成螺栓复紧、端口防水、铭牌拍照和安装位置复核。

3. **线缆敷设**
   - 本批次设计线缆敷设距离合计约 **{bom["cable_total"]} 米**，施工放缆应预留 3% 至 5% 工艺余量。
   - 电源线、光缆应分槽或分层敷设；无法分离时须增加阻燃隔板并做好交越标识。
   - 线缆转弯半径不得小于线缆外径的 10 倍，桥架内线缆填充率建议不超过 40%。
   - 光缆两端应挂永久性标签，标签内容应包含站点编号、起止端口、方向和施工日期。

4. **供电与接地**
   - 上电前测量输入电压、接地电阻和空开容量，确认无短路、反接、虚接和松动端子。
   - 电源线端接必须压接牢固，线鼻子规格与线径匹配，端子处不得露铜。
   - 所有设备保护地应接入站点接地排，接地点除锈后做防腐处理。

5. **开通联调**
   - 设备启动后检查 BBU-AAU 光链路、GPS/北斗同步、网管告警和小区激活状态。
   - 光链路需记录收发光功率，异常时优先排查尾纤极性、光模块规格、端口配置和弯折半径。
   - 联调完成后导出网管无告警截图、基础参数截图和测试记录。

### 四、安全注意事项

- 电力线与通信线交越时应保持安全净距，平行敷设距离不足时需采取隔离保护措施。
- 与强电管线交越的部位需设置明显警示标识，电力交越距离必须大于设计与现行规范规定值。
- 高处作业必须执行安全带高挂低用，楼面临边、洞口和爬梯区域需先防护后施工。
- 室外穿墙孔、馈线窗和设备端口应完成防水封堵，防止雨水倒灌造成设备故障。
- 所有接地点必须除锈、压接牢固并做防腐处理，接地电阻应满足站点验收要求。
- 涉及停送电、配电箱开盖、弱电井作业和夜间施工时，必须执行审批、监护和复核制度。

### 五、质量验收与交付资料

| 验收项 | 交付要求 |
|---|---|
| 设备安装 | 设备位置、朝向、挂高、紧固、防水、铭牌照片齐全 |
| 线缆工艺 | 路由整齐、绑扎间距一致、转弯半径合规、标签双端一致 |
| 电源接入 | 空开容量、输入电压、端子压接、线缆颜色和极性复核通过 |
| 接地系统 | 接地线规格、接地点防腐、接地电阻测试记录齐全 |
| 光链路 | 收发光功率、端口对应关系、链路状态截图齐全 |
| 资料闭环 | 竣工图、变更记录、测试记录、隐蔽工程照片和问题整改记录归档 |

### 六、风险闭环建议

- 对线缆路由超过平均值较多的站点，建议施工前二次踏勘，确认桥架、竖井和穿墙孔容量。
- 对取电方式存在产权或计量边界的站点，建议先完成业主确认和停送电审批，再安排设备上电。
- 对楼面站和宏站，建议把临边防护、吊装路径、天气条件和人员资质作为开工前检查项。
- 对室分站，建议重点核查弱电井空间、消防封堵恢复和物业施工窗口。
"""

    if mode == "生成BOM清单":
        return overview_block + "\n" + bom_block
    if mode == "生成工艺指导书":
        return overview_block + "\n" + guide_block
    return overview_block + "\n" + bom_block + "\n" + guide_block


def call_llm_api(
    data: pd.DataFrame,
    mode: str,
    api_url: str,
    model: str,
    api_key: str,
    timeout_seconds: int,
    sample_rows: int,
) -> str:
    """调用 OpenAI 兼容的 Chat Completions 接口生成交付文档。"""
    llm_context = build_llm_context(data, sample_rows)
    prompt = f"""
你是一名通信基建工程交付专家。请基于下方工程摘要，生成一份专业、可交付的中文施工文档。

生成模式：{mode}

工程摘要 JSON：
{llm_context}

输出要求：
1. 使用 Markdown。
2. 必须包含工程概况、BOM 物料统计表、工序指导书、安全注意事项、质量验收标准、风险闭环建议。
3. BOM 数量必须优先采用工程摘要 JSON 中的 bom_estimate，不要自行改写数量。
4. 语言要像真实通信施工交付文件，避免营销化表达。
5. 如涉及电力线与通信线交越，必须提示安全净距、隔离保护、警示标识和复核记录。
6. 对大路由、弱电井取电、楼面站/宏站高处作业、端口防水分别给出具体执行建议。
"""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你负责把通信设计元数据转化为施工 BOM 和工序指导书。"},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    api_request = request.Request(
        api_url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with request.urlopen(api_request, timeout=timeout_seconds) as response:
            response_data = json.loads(response.read().decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError("大模型 API 返回内容不是有效 JSON。") from exc
    except (TimeoutError, socket.timeout) as exc:
        raise RuntimeError(
            f"大模型 API 在 {timeout_seconds} 秒内未返回结果。建议提高超时时间、减少样本行数，或切换为本地 Mock 先生成交付初稿。"
        ) from exc
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"大模型 API 返回错误：HTTP {exc.code} {detail[:300]}") from exc
    except error.URLError as exc:
        if isinstance(exc.reason, (TimeoutError, socket.timeout)):
            raise RuntimeError(
                f"大模型 API 在 {timeout_seconds} 秒内未返回结果。建议提高超时时间、减少样本行数，或切换为本地 Mock 先生成交付初稿。"
            ) from exc
        raise RuntimeError(f"无法连接大模型 API：{exc.reason}") from exc

    try:
        return response_data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("大模型 API 返回格式不符合 Chat Completions 兼容结构。") from exc


# =============================
# 侧边栏：配置与控制台
# =============================
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="brand-mark">5G</div>
            <div class="brand-title">Delivery Intelligence</div>
            <div class="brand-sub">BOM automation · Work order drafting</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("控制台")

    uploaded_file = st.file_uploader(
        "上传基站设计元数据表",
        type=["xlsx", "csv"],
        help="支持前序设计软件导出的 Excel 或 CSV 结构化表格。",
    )

    mode = st.selectbox(
        "生成模式",
        ["生成BOM清单", "生成工艺指导书", "全量生成"],
        index=2,
    )

    llm_engine = st.selectbox(
        "AI引擎",
        ["本地Mock（无需密钥）", "真实大模型API（OpenAI兼容）"],
    )

    with st.expander("真实API配置", expanded=False):
        api_url = st.text_input(
            "API地址",
            value=os.getenv("LLM_API_URL", "https://api.openai.com/v1/chat/completions"),
            help="填写兼容 Chat Completions 的接口地址。",
        )
        model_name = st.text_input(
            "模型名称",
            value=os.getenv("LLM_MODEL", "gpt-4.1-mini"),
            help="示例：gpt-4.1-mini，或你所使用平台提供的模型名称。",
        )
        api_key = st.text_input(
            "API Key",
            value=os.getenv("LLM_API_KEY", ""),
            type="password",
        )
        api_timeout = st.number_input(
            "API超时时间（秒）",
            min_value=30,
            max_value=600,
            value=int(os.getenv("LLM_TIMEOUT", DEFAULT_API_TIMEOUT)),
            step=30,
            help="大型工程文件建议设置为 180-300 秒。",
        )
        sample_rows = st.number_input(
            "送入模型的样本行数",
            min_value=5,
            max_value=200,
            value=int(os.getenv("LLM_SAMPLE_ROWS", DEFAULT_SAMPLE_ROWS)),
            step=5,
            help="系统会把全量数据压缩为工程摘要，只附带少量样本行给模型参考。",
        )
        fallback_to_mock = st.checkbox(
            "API失败时自动生成本地工程报告",
            value=True,
            help="开启后，API 超时或网络异常时不会中断流程，会自动使用规则引擎生成交付报告。",
        )

    start_button = st.button(
        "启动数智化指令转化",
        type="primary",
        use_container_width=True,
    )


try:
    df = load_design_file(uploaded_file) if uploaded_file else build_demo_dataframe()
except Exception as exc:
    st.error(f"文件读取失败，请检查表头、编码或文件格式。错误信息：{exc}")
    st.stop()

clean_df, validation_errors, validation_warnings = validate_design_data(df)
work_df = clean_df if not validation_errors else df
data_source_label = uploaded_file.name if uploaded_file else "系统内置模拟数据"


# =============================
# 主区域：标题与状态总览
# =============================
st.markdown(
    f"""
    <div class="hero-shell">
        <div class="hero-topline">
            <div>
                <div class="hero-badge">Demo 交付工作台</div>
                <div class="main-title">5G通信基建数智化交付系统</div>
                <div class="sub-title">
                    读取设计元数据表，完成字段校验、规则引擎估算、AI 报告生成和 Word 交付文件导出。
                </div>
            </div>
            <div class="hero-chip-row">
                <span class="hero-chip">数据源：{html.escape(data_source_label)}</span>
                <span class="hero-chip">模式：{html.escape(mode)}</span>
                <span class="hero-chip">引擎：{html.escape(llm_engine)}</span>
            </div>
        </div>
        <div class="workflow-row">
            <div class="workflow-step">
                <div class="workflow-kicker">01 Intake</div>
                <div class="workflow-title">读取设计元数据</div>
            </div>
            <div class="workflow-step">
                <div class="workflow-kicker">02 Rules</div>
                <div class="workflow-title">校验字段与 BOM</div>
            </div>
            <div class="workflow-step">
                <div class="workflow-kicker">03 AI Draft</div>
                <div class="workflow-title">生成交付指令</div>
            </div>
            <div class="workflow-step">
                <div class="workflow-kicker">04 Export</div>
                <div class="workflow-title">导出 Word 报告</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =============================
# 主区域上方：原始数据透视与校验
# =============================
preview_col, quality_col = st.columns([1.65, 1], gap="large")

with preview_col:
    with st.container(border=True):
        st.markdown(
            """
            <div class="section-title">原始数据透视</div>
            <div class="section-note">展示前 5 行设计元数据，用于快速确认表头、站点类型和设备型号。</div>
            """,
            unsafe_allow_html=True,
        )
        st.dataframe(df.head(5), use_container_width=True, hide_index=True)

with quality_col:
    with st.container(border=True):
        st.markdown(
            """
            <div class="section-title">数据质量校验</div>
            <div class="section-note">生成前先检查必填字段、线缆距离和站点编号完整性。</div>
            """,
            unsafe_allow_html=True,
        )
        if validation_errors:
            for validation_error in validation_errors:
                st.error(validation_error)
        elif validation_warnings:
            for validation_warning in validation_warnings:
                st.warning(validation_warning)
        else:
            st.success("数据结构校验通过，可用于生成交付指令。")

if llm_engine.startswith("真实") and len(work_df) > sample_rows:
    st.markdown(
        f"""
        <div class="report-hint">
            大文件处理策略：当前共有 {len(work_df)} 行记录，系统会先生成全量工程摘要，再仅附带 {sample_rows} 行样本给外接 API，降低超时和上下文溢出风险。
        </div>
        """,
        unsafe_allow_html=True,
    )

summary_bom = estimate_bom(work_df)
st.markdown(
    """
    <div class="section-title">规则指标总览</div>
    <div class="section-note">基于全量数据计算的交付规模指标，用于判断本次任务复杂度。</div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    f"""
    <div class="metric-strip">
        <div class="metric-box">
            <div class="metric-label">记录数</div>
            <div class="metric-value">{len(work_df)}</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">线缆总长</div>
            <div class="metric-value">{summary_bom["cable_total"]} m</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">字段数</div>
            <div class="metric-value">{len(work_df.columns)}</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">生成模式</div>
            <div class="metric-value" style="font-size: 18px;">{html.escape(mode)}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =============================
# 主区域下方：智能转化结果
# =============================
st.markdown(
    """
    <div class="section-title">智能转化结果</div>
    <div class="section-note">生成过程会显示阶段百分比，完成后可预览报告并下载 Word 文件。</div>
    """,
    unsafe_allow_html=True,
)

if "ai_result" not in st.session_state:
    st.session_state.ai_result = ""

if start_button:
    if validation_errors:
        st.error("当前数据缺少必填字段，请修正后再启动转化。")
        st.stop()

    if llm_engine.startswith("真实") and (not api_url or not model_name or not api_key):
        st.error("真实大模型 API 模式需要填写 API 地址、模型名称和 API Key。")
        st.stop()

    progress = st.progress(0, text="0% 准备启动数智化转化任务")
    phase_placeholder = st.empty()

    render_phase(phase_placeholder, 15, "数据结构校验", "正在核对必填字段、线缆距离和站点记录完整性。")
    progress.progress(15, text="15% 数据结构校验完成")
    time.sleep(0.25)

    bom_preview = estimate_bom(work_df)
    render_phase(
        phase_placeholder,
        35,
        "规则引擎估算",
        f"已完成 {bom_preview['site_count']} 个站点、{bom_preview['cable_total']} 米线缆的物料规则估算。",
    )
    progress.progress(35, text="35% 规则引擎完成 BOM 估算")
    time.sleep(0.25)

    render_phase(phase_placeholder, 55, "AI上下文压缩", "正在把大型工程表压缩为站点分布、设备分布、取电方式、长路由风险和样本行。")
    progress.progress(55, text="55% 工程摘要已生成，准备调用 AI 引擎")
    time.sleep(0.25)

    if llm_engine.startswith("真实"):
        render_phase(
            phase_placeholder,
            60,
            "AI生成中",
            f"正在等待外接 API 返回，最长等待 {api_timeout} 秒。大文件已按摘要+{sample_rows}行样本送入模型。",
        )
        progress.progress(60, text=f"60% AI生成中，已等待 0 秒 / {api_timeout} 秒")

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                call_llm_api,
                work_df,
                mode,
                api_url,
                model_name,
                api_key,
                int(api_timeout),
                int(sample_rows),
            )
            start_time = time.time()
            while not future.done():
                elapsed = int(time.time() - start_time)
                percent = min(94, 60 + int((elapsed / max(int(api_timeout), 1)) * 34))
                render_phase(
                    phase_placeholder,
                    percent,
                    "AI生成中",
                    f"外接 API 正在处理工程摘要，已等待 {elapsed} 秒 / {api_timeout} 秒。页面仍在运行，请勿重复点击。",
                )
                progress.progress(percent, text=f"{percent}% AI生成中，已等待 {elapsed} 秒 / {api_timeout} 秒")
                time.sleep(0.5)

            try:
                st.session_state.ai_result = future.result()
            except Exception as exc:
                if fallback_to_mock:
                    st.warning(f"{exc} 已自动切回本地规则引擎报告，避免本次任务中断。")
                    st.session_state.ai_result = mock_llm_response(work_df, mode)
                else:
                    st.error(str(exc))
                    render_phase(phase_placeholder, 100, "任务中断", "外接 API 未在预期时间内返回，已停止生成。")
                    progress.progress(100, text="100% 任务中断")
                    st.stop()
    else:
        for percent in (70, 82, 94):
            render_phase(phase_placeholder, percent, "本地报告生成", "正在根据规则引擎结果生成工程交付指令报告。")
            progress.progress(percent, text=f"{percent}% 本地工程报告生成中")
            time.sleep(0.25)
        st.session_state.ai_result = mock_llm_response(work_df, mode)

    render_phase(phase_placeholder, 100, "报告封装完成", "已完成报告正文生成，可在下方预览并下载 Word 文件。")
    progress.progress(100, text="100% 数智化指令转化完成")
    st.success("数智化指令转化完成")

if st.session_state.ai_result:
    # 使用 Streamlit 原生边框容器作为结果卡片，避免自定义 HTML 影响 markdown 表格渲染。
    with st.container(border=True):
        st.markdown(st.session_state.ai_result)

    report_bytes = build_word_report(st.session_state.ai_result, work_df, mode)
    st.download_button(
        "一键下载转化报告 (Word)",
        data=report_bytes,
        file_name="5G通信基建数智化交付报告.doc",
        mime="application/msword",
        use_container_width=True,
        on_click=show_download_toast,
    )
else:
    st.markdown(
        """
        <div class="report-hint">
            等待任务启动：请在左侧选择生成模式与 AI 引擎，然后点击“启动数智化指令转化”。
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================
# requirements.txt 依赖包列表
# streamlit
# pandas
# openpyxl
# =============================
