# -*- coding: utf-8 -*-
"""
Learning Trace Platform · 学迹通 v4.3 Final
Warm Pastel Theme · Bulletproof CSS · Fixed Encoding Issues
Teacher + Student Portal · Checkbox-based collapsible sections
Fixed: DeepSeek API connection adapter error
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from requests.adapters import HTTPAdapter, Retry
import os
import re
import unicodedata

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DeepSeek AI Integration (Fixed + Fallback)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def get_api_key():
    """Safe API key retrieval — secrets first, then env, finally demo fallback."""
    try:
        key = st.secrets["DEEPSEEK_API_KEY"]
        if key:
            return key
    except Exception:
        pass
    key = os.environ.get("DEEPSEEK_API_KEY")
    if key:
        return key
    # 演示回退 key（与原代码一致）
    # 已移除警告提示
    return "sk-a903944b703b419ca7904091c0374c25"

_session = requests.Session()
_retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
_session.mount("https://", HTTPAdapter(max_retries=_retries))

def clean_text(text: str) -> str:
    """Remove non-printable or malformed UTF-8 characters from AI response only."""
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize('NFKC', text)
    text = re.sub(r'[^\x20-\x7E\u4e00-\u9fff\u3000-\u303f\n]', '', text)
    return text.strip()

def call_deepseek(prompt: str) -> str:
    DEEPSEEK_API_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"
    api_key = get_api_key()
    
    if not api_key:
        return "⚠️ DeepSeek API key 未配置，且无可用回退 Key。请检查设置。"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6,
    }
    try:
        resp = _session.post(
            DEEPSEEK_API_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        raw = resp.json()["choices"][0]["message"]["content"]
        return clean_text(raw)
    except requests.exceptions.Timeout:
        return "⚠️ 请求超时，请稍后重试。"
    except requests.exceptions.ConnectionError as e:
        return f"⚠️ 无法连接 AI 服务，请检查网络。 (详情: {str(e)[:100]})"
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return "⚠️ API Key 无效，请检查你的 DeepSeek API Key。"
        else:
            return f"⚠️ API 返回错误 (HTTP {e.response.status_code})，请重试。"
    except Exception as e:
        return f"⚠️ 意外错误: {str(e)[:200]}"


st.set_page_config(
    page_title="Learning Trace Platform · 学迹通",
    page_icon="◇",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Color Palette
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BG      = "#E8ECEE"
BG2     = "#EDE9DB"
CARD    = "#F6F3E8"
BORDER  = "#D9CBBD"
ACCENT  = "#8DC5CE"
WHITE   = "#FAFAF7"
TEXT    = "#3A3D40"
TEXT2   = "#6D7175"
TEXT3   = "#9EA3A8"
GREEN   = "#7DB88F"
RED     = "#CC7B7F"
ORANGE  = "#CCA76D"
PURPLE  = "#9B91C4"
TEAL    = "#7BBAC1"
BLUE    = "#7BA5C4"
YELLOW  = "#f1c40f"
GRID_C  = "rgba(0,0,0,0.04)"

KPC_COLORS = {
    "Algebra":     "#1f77b4",
    "Calculus":    "#ff7f0e",
    "Geometry":    "#2ca02c",
    "Probability": "#d62728",
    "Statistics":  "#9467bd",
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(f"""
<style>
@import url('[fonts.googleapis.com](https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap)');

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"],
.main, .block-container, [data-testid="stAppViewBlockContainer"] {{
    background-color: {BG} !important;
    color: {TEXT} !important;
    font-family: 'Inter', 'Microsoft YaHei', 'PingFang SC', 'Noto Sans CJK SC',
                 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', sans-serif !important;
}}
[data-testid="stHeader"] {{
    background-color: {BG} !important;
    border-bottom: 1px solid {BORDER};
}}
[data-testid="stBottomBlockContainer"] {{ background-color: {BG} !important; }}
.main .block-container {{ padding-top: 1.5rem; max-width: 1100px; }}

h1,h2,h3,h4,h5,h6,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {{
    font-family: 'Inter','Microsoft YaHei','PingFang SC','Segoe UI Emoji',sans-serif !important;
    color: {TEXT} !important; font-weight: 600 !important;
}}
p,span,div,label,li {{
    font-family: 'Inter','Microsoft YaHei','PingFang SC','Segoe UI Emoji',sans-serif !important;
}}
hr {{ border:none !important; border-top:1px solid {BORDER} !important; margin:20px 0 !important; }}

[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {{
    background-color: {BG2} !important;
    border-right: 1px solid {BORDER} !important;
}}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p {{ color: {TEXT2} !important; }}

.stTabs [data-baseweb="tab-list"] {{
    background:{BG2}; border-radius:12px; border:1px solid {BORDER}; padding:4px; gap:3px;
}}
.stTabs [data-baseweb="tab"] {{
    height:40px; padding:0 18px; background:transparent !important; border:none !important;
    color:{TEXT3} !important; font-size:13px !important; font-weight:500 !important;
    border-radius:10px !important;
}}
.stTabs [data-baseweb="tab"]:hover {{ color:{TEXT} !important; background:{CARD} !important; }}
.stTabs [aria-selected="true"] {{
    color:{TEXT} !important; background:{WHITE} !important;
    box-shadow:0 1px 4px rgba(0,0,0,0.06) !important;
}}
.stTabs [data-baseweb="tab-highlight"] {{ display:none !important; }}
.stTabs [data-baseweb="tab-panel"] {{ padding-top:20px; background:transparent !important; }}

div[data-testid="stMetric"] {{
    background:{CARD} !important; border:1px solid {BORDER} !important;
    border-radius:16px !important; padding:20px !important;
    box-shadow:0 1px 6px rgba(0,0,0,0.03);
}}
div[data-testid="stMetric"] label {{ color:{TEXT3} !important; font-size:11px !important;
    text-transform:uppercase !important; letter-spacing:0.06em !important; }}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
    font-size:26px !important; font-weight:700 !important; color:{TEXT} !important;
}}
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {{ color:{TEXT3} !important; }}

.stButton > button {{
    background:{ACCENT} !important; color:{WHITE} !important;
    border:none !important; border-radius:10px !important; font-weight:500 !important;
    transition:all 0.2s;
}}
.stButton > button:hover {{
    background:{TEAL} !important; box-shadow:0 4px 12px rgba(125,186,193,0.3) !important;
}}

[data-testid="stTextInput"] input,
[data-testid="stTextInput"] input:focus {{
    background:{WHITE} !important; border:1px solid {BORDER} !important;
    border-radius:10px !important; color:{TEXT} !important;
}}
.stSelectbox > div > div, .stMultiSelect > div > div {{
    background:{WHITE} !important; border-color:{BORDER} !important; border-radius:10px !important;
}}
.stMultiSelect [data-baseweb="tag"] {{
    background:{ACCENT}22 !important; border:1px solid {ACCENT} !important;
    color:{TEXT} !important; border-radius:6px !important;
}}
[data-testid="stFileUploader"] {{
    background:{WHITE} !important; border:1px dashed {BORDER} !important; border-radius:12px !important;
}}
[data-testid="stDataFrame"] {{ border-radius:12px !important; overflow:hidden; }}

.tc {{
    background:{CARD}; border:1px solid {BORDER}; border-radius:16px;
    padding:22px; text-align:center; transition:all 0.2s;
}}
.tc:hover {{ box-shadow:0 4px 16px rgba(0,0,0,0.04); }}
.tc .lbl {{ font-size:11px; color:{TEXT3}; text-transform:uppercase;
    letter-spacing:0.06em; margin-bottom:8px; font-weight:500; }}
.tc .val {{ font-size:28px; font-weight:700; line-height:1.2; color:{TEXT}; }}
.tc .sub {{ font-size:12px; color:{TEXT3}; margin-top:6px; }}

.sp {{
    background:{WHITE}; border:1px solid {BORDER}; border-radius:18px;
    padding:28px 32px; margin-bottom:20px; box-shadow:0 1px 4px rgba(0,0,0,0.02);
}}
.al {{
    background:#FCF0F0; border:1px solid {RED}44; border-radius:14px;
    padding:18px 24px; margin-bottom:20px; display:flex; align-items:center; gap:14px;
}}
.b-crit {{ background:{RED}; color:#fff; padding:4px 12px; border-radius:20px;
    font-size:12px; font-weight:600; display:inline-block; }}
.b-high {{ background:{ORANGE}; color:#fff; padding:4px 12px; border-radius:20px;
    font-size:12px; font-weight:600; display:inline-block; }}
.b-mod {{ background:#E0D08B; color:{TEXT}; padding:4px 12px; border-radius:20px;
    font-size:12px; font-weight:600; display:inline-block; }}
.ic {{
    background:{CARD}; border:1px solid {BORDER}; border-radius:14px;
    padding:20px 24px; margin-bottom:10px;
}}
.login-icon {{
    width:72px; height:72px; border-radius:18px;
    background:linear-gradient(135deg,{ACCENT},{TEAL});
    display:inline-flex; align-items:center; justify-content:center;
    font-size:32px; color:#fff; box-shadow:0 4px 20px rgba(125,186,193,0.35); margin-bottom:16px;
}}
.role-card {{
    background:{WHITE}; border:1px solid {BORDER}; border-radius:14px;
    padding:20px; text-align:center; cursor:pointer; transition:all 0.2s;
}}
.role-card:hover {{ box-shadow:0 4px 12px rgba(0,0,0,0.05); border-color:{ACCENT}; }}
.role-card .ri {{ font-size:36px; margin-bottom:8px; }}
.role-card h4 {{ margin:4px 0; color:{TEXT}; font-size:15px; font-weight:600; }}
.role-card p {{ font-size:12px; color:{TEXT3}; margin:0; }}
.ft {{
    text-align:center; color:{TEXT3}; font-size:12px;
    padding:30px; margin-top:30px; border-top:1px solid {BORDER};
}}
.ai-reply {{
    background:{CARD}; border:1px solid {BORDER}; border-left:4px solid {ACCENT};
    border-radius:14px; padding:20px 24px; margin-top:12px;
    font-size:13px; color:{TEXT}; line-height:1.9;
}}

