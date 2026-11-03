# config.py
import streamlit as st

try:
    # 优先从云端的安全密钥库读取
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    # 如果本地没配置，就留空（本地测试时你可以临时把 Key 填在引号里）
    API_KEY = "" 

API_URL = "https://openrouter.ai/api/v1/chat/completions"

# 选一个你测试最稳的免费模型
MODEL_NAME = "nvidia/nemotron-3-ultra-550b-a55b:free" 

CHART_TYPES = [
    "柱状图", "折线图", "面积图", "堆叠柱状图", 
    "饼图 (环形)", "散点图", "箱线图", "热力图", 
    "瀑布图", "漏斗图", "雷达图"
]

DEFAULT_COLOR = "#1f77b4"