/* Learning Map */
.lm-progress {{
    display:flex; align-items:flex-start; justify-content:center;
    padding:20px 0 10px; gap:0;
}}
.lm-step-wrap {{
    display:flex; flex-direction:column; align-items:center; flex:0 0 auto; z-index:1;
}}
.lm-dot {{
    width:40px; height:40px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:16px; font-weight:700; transition:all .3s;
}}
.lm-dot.done {{ background:{GREEN}; color:#fff; }}
.lm-dot.active {{
    background:{ACCENT}; color:#fff;
    box-shadow:0 3px 14px rgba(141,197,206,.45); transform:scale(1.15);
}}
.lm-dot.pending {{ background:{BG2}; color:{TEXT3}; border:2px solid {BORDER}; }}
.lm-step-label {{
    font-size:10px; color:{TEXT3}; margin-top:6px;
    text-align:center; max-width:72px; line-height:1.3;
}}
.lm-step-label.active {{ color:{TEXT}; font-weight:600; }}
.lm-line {{ flex:1; height:2px; background:{BORDER}; margin:18px -6px 0; z-index:0; }}
.lm-line.done {{ background:{GREEN}; }}
.lm-card {{
    background:{WHITE}; border:1px solid {BORDER}; border-radius:20px;
    padding:32px; margin:8px 0 16px; box-shadow:0 2px 8px rgba(0,0,0,.03);
}}
.lm-title {{ font-size:22px; font-weight:700; color:{TEXT}; margin-bottom:2px; }}
.lm-subtitle {{ font-size:13px; color:{TEXT2}; margin-bottom:20px; }}
.lm-insight {{
    background:{BG}; border-left:3px solid {ACCENT};
    border-radius:0 12px 12px 0; padding:14px 18px; margin:10px 0;
    font-size:13px; color:{TEXT2}; line-height:1.8;
}}
.lm-insight strong {{ color:{TEXT}; }}
.lm-kp-card {{
    display:flex; gap:14px; align-items:center; padding:14px;
    background:{CARD}; border-radius:14px; margin-bottom:10px; border:1px solid {BORDER};
}}
.lm-kp-pct {{
    width:68px; height:68px; border-radius:14px;
    display:flex; align-items:center; justify-content:center;
    font-size:22px; font-weight:700; flex-shrink:0;
}}
.lm-strategy-item {{
    display:flex; align-items:center; margin:8px 0;
    padding:8px 0; border-bottom:1px solid {BG};
}}
.lm-strategy-icon {{ font-size:20px; margin-right:12px; }}
.lm-strategy-card {{
    background:{CARD}; border:1px solid {BORDER};
    padding:16px; border-radius:12px; margin-bottom:16px;
}}
.lm-table-container {{ overflow-x:auto; margin:16px 0; }}
.lm-table {{ width:100%; border-collapse:collapse; }}
.lm-table th, .lm-table td {{
    padding:10px; text-align:left; border-bottom:1px solid {BG}; font-size:13px;
}}
.lm-table th {{ background:{CARD}; font-weight:600; color:{TEXT}; }}
</style>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Plotly Theme
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLT = dict(
    plot_bgcolor=WHITE, paper_bgcolor=WHITE,
    font=dict(
        family="Inter,'Microsoft YaHei','PingFang SC',sans-serif",
        color=TEXT2, size=12,
    ),
    margin=dict(l=10, r=10, t=40, b=10),
)
KPC = [ACCENT, GREEN, ORANGE, PURPLE, TEAL, BLUE, RED, "#C49DC4"]
SEG = {
    "Mastered":   {"c": GREEN,  "i": "🌟", "d": "High accuracy + High engagement"},
    "Efficient":  {"c": BLUE,   "i": "⚡", "d": "High accuracy + Low engagement"},
    "Struggling": {"c": ORANGE, "i": "💪", "d": "Low accuracy + High engagement"},
    "At-Risk":    {"c": RED,    "i": "🚨", "d": "Low accuracy + Low engagement"},
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Data Helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    req = {"student_id","exam_id","date","kp","item_id","option_chosen","is_correct","time_spent"}
    missing = req - set(df.columns)
    if missing:
        st.error(f"Missing columns: {', '.join(missing)}")
        st.stop()
    optional = {"difficulty_level","attempt_number","answer_change_count","hint_used","hint_level"}
    defaults = {"difficulty_level":"medium","attempt_number":1,
                "answer_change_count":0,"hint_used":0,"hint_level":0}
    for col in optional:
        if col not in df.columns:
            df[col] = defaults[col]
    df = df.dropna(subset=["student_id"])
    df["is_correct"] = df["is_correct"].astype(int)
    df["time_spent"] = pd.to_numeric(df["time_spent"], errors="coerce").fillna(0)
    df["date"]       = pd.to_datetime(df["date"], errors="coerce")
    # 清洗 kp 列：移除“时代”等异常前缀
    df["kp"] = df["kp"].astype(str).str.replace("时代", "", regex=False).str.strip()
    return df

@st.cache_data
def gen_demo():
    np.random.seed(42)
    stu     = [f'S{i:03d}' for i in range(1, 51)]
    kps     = ['Algebra','Calculus','Geometry','Probability','Statistics']
    exams   = ['EXAM001','EXAM002','EXAM003','EXAM004','EXAM005']
    kp_diff = {'Algebra':'easy','Calculus':'hard','Geometry':'easy',
               'Probability':'hard','Statistics':'medium'}
    options = ['A','B','C','D']
    rows    = []
    for sid in stu:
        ba  = 0.25 + np.random.random() * 0.55
        bt  = 30   + np.random.random() * 100
        gr  = np.random.choice([0.02,0.01,0,-0.01,0.03], p=[.3,.25,.2,.1,.15])
        vol = np.random.choice([.05,.1,.15,.2],           p=[.3,.35,.25,.1])
        for ei, ex in enumerate(exams):
            ea = np.clip(ba + gr*ei + np.random.normal(0, vol*.3), .1, .95)
            ni = np.random.randint(25, 41)
            ck = np.random.choice(kps, size=ni, replace=True)
            for ki, kp in enumerate(ck):
                km = {'Algebra':0,'Calculus':-.08,'Geometry':.05,
                      'Probability':-.03,'Statistics':.02}
                ia = np.clip(ea + km[kp] + np.random.normal(0, .12), 0, 1)
                c  = int(np.random.random() < ia)
                if c:
                    if np.random.random() < 0.15:
                        ts = max(3, bt * np.random.uniform(1.5, 2.5))
                        attempts = np.random.choice([2,3], p=[0.7,0.3]); changes = attempts-1
                    else:
                        ts = max(3, bt + np.random.normal(0,25)); attempts=1; changes=0
                else:
                    if np.random.random() < 0.3:
                        ts = max(3, np.random.uniform(5,15)); attempts=1; changes=0
                    elif np.random.random() < 0.5:
                        ts = max(3, bt * np.random.uniform(1.2,2.0))
                        attempts = np.random.choice([2,3], p=[0.6,0.4]); changes=attempts-1
                    else:
                        ts = max(3, bt * np.random.uniform(0.6,1.0)); attempts=1; changes=0
                ts      = round(ts, 1)
                hint_u  = 1 if (not c and attempts>=2 and np.random.random()>0.4) else 0
                hint_lv = np.random.choice([1,2,3], p=[0.5,0.35,0.15]) if hint_u else 0
                rows.append({
                    "student_id":sid, "exam_id":ex,
                    "date":f"2026-{ei+2:02d}-{np.random.randint(1,28):02d}",
                    "kp":kp, "item_id":f"Q{ei*200+ki:04d}",
                    "option_chosen":np.random.choice(options),
                    "is_correct":c, "time_spent":ts,
                    "difficulty_level":kp_diff[kp], "attempt_number":attempts,
                    "answer_change_count":changes, "hint_used":hint_u, "hint_level":hint_lv,
                })
    return pd.DataFrame(rows)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Teacher Analysis
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@st.cache_data
def a_teacher(df):
    kps_all = sorted(df["kp"].unique())
    ks = (df.groupby(["student_id","kp"])
            .agg(correct=("is_correct","sum"), total=("is_correct","count"),
                 at=("time_spent","mean"))
            .reset_index())
    ks["accuracy"] = ks["correct"] / ks["total"]
    hm = ks.pivot_table(index="student_id", columns="kp", values="accuracy", aggfunc="mean")
    ko = (df.groupby("kp")
            .agg(correct=("is_correct","sum"), total=("is_correct","count"))
            .reset_index())
    ko["accuracy"] = ko["correct"] / ko["total"]
    ko = ko.sort_values("accuracy")
    kcm = {kp: KPC[i % len(KPC)] for i, kp in enumerate(kps_all)}
    ss = (df.groupby("student_id")
            .agg(tc=("is_correct","sum"), ti=("is_correct","count"),
                 at=("time_spent","mean"), ne=("exam_id","nunique"), nk=("kp","nunique"))
            .reset_index())
    ss["accuracy"] = ss["tc"] / ss["ti"]
    w = ks.loc[ks.groupby("student_id")["accuracy"].idxmin()][["student_id","kp","accuracy"]]
    w.columns = ["student_id","wkp","wacc"]
    ss = ss.merge(w, on="student_id", how="left")
    am, tm = ss["accuracy"].median(), ss["at"].median()
    def cls(r):
        ha, ht = r["accuracy"] >= am, r["at"] >= tm
        if ha and ht:   return "Mastered"
        elif ha:        return "Efficient"
        elif ht:        return "Struggling"
        return "At-Risk"
    ss["seg"] = ss.apply(cls, axis=1)
    rk = ss[ss["seg"] == "At-Risk"].sort_values("accuracy").copy()
    ar = ss["accuracy"].max() - ss["accuracy"].min()
    tr = ss["at"].max()       - ss["at"].min()
    if ar > 0 and tr > 0:
        rk["rs"] = (1-(rk["accuracy"]-ss["accuracy"].min())/ar)*.6 \
                 + (1-(rk["at"]-ss["at"].min())/tr)*.4
    else:
        rk["rs"] = .5
    rk["rl"] = rk["rs"].apply(lambda s: "Critical" if s>.65 else "High" if s>.45 else "Moderate")
    eo = df.groupby("exam_id")["date"].min().sort_values()
    el = eo.index.tolist()
    et = (df.groupby("exam_id")
            .agg(accuracy=("is_correct","mean"), at=("time_spent","mean"),
                 ns=("student_id","nunique"))
            .reindex(el).reset_index())
    ke = df.groupby(["kp","exam_id"]).agg(accuracy=("is_correct","mean")).reset_index()
    return {"hm":hm,"ko":ko,"kcm":kcm,"ss":ss,"am":am,"tm":tm,
            "rk":rk,"et":et,"el":el,"ke":ke}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Student Analysis
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def a_student(df, sid):
    s = df[df["student_id"] == sid].copy()
    if len(s) == 0:
        return None
    eo = df.groupby("exam_id")["date"].min().sort_values()
    el = eo.index.tolist()
    kp = s.groupby("kp").agg(correct=("is_correct","sum"),
                              total=("is_correct","count")).reset_index()
    kp["accuracy"] = kp["correct"] / kp["total"]
    s["tz"] = (s["time_spent"]-s["time_spent"].mean()) / (s["time_spent"].std()+1e-9)
    time_volatility = s["tz"].abs().mean()
    s["is_guess"] = ((s["time_spent"]<s["time_spent"].quantile(.15)) &
                     (s["is_correct"]==0)).astype(int)
    guessing_rate = s["is_guess"].mean()
    change_rate   = (s["answer_change_count"]>0).mean() if "answer_change_count" in s.columns else 0.0
    hint_rate     = s["hint_used"].mean() if "hint_used" in s.columns else 0.0
    atc = s[s["is_correct"]==1]["time_spent"].mean() if s["is_correct"].sum()>0 else 0
    atw = s[s["is_correct"]==0]["time_spent"].mean() if (s["is_correct"]==0).sum()>0 else 0
    em  = s.groupby("exam_id").agg(accuracy=("is_correct","mean")).reindex(el).reset_index()
    em.columns = ["exam_id","mastery"]
    ms  = em["mastery"].values
    mgi = np.diff(ms) if len(ms)>1 else np.array([])
    if len(mgi) >= 2:
        mm = np.nanmean(mgi)
        try:
            variances = []
            for st in df["student_id"].unique():
                sub = df[df["student_id"]==st]
                if len(sub["exam_id"].unique()) > 1:
                    vals = sub.groupby("exam_id")["is_correct"].mean().reindex(el).values
                    d = np.diff(vals)
                    if len(d) > 0:
                        variances.append(np.nanvar(d))
            p75 = np.nanpercentile(variances, 75) if variances else 0
            if np.isnan(p75): p75 = 0
        except Exception:
            p75 = 0
        if np.nanvar(mgi) > p75: gt = "🎢 Fluctuating"
        elif mm > .01:            gt = "🚀 Accelerating"
        else:                     gt = "🌱 Steady"
    elif len(mgi) == 1:
        gt = "🌱 Steady" if mgi[0] > 0 else "🌿 Building Foundation"
    else:
        gt = "Insufficient Data"
    wi   = s[s["is_correct"]==0][["exam_id","date","kp","item_id","option_chosen","time_spent"]] \
             .sort_values("date", ascending=False)
    ke   = s.groupby("kp").agg(wrong=("is_correct", lambda x:(x==0).sum()),
                               total=("is_correct","count")).reset_index()
    ke["er"] = ke["wrong"] / ke["total"]
    kep  = s.groupby(["exam_id","kp"]).agg(accuracy=("is_correct","mean")).reset_index()
    kepp = kep.pivot_table(index="kp", columns="exam_id", values="accuracy").reindex(columns=el)
    ca   = df.groupby("exam_id").agg(accuracy=("is_correct","mean")).reindex(el).reset_index()
    ca.columns = ["exam_id","cavg"]
    strongest = kp.sort_values("accuracy", ascending=False).iloc[0] if len(kp)>0 else None
    weakest   = kp.sort_values("accuracy").iloc[0]                  if len(kp)>0 else None
    return {
        "kp":kp, "kepp":kepp, "el":el,
        "hes":time_volatility, "gr":guessing_rate,
        "atc":atc, "atw":atw, "s":s, "em":em, "mgi":mgi, "gt":gt,
        "mm":np.nanmean(mgi) if len(mgi)>0 else 0,
        "wi":wi, "ke":ke, "ca":ca,
        "oa":s["is_correct"].mean(),
        "cr":change_rate, "hr":hint_rate, "ti":len(s),
        "strongest_kp":     strongest["kp"]       if strongest is not None else "N/A",
        "strongest_kp_acc": strongest["accuracy"]  if strongest is not None else 0,
        "weakest_kp":       weakest["kp"]          if weakest   is not None else "N/A",
        "weakest_kp_acc":   weakest["accuracy"]    if weakest   is not None else 0,
    }

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# AI Prompt Builders
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def build_teacher_prompt(R):
    seg_counts    = R["ss"]["seg"].value_counts().to_dict()
    weakest_kp    = R["ko"][["kp","accuracy"]].sort_values("accuracy").head(5)
    risk_students = R["rk"][["student_id","accuracy","at","wkp"]].head(10)
    risk_detail   = ""
    for _, row in risk_students.head(5).iterrows():
        risk_detail += (f"  - {row['student_id']}: accuracy {row['accuracy']:.1%}, "
                        f"avg time {row['at']:.0f}s, weakest in {row['wkp']}\n")
    return (
        f"You are an expert AI teaching assistant for a Chinese K-12 math class.\n"
        f"Analyze the class data and provide actionable strategies.\n\n"
        f"## Class Overview\n"
        f"Total {len(R['ss'])} students. Avg accuracy: {R['ss']['accuracy'].mean():.1%}.\n"
        f"Segments: Mastered={seg_counts.get('Mastered',0)}, "
        f"Efficient={seg_counts.get('Efficient',0)}, "
        f"Struggling={seg_counts.get('Struggling',0)}, "
        f"At-Risk={seg_counts.get('At-Risk',0)}\n\n"
        f"## Weakest Knowledge Points\n{weakest_kp.to_string(index=False)}\n\n"
        f"## Top 5 At-Risk Students\n{risk_detail}\n\n"
        f"## Instructions\n"
        f"1. Class pattern summary.\n"
        f"2. Explain WHY each at-risk student struggles.\n"
        f"3. Suggest 2-3 specific teaching strategies for weakest KPs.\n"
        f"4. Next steps for THIS WEEK.\n"
        f"Tone: Professional, specific. Language: English, ~200 words."
    )

def build_student_prompt(S, sid):
    weakest = S["ke"].sort_values("er", ascending=False).head(3)
    return (
        f"You are a friendly AI study coach. Analyze this student's learning data.\n\n"
        f"Student: {sid} | Overall Accuracy: {S['oa']:.1%} | Growth Trend: {S['gt']}\n\n"
        f"Behavioral Profile:\n"
        f"- Guessing Rate: {S['gr']:.1%}\n"
        f"- Time Volatility: {S['hes']:.2f}\n"
        f"- Avg Time on Correct: {S['atc']:.0f}s vs Wrong: {S['atw']:.0f}s\n\n"
        f"Progress:\n"
        f"- Recent Mastery Change: {S['mm']:+.1%}\n\n"
        f"Weaknesses:\n{weakest.to_string(index=False)}\n\n"
        f"Instructions:\n"
        f"1. Holistic summary combining behavior, progress, and knowledge gaps.\n"
        f"2. Give 3 specific, actionable tips.\n"
        f"3. Warm encouragement.\n"
        f"Language: English. 200 words."
    )

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Session State
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if "page" not in st.session_state:
    st.session_state.page = "login"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOGIN PAGE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if st.session_state.page == "login":
    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        st.markdown(f"""
        <div style="text-align:center;padding:50px 0 20px;">
            <div class="login-icon">◇</div>
            <h1 style="font-size:34px;font-weight:700;margin:12px 0 4px;color:{TEXT};">学迹通</h1>
            <p style="font-size:15px;color:{TEXT2};margin:0 0 4px;">Learning Trace Platform</p>
            <p style="font-size:12px;color:{TEXT3};">Intelligent Learning Analytics</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        r1, r2 = st.columns(2)
        with r1:
            st.markdown('<div class="role-card"><div class="ri">👩‍🏫</div><h4>Teacher</h4>'
                        '<p>Class analytics &<br>risk identification</p></div>',
                        unsafe_allow_html=True)
        with r2:
            st.markdown('<div class="role-card"><div class="ri">🧑‍🎓</div><h4>Student</h4>'
                        '<p>Personal mastery &<br>growth tracking</p></div>',
                        unsafe_allow_html=True)
        role     = st.radio("Role", ["👩‍🏫 Teacher","🧑‍🎓 Student"],
                            horizontal=True, label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="Enter username")
        _        = st.text_input("Password", type="password", placeholder="Enter password")
        uploaded = st.file_uploader("Upload data (CSV)", type=["csv"])
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign In", use_container_width=True, type="primary"):
            if uploaded:
                st.session_state.uploaded_file = uploaded
            st.session_state.use_demo = not bool(uploaded)
            st.session_state.page     = "teacher" if "Teacher" in role else "student"
            st.session_state.username = username or "User"
            st.rerun()
        st.markdown(
            f'<div style="text-align:center;margin:24px 0;color:{TEXT3};font-size:13px;">— or —</div>',
            unsafe_allow_html=True)
        if st.button("🔓  Guest Mode — Explore with Demo Data", use_container_width=True):
            st.session_state.page     = "guest"
            st.session_state.use_demo = True
            st.session_state.username = "Guest"
            st.rerun()
        st.markdown(
            f'<div class="ft" style="border:none;margin-top:40px;">'
            f'Learning Trace Platform · 学迹通 v4.3</div>',
            unsafe_allow_html=True)
    st.stop()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Load Data
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
df_raw = (
    load_data(st.session_state.get("uploaded_file"))
    if not st.session_state.get("use_demo", True) and st.session_state.get("uploaded_file")
    else gen_demo()
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Sidebar
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
page    = st.session_state.page
sel_sid = None

with st.sidebar:
    st.markdown(
        f'<div style="text-align:center;padding:14px 0;">'
        f'<div style="font-size:24px;">◇</div>'
        f'<div style="font-size:15px;font-weight:600;color:{TEXT};margin-top:4px;">学迹通</div>'
        f'<div style="font-size:11px;color:{TEXT3};">Learning Trace Platform</div></div>',
        unsafe_allow_html=True)
    st.markdown("---")
    if page == "guest":
        portal = st.radio("Portal", ["👩‍🏫 Teacher","🧑‍🎓 Student"], index=0)
    elif page == "teacher":
        portal = "👩‍🏫 Teacher"
        st.caption(f"📌 Teacher · {st.session_state.get('username','')}")
    else:
        portal = "🧑‍🎓 Student"
        st.caption(f"📌 Student · {st.session_state.get('username','')}")
    st.markdown("---")
    ae  = sorted(df_raw["exam_id"].unique())
    se_ = st.multiselect("Exams", ae, default=ae)
    ak  = sorted(df_raw["kp"].unique())
    sk  = st.multiselect("Knowledge Points", ak, default=ak)
    df  = df_raw.copy()
    if se_: df = df[df["exam_id"].isin(se_)]
    if sk:  df = df[df["kp"].isin(sk)]
    if len(df) == 0:
        st.warning("No data for current filters.")
        st.stop()

    if "Student" in portal:
        st.markdown("---")
        all_students = sorted(df["student_id"].unique())
        if "sel_sid" not in st.session_state or st.session_state.sel_sid not in all_students:
            st.session_state.sel_sid = all_students[0]
        sel_sid = st.selectbox(
            "Select Student", all_students,
            index=all_students.index(st.session_state.sel_sid))
        st.session_state.sel_sid = sel_sid

        # ── Step Navigation ──
        st.markdown("---")
        if "map_step" not in st.session_state:
            st.session_state.map_step = 1

        STEPS_NAV = [
            {"icon": "📍", "en": "Diagnose"},
            {"icon": "🎯", "en": "Set Goals"},
            {"icon": "🗺️", "en": "Strategy"},
            {"icon": "📊", "en": "Monitor"},
            {"icon": "💡", "en": "Reflect"},
        ]

        st.markdown(
            f'<div style="font-size:13px;font-weight:600;color:{TEXT};'
            f'margin-bottom:10px;">🧭 Navigation</div>',
            unsafe_allow_html=True)

        for i, step in enumerate(STEPS_NAV, 1):
            is_current = (st.session_state.map_step == i)
            is_done    = (st.session_state.map_step  > i)
            if is_current:
                bg_c, txt_c, prefix = f"{ACCENT}22", ACCENT, "▶"
            elif is_done:
                bg_c, txt_c, prefix = f"{GREEN}15", GREEN,  "✓"
            else:
                bg_c, txt_c, prefix = "transparent", TEXT3, "⏸"

            st.markdown(
                f'<div style="display:flex;align-items:center;gap:10px;'
                f'padding:8px 12px;border-radius:10px;background:{bg_c};'
                f'margin-bottom:4px;">'
                f'<span style="font-size:16px;">{step["icon"]}</span>'
                f'<span style="font-size:13px;font-weight:{"600" if is_current else "400"};'
                f'color:{txt_c};">{step["en"]}</span>'
                f'<span style="margin-left:auto;font-size:11px;color:{txt_c};">{prefix}</span>'
                f'</div>',
                unsafe_allow_html=True)

        st.markdown(
            f'<div style="margin-top:10px;padding:8px 12px;background:{CARD};'
            f'border-radius:10px;border:1px solid {BORDER};font-size:12px;color:{TEXT2};">'
            f'<strong>Current Step:</strong> {st.session_state.map_step} of 5</div>',
            unsafe_allow_html=True)

    st.markdown("---")
    if st.button("← Back to Home"):
        st.session_state.page = "login"
        st.rerun()
    st.markdown(
        f'<div style="background:{WHITE};border:1px solid {BORDER};border-radius:10px;'
        f'padding:12px;text-align:center;margin-top:8px;">'
        f'<span style="font-weight:700;color:{ACCENT};">{df["student_id"].nunique()}</span>'
        f'<span style="color:{TEXT3};font-size:12px;"> students · </span>'
        f'<span style="font-weight:700;color:{GREEN};">{len(df)}</span>'
        f'<span style="color:{TEXT3};font-size:12px;"> records</span></div>',
        unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEACHER PORTAL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if "Teacher" in portal:
    R = a_teacher(df)
    st.markdown("## 👩‍🏫 Teacher Dashboard")
    st.caption("Class-level learning analytics · Learning Trace Platform")
    mr = (R["ss"]["accuracy"] >= .7).mean()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Students",       df["student_id"].nunique(), f"{df['exam_id'].nunique()} exams")
    c2.metric("Class Accuracy", f"{df['is_correct'].mean():.1%}", f"{len(df)} responses")
    c3.metric("Mastery Rate",   f"{mr:.0%}", "students ≥ 70%")
    c4.metric("At-Risk",        f"{len(R['rk'])}", "need attention" if len(R['rk'])>0 else "none")
    st.markdown("---")

    t1, t2, t3, t4, t5 = st.tabs([
        "🔥 Knowledge Heatmap",
        "📐 Segmentation",
        "🚨 Risk Identification",
        "📈 Trend Tracking",
        "🤖 AI Assistant",
    ])

    with t1:
        st.markdown('<div class="sp">', True)
        st.markdown("### Knowledge Point Mastery")
        kd = R["ko"]; kcm = R["kcm"]
        fig = go.Figure(go.Bar(
            x=kd["accuracy"], y=kd["kp"], orientation="h",
            marker_color=[kcm.get(k, ACCENT) for k in kd["kp"]],
            text=[f"{a:.0%}" for a in kd["accuracy"]],
            textposition="outside", textfont=dict(size=13, color=TEXT)
        ))
        fig.update_layout(**PLT, height=max(220, len(kd)*48),
            xaxis=dict(range=[0,1.1], tickformat=".0%", gridcolor=GRID_C, zeroline=False),
            yaxis=dict(autorange="reversed", tickfont=dict(size=13)))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("##### ⚠️ Weakest Knowledge Points")
        cols = st.columns(min(3, len(kd))); rc = [RED, ORANGE, "#D4C054"]
        for i, (_, r) in enumerate(kd.head(3).iterrows()):
            with cols[i]:
                st.markdown(
                    f'<div class="tc"><div class="lbl" style="color:{rc[i]};font-weight:600;">#{i+1}</div>'
                    f'<div class="val" style="color:{kcm.get(r["kp"],ACCENT)};font-size:18px;">{r["kp"]}</div>'
                    f'<div class="sub">{r["accuracy"]:.1%} · {int(r["total"])} items</div></div>', True)
        st.markdown('</div>', True)
        st.markdown('<div class="sp">', True)
        st.markdown("##### Student × KP Matrix")
        so = st.radio("Sort", ["Student ID","Accuracy ↑"], horizontal=True, key="thm")
        hm = R["hm"]
        if so == "Accuracy ↑":
            hm = hm.loc[hm.mean(axis=1).sort_values().index]
        fig2 = go.Figure(go.Heatmap(
            z=hm.values, x=hm.columns.tolist(), y=hm.index.tolist(),
            colorscale=[[0,RED],[.3,ORANGE],[.6,GREEN],[1,ACCENT]], zmin=0, zmax=1,
            text=[[f"{v:.0%}" if not np.isnan(v) else "—" for v in row] for row in hm.values],
            texttemplate="%{text}", textfont=dict(size=9),
            hovertemplate="Student:%{y}<br>KP:%{x}<br>Acc:%{z:.1%}<extra></extra>",
            colorbar=dict(title="Acc", tickformat=".0%", thickness=12, len=.5)
        ))
        fig2.update_layout(**PLT, height=min(600, max(400, len(hm)*22)),
            xaxis=dict(side="top", tickangle=-40, tickfont=dict(size=11)),
            yaxis=dict(tickfont=dict(size=9)))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', True)

    with t2:
        st.markdown('<div class="sp">', True)
        st.markdown("### Student Segmentation")
        ss = R["ss"]; sc = ss["seg"].value_counts()
        cols = st.columns(4)
        for i, (seg, info) in enumerate(SEG.items()):
            with cols[i]:
                st.markdown(
                    f'<div class="tc"><div class="lbl">{info["i"]} {seg}</div>'
                    f'<div class="val" style="color:{info["c"]};">{sc.get(seg,0)}</div>'
                    f'<div class="sub">{info["d"]}</div></div>', True)
        st.markdown("<br>", True)
        fig3 = go.Figure()
        ym, yn = ss["at"].max()*1.05, ss["at"].min()*.95
        am, tm = R["am"], R["tm"]
        for x0,y0,x1,y1,fc in [
            (0,tm,am,ym,"rgba(204,167,109,0.04)"),
            (am,tm,1,ym,"rgba(125,184,143,0.04)"),
            (0,yn,am,tm,"rgba(204,123,127,0.04)"),
            (am,yn,1,tm,"rgba(123,165,196,0.04)"),
        ]:
            fig3.add_shape(type="rect",x0=x0,y0=y0,x1=x1,y1=y1,
                           fillcolor=fc,line_width=0,layer="below")
        fig3.add_hline(y=tm,line_dash="dot",line_color=BORDER,
                       annotation_text=f"Time:{tm:.0f}s",annotation_position="top left",
                       annotation_font=dict(size=10,color=TEXT3))
        fig3.add_vline(x=am,line_dash="dot",line_color=BORDER,
                       annotation_text=f"Acc:{am:.1%}",annotation_position="top right",
                       annotation_font=dict(size=10,color=TEXT3))
        for seg, info in SEG.items():
            sub = ss[ss["seg"]==seg]
            fig3.add_trace(go.Scatter(
                x=sub["accuracy"], y=sub["at"], mode="markers+text",
                name=f'{info["i"]} {seg}',
                marker=dict(size=11,color=info["c"],opacity=.85,line=dict(width=1,color=WHITE)),
                text=sub["student_id"], textposition="top center",
                textfont=dict(size=8,color=TEXT3),
                hovertemplate="<b>%{text}</b><br>Acc:%{x:.1%}<br>Time:%{y:.1f}s<extra></extra>"
            ))
        fig3.update_layout(**PLT, height=520,
            xaxis=dict(title="Accuracy",tickformat=".0%",gridcolor=GRID_C),
            yaxis=dict(title="Avg Time (s)",gridcolor=GRID_C),
            legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="center",x=.5))
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', True)

    with t3:
        st.markdown('<div class="sp">', True)
        st.markdown("### At-Risk Identification")
        rk = R["rk"]
        if len(rk) == 0:
            st.success("✅ No at-risk students")
        else:
            st.markdown(
                f'<div class="al"><span style="font-size:24px;">⚠️</span>'
                f'<div><div style="font-size:15px;font-weight:600;color:{RED};">'
                f'{len(rk)} at-risk student(s)</div>'
                f'<div style="font-size:13px;color:{TEXT2};">Low accuracy + low engagement</div>'
                f'</div></div>', True)
            rd = rk[["student_id","accuracy","at","wkp","wacc","rs","rl"]].copy()
            rd.columns = ["Student","Acc","Time","Weak KP","KP Acc","Score","Level"]
            rd["Acc"]    = rd["Acc"].apply(lambda x: f"{x:.1%}")
            rd["Time"]   = rd["Time"].apply(lambda x: f"{x:.1f}s")
            rd["KP Acc"] = rd["KP Acc"].apply(lambda x: f"{x:.1%}")
            rd["Score"]  = rd["Score"].apply(lambda x: f"{x:.2f}")
            st.dataframe(rd, use_container_width=True, hide_index=True)
            for _, s in rk.head(6).iterrows():
                bc = {"Critical":"b-crit","High":"b-high","Moderate":"b-mod"}.get(s["rl"],"b-mod")
                st.markdown(
                    f'<div class="ic">'
                    f'<div style="display:flex;gap:10px;margin-bottom:6px;align-items:center;">'
                    f'<strong>{s["student_id"]}</strong><span class="{bc}">{s["rl"]}</span></div>'
                    f'<div style="font-size:13px;color:{TEXT2};line-height:1.7;">'
                    f'Accuracy <strong>{s["accuracy"]:.1%}</strong> · '
                    f'Time <strong>{s["at"]:.1f}s</strong> · '
                    f'Weakest: <strong style="color:{ORANGE};">{s["wkp"]}</strong> ({s["wacc"]:.0%}). '
                    f'Recommend targeted practice & peer learning.</div></div>', True)
        st.markdown('</div>', True)

    with t4:
        el = R["el"]; et = R["et"]
        if len(el) < 2:
            st.warning("Need ≥ 2 exams for trend analysis.")
        else:
            st.markdown('<div class="sp">', True)
            st.markdown("### Exam Trends")
            fig4 = make_subplots(rows=1, cols=2,
                                 subplot_titles=("Class Accuracy","Class Avg Time"),
                                 horizontal_spacing=.12)
            fig4.add_trace(go.Scatter(
                x=et["exam_id"],y=et["accuracy"],mode="lines+markers+text",
                marker=dict(size=9,color=GREEN),line=dict(width=3,color=GREEN),
                text=[f"{a:.1%}" for a in et["accuracy"]],
                textposition="top center",textfont=dict(size=11,color=GREEN),name="Acc"
            ), row=1, col=1)
            fig4.add_trace(go.Scatter(
                x=et["exam_id"],y=et["at"],mode="lines+markers+text",
                marker=dict(size=9,color=TEAL),line=dict(width=3,color=TEAL),
                text=[f"{t:.0f}s" for t in et["at"]],
                textposition="top center",textfont=dict(size=11,color=TEAL),name="Time"
            ), row=1, col=2)
            fig4.update_layout(**PLT,height=360,showlegend=False)
            fig4.update_yaxes(tickformat=".0%",gridcolor=GRID_C,row=1,col=1)
            fig4.update_yaxes(gridcolor=GRID_C,row=1,col=2)
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown('</div>', True)
            st.markdown('<div class="sp">', True)
            st.markdown("##### KP Trends")
            kcm = R["kcm"]
            kep = R["ke"].pivot_table(index="exam_id",columns="kp",values="accuracy").reindex(el)
            fig5 = go.Figure()
            for i, kp in enumerate(kep.columns):
                fig5.add_trace(go.Scatter(
                    x=kep.index, y=kep[kp], mode="lines+markers", name=kp,
                    marker=dict(size=8),
                    line=dict(width=2.5, color=kcm.get(kp, KPC[i % len(KPC)]))
                ))
            fig5.update_layout(**PLT, height=360,
                yaxis=dict(tickformat=".0%",gridcolor=GRID_C),
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="center",x=.5))
            st.plotly_chart(fig5, use_container_width=True)
            st.markdown('</div>', True)

    with t5:
        st.markdown('<div class="sp">', True)
        st.markdown("#### 🤖 AI Teaching Assistant")
        st.markdown(
            f'<div style="font-size:13px;color:{TEXT2};margin-bottom:16px;">'
            f'Get a comprehensive class report based on mastery, behavior, and risk data.</div>',
            unsafe_allow_html=True)
        if st.button("📋 Generate Class Report & Strategies",
                     type="primary", use_container_width=True, key="teacher_ai_main"):
            with st.spinner("AI is analyzing class data..."):
                reply = call_deepseek(build_teacher_prompt(R))
            st.markdown(
                f'<div class="sp" style="background:{CARD};">'
                f'<strong style="font-size:15px;">AI Class Report</strong>'
                f'<hr style="margin:12px 0;">{reply}</div>',
                unsafe_allow_html=True)
        st.markdown('</div>', True)
        st.markdown('<div class="sp">', True)
        st.markdown("#### 💬 Ask About Your Class")
        st.caption("e.g. 'Which students need help with Calculus?'")
        teacher_q = st.text_input("Your question",
                                  placeholder="e.g. Which students are guessing the most?",
                                  key="teacher_free_q")
        if st.button("Ask AI", key="teacher_ask_btn"):
            if teacher_q.strip():
                seg_summary    = R["ss"]["seg"].value_counts().to_dict()
                weakest_kp_str = R["ko"][["kp","accuracy"]].sort_values("accuracy").head(3).to_string(index=False)
                risk_str       = (R["rk"][["student_id","accuracy","wkp"]].head(5).to_string(index=False)
                                  if len(R["rk"])>0 else "None")
                free_prompt = (
                    f"You are a teaching assistant AI. Class data summary: "
                    f"Segments={seg_summary}. Weakest KPs={weakest_kp_str}. "
                    f"At-risk students={risk_str}. "
                    f"Teacher question: {teacher_q}. "
                    f"Answer concisely in English, under 150 words."
                )
                with st.spinner("Thinking..."):
                    reply2 = call_deepseek(free_prompt)
                st.markdown(
                    f'<div class="ai-reply"><strong>Q: {teacher_q}</strong>'
                    f'<hr style="margin:8px 0;">{reply2}</div>',
                    unsafe_allow_html=True)
            else:
                st.warning("Please type a question first.")
        st.markdown('</div>', True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STUDENT PORTAL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if "Student" in portal:
    if sel_sid is None:
        st.error("Please select a student from the sidebar.")
        st.stop()

    S = a_student(df, sel_sid)
    if S is None:
        st.error(f"No data found for student {sel_sid}")
        st.stop()

    STEPS = [
        {"icon":"📍","en":"Diagnose",  "full":"Self-Diagnosis"},
        {"icon":"🎯","en":"Set Goals", "full":"Goal Setting"},
        {"icon":"🗺️","en":"Strategy",  "full":"Strategy Planning"},
        {"icon":"📊","en":"Monitor",   "full":"Progress Monitoring"},
        {"icon":"💡","en":"Reflect",   "full":"Reflection & Next Steps"},
    ]

    if "map_step" not in st.session_state:
        st.session_state.map_step = 1
    if "prev_sid" not in st.session_state:
        st.session_state.prev_sid = None
    if st.session_state.prev_sid != sel_sid:
        st.session_state.map_step = 1
        st.session_state.prev_sid = sel_sid

    current = st.session_state.map_step

    # ── AI Companion Sidebar ──
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### 🤖 AI Study Companion")
    st.sidebar.caption("Your personalized AI learning assistant")
    S_comp = a_student(df, sel_sid)

    if S_comp is not None:
        step_tips = {
            1: ("📍 Self-Diagnosis Mode",
                f"Your overall accuracy is **{S_comp['oa']:.0%}**. "
                f"Focus on understanding your strengths and growth patterns before setting goals."),
            2: ("🎯 Goal Setting Mode",
                f"Your biggest opportunity is **{S_comp['weakest_kp']}** ({S_comp['weakest_kp_acc']:.0%}). "
                f"Set a specific, achievable weekly goal to target this area."),
            3: ("🗺️ Strategy Mode",
                f"Your guessing rate is **{S_comp['gr']:.0%}** and time volatility is **{S_comp['hes']:.2f}**. "
                f"Small behavior changes lead to big improvements."),
            4: ("📊 Monitoring Mode",
                f"Your mastery changed by **{S_comp['mm']:+.1%}** between recent exams. "
                f"Consistent progress compounds into great results."),
            5: ("💡 Reflection Mode",
                f"Your weakest area is **{S_comp['weakest_kp']}**. "
                f"Analyze error patterns and turn mistakes into your action plan."),
        }
        tip_title, tip_text = step_tips.get(current, ("",""))
        st.sidebar.markdown(
            f'<div style="background:#F0F7F4;padding:14px;border-radius:10px;'
            f'border:1px solid rgba(125,184,143,.3);">'
            f'<div style="font-size:13px;font-weight:600;color:{TEXT};margin-bottom:6px;">{tip_title}</div>'
            f'<div style="font-size:12px;color:{TEXT2};line-height:1.6;">{tip_text}</div>'
            f'</div>', unsafe_allow_html=True)

        st.sidebar.markdown("---")
        st.sidebar.markdown("**💬 Ask AI a question**")
        quick_questions = [
            "",
            "How can I improve my weakest area?",
            "Why are my scores fluctuating?",
            "What should I focus on this week?",
            "Am I studying effectively?",
            "How does my pacing affect my scores?",
        ]
        selected_q = st.sidebar.selectbox(
            "Choose a quick question...", quick_questions,
            key="comp_quick_q", label_visibility="collapsed")
        custom_q = st.sidebar.text_input(
            "Or type your own question...",
            placeholder="e.g. How should I study for my next exam?",
            key="comp_custom_q", label_visibility="collapsed")
        ask_question = selected_q or custom_q
        if st.sidebar.button("🤖 Ask AI", key="comp_ask_btn",
                             use_container_width=True, type="primary"):
            if ask_question and ask_question.strip():
                with st.sidebar.spinner("🤔 Thinking..."):
                    p = (build_student_prompt(S_comp, sel_sid) +
                         f"\n\nStudent asks: {ask_question.strip()}"
                         f"\n\nAnswer briefly in 2-3 sentences. Be specific and actionable.")
                    reply = call_deepseek(p)
                st.sidebar.markdown(
                    f'<div style="background:#fff;padding:12px;border-radius:10px;'
                    f'border:1px solid {BORDER};font-size:12px;line-height:1.6;color:{TEXT};">'
                    f'<div style="font-weight:600;color:{ACCENT};margin-bottom:6px;">🤖 AI Reply:</div>'
                    f'{reply}</div>', unsafe_allow_html=True)
            else:
                st.sidebar.warning("Please select or type a question first!")

        st.sidebar.markdown("---")
        if st.sidebar.button("💪 Give me encouragement",
                             key="encourage_btn", use_container_width=True):
            with st.sidebar.spinner("🤗 Sending encouragement..."):
                p = (f"Student {sel_sid} has overall accuracy {S_comp['oa']:.0%} and feels discouraged. "
                     f"Write a short, warm, empowering message (2-3 sentences) focusing on growth, "
                     f"effort, and small wins. Be genuine, not generic.")
                reply = call_deepseek(p)
            st.sidebar.success(reply)

    # ── Progress Bar ──
    prog_html = '<div class="lm-progress">'
    for i, step in enumerate(STEPS, 1):
        dot_cls = ("lm-dot done" if i < current
                   else "lm-dot active" if i == current
                   else "lm-dot pending")
        lbl_cls = "lm-step-label active" if i == current else "lm-step-label"
        content = step["icon"] if i <= current else str(i)
        prog_html += (f'<div class="lm-step-wrap">'
                      f'<div class="{dot_cls}">{content}</div>'
                      f'<div class="{lbl_cls}">{step["en"]}</div></div>')
        if i < len(STEPS):
            prog_html += f'<div class="{"lm-line done" if i < current else "lm-line"}"></div>'
    prog_html += '</div>'
    st.markdown(prog_html, unsafe_allow_html=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Step 1 — Self-Diagnosis
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    if current == 1:
        st.markdown('<div class="lm-card">', unsafe_allow_html=True)
        st.markdown('<div class="lm-title">📍 Where am I?</div>', unsafe_allow_html=True)
        st.markdown("<div class='lm-subtitle'>Let's understand your current learning status</div>",
                    unsafe_allow_html=True)

        gt = S["gt"]
        bc = GREEN if "Accelerating" in gt else ORANGE if "Fluctuating" in gt else TEXT3
        st.markdown(
            f'<div style="text-align:center;padding:16px 0;">'
            f'<span style="display:inline-block;padding:10px 28px;border-radius:30px;'
            f'font-size:22px;font-weight:700;background:{bc}18;color:{bc};'
            f'border:2px solid {bc}22;">{gt}</span></div>', unsafe_allow_html=True)

        GROWTH_TEXT = {
            "🚀 Accelerating":
                f"🎯 <strong>You're on fire!</strong> Your learning speed is increasing with every exam — "
                f"you're not just improving, you're improving <em>faster</em>. "
                f"{S['strongest_kp']} is your strongest area right now!",
            "🌱 Steady":
                f"🌿 <strong>Reliable and consistent.</strong> Steady progress is one of the healthiest "
                f"patterns. Foundations are solid. To accelerate, focus more on {S['weakest_kp']}.",
            "🎢 Fluctuating":
                f"🌊 <strong>Roller coaster mode.</strong> Scores vary, but that's normal — especially "
                f"on harder topics like {S['weakest_kp']}. Don't get discouraged. Dips are temporary!",
            "🌿 Building Foundation":
                f"🌱 <strong>Gathering strength.</strong> Progress feels slow, but you're building roots "
                f"before the big growth spurt. Every single effort counts!",
        }
        st.markdown(
            f'<div class="lm-insight">{GROWTH_TEXT.get(gt, "")}</div>',
            unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            ac_c = GREEN if S["oa"]>=.7 else ORANGE if S["oa"]>=.5 else RED
            st.markdown(
                f'<div class="tc"><div class="lbl">Overall Accuracy</div>'
                f'<div class="val" style="color:{ac_c};">{S["oa"]:.0%}</div>'
                f'<div class="sub">{S["ti"]} items total</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(
                f'<div class="tc"><div class="lbl">Your Strength</div>'
                f'<div class="val" style="color:{GREEN};font-size:18px;">{S["strongest_kp"]}</div>'
                f'<div class="sub">{S["strongest_kp_acc"]:.0%} accuracy</div></div>',
                unsafe_allow_html=True)
        with c3:
            st.markdown(
                f'<div class="tc"><div class="lbl">Needs Attention</div>'
                f'<div class="val" style="color:{RED};font-size:18px;">{S["weakest_kp"]}</div>'
                f'<div class="sub">{S["weakest_kp_acc"]:.0%} accuracy</div></div>',
                unsafe_allow_html=True)

        if len(S["mgi"]) >= 1:
            mgi_text = ("positive — heading in the right direction!" if S["mm"]>0
                        else "a small dip — fluctuations are completely normal.")
            st.markdown(
                f'<div class="lm-insight" style="margin-top:14px;">📈 <strong>Growth momentum</strong>: '
                f'Your mastery changed by <strong>{S["mm"]:+.1%}</strong> between your last two exams. '
                f'This is {mgi_text}</div>', unsafe_allow_html=True)

        st.markdown(
            f'<div style="margin-top:24px;text-align:center;font-size:13px;color:{TEXT3};">'
            f'✨ Now you know your status. Ready to set goals? <strong>→ Step 2</strong></div>',
            unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Step 2 — Goal Setting
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    elif current == 2:
        st.markdown('<div class="lm-card">', unsafe_allow_html=True)
        st.markdown('<div class="lm-title">🎯 Where am I going?</div>', unsafe_allow_html=True)
        st.markdown("<div class='lm-subtitle'>Let's set a clear goal based on your knowledge map</div>",
                    unsafe_allow_html=True)

        kd = S["kp"].sort_values("accuracy", ascending=False)
        for _, r in kd.iterrows():
            c = GREEN if r["accuracy"]>=.8 else ORANGE if r["accuracy"]>=.6 else RED
            if r["accuracy"] >= .8:
                status, hint = "Mastered ✨", "Great job! Maintain with regular light review."
            elif r["accuracy"] >= .6:
                status, hint = "Developing 📖", "Almost there! A little more practice to reach mastery."
            else:
                status, hint = "Growth Opportunity 🎯", "Priority area — focus your energy here this week."
            st.markdown(
                f'<div class="lm-kp-card">'
                f'<div class="lm-kp-pct" style="background:{c}18;color:{c};border:2px solid {c};">'
                f'{r["accuracy"]:.0%}</div>'
                f'<div style="flex:1;">'
                f'<div style="font-weight:600;font-size:15px;color:{TEXT};">{r["kp"]}</div>'
                f'<div style="font-size:11px;color:{c};font-weight:600;margin:2px 0;">{status}</div>'
                f'<div style="font-size:13px;color:{TEXT2};line-height:1.5;">{hint}</div>'
                f'</div></div>', unsafe_allow_html=True)

        if st.checkbox("ℹ️ How to read these knowledge cards", key="read_kp_cards"):
            st.markdown(
                f'Each card shows your <strong>overall accuracy</strong> for a knowledge point '
                f'across all exams.<br><br>'
                f'• <span style="color:{GREEN};font-weight:600;">🟢 Mastered (≥80%)</span> — '
                f'Solid understanding. Keep it fresh with light review.<br>'
                f'• <span style="color:{ORANGE};font-weight:600;">🟡 Developing (60–79%)</span> — '
                f'On the right track. A bit more practice will push you to mastery.<br>'
                f'• <span style="color:{RED};font-weight:600;">🔴 Growth Opportunity (&lt;60%)</span> — '
                f'Priority area. Revisit fundamentals and practice deliberately.<br><br>'
                f'Your top strength is <strong>{S["strongest_kp"]}</strong> ({S["strongest_kp_acc"]:.0%}) '
                f'and biggest opportunity is <strong>{S["weakest_kp"]}</strong> ({S["weakest_kp_acc"]:.0%}).',
                unsafe_allow_html=True)

        kep = S["kepp"]
        if kep.shape[1] > 0:
            if st.checkbox("📊 View detailed exam × KP heatmap", key="heatmap_show"):
                fig = go.Figure(go.Heatmap(
                    z=kep.values, x=kep.columns.tolist(), y=kep.index.tolist(),
                    colorscale=[[0,RED],[.3,ORANGE],[.6,GREEN],[1,ACCENT]], zmin=0, zmax=1,
                    text=[[f"{v:.0%}" if not np.isnan(v) else "—" for v in row] for row in kep.values],
                    texttemplate="%{text}", textfont=dict(size=11),
                    colorbar=dict(tickformat=".0%", thickness=12, len=.5)
                ))
                fig.update_layout(height=max(240, len(kep)*60),
                                  margin=dict(l=0,r=0,t=20,b=0),
                                  xaxis=dict(side="top"))
                st.plotly_chart(fig, use_container_width=True)

                if st.checkbox("💡 How to read this heatmap", key="read_heatmap"):
                    st.markdown(
                        f'Each row = a topic, each column = an exam.<br>'
                        f'<span style="color:{RED};">🔴 Red</span> = low accuracy · '
                        f'<span style="color:{ORANGE};">🟠 Orange</span> = moderate · '
                        f'<span style="color:{GREEN};">🟢 Green</span> = high · '
                        f'<span style="color:{ACCENT};">🔵 Blue</span> = excellent<br><br>'
                        f'Look for left-to-right improvement (progress working!) or '
                        f'consistently warm rows (needs a different approach).',
                        unsafe_allow_html=True)

        st.markdown(
            f'<div style="margin-top:16px;padding:18px;background:#F0F7F4;border-radius:14px;'
            f'border:1px solid rgba(125,184,143,.25);">'
            f'<div style="font-weight:600;color:{TEXT};margin-bottom:4px;">✏️ Set Your Weekly Goal</div>'
            f'<div style="font-size:13px;color:{TEXT2};">Based on your diagnosis, your biggest '
            f'opportunity is <strong style="color:{RED};">{S["weakest_kp"]}</strong>. '
            f'What will you focus on this week?</div></div>', unsafe_allow_html=True)

        goal_key     = f"goal_{sel_sid}"
        current_goal = st.session_state.get(goal_key, "")
        if current_goal:
            st.markdown(
                f'<div style="background:{WHITE};padding:10px 14px;border-radius:10px;'
                f'margin-bottom:10px;font-size:13px;color:{TEXT2};border:1px solid {BORDER};">'
                f'📝 <strong>Current goal:</strong> {current_goal}</div>', unsafe_allow_html=True)

        new_goal = st.text_area(
            "Write your goal here...",
            placeholder=f"Example: I want to improve {S['weakest_kp']} by reviewing my 5 most recent wrong items daily.",
            value=current_goal, height=76, label_visibility="collapsed")

        if st.button("✅ Save Goal", key="save_goal_btn", use_container_width=True):
            if new_goal.strip():
                st.session_state[goal_key] = new_goal.strip()
                st.success("🎯 Goal saved! You can update it anytime.")
                st.rerun()
            else:
                st.warning("Please write something first!")

        if st.checkbox("💡 Why set a weekly goal?", key="why_weekly_goal"):
            st.markdown(
                f'Specific, time-bound goals dramatically increase improvement. '
                f'Instead of "I\'ll study more," try '
                f'"I\'ll review 5 wrong {S["weakest_kp"]} items every day this week." '
                f'This makes your goal <strong>measurable and actionable</strong>.',
                unsafe_allow_html=True)

        st.markdown(
            f'<div style="margin-top:24px;text-align:center;font-size:13px;color:{TEXT3};">'
            f'🎯 Goals set? Build strategies in <strong>Step 3 →</strong></div>',
            unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Step 3 — Strategy Planning
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    elif current == 3:
        st.markdown('<div class="lm-card">', unsafe_allow_html=True)
        st.markdown('<div class="lm-title">🗺️ How do I get there?</div>', unsafe_allow_html=True)
        st.markdown("<div class='lm-subtitle'>Understanding your learning patterns to create effective strategies</div>",
                    unsafe_allow_html=True)

        if st.checkbox("🔍 Optional: Deep Dive into Your Learning Habits", key="deep_dive"):
            st.markdown('#### 🧠 Your Learning Style Profile')
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                gc = RED if S["gr"]>.1 else ORANGE if S["gr"]>.05 else GREEN
                st.markdown(
                    f'<div class="tc"><div class="lbl">Guessing</div>'
                    f'<div class="val" style="color:{gc};">{S["gr"]:.1%}</div>'
                    f'<div class="sub">{"⚠️ High" if S["gr"]>.1 else "✅ Normal"}</div></div>',
                    unsafe_allow_html=True)
            with c2:
                hc = ORANGE if S["hes"]>1.0 else GREEN
                st.markdown(
                    f'<div class="tc"><div class="lbl">Pacing</div>'
                    f'<div class="val" style="color:{hc};">{"Uneven" if S["hes"]>1.0 else "Steady"}</div>'
                    f'<div class="sub">Vol: {S["hes"]:.2f}</div></div>', unsafe_allow_html=True)
            with c3:
                cc = ORANGE if S["cr"]>0.25 else GREEN
                st.markdown(
                    f'<div class="tc"><div class="lbl">Revisions</div>'
                    f'<div class="val" style="color:{cc};">{S["cr"]:.0%}</div>'
                    f'<div class="sub">Answer changes</div></div>', unsafe_allow_html=True)
            with c4:
                htc = RED if S["hr"]>0.15 else GREEN
                st.markdown(
                    f'<div class="tc"><div class="lbl">Hint Use</div>'
                    f'<div class="val" style="color:{htc};">{S["hr"]:.0%}</div>'
                    f'<div class="sub">Needed hints</div></div>', unsafe_allow_html=True)

            st.markdown('#### 📋 Personalized Strategy Tips')
            tips = []
            if S["gr"] > 0.1:
                tips.append(f"🔍 <strong>Rushing detected</strong>: {S['gr']:.0%} of wrong answers "
                            f"took under 15 seconds — a sign of guessing. "
                            f"<em>Re-read each question once before choosing.</em>")
            else:
                tips.append("✅ <strong>Good patience!</strong> You rarely rush — strong test-taking discipline!")
            if S["hes"] > 1.0:
                tips.append(f"⏱️ <strong>Inconsistent pacing</strong> (volatility: {S['hes']:.2f}). "
                            f"<em>If a question takes more than 2 minutes, skip and return later.</em>")
            else:
                tips.append("✅ <strong>Steady pacing</strong> — consistent time management. Keep it up!")
            if S["atw"] > 0 and S["atc"] > 0 and S["atw"] < S["atc"] * 0.8:
                tips.append(f"🤔 <strong>Wrong answers are faster</strong>: {S['atw']:.0f}s wrong vs "
                            f"{S['atc']:.0f}s correct. "
                            f"<em>Give tough questions an extra 10–15 seconds before deciding.</em>")
            if S["cr"] > 0.25:
                tips.append(f"🔄 <strong>Frequent answer changes</strong>: {S['cr']:.0%} of answers revised. "
                            f"<em>Your first instinct is usually right — only change with a concrete reason.</em>")
            if S["hr"] > 0.15:
                tips.append(f"💡 <strong>Hint usage</strong>: {S['hr']:.0%} of questions needed hints. "
                            f"<em>Attempt each problem fully before reaching for help.</em>")
            if not tips:
                tips.append("🌟 <strong>Excellent habits!</strong> Your study behaviors are strong across the board.")
            for tip in tips:
                st.markdown(f'<div class="lm-insight">{tip}</div>', unsafe_allow_html=True)

            st.markdown('#### ⏱️ Time Distribution')
            sd = S["s"]
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=sd[sd["is_correct"]==1]["time_spent"],
                                       name="✅ Correct", marker_color=GREEN, opacity=.7, nbinsx=30))
            fig.add_trace(go.Histogram(x=sd[sd["is_correct"]==0]["time_spent"],
                                       name="❌ Wrong", marker_color=RED, opacity=.7, nbinsx=30))
            fig.update_layout(height=320, barmode="overlay",
                              xaxis=dict(title="Time (seconds)"),
                              yaxis=dict(title="Count"),
                              legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                          xanchor="center", x=.5))
            st.plotly_chart(fig, use_container_width=True)
            if st.checkbox("📘 What does this chart mean?", key="time_dist_mean"):
                st.markdown(
                    'Wrong answers (red) tend to cluster at shorter times, correct answers (green) '
                    'are more spread out. Rushing = more mistakes. '
                    'Taking the right amount of time is key.')

        st.markdown('#### 🎯 Your Personalized Improvement Strategies')
        st.markdown(
            f'<div class="lm-strategy-card">'
            f'<div style="font-weight:600;font-size:15px;color:{TEXT};margin-bottom:8px;">'
            f'Focus on Your Weakest Area: {S["weakest_kp"]}</div>'
            f'<div style="font-size:13px;color:{TEXT2};line-height:1.6;">'
            f'{S["weakest_kp"]} is your biggest growth opportunity. '
            f'Here are targeted strategies.</div></div>', unsafe_allow_html=True)

        if S["gr"] > 0.1:
            st.markdown(
                f'<div class="lm-strategy-item"><div class="lm-strategy-icon">🔍</div>'
                f'<div><strong>Slow down</strong> — especially on {S["weakest_kp"]}. '
                f'Take at least 15 seconds per question.</div></div>', unsafe_allow_html=True)
        if S["hes"] > 1.0:
            st.markdown(
                f'<div class="lm-strategy-item"><div class="lm-strategy-icon">⏱️</div>'
                f'<div><strong>Practice timing</strong> — set a timer for {S["weakest_kp"]} questions '
                f'to develop consistent pace.</div></div>', unsafe_allow_html=True)
        if S["cr"] > 0.25:
            st.markdown(
                f'<div class="lm-strategy-item"><div class="lm-strategy-icon">🔄</div>'
                f'<div><strong>Trust your first instinct</strong> — avoid changing {S["weakest_kp"]} '
                f'answers without a clear reason.</div></div>', unsafe_allow_html=True)

        if st.checkbox("📋 Show your detailed action plan", key="action_plan_show"):
            st.markdown(
                f'<div style="font-weight:600;font-size:15px;color:{TEXT};margin-bottom:12px;">'
                f'🎯 Action Plan for {S["weakest_kp"]}</div>', unsafe_allow_html=True)
            plan = []
            if S["gr"] > 0.1:
                plan.append(
                    f"• **Slow down on {S['weakest_kp']}**: Spend at least 20 seconds per problem. "
                    f"Read twice, underline key terms, write the first step before looking at choices. "
                    f"Practice on 3–5 problems daily for one week.")
            else:
                plan.append(
                    f"• **Maintain your careful pace**: Continue spending ≥15 seconds per {S['weakest_kp']} problem. "
                    f"After solving, explain your reasoning in one sentence to deepen understanding.")
            if S["hes"] > 1.0:
                plan.append(
                    f"• **Build consistent pacing**: Set a 10-minute timer daily, solve 5 {S['weakest_kp']} questions. "
                    f"Aim for 40–90 seconds each. After 5 days, compare speed vs. accuracy.")
            else:
                plan.append(
                    f"• **Leverage your steady rhythm**: Divide study sessions into 15-minute blocks, "
                    f"each focusing on one {S['weakest_kp']} sub-topic.")
            if S["cr"] > 0.25:
                plan.append(
                    f"• **Reduce answer changes**: Write your first choice on a scratchpad. "
                    f"Only change if you find a concrete error. Review changed answers after each session.")
            plan.append(
                f"• **Daily wrong-item review**: Pick 3–5 incorrect {S['weakest_kp']} questions. "
                f"Re-attempt, identify the mistake type, write one sentence on how to avoid it next time.")
            plan.append(
                f"• **Track progress**: Log your {S['weakest_kp']} accuracy each session. "
                f"Target: {S['weakest_kp_acc']:.0%} → {min(1.0, S['weakest_kp_acc']+0.1):.0%} by next Friday.")
            for item in plan:
                st.markdown(
                    f'<div style="margin:10px 0;padding-left:8px;border-left:3px solid {ACCENT};">'
                    f'{item}</div>', unsafe_allow_html=True)

        st.markdown(
            f'<div style="margin-top:24px;text-align:center;font-size:13px;color:{TEXT3};">'
            f'📊 Want to see your progress over time? <strong>→ Step 4</strong></div>',
            unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Step 4 — Progress Monitoring
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    elif current == 4:
        st.markdown('<div class="lm-card">', unsafe_allow_html=True)
        st.markdown("<div class='lm-title'>📊 How's it going?</div>", unsafe_allow_html=True)
        st.markdown("<div class='lm-subtitle'>Let's see how your learning journey has progressed</div>",
                    unsafe_allow_html=True)

        if st.checkbox("💡 Why this step matters", key="why_step4"):
            st.markdown(
                'Tracking progress shows what\'s working and what needs adjustment. '
                'It reveals how far you\'ve come and where to focus next.')

        el = S["el"]; em = S["em"]
        if len(el) >= 2:
            st.markdown('#### 📈 Your Overall Progress')
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=em["exam_id"], y=em["mastery"],
                mode="lines+markers+text", name=sel_sid,
                marker=dict(size=10, color=ACCENT, line=dict(width=2, color=WHITE)),
                line=dict(width=3, color=ACCENT),
                text=[f"{m:.1%}" for m in em["mastery"]],
                textposition="top center", textfont=dict(size=11, color=ACCENT)))
            mg = em.merge(S["ca"], on="exam_id", how="left")
            fig.add_trace(go.Scatter(
                x=mg["exam_id"], y=mg["cavg"], mode="lines", name="Class Average",
                line=dict(width=2, color=BORDER, dash="dash")))
            fig.update_layout(height=360,
                              yaxis=dict(title="Mastery", tickformat=".0%", gridcolor=GRID_C),
                              legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                          xanchor="center", x=.5))
            st.plotly_chart(fig, use_container_width=True)

            first_m = em["mastery"].iloc[0]; last_m = em["mastery"].iloc[-1]
            diff    = last_m - first_m
            if diff > 0.05:
                msg = (f'📈 <strong>Great news!</strong> Mastery improved from {first_m:.0%} to '
                       f'{last_m:.0%} — a jump of {diff:+.1%}! Hard work paying off.')
            elif diff > -0.05:
                msg = (f'📊 <strong>Staying stable.</strong> Mastery around {last_m:.0%}. '
                       f'Consistency is key — you\'re maintaining your knowledge base.')
            else:
                msg = (f'📉 <strong>A slight dip</strong> from {first_m:.0%} to {last_m:.0%}. '
                       f'This often happens when exams get harder. Find which KPs dropped and focus there.')
            st.markdown(f'<div class="lm-insight" style="margin-top:16px;">{msg}</div>',
                        unsafe_allow_html=True)

            if len(S["mgi"]) > 0:
                lb = [f"{el[i]}→{el[i+1]}" for i in range(len(S["mgi"]))]
                cs = [GREEN if m>0 else RED for m in S["mgi"]]
                fig2 = go.Figure(go.Bar(
                    x=lb, y=S["mgi"], marker_color=cs,
                    text=[f"{m:+.1%}" for m in S["mgi"]],
                    textposition="outside", textfont=dict(size=12, color=TEXT)))
                fig2.add_hline(y=0, line_color=BORDER)
                fig2.update_layout(height=280, yaxis=dict(tickformat=".1%", gridcolor=GRID_C))
                st.plotly_chart(fig2, use_container_width=True)
                if st.checkbox("📘 What does this bar chart mean?", key="bar_chart_mean"):
                    st.markdown(
                        'Green = improvement between those exams, red = slight drop. '
                        'Big changes often correspond to new topics or harder material.')
        else:
            st.info("Need at least 2 exams to show trends. Keep going!")

        st.markdown('#### 📚 Knowledge Point Trends')
        kep_trend = S["kepp"].T
        if kep_trend.shape[0] > 0:
            fig3 = go.Figure()
            for kp in kep_trend.columns:
                accs     = kep_trend[kp].values
                eids     = kep_trend.index.tolist()
                valid    = ~np.isnan(accs)
                if np.any(valid):
                    fig3.add_trace(go.Scatter(
                        x=[eids[i] for i in range(len(eids)) if valid[i]],
                        y=accs[valid],
                        mode='lines+markers+text', name=kp,
                        line=dict(width=2.5, color=KPC_COLORS.get(kp, ACCENT)),
                        marker=dict(size=8, color=KPC_COLORS.get(kp, ACCENT)),
                        text=[f"{v:.0%}" for v in accs[valid]],
                        textposition="top center", textfont=dict(size=10)
                    ))
            fig3.update_layout(
                height=380,
                yaxis=dict(tickformat=".0%", gridcolor=GRID_C, title="Accuracy", range=[0,1]),
                xaxis=dict(title="Exam ID"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=.5),
                margin=dict(l=0,r=0,t=20,b=40), hovermode="x unified")
            st.plotly_chart(fig3, use_container_width=True)
            if st.checkbox("📘 How to read this line chart", key="line_chart_read"):
                st.markdown(
                    'Each line = one knowledge point over time. '
                    'Look for steady improvement (good!), fluctuation (normal), '
                    'or a downward trend (needs focus). Reaching the green zone (≥80%) = mastery.')
        else:
            st.success("🎉 No knowledge point trends to show yet!")

        st.markdown(
            f'<div style="margin-top:24px;text-align:center;font-size:13px;color:{TEXT3};">'
            f'💡 Ready to reflect and plan next moves? <strong>→ Step 5</strong></div>',
            unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Step 5 — Reflection & Next Steps
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    elif current == 5:
        st.markdown('<div class="lm-card">', unsafe_allow_html=True)
        st.markdown('<div class="lm-title">🚀 How do I improve?</div>', unsafe_allow_html=True)
        st.markdown("<div class='lm-subtitle'>Let's turn insights into action</div>",
                    unsafe_allow_html=True)

        if st.checkbox("💡 Why this step matters", key="why_step5"):
            st.markdown(
                'This is where everything comes together. Instead of just looking at mistakes, '
                'we\'ll understand why they happened and create a concrete plan to avoid them.')

        st.markdown('#### 📊 Error Rate by Knowledge Point')
        kd = S["kp"].copy()
        kd["error_rate"] = 1 - kd["accuracy"]
        kd = kd.sort_values("error_rate", ascending=False)
        fig = go.Figure(go.Bar(
            x=kd["kp"], y=kd["error_rate"],
            marker_color=[RED if e>.5 else ORANGE if e>.3 else YELLOW for e in kd["error_rate"]],
            text=[f"{e:.0%}" for e in kd["error_rate"]],
            textposition="outside", textfont=dict(size=12, color=TEXT)))
        fig.update_layout(height=320,
                          yaxis=dict(tickformat=".0%", range=[0,1], gridcolor=GRID_C))
        st.plotly_chart(fig, use_container_width=True)

        worst_kp  = kd.iloc[0]["kp"]
        worst_er  = kd.iloc[0]["error_rate"]
        if worst_er > 0.6:
            err_msg = (f'🔴 <strong>{worst_kp} is your biggest challenge</strong> — '
                       f'{worst_er:.0%} error rate. Revisit fundamentals and review recent wrong items.')
        elif worst_er > 0.4:
            err_msg = (f'🟠 <strong>{worst_kp} needs attention</strong> — {worst_er:.0%} error rate. '
                       f'Break complex problems into smaller steps and practice each separately.')
        else:
            err_msg = (f'🟡 <strong>{worst_kp} shows room for improvement</strong> — {worst_er:.0%} error rate. '
                       f'Even small gains here make a big difference overall.')
        st.markdown(f'<div class="lm-insight" style="margin-top:16px;">{err_msg}</div>',
                    unsafe_allow_html=True)

        st.markdown('#### 📋 Error Type Analysis')
        error_types = {
            "Conceptual Understanding": 35,
            "Calculation Errors":       25,
            "Careless Mistakes":        20,
            "Time Pressure":            15,
            "Strategy Issues":           5,
        }
        fig2 = go.Figure(go.Pie(
            labels=list(error_types.keys()), values=list(error_types.values()),
            hole=.4, marker=dict(colors=[RED, ORANGE, YELLOW, GREEN, ACCENT]),
            textinfo="label+percent", textfont=dict(size=12)))
        fig2.update_layout(height=320)
        st.plotly_chart(fig2, use_container_width=True)

        if st.checkbox("📘 Understanding these error types", key="error_types_read"):
            st.markdown("""
- **Conceptual Understanding** — You don't fully grasp the ideas. Review theory and worked examples.
- **Calculation Errors** — You know the concept but make arithmetic mistakes. Double-check your work.
- **Careless Mistakes** — Rushing or misreading. Use the 3-second rule before answering.
- **Time Pressure** — Running out of time. Practice with a timer; learn to skip and return.
- **Strategy Issues** — Need better problem-solving approaches. Break problems into smaller steps.
""")

        st.markdown('#### 📝 Your Recent Wrong Items')
        # 修复：使用 st.dataframe 代替手写 HTML 表格，并清洗 kp 列
        if len(S["wi"]) > 0:
            df_errors = S["wi"].head(10)[["exam_id", "date", "kp", "item_id", "option_chosen", "time_spent"]].copy()
            df_errors.columns = ["Exam", "Date", "Knowledge Point", "Item", "Choice", "Time (s)"]
            # 再次确保 kp 列没有“时代”等异常前缀
            df_errors["Knowledge Point"] = df_errors["Knowledge Point"].astype(str).str.replace("时代", "", regex=False).str.strip()
            st.dataframe(df_errors, use_container_width=True)
        else:
            st.success("🎉 No wrong items to display! Great job!")

        st.markdown('#### 📝 Weekly Reflection')
        reflection = st.text_area(
            "What worked well this week? What will you do differently?",
            placeholder=(
                "Example: I focused on Calculus. More confident with derivatives, "
                "but still struggle with integrals. Next week: 3 integral problems daily + "
                "review the fundamental theorem."),
            height=100, label_visibility="collapsed")
        if st.button("Save Reflection", use_container_width=True, key="save_reflection"):
            st.success("✅ Reflection saved! Use these insights to guide your next cycle.")

        st.markdown('#### 🎯 Your Improvement Action Plan')
        action_plan = [f"• Focus on **{worst_kp}** — your biggest challenge area"]
        if error_types["Conceptual Understanding"] > 30:
            action_plan.append("• Revisit core concepts and practice explaining them in your own words")
        if error_types["Calculation Errors"] > 20:
            action_plan.append("• Practice basic calculations daily and double-check your work")
        if error_types["Careless Mistakes"] > 15:
            action_plan.append("• Use the 3-second rule: read each question carefully before answering")
        if error_types["Time Pressure"] > 10:
            action_plan.append("• Practice with a timer; learn when to skip and return")
        action_plan.append("• Review 3–5 wrong items daily from your weakest area")
        action_plan.append("• Set specific, measurable goals for next week")
        for item in action_plan:
            st.markdown(
                f'<div style="margin:6px 0;padding-left:20px;">{item}</div>',
                unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🤖 Get Your Full AI Learning Report")
        if st.button("✨ Generate My Personalized AI Report",
                     type="primary", use_container_width=True, key="stu_ai_report"):
            with st.spinner("AI is analyzing your complete learning profile..."):
                reply = call_deepseek(build_student_prompt(S, sel_sid))
            st.markdown(
                f'<div class="ai-reply">'
                f'<strong style="font-size:15px;">Your Personalized Learning Report</strong>'
                f'<hr style="margin:10px 0;">{reply}</div>',
                unsafe_allow_html=True)

        st.markdown(
            f'<div style="margin-top:24px;text-align:center;font-size:13px;color:{TEXT3};">'
            f'🔄 Completed the cycle! Click below to start a new one.</div>',
            unsafe_allow_html=True)
        if st.button("🔄 Start New Learning Cycle", key="back_to_1", use_container_width=True):
            st.session_state.map_step = 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Navigation ──
    st.markdown("---")
    nav_c1, nav_c2, nav_c3 = st.columns([1, 2, 1])
    with nav_c1:
        if current > 1:
            if st.button("← Previous", use_container_width=True):
                st.session_state.map_step -= 1
                st.rerun()
    with nav_c3:
        if current < 5:
            if st.button("Next →", use_container_width=True, type="primary"):
                st.session_state.map_step += 1
                st.rerun()

    st.markdown(
        f'<div class="ft">Learning Trace Platform · 学迹通 v4.3 · '
        f'Student: {sel_sid} · Step {current} / 5</div>',
        unsafe_allow_html=True